# Playbook : investigating a Sentinel ingestion spike

Work the seven KQL files in order. Each one takes about a minute to
edit and run. After each query, the section below tells you what to
look for and which file to open next.

Before you start, open Advanced Hunting in another tab:
`https://security.microsoft.com/v2/advanced-hunting`

## The one knob you change

Every query has a date block at the top. It looks like this:

```kql
let spikeStart = datetime(2026-06-09);
let spikeEnd   = datetime(2026-06-12);
let baseEnd    = spikeStart;
let baseStart  = baseEnd - 7d;
```

Set `spikeStart` to the first day you saw elevated volume. Set
`spikeEnd` to the last day, or to today if the spike is ongoing. Leave
the other two lines alone. Do this once at the top of each file as you
open it.

## Step 0 : name the table that spiked

**File**: [00_what_table_spiked.kql](00_what_table_spiked.kql)
**Where to run**: Sentinel Logs (Azure portal), not Advanced Hunting.
This query reads the workspace `Usage` table, which lives in Sentinel.

**What you edit**: the date block at the top.

**What you look for**: the top row of the output. That is the
DataType (table) with the largest daily GB delta during the spike
window vs the prior 7 days. If one row is much larger than the next,
that is the table to investigate.

**What you do next**: write down the DataType name. Open the next
file and continue.

## Step 1 : pin the exact hour the spike started

**File**: [01_when_spiked_timechart.kql](01_when_spiked_timechart.kql)
**Where to run**: Advanced Hunting (or Sentinel Logs, either works).

**What you edit**:
- The date block at the top.
- On the first table line below the let block, swap `DeviceEvents`
  for the DataType from step 0 if it is different (for example
  `DeviceFileEvents`).

**What you look for**: render the chart as a line chart. Hover over
the curve. Note the exact hour the line jumps. Also note whether the
curve is back to baseline yet or still elevated.

**What you do next**: if the table has an `ActionType` column
(DeviceEvents, DeviceFileEvents, DeviceProcessEvents, etc.), go to
step 2. If it does not (SecurityEvent, Syslog, CommonSecurityLog,
custom logs), skip step 2 and go to step 3.

## Step 2 : find the noisy ActionType

**File**: [02_top_actiontypes.kql](02_top_actiontypes.kql)
**Where to run**: Advanced Hunting.

**What you edit**:
- The date block at the top.
- Swap the table name on the first table line if your spike is in a
  different Device* table.

**What you look for**: ranked list of ActionType values during the
spike window. Often one or two ActionTypes account for 80 percent of
the volume (for example `FileCreated`, `AntivirusScanCompleted`,
`ProcessCreated`). Note the top one or two.

**What you do next**: open step 3.

## Step 3 : name the binary driving the spike

This is the most important query in the playbook. The top row of the
output almost always names the binary that is responsible for the
extra volume.

**File**: [03_spike_vs_baseline.kql](03_spike_vs_baseline.kql)
**Where to run**: Advanced Hunting.

**What you edit**:
- The date block at the top.
- Swap the table name if needed.
- Optional: if step 2 named a dominant ActionType, set the
  `actionFilter` line near the top to that ActionType. This narrows
  the comparison and gives cleaner results.
- Tune `Spike > 10000` if the table is very high volume; raise it to
  `100000` or `1000000` so the output is not flooded with noise rows.

**What you look for**: the output is grouped by
`(InitiatingProcessParentFileName, InitiatingProcessFileName,
InitiatingProcessVersionInfoCompanyName)`. The top five rows by
`Delta` are the candidate culprits. Look at the company name column:
Microsoft Corporation, third party vendor, blank? Look at the parent
process and child process pair: do they belong to a known servicing
stack, an antivirus engine, a backup agent, an installer?

**What you do next**: scan [FINGERPRINTS.md](FINGERPRINTS.md). If the
top one or two rows match a fingerprint, you may have your answer.
Either way, go to step 4 to confirm with destination data.

## Step 4 : confirm with destination data

**File**: [04_top_destinations.kql](04_top_destinations.kql)
**Where to run**: Advanced Hunting.

**What you edit**: the file has one block active at the top
(DeviceFileEvents) and several commented blocks for other tables.
Uncomment the block that matches your spike table and comment the
others. Then set the date block and put the suspect binary name from
step 3 into the filter line.

**What you look for**:
- DeviceFileEvents: top folder roots being written. Servicing stack
  writes show up under `c:\windows\winsxs\` and similar.
- DeviceNetworkEvents: top remote IP plus port pairs. Update activity
  shows up against Microsoft IP ranges on 443.
- DeviceRegistryEvents: top registry key roots. Update activity shows
  up under `HKLM\COMPONENTS` and similar.
- DeviceImageLoadEvents: top DLLs loaded. Helps when the binary
  itself is generic (svchost) and you need the workload identity.

**What you do next**: open step 5.

## Step 5 : decide fleet wide or a few broken devices

**File**: [05_device_concentration.kql](05_device_concentration.kql)
**Where to run**: Advanced Hunting.

**What you edit**: date block, table name, and (optional) suspect
binary filter near the top.

**What you look for**: the output is top 25 devices by event count
during the spike, with a `FleetShare` percent column.

Two patterns:
- **Spread across thousands of devices with low per device share**:
  fleet wide rollout. Patch Tuesday, Defender platform update, AV
  scan window, MDM enrolment wave. Nothing to fix at the device
  level.
- **Top 5 devices with very high share each**: a small number of
  runaway agents. Open a ticket on those device names.

**What you do next**: if the pattern is fleet wide and step 3 matched
a fingerprint, you are done. Write the closeout using the matching
row in [FINGERPRINTS.md](FINGERPRINTS.md). If the pattern is the
runaway device case, go to step 6 with one of the device names.

## Step 6 : prove root cause on a single device

**File**: [06_drill_processtree.kql](06_drill_processtree.kql)
**Where to run**: Advanced Hunting.

**What you edit**: at the top, set:
- `device` to a device name from step 5
- `suspect` to a process name from step 3 (or remove the filter to
  see all activity)
- `windowStart` to the hour the spike began on that device
- `windowEnd` is windowStart plus 3 hours by default

**What you look for**: the full parent chain for the suspect process
on that device during the window. You should see the call stack that
caused the volume. For Windows servicing this looks like
`services.exe`, then `TrustedInstaller.exe`, then `tiworker.exe`. For
a third party agent it looks like the agent service spawning its
worker process.

**What you do next**: write your closeout using the structure below.

## What "done" looks like

A closeout has three parts:

1. **Outcome**: one sentence. "Spike was X. No transform changes
   needed." or "Spike is the Y agent on Z devices, opening a ticket."
2. **Evidence chain**: one short paragraph or three to five bullets
   that walk through what each query showed. Reference the file
   names so a reviewer can rerun the queries.
3. **Brief language**: a short paragraph written for leadership.
   Plain English, no KQL.
