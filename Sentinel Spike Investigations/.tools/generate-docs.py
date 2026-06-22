"""
Generates the publication docs for the Sentinel Spike Investigations folder.

Writes the three Markdown files (README.md, PLAYBOOK.md,
workbook/README.md) and renders a matching .html sibling for each one using
the same minimal CSS template the existing HTML files already use.

Run from the folder root:
    python .tools/generate-docs.py
"""
from __future__ import annotations
import os
import sys
import textwrap
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

HTML_TEMPLATE = (
    "<!doctype html><html><head><meta charset='utf-8'>"
    "<title>{title}</title>"
    "<style>body{{font-family:Segoe UI,Arial,sans-serif;max-width:900px;"
    "margin:2em auto;padding:0 1em;color:#222;line-height:1.55}}"
    "code{{background:#f3f3f3;padding:1px 4px;border-radius:3px}}"
    "pre{{background:#f6f8fa;padding:12px;border-radius:6px;overflow-x:auto}}"
    "h1,h2,h3{{border-bottom:1px solid #eee;padding-bottom:4px}}"
    "blockquote{{border-left:4px solid #ccc;padding-left:12px;color:#555;"
    "margin-left:0}}table{{border-collapse:collapse}}"
    "th,td{{border:1px solid #ddd;padding:4px 8px}}"
    "</style></head><body>{body}</body></html>"
)


def render(md_path: str, title: str) -> None:
    with open(md_path, "r", encoding="utf-8") as fh:
        text = fh.read()
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
    )
    out = HTML_TEMPLATE.format(title=title, body=html_body)
    html_path = os.path.splitext(md_path)[0] + ".html"
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"  rendered {os.path.relpath(html_path, ROOT)}")


def write(rel_path: str, content: str) -> str:
    out_path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content.lstrip("\n"))
    print(f"  wrote {rel_path} ({len(content)} chars)")
    return out_path


# ---------------------------------------------------------------------------
# README.md (top level)
# ---------------------------------------------------------------------------
README_MD = r"""
# Sentinel Spike Investigations

A complete, repeatable answer to one question:

> Table X in Sentinel just spiked. What is driving it, and what do I
> tell leadership?

The package contains a step by step KQL playbook and a Sentinel Workbook
that automates the whole flow so most investigations finish in minutes
with a ready to paste closeout.

## Who this is for

- SOC analysts on the front line of ingestion alerts.
- Detection engineers tuning data collection rules.
- Sentinel and Defender XDR admins who need to defend ingestion cost
  to leadership.
- Anyone who has ever had to answer the question "why did our log
  bill go up this week" in a hurry.

## What is in this folder

| File or folder | What it is |
|---|---|
| [README.md](README.md) | This file. Start here. |
| [PLAYBOOK.md](PLAYBOOK.md) | The manual, query by query procedure. Edit one date block, run, read, repeat. |
| [workbook/](workbook/) | An optional Sentinel Workbook that runs every step of the playbook in place, with color coded deltas, attribution lookup, and drilldown on click. |
| [workbook/spike-investigator.workbook.json](workbook/spike-investigator.workbook.json) | The workbook itself. Import once via Sentinel : Workbooks : Add workbook : Advanced Editor. |
| [workbook/README.md](workbook/README.md) | One time import instructions and an item by item tour of the workbook. |
| [00_what_table_spiked.kql](00_what_table_spiked.kql) | Ranks every billable `DataType` by daily GB delta. Names the table that grew. |
| [01_when_spiked_timechart.kql](01_when_spiked_timechart.kql) | Hourly timechart for the suspect table across the spike window plus 7 days of baseline. Pins the start hour. |
| [02_top_actiontypes.kql](02_top_actiontypes.kql) | For tables with an `ActionType` column, ranks ActionType during the spike. Usually one or two ActionTypes account for most of the volume. |
| [03_spike_vs_baseline.kql](03_spike_vs_baseline.kql) | The key query. Joins spike vs prior 7 days grouped by parent process, init process, and company. Top row almost always names the binary. |
| [04_top_destinations.kql](04_top_destinations.kql) | Once a binary is named, shows where it is writing files, connecting on the network, touching the registry, or loading DLLs. |
| [05_device_concentration.kql](05_device_concentration.kql) | Top 25 devices with FleetShare percent. Decides fleet wide rollout vs a handful of broken hosts. |
| [06_drill_processtree.kql](06_drill_processtree.kql) | Full parent chain for the suspect process on one device in a 3 hour window. The proof you paste into the brief. |

Every Markdown file has a sibling `.html` rendered with the same
template so the package can be browsed without a Markdown viewer.

## The three modes of use

You can drive this package in three different ways depending on how
much tooling you have. Pick the one that fits your environment.

### Mode 1 : KQL only

Open Advanced Hunting (Defender XDR) and Sentinel Logs in side by
side browser tabs. Work the seven `.kql` files in order. Edit one
date block per file. No imports, no setup, no extra permissions.
This is the canonical mode and works in any tenant.

Best for: a one off spike, a tenant where you do not own the
workbook gallery, training a new analyst from first principles.

### Mode 2 : Workbook

Import [workbook/spike-investigator.workbook.json](workbook/spike-investigator.workbook.json)
into Sentinel : Workbooks once. After that every spike becomes a
fill in the parameters exercise. The workbook runs every query, color
codes the deltas (green = below baseline, red = above), shows vendor
and product attribution next to each binary, and lets you click a
device row to pin Step 5.

Best for: a SOC that responds to ingestion alerts more than once a
month. The setup pays for itself the second time you use it.

### Mode 3 : Both

Use the workbook for the first pass. When something does not fit a
known pattern, drop into the raw KQL files to extend, customise,
or save a tenant specific variant. The workbook and the files share
the same query shapes so what you learn in one transfers cleanly to
the other.

## Fast path

If a spike alert just fired and you have an hour, do this:

1. Open [PLAYBOOK.md](PLAYBOOK.md).
2. Run Step 0 in Sentinel Logs to name the table.
3. Run Steps 1, 2, 3 in Advanced Hunting against that table.
4. Run Steps 4, 5, 6 to confirm root cause and write your closeout
   using the structure at the bottom of the playbook.

If you have the workbook imported, replace steps 2 through 5 with
"set the parameters at the top of the workbook" and read down the
page.

## Prerequisites

| Capability | Used by |
|---|---|
| Sentinel reader on the target workspace | Step 0 (Usage table is in Sentinel, not Defender XDR) |
| Microsoft Defender XDR Advanced Hunting access | Steps 1 through 6, plus every query in the workbook |
| Defender XDR data connector enabled on the Sentinel workspace | Workbook only (so the `Device*` tables land in Log Analytics where the workbook reads them) |
| A text editor for the KQL files | VS Code is ideal. Notepad works. |

The KQL files themselves have no other dependencies. They reference
only built in tables (`Usage` for Step 0, `Device*` and a few
Sentinel native tables for the rest).

## Glossary

A short reference so the rest of the package reads consistently.

- **DataType**: the column the Sentinel `Usage` table uses for the
  table name. Same value as the table you would query (e.g.
  `DeviceFileEvents`).
- **Spike window**: the date range the spike covers. Set this to the
  first and last day of elevated volume, or first day and today if
  the spike is ongoing.
- **Baseline window**: the comparable period of normal volume. The
  KQL files default to the 7 days immediately before the spike. The
  workbook lets you pick any window with a time picker.
- **Per day normalisation**: dividing the windowed total by the
  number of days in the window so a 3 day spike can be compared
  directly to a 7 day baseline.
- **ActionType**: the second level classifier on the `Device*` tables
  (`FileCreated`, `ProcessCreated`, `AntivirusScanCompleted`, etc.).
  One ActionType usually drives most of any spike on those tables.
- **Initiator triplet**: the three columns Step 3 groups by, which
  uniquely identify a chain of activity on a device:
  `InitiatingProcessParentFileName` (grandparent of the action),
  `InitiatingProcessFileName` (the binary that did the action), and
  `InitiatingProcessVersionInfoCompanyName` (signing publisher).
- **Vendor and product attribution**: the workbook joins each row
  from Step 3 and Step 5 against the binary metadata
  (`InitiatingProcessVersionInfoCompanyName` and `ProductName`) so
  the table shows publisher and product name next to each binary
  even when only the file name is interesting.
- **Fleet share**: percentage of the total spike events that a
  single device accounts for. High fleet share on one device means
  the device is broken. Low fleet share spread across thousands of
  devices means a fleet wide rollout.
- **Closeout**: the three part write up you produce at the end of an
  investigation. Outcome (one sentence), evidence chain (which queries
  showed what), brief language (plain English for leadership).

## How the workbook and the KQL files relate

The workbook does not invent any new queries. Every query in it is a
direct port of the KQL file with the same step number, with three
differences:

1. **Parameters instead of literals**. The date block is replaced
   with workbook parameters (`{SpikeRange}` and `{BaselineRange}`)
   so the picker UI drives the dates.
2. **Per day normalisation everywhere**. Both spike and baseline are
   divided by their day count so any two windows are directly
   comparable.
3. **Attribution join**. Steps 3 and 5 join against a small lookup
   that pulls vendor and product name from the binary metadata so
   the table shows the publisher next to the file name.

If you want to understand a workbook query, open the matching
numbered `.kql` file. The intent is identical.

## Anomaly section in the workbook

The workbook starts with an extra section that does not exist as a
standalone `.kql` file: a 30 day anomaly scan across every billable
table using `series_decompose_anomalies`. It surfaces tables that
spiked abruptly in a single day and were ignored.

This is intentionally narrow. The scan catches abrupt one day jumps
against a linefit baseline. A sustained, multi day rise (the
DeviceFileEvents pattern in this lab is a good example) is absorbed
into the baseline and scores below the alerting threshold. Sustained
rises are what Steps 0 through 3 are designed to catch, so the two
views are complementary, not duplicative.

There are also two trivia guards in the anomaly query:

- `MinDailyVolume = 100` filters out near zero tables that read as
  100 percent anomalies on a 0 row to 1 row jump.
- `Score >= 3.0` is the standard `series_decompose_anomalies` cutoff.

If the anomaly section returns zero rows, that is the healthy state:
no abrupt one day spikes worth chasing. Steps 0 through 3 still
apply.

## Limitations and known gaps

- **Anomaly section only catches abrupt one day spikes**. Sustained
  multi day rises do not score above the threshold. Use Steps 0
  through 3 for those, which is what they are designed for.
- **The workbook needs the Defender XDR data connector**. Without
  the connector, the `Device*` tables are empty in Log Analytics and
  the workbook returns no rows. The standalone `.kql` files still
  work in Advanced Hunting in that case.
- **Step 0 reads the `Usage` table**, which only exists in Sentinel,
  not in Defender XDR Advanced Hunting. Run it in Sentinel Logs.
- **`series_decompose_anomalies` is sensitive to gaps**. A table
  that was paused for a day and resumed reads as an anomaly. Treat
  scores between 3 and 5 with care.

## When NOT to use this package

- For cost forecasting or chargeback reports. Use the Sentinel
  Workspace usage workbook in the Azure portal.
- For real time alerting on volume changes. Use scheduled analytics
  rules.
- For investigating a specific security alert or incident. Use the
  alert page in Defender XDR.

This package is for one specific case: a table volume spiked,
leadership wants to know why, and you have a short window to find
out and write it up.

## Closeout template

Every investigation finishes with this structure. Paste it into the
ticket or brief:

```
Outcome
-------
<one sentence: what is the spike, was anything broken, what action
follows?>

Evidence chain
--------------
- Step 0 (00_what_table_spiked.kql): <which table led, by how much>
- Step 1 (01_when_spiked_timechart.kql): <when it started, ongoing or not>
- Step 2 (02_top_actiontypes.kql): <which ActionType dominated>
- Step 3 (03_spike_vs_baseline.kql): <named binary and parent>
- Step 4 (04_top_destinations.kql): <where the binary wrote / connected>
- Step 5 (05_device_concentration.kql): <fleet wide or a few hosts>
- Step 6 (06_drill_processtree.kql): <full parent chain on one host>

Brief language
--------------
<plain English paragraph for leadership: no KQL, name the activity,
state whether action is required.>
```

## Layout of a typical investigation

A normal investigation ends in three to fifteen minutes of click time
plus query runtime. The walltime is dominated by KQL queries against
big tables. Expect:

- Step 0 against `Usage`: a few seconds.
- Steps 1 and 2 hourly against one `Device*` table over 10 days:
  10 to 30 seconds each.
- Step 3 over 10 days grouped by three columns: 20 to 90 seconds.
- Steps 4 through 6 narrowed by binary or device: a few seconds each.

If a query times out, narrow the spike window first, then the table
filter, then add an `ActionType` prefilter.

## Repo, license, and contribution

This folder lives in the public `johnB007/Troubleshooting` repository
on GitHub. Pull requests are welcome.
"""

# ---------------------------------------------------------------------------
# PLAYBOOK.md
# ---------------------------------------------------------------------------
PLAYBOOK_MD = r"""
# Playbook : investigating a Sentinel ingestion spike

Work the seven KQL files in order. Each one takes about a minute to
edit and run. After each query, the section below tells you what to
look for, how to read the output, and which file to open next.

Before you start, open two browser tabs:

- Advanced Hunting:
  `https://security.microsoft.com/v2/advanced-hunting`
- Sentinel Logs in the Azure portal (for Step 0, which reads the
  `Usage` table that only exists in Sentinel).

If you also have the workbook imported, you can drive the same steps
from `Sentinel : Workbooks : Spike Investigator` instead of pasting
KQL by hand. See [workbook/README.md](workbook/README.md). This
playbook stays useful as the reference for what each step does and
how to read the output.

## The one knob you change

Every numbered query file has a date block at the top:

```kql
let spikeStart = datetime(2026-06-09);
let spikeEnd   = datetime(2026-06-12);
let baseEnd    = spikeStart;
let baseStart  = baseEnd - 7d;
```

Set `spikeStart` to the first day you saw elevated volume. Set
`spikeEnd` to the last day, or to today if the spike is ongoing.
Leave the other two lines alone. Repeat this once per file as you
open it. Some files also have a `table name` line you swap if the
spike is in a `Device*` table other than `DeviceEvents`.

## Step 0 : name the table that spiked

**File**: [00_what_table_spiked.kql](00_what_table_spiked.kql)
**Where to run**: Sentinel Logs in the Azure portal. The `Usage`
table lives in Sentinel and is not available in Defender XDR
Advanced Hunting.

**What you edit**: the date block at the top.

**What the query returns**: every billable `DataType` with four
columns:

- `BaselinePerDayGB`: average GB per day during the prior 7 days.
- `SpikePerDayGB`: average GB per day during the spike window.
- `DeltaPerDayGB`: the difference, top of the table.
- `RatioVsBaseline`: spike per day divided by baseline per day. A
  ratio of `2.0` means double the normal volume. The query returns
  the spike value itself when the baseline is zero so a brand new
  table reads as its own GB per day.

**How to read it**:

- The top row is the table that grew the most in absolute GB. That
  is the table to investigate.
- A ratio above `1.5` is interesting. Below that is noise.
- A baseline of `0.0` plus a non zero spike means a brand new table
  appeared. Treat it as a connector change rather than a spike.

**What you do next**: write down the `DataType` name. If the top row
is a `Device*` table, continue to Step 1. If it is one of the
Sentinel native tables (`SecurityEvent`, `Syslog`, `CommonSecurityLog`,
`AzureDiagnostics`, `Heartbeat`, custom `*_CL`), skip Step 2 because
those tables do not have an `ActionType` column. Steps 1 and 3 still
apply.

## Step 1 : pin the exact hour the spike started

**File**: [01_when_spiked_timechart.kql](01_when_spiked_timechart.kql)
**Where to run**: Advanced Hunting (or Sentinel Logs, either works).

**What you edit**:

- The date block at the top.
- The table name on the first table line below the let block. Swap
  `DeviceEvents` for the DataType from Step 0 if it is different.

**What the query returns**: an hourly bin of event counts across the
spike window plus 7 days of baseline. Render as a line chart.

**How to read it**:

- Hover the chart and find the exact hour the line jumps. Write it
  down. You will use it for Step 6.
- Note whether the curve is back to baseline yet or still elevated.
  Active spikes need an immediate decision. Concluded spikes are
  cleanup write ups.
- A flat curve at a new elevation is a step change, usually a
  configuration push (new ActionTypes captured, new DCR, agent
  update). A bell curve is a transient (Patch Tuesday, scheduled AV
  scan, signature push).

**What you do next**: if the table has an `ActionType` column
(any `Device*` table), continue to Step 2. Otherwise skip to Step 3.

## Step 2 : find the noisy ActionType

**File**: [02_top_actiontypes.kql](02_top_actiontypes.kql)
**Where to run**: Advanced Hunting.

**What you edit**:

- The date block.
- The table name if you are on a Device* table other than
  `DeviceEvents`.

**What the query returns**: ranked list of ActionType values during
the spike with three columns:

- `Events`: count.
- `Devices`: distinct devices that produced the ActionType.
- `EventsPerDevice`: events divided by devices.

**How to read it**:

- One or two ActionTypes usually account for the majority of the
  spike (`FileCreated`, `ProcessCreated`,
  `AntivirusScanCompleted`, `RegistryValueSet`, etc.). Note them.
- A high `EventsPerDevice` on a small `Devices` number is a single
  device problem. A low `EventsPerDevice` across thousands of
  devices is a fleet wide rollout.
- The combination `FileCreated` + thousands of devices + balanced
  per device count is almost always Patch Tuesday or a Defender
  platform update.

**What you do next**: continue to Step 3. Optionally feed the top
ActionType into the `actionFilter` line in Step 3 for cleaner
results.

## Step 3 : name the binary driving the spike

This is the most important query in the playbook. The top row of
the output almost always names the binary that is responsible for
the extra volume.

**File**: [03_spike_vs_baseline.kql](03_spike_vs_baseline.kql)
**Where to run**: Advanced Hunting.

**What you edit**:

- The date block.
- The table name if needed.
- Optional: if Step 2 named a dominant ActionType, set the
  `actionFilter` line to that ActionType to narrow the comparison.
- Tune the `where Spike > 10000` threshold. Raise it to `100000`
  or `1000000` on very high volume tables so the result is not
  flooded with noise rows.

**What the query returns**: rows grouped by the initiator triplet
(`Parent`, `Init`, `Company`) with five numeric columns:

- `Baseline`: events in the prior 7 days for this triplet.
- `Spike`: events in the spike window for this triplet.
- `Delta`: spike minus baseline.
- `Ratio`: spike divided by baseline. Returns the spike value when
  baseline is zero so brand new activity is visible.

**How to read it**:

- Sort by `Delta` descending. The top five rows are the candidate
  culprits.
- Read the `Company` column. Microsoft Corporation rows are almost
  always servicing or Defender activity. Third party publisher rows
  are agent activity. Blank Company values are usually scripts or
  custom binaries.
- Read the `Parent` and `Init` pair. Known servicing pairs include
  `services.exe` to `TrustedInstaller.exe`, then
  `TrustedInstaller.exe` to `tiworker.exe`. Known Defender pairs
  include `services.exe` to `MsMpEng.exe`. Known third party agent
  pairs include the agent service spawning its worker process.

**What you do next**: read the top one or two `Init` values. A
recognised servicing or agent binary usually points straight at the
cause. Continue to Step 4 for confirmation.

**Worked example from the lab**: the top row was
`Init = MsMpEng.exe`, `Parent = services.exe`,
`Company = microsoft corporation`, `Delta = 1.2M`. This is the
Microsoft Defender platform and signature update pattern. The
investigation closed at this step.

## Step 4 : confirm with destination data

**File**: [04_top_destinations.kql](04_top_destinations.kql)
**Where to run**: Advanced Hunting.

**What you edit**: the file has one block active at the top
(`DeviceFileEvents`) and several commented blocks for other tables.
Uncomment the block that matches your spike table and comment the
others. Then set the date block and put the suspect binary name
from Step 3 into the `initFilter` line.

**What the query returns**: depends on the block:

- `DeviceFileEvents` block: top folder roots written or modified
  by the suspect binary, with sample file names and the command
  line that started the binary.
- `DeviceProcessEvents` block: top command lines.
- `DeviceNetworkEvents` block: top remote IP + port pairs with a
  sample URL.
- `DeviceRegistryEvents` block: top registry key roots and
  ActionType pairs.
- `DeviceImageLoadEvents` block: top DLLs loaded with the signers.

**How to read it**:

- Servicing stack writes show up under `c:\windows\winsxs\`,
  `c:\windows\softwaredistribution\`, and `c:\windows\system32\`.
- Defender platform updates show up under
  `c:\programdata\microsoft\windows defender\`.
- Third party agent reinstalls show up under `c:\program files\`
  or `c:\programdata\<vendor>\`.
- Backup agent activity shows up under `c:\windows\system32\` for
  the VSS provider and the backup vendor folder for the snapshot
  metadata.

**What you do next**: continue to Step 5.

## Step 5 : decide fleet wide or a few broken devices

**File**: [05_device_concentration.kql](05_device_concentration.kql)
**Where to run**: Advanced Hunting.

**What you edit**: date block, table name, and optional suspect
binary filter near the top.

**What the query returns**: top 25 devices by event count during
the spike with three columns:

- `Events`: count on this device.
- `DistinctInitiators`: number of distinct binaries on this device
  that produced events in the window.
- `FleetShare`: percent of total spike events accounted for by
  this device.

**How to read it**:

- Many devices, each with low `FleetShare`: fleet wide rollout.
  Patch Tuesday, Defender platform update, AV scan window, MDM
  enrolment wave. Nothing to fix at the device level.
- Five devices, each with high `FleetShare`: a small number of
  runaway agents. Open a ticket on those device names. Treat
  every device above 5 percent fleet share as a candidate for
  individual investigation.
- One device with 80 percent fleet share: a single broken host.
  Go straight to Step 6 with that device name.

**What you do next**: if the pattern is fleet wide and Step 3
named a recognised binary, you are done. Write the closeout using
the structure at the bottom of this playbook. If the pattern is the
runaway device case, continue to Step 6 with one of the device
names.

## Step 6 : prove root cause on a single device

**File**: [06_drill_processtree.kql](06_drill_processtree.kql)
**Where to run**: Advanced Hunting.

**What you edit**: at the top of the file, set:

- `device`: a device name from Step 5.
- `suspect`: a process name from Step 3 (or empty string to drop
  the filter and see all activity).
- `windowStart`: the hour the spike began on that device.
- `windowEnd`: defaults to `windowStart + 3h`.

**What the query returns**: the full parent chain for the suspect
process on that device in the window, projected to:

- `Timestamp`
- `Grandparent` = `InitiatingProcessParentFileName`
- `Parent` = `InitiatingProcessFileName`
- `Child` = `FileName`
- `ChildCmd` = `ProcessCommandLine`
- account names and folder paths for both initiator and child.

**How to read it**:

- Windows servicing call stack: `services.exe` to
  `TrustedInstaller.exe` to `tiworker.exe`.
- Defender platform update: `services.exe` to `MsMpEng.exe`, with
  child `MsMpEng.exe`, `MpCmdRun.exe`, `MpDefenderCoreService.exe`.
- Third party agent: the vendor service spawning its worker
  process repeatedly, often once per minute.
- Scripted custom workload: `powershell.exe` or `cmd.exe` as the
  parent, with the same command line repeating.

**What you do next**: write your closeout using the structure
below.

## What "done" looks like

A closeout has three parts. Paste them into the ticket in this
order.

### 1. Outcome

One sentence. State what the spike is and whether any action
follows.

> Spike on `DeviceEvents` between 2026-06-09 and 2026-06-12 is the
> Microsoft Defender platform and signature update wave following
> Patch Tuesday. No action required.

### 2. Evidence chain

Three to five bullets. Reference the file names so a reviewer can
rerun the queries.

> - `00_what_table_spiked.kql`: `DeviceEvents` led at +1.8 GB per
>   day delta.
> - `01_when_spiked_timechart.kql`: spike started 2026-06-09 04:00 UTC.
> - `02_top_actiontypes.kql`: `AntivirusScanCompleted` accounted
>   for 78 percent of the volume.
> - `03_spike_vs_baseline.kql`: top row was `MsMpEng.exe` under
>   `services.exe` with `Delta = 1.2M`.
> - `05_device_concentration.kql`: 1,420 distinct devices with no
>   single device above 1 percent fleet share. Fleet wide.

### 3. Brief language

A short paragraph for leadership in plain English. No KQL.

> The recent ingestion spike was caused by the regular Microsoft
> Defender platform and signature update wave that follows Patch
> Tuesday. Activity is concentrated on the Defender engine
> (`MsMpEng.exe`) across the entire monitored fleet and is
> expected. Volume is returning to baseline as the wave completes.
> No tuning, no rule changes, and no device action are required.

## Anti patterns

Things that look like shortcuts but cost time:

- **Skipping Step 0** because you "already know which table spiked".
  The `Usage` table is the only authoritative ranking. Sometimes
  the alert names the wrong table.
- **Setting the spike window too wide**. A 30 day window dilutes
  every comparison. Keep the spike window to the actual elevated
  days plus or minus one.
- **Setting the baseline window too short**. Five days is too
  noisy. Seven to fourteen days is the sweet spot. The workbook
  uses 14 by default.
- **Lowering the `Spike > 10000` threshold in Step 3 too far**.
  On high volume tables, 10000 is already too low. Raise it before
  you lower it.
- **Reading `Ratio` without `Delta`**. A row with `Spike = 5,
  Baseline = 1, Ratio = 5.0` is noise. Always sort by `Delta` first.
- **Calling Patch Tuesday "an incident"**. Well understood patterns
  should close fast without organisational noise.

## Where this leaves you

After Step 6 you have:

- A named table.
- A named binary.
- A named publisher.
- A named pattern or a custom closeout.
- An evidence chain that any reviewer can reproduce in minutes.

That is enough to close the alert, file the brief, and move on.
"""

# ---------------------------------------------------------------------------
# workbook/README.md
# ---------------------------------------------------------------------------
WORKBOOK_README_MD = r"""
# Sentinel Spike Investigator workbook

The Sentinel Workbook in this folder is the automated path for the
playbook in the parent folder. Instead of opening the seven `.kql`
files one at a time and pasting results between tabs, the workbook
runs every step in place against the connected Log Analytics
workspace with color coded deltas, vendor and product attribution,
and click to drill on devices.

This README documents the import, the parameters, every step in the
workbook, and how to extend it.

## Prerequisites

1. A Sentinel enabled Log Analytics workspace.
2. The **Microsoft Defender XDR** data connector turned on so the
   `Device*` tables land in the workspace. Without the connector the
   queries return zero rows. The raw `.kql` files still work in
   Defender XDR Advanced Hunting in that case.
3. Workbook contributor permissions on the workspace, or the
   workspace owner running the import on your behalf.

## One time import

1. Sentinel : Workbooks : **+ Add workbook**.
2. **Edit** (pencil icon).
3. **Advanced Editor** (the `</>` icon at the top of the edit toolbar).
4. Gallery Template kind: **JSON**.
5. Paste the entire contents of
   [spike-investigator.workbook.json](spike-investigator.workbook.json)
   into the editor. Replace whatever placeholder is already there.
6. **Apply**.
7. **Done Editing**.
8. **Save**. Pick a workspace and a name (suggested: `Spike Investigator`).

Once saved, the workbook appears under **My workbooks** and can be
opened any time a spike alert fires.

## Updating the workbook later

When this repo ships a new version, repeat the import:

1. Open the saved workbook in Sentinel.
2. Edit : Advanced Editor.
3. Replace the JSON with the new contents of
   `spike-investigator.workbook.json`.
4. Apply : Done Editing : Save.

The workbook does not auto update. If you want the latest version,
you re paste it.

## The parameters at the top

Every query in the workbook is driven from a parameter row at the
top. Setting these is the only step you take per investigation.

| Parameter | Type | Default | What it does |
|---|---|---|---|
| `Table` | dropdown | `DeviceFileEvents` | The `Device*` table to investigate. Drives Steps 1 through 5. |
| `SpikeRange` | time range picker | last 3 days | Start and end of the spike window. Drives every query. |
| `BaselineRange` | time range picker | last 14 days ending at the spike start | Comparison window for Steps 0, 2, and 3. |
| `SelectPct` | text | `5` | Floor for which ActionTypes Step 2's chart shows. Lower means more bars, more noise. |
| `Threshold` | text | `10000` | The `Spike > N` cutoff in Step 3. Raise on very high volume tables. |
| `Device` | text | empty | The device name Step 5 drills into. Set by clicking a row in Step 4. |

The two time pickers are independent. Set the `SpikeRange` to the
days that look high. Set the `BaselineRange` to a comparable period
of normal volume. Two weeks ending at the spike start is the
default and a good choice.

## The sections, top to bottom

The workbook renders the same flow as the playbook with two
additions at the top: an intro and an anomaly scan.

### Intro

Plain text explaining what the workbook does and how the parameters
drive it. No queries.

### Anomalous tables (last 30 days, score >= 3)

`q-anomaly`. A 30 day anomaly scan across every billable table using
`series_decompose_anomalies`. Surfaces tables whose daily volume
spiked abruptly in a single day and scored above the standard
threshold.

Columns: `DataType`, `AnomalyDay`, `Actual` (GB on that day),
`Expected` (expected GB from the linefit baseline), `Score`,
`PercentIncrease`.

- The scan catches abrupt one day spikes. Sustained multi day rises
  are absorbed into the linefit baseline and do not surface here.
  Use Steps 0 through 3 for sustained rises.
- `PercentIncrease` uses the standard formula `(Actual - Expected) / Expected`
  so a 100 to 1000 jump reads as 900 percent, not 90 percent.
- A `MinDailyVolume = 100` floor filters out near zero tables that
  read as 100 percent anomalies on a 0 row to 1 row jump.
- Zero rows is the healthy state.

### Step 0 : confirm the spike

Two visualisations side by side.

- `q-step0`. Barchart titled "Events per day: baseline window vs
  spike window" for the selected `Table`. Both bars are per day
  normalised so a 3 day spike compares directly against a 14 day
  baseline.
- `q-step0-trend`. Linechart spanning both windows so the analyst
  can see the full daily trend rather than just the two summary
  bars. Useful to spot a multi day ramp vs a one day spike.

### Step 1 : ActionType breakdown during the spike

`q-step1`. Table showing the top 20 ActionType values during the
spike window with vendor attribution. Columns: `ActionType`,
`Events`, `Devices`, `EventsPerDevice`, `TopInitiator`,
`TopCompany`.

The attribution is a join against the binary metadata so the table
shows which publisher's binary produced each ActionType, not just
the action name. A single ActionType driven by `MsMpEng.exe` from
Microsoft Corporation tells a different story than the same
ActionType driven by an unknown binary.

### Step 2 : ActionType spike vs baseline

Two views.

- `q-step2`. Numeric table per ActionType: `BasePerDay`, `SpikePerDay`,
  `Delta`, `Ratio`. Same shape as the per day normalisation in Step 0
  but split by ActionType.
- `q-step2-chart`. Top 15 ActionTypes with the same numbers in a
  table that uses the following coloring:
  - `BasePerDay`: blue heatmap. Higher is darker blue.
  - `SpikePerDay`: red heatmap. Higher is darker red.
  - `Delta`: diverging thresholds. Positive deltas are red (above
    baseline). Negative deltas are green (below baseline). Zero is
    grey.

### Step 3 : process pairs that grew the most

`q-step3`. The most important table in the workbook. Same query as
[03_spike_vs_baseline.kql](../03_spike_vs_baseline.kql) but with
two upgrades:

- **Per day normalisation** of both Spike and Baseline.
- **Vendor and product attribution** joined on
  `InitiatingProcessFileName` so the table shows publisher and
  product name next to the binary even when the file name alone is
  generic.

Columns: `ParentName`, `InitName`, `Vendors`, `Products`,
`BasePerDay`, `SpikePerDay`, `Delta`, `Ratio`, `AboveThreshold`.

The `AboveThreshold` column uses true/false text with threshold
coloring: green `true` when the row is above the `Threshold`
parameter, red `false` when it is below. Sort by `Delta` descending
and read the top five rows.

`Delta` uses the same diverging thresholds as Step 2's chart so the
sign is obvious at a glance.

### Step 4 : devices contributing the most rows

`q-step4`. Top 50 devices in the spike with `Events`,
`DistinctInitiators`, `TopInitiator`, `FleetShare` percent. **Click
any row** and the workbook pins that device name into the `Device`
parameter, which makes Step 5 appear below.

### Step 5 : process tree for `{Device}`

`q-step5`. Top process pairs on the device the analyst clicked in
Step 4, in the spike window, with the same vendor and product
attribution join as Step 3.

Columns: `ParentName`, `InitName`, `Vendors`, `Products`, `Events`.

The query is hidden until a `Device` is selected. To clear it, set
the `Device` parameter to empty at the top of the workbook.

## What the workbook does not do

- It does not write back to Sentinel. The output is a view and a
  closeout, not an automated action.
- It does not run anything on a schedule. It runs when an analyst
  opens it and sets the time pickers.
- The dataset is whatever is in Log Analytics. If MDE streaming is
  filtered or delayed at the connector, the workbook reflects that.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Every query returns "no data" | Defender XDR data connector is off or the chosen `Table` is empty | Enable the Defender XDR data connector. Pick another `Table` from the dropdown. |
| Step 3 returns hundreds of rows | `Threshold` parameter is too low for the table volume | Raise `Threshold` to `100000` or `1000000`. |
| Step 5 is blank | `Device` parameter is empty | Click any row in Step 4 to pin a device. |
| A column shows true/false as plain text | The workbook was edited and the threshold representation was changed | The threshold `representation` must be one of `Success` / `Failed` / `Critical` / `Warning` / `Pending` / `Info` / `Unknown` / `Disabled`. Heatmap palette names like `green`, `redBright` only work for formatter type 4, not for threshold formatter type 18. |
| `Delta` column is all red regardless of sign | `Delta` is using a monochrome palette instead of diverging thresholds | Switch the column formatter to type 18 (thresholds) with `> 0 -> Failed`, `< 0 -> Success`, default `Unknown`. |
| Anomaly section returns zero rows | No abrupt one day spikes in the last 30 days | Healthy state. Run Steps 0 through 3 for sustained, multi day rises. |

## File layout

| File | What it is |
|---|---|
| [spike-investigator.workbook.json](spike-investigator.workbook.json) | The workbook JSON. Paste this into the Advanced Editor. |
| [README.md](README.md) | This file. Import instructions and per item documentation. |
| [README.html](README.html) | Rendered HTML sibling. Same content as the Markdown, no viewer required. |
"""

# ---------------------------------------------------------------------------
# Write everything, then render HTML siblings.
# ---------------------------------------------------------------------------
def main() -> int:
    print("Writing Markdown files...")
    paths = [
        ("README.md", README_MD),
        ("PLAYBOOK.md", PLAYBOOK_MD),
        ("workbook/README.md", WORKBOOK_README_MD),
    ]
    written = []
    for rel, body in paths:
        written.append(write(rel, body))

    print("Rendering HTML siblings...")
    titles = {
        "README.md": "Sentinel Spike Investigations",
        "PLAYBOOK.md": "Playbook : investigating a Sentinel ingestion spike",
        "workbook/README.md": "Sentinel Spike Investigator workbook",
    }
    for rel, body in paths:
        full = os.path.join(ROOT, rel)
        render(full, titles[rel])

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
