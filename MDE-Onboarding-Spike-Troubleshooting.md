# MDE Onboarding Spike Troubleshooting

KQL playbook for investigating sudden increases in onboarded device counts over the last 30 days.
Run these in Microsoft Defender XDR Advanced Hunting (security.microsoft.com, then Hunting, then Advanced hunting).

> `DeviceInfo` retention in Advanced Hunting is 30 days. Use `ago(30d)` as the max window.

---

## 1. Confirm the spike. Daily onboarded trend

Establishes the baseline shape of the data and shows whether the spike is real, gradual, or a one day anomaly.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize arg_max(Timestamp, MergedToDeviceId) by DeviceId, bin(Timestamp, 1d)
| where isempty(MergedToDeviceId)
| summarize OnboardedDevices = dcount(DeviceId) by Day = bin(Timestamp, 1d)
| order by Day asc
| render timechart
```

---

## 2. Day over day delta. Quantify the spike

Shows the exact day or days the count jumped and by how much.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize Devices = dcount(DeviceId) by Day = bin(Timestamp, 1d)
| order by Day asc
| extend PrevDay = prev(Devices),
         Delta = Devices - prev(Devices),
         PctChange = round(100.0 * (Devices - prev(Devices)) / todouble(prev(Devices)), 1)
| project Day, Devices, PrevDay, Delta, PctChange
```

Look for any row where `PctChange` is greater than 5 percent. Those are your spike days.

---

## 3. Anomaly detection. Let KQL flag the spike

Uses time series decomposition to highlight outlier days automatically. Advanced Hunting does not support `anomalychart`, so the result is unpacked into three series and rendered as a timechart. Days with a non zero `Anomaly` value are the flagged outliers.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize Devices = dcount(DeviceId) by Day = bin(Timestamp, 1d)
| make-series Devices = sum(Devices) default = 0 on Day from ago(30d) to now() step 1d
| extend (anomalies, score, baseline) = series_decompose_anomalies(Devices, 2.0)
| mv-expand Day to typeof(datetime), Devices to typeof(long), baseline to typeof(double), anomalies to typeof(int), score to typeof(double)
| extend Anomaly = iff(anomalies != 0, Devices, long(null))
| project Day, Devices, Baseline = baseline, Anomaly, Score = score
| render timechart
```

Lower the `2.0` threshold to `1.5` to flag smaller deviations. To see only the flagged days as a table, append `| where isnotnull(Anomaly)` before the render.

---

## 4. New onboardings per day. The actual driver

`DeviceInfo` reports a row per device per day, so a flat onboarded count can still hide a wave of newly onboarded devices. This query isolates devices whose first onboarded day falls in each bucket.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d)
| order by Day asc
| render columnchart
```

A spike here means real onboarding activity such as a deployment, GPO push, or new tenant integration. A flat line here while query 1 is spiking means the same devices are flapping or re-reporting.

---

## 5. Break down the spike by OS or DeviceType

Identify whether the spike is workstations, servers, mobile, or IoT.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, OSPlatform, DeviceType) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d), OSPlatform
| order by Day asc, NewlyOnboarded desc
| render stackedareachart
```

Swap `OSPlatform` for `DeviceType` to see workstation versus server versus mobile mix. Advanced Hunting does not accept the `with (kind=stacked)` modifier, so use `stackedareachart` or `columnchart` (unstacked).

---

## 6. Break down by JoinType or domain

A common spike cause is a new domain or AAD tenant being merged in.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, JoinType, AadDeviceId) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d), JoinType
| order by Day asc, NewlyOnboarded desc
```

---

## 7. Onboarding source. Which mechanism added them

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, OnboardingMethod) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d), OnboardingMethod
| order by Day asc, NewlyOnboarded desc
```

Watch for a sudden surge from a single `OnboardingMethod` such as GPO, Intune, Local Script, MECM, or Defender for Cloud.

---

## 8. Status flapping. Devices re-reporting Onboarded

If the total onboarded number is spiking but newly onboarded is flat, you may be seeing devices toggle states. This finds devices that changed `OnboardingStatus` recently.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| summarize StatusValues = make_set(OnboardingStatus), Days = dcount(bin(Timestamp, 1d)) by DeviceId
| where array_length(StatusValues) > 1
| extend DeviceId, Statuses = tostring(StatusValues)
| project DeviceId, Statuses, Days
| top 100 by Days desc
```

---

## 9. Merged device check. Duplicates inflating counts

A common culprit is AAD or AD merges creating temporary duplicate `DeviceId` values before the merge link is established.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where isnotempty(MergedToDeviceId)
| summarize FirstMerge = min(Timestamp) by DeviceId
| summarize MergedDevices = dcount(DeviceId) by Day = bin(FirstMerge, 1d)
| order by Day asc
| render columnchart
```

If merge events spike alongside the onboarded count, the spike is partially artificial. The same physical devices are being counted under multiple `DeviceId` values.

---

## 10. List the actual spike day devices

Once you know the spike day or days from query 2, dump the device list for that day.

```kql
let SpikeDay = datetime(2026-04-28);  // set to your spike day
DeviceInfo
| where Timestamp between (SpikeDay .. SpikeDay + 1d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, DeviceName, OSPlatform, DeviceType, JoinType, OnboardingMethod, PublicIP) by DeviceId
| where FirstOnboarded between (SpikeDay .. SpikeDay + 1d)
| project DeviceId, DeviceName, OSPlatform, DeviceType, JoinType, OnboardingMethod, PublicIP, FirstOnboarded
| order by DeviceName asc
```

Patterns to look for: shared `OnboardingMethod`, common `PublicIP` or subnet, similar naming convention, same `JoinType`.

---

## 11. Weekend dip and saw tooth pattern

If the daily trend shows a clean repeating dip every 7 days (typically Saturday and Sunday), that is not a real fluctuation in onboarded count. It is a reporting artifact.

`DeviceInfo` writes a row per device only on days the device sends telemetry. Workstations that are powered off over the weekend do not appear that day, so `dcount(DeviceId) by Day` drops. Servers stay on, workstations do not, which produces the weekly saw tooth.

The Defender portal smooths this by showing the current onboarded inventory (cumulative), not devices that reported on a single day.

### Stable line using a rolling presence window

A device counts as onboarded if it reported within the last 7 days. This matches the portal's view and removes the weekend dip.

```kql
let lookback = 7d;
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| project DeviceId, Day = bin(Timestamp, 1d), MergedToDeviceId
| where isempty(MergedToDeviceId)
| extend WindowDay = range(Day, Day + lookback - 1d, 1d)
| mv-expand WindowDay to typeof(datetime)
| where WindowDay <= now()
| summarize OnboardedDevices = dcount(DeviceId) by Day = WindowDay
| order by Day asc
| render timechart
```

If you want to confirm weekends are the cause, group by day of week.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize Devices = dcount(DeviceId) by Day = bin(Timestamp, 1d)
| extend DayOfWeek = format_datetime(Day, "ddd")
| summarize AvgDevices = avg(Devices) by DayOfWeek
| order by AvgDevices desc
```

Saturday and Sunday averages noticeably below weekdays confirm the pattern is workstation reporting, not real onboarding change.

---

## Triage checklist

1. Run query 1. Is the spike real or just visual noise?
2. Run query 2. Which day or days, and how big in absolute and percent terms?
3. Run query 4. Is it new devices or the same devices flapping?
4. If new devices, run queries 5, 6, and 7 to identify the deployment vector.
5. If flapping, run queries 8 and 9 to check status churn and merge artifacts.
6. Run query 10 for the spike day or days to get the device list and find the common attribute.

Most spikes resolve to one of the following.

* Bulk onboarding rollout (Intune, GPO, or MECM push). Visible in queries 5 and 7 with a dominant method.
* Tenant or domain merger. Visible in query 6 with a new `JoinType` or AAD tenant.
* Merged device backlog. Visible in query 9. Counts will self correct as MDE finishes the merge.
* Reporting flap from network or agent restarts. Visible in query 8 with high status change counts.
