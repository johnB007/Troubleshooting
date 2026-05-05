# MDE Onboarding Spike Troubleshooting

KQL playbook for investigating sudden increases in onboarded device counts over the last 30 days.
Run these in **Microsoft Defender XDR Advanced Hunting** (`security.microsoft.com` → Hunting → Advanced hunting).

> `DeviceInfo` retention in Advanced Hunting is 30 days. Use `ago(30d)` as the max window.

---

## 1. Confirm the spike — daily onboarded trend

Establishes the baseline shape of the data and shows whether the spike is real, gradual, or a one-day anomaly.

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

## 2. Day-over-day delta — quantify the spike

Shows the exact day(s) the count jumped and by how much.

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

Look for any row where `PctChange` > 5% — that's your spike day(s).

---

## 3. Anomaly detection — let KQL flag the spike

Uses time-series decomposition to highlight outlier days automatically.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize Devices = dcount(DeviceId) by Day = bin(Timestamp, 1d)
| make-series Devices = sum(Devices) default = 0 on Day from ago(30d) to now() step 1d
| extend (anomalies, score, baseline) = series_decompose_anomalies(Devices, 2.0)
| render anomalychart with(anomalycolumns=anomalies, title="Onboarded Device Spikes")
```

Lower the `2.0` threshold to `1.5` to flag smaller deviations.

---

## 4. New onboardings per day — the actual driver

`DeviceInfo` reports a row per device per day, so a flat onboarded count can still hide a wave of *newly* onboarded devices. This query isolates devices whose **first** onboarded day falls in each bucket.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d)
| order by Day asc
| render columnchart
```

A spike here = real onboarding activity (deployment, GPO push, new tenant integration). A flat line here while #1 is spiking = the same devices are flapping/re-reporting.

---

## 5. Break down the spike by OS / DeviceType

Identify whether the spike is workstations, servers, mobile, or IoT.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, OSPlatform, DeviceType) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d), OSPlatform
| order by Day asc, NewlyOnboarded desc
| render columnchart with (kind=stacked)
```

Swap `OSPlatform` for `DeviceType` to see workstation vs server vs mobile mix.

---

## 6. Break down by JoinType / domain

Common spike cause: a new domain or AAD tenant being merged in.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, JoinType, AadDeviceId) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d), JoinType
| order by Day asc, NewlyOnboarded desc
```

---

## 7. Onboarding source — which mechanism added them

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where OnboardingStatus =~ "Onboarded"
| summarize FirstOnboarded = min(Timestamp), arg_max(Timestamp, OnboardingMethod) by DeviceId
| summarize NewlyOnboarded = dcount(DeviceId) by Day = bin(FirstOnboarded, 1d), OnboardingMethod
| order by Day asc, NewlyOnboarded desc
```

Watch for a sudden surge from a single `OnboardingMethod` (GPO, Intune, Local Script, MECM, Defender for Cloud, etc.).

---

## 8. Status flapping — devices re-reporting Onboarded

If the *total* onboarded number is spiking but newly onboarded is flat, you may be seeing devices toggle states. This finds devices that changed `OnboardingStatus` recently.

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

## 9. Merged-device check — duplicates inflating counts

A common culprit: AAD/AD merges create temporary duplicate `DeviceId`s before the merge link is established.

```kql
DeviceInfo
| where Timestamp > ago(30d)
| where isnotempty(MergedToDeviceId)
| summarize FirstMerge = min(Timestamp) by DeviceId
| summarize MergedDevices = dcount(DeviceId) by Day = bin(FirstMerge, 1d)
| order by Day asc
| render columnchart
```

If merge events spike alongside the onboarded count, the spike is partially artificial — the same physical devices are being counted under multiple `DeviceId`s.

---

## 10. List the actual spike-day devices

Once you know the spike day(s) from query #2, dump the device list for that day.

```kql
let SpikeDay = datetime(2026-04-28);  // <-- set to your spike day
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

## Triage checklist

1. Run **#1** — is the spike real or just visual noise?
2. Run **#2** — which day(s) and how big in absolute and percent terms?
3. Run **#4** — is it new devices or the same devices flapping?
4. If new devices: run **#5, #6, #7** to identify the deployment vector.
5. If flapping: run **#8** and **#9** to check status churn and merge artifacts.
6. Run **#10** for the spike day(s) to get the device list and find the common attribute.

Most spikes resolve to one of:
- **Bulk onboarding rollout** (Intune/GPO/MECM push) — visible in #5 + #7 with a dominant method.
- **Tenant or domain merger** — visible in #6 with a new `JoinType` or AAD tenant.
- **Merged-device backlog** — visible in #9; counts will self-correct as MDE finishes the merge.
- **Reporting flap** (network/agent restarts) — visible in #8 with high status-change counts.
