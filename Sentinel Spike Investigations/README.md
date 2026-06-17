# Sentinel Spike Investigations

A ready playbook for the question "table X spiked, what is driving it?"
in Microsoft Sentinel and Defender XDR. Seven numbered KQL files plus
this playbook walk you from the first alert to a closeout you can paste
into a brief.

## What is in this folder

| File | Purpose |
|---|---|
| [PLAYBOOK.md](PLAYBOOK.md) | The step by step procedure. Open this first when a spike fires. |
| [FINGERPRINTS.md](FINGERPRINTS.md) | One page quick reference of known spike patterns. Match the top of your spike vs baseline output against this list and you may be done. |
| [00_what_table_spiked.kql](00_what_table_spiked.kql) | Ranks every billable DataType by daily GB delta. Names the table. |
| [01_when_spiked_timechart.kql](01_when_spiked_timechart.kql) | Hourly timechart for the chosen table over the spike plus 7 days of baseline. |
| [02_top_actiontypes.kql](02_top_actiontypes.kql) | For tables that have ActionType (DeviceEvents, DeviceFileEvents, etc.), ranks ActionType during the spike. |
| [03_spike_vs_baseline.kql](03_spike_vs_baseline.kql) | The most important query. Names the binary driving the spike by joining spike window vs prior 7 days on parent process, child process, and company. |
| [04_top_destinations.kql](04_top_destinations.kql) | Once you have a binary, shows where it is writing, connecting, or registering. |
| [05_device_concentration.kql](05_device_concentration.kql) | Fleet wide rollout or a small number of broken devices? Top 25 devices with fleet share. |
| [06_drill_processtree.kql](06_drill_processtree.kql) | Final proof. Pulls DeviceProcessEvents for one suspect device in a 3 hour window and shows the parent chain. |

## Fast path

If you are reading this during a live spike, do this:

1. Open [PLAYBOOK.md](PLAYBOOK.md).
2. Work the seven queries in order. Each query takes about a minute to
   edit and run.
3. After query 03 produces a result, scan [FINGERPRINTS.md](FINGERPRINTS.md).
   If the top binaries match one of the known patterns, jump to the
   closeout language in that row and you are done.
4. If nothing matches, finish queries 04, 05, and 06 to confirm root
   cause, then write your own closeout following the structure in the
   playbook.

## Prerequisites

- Access to Microsoft Defender XDR Advanced Hunting:
  `https://security.microsoft.com/v2/advanced-hunting`
- Access to Microsoft Sentinel Logs in the Azure portal for query 00,
  which runs against the workspace `Usage` table.
- A text editor for editing the date range at the top of each KQL file.
  VS Code is fine. Notepad works.

## Why this exists

The Sentinel ingestion workbook tells you which vendor or table grew.
It does not tell you which binary inside the table caused the growth.
The seven queries in this folder fill that gap. The most important one
is query 03, which compares the spike window against the prior 7 days
grouped by parent process, child process, and company. The top row of
that result almost always names the culprit.

## When NOT to use this

- For cost forecasting or chargeback. Use the ingestion workbook.
- For real time alerting on volume. Use scheduled analytics rules.
- For investigations of a specific alert or incident. Use the alert
  page in Defender XDR.

This folder is for the narrow case: a table volume spiked, leadership
wants to know why, and you have a few hours to find out and write it
up.
