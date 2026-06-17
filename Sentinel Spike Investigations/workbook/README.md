# Sentinel Spike Investigator workbook

This is the optional automated path for the playbook in the parent
folder. Instead of opening the seven `.kql` files one at a time and
pasting results between tabs, this workbook runs every step in place
against the connected Log Analytics workspace.

## Prerequisites

1. A Sentinel enabled Log Analytics workspace.
2. The **Microsoft Defender XDR** data connector turned on so the
   `Device*` tables land in the workspace. Without that connector,
   the queries in this workbook will return zero rows. The raw KQL
   files in the parent folder still work in Advanced Hunting in that
   case.

## Import

1. Sentinel : Workbooks : **+ Add workbook**.
2. Edit : **Advanced Editor** : Gallery Template : **JSON**.
3. Paste the contents of `spike-investigator.workbook.json`.
4. Apply : Done Editing : **Save**. Pick a workspace and a name
   (suggested: `Spike Investigator`).

Once saved it shows up in **My workbooks** and can be opened any time
a spike alert fires.

## How to drive it

1. Set the **Table to investigate** dropdown (defaults to
   `DeviceFileEvents`).
2. Set the **Spike window** time picker to the day or days that look
   high.
3. Set the **Baseline window** time picker to a comparable period of
   normal volume. Two weeks is a good default.
4. Adjust the **Delta threshold** if Step 3 returns too many or too
   few rows. Start at `10000`.
5. Work down the page. Each query runs automatically.
6. In Step 4 (top devices), **click a row**. That pins the device
   name into the `Device` parameter and Step 5 appears below it.
7. Once a pattern is clear, pick the matching value in the
   **Fingerprint match** dropdown at the top. The closeout language
   appears at the bottom, ready to copy.

## What the workbook does not do

- It does not replace the FINGERPRINTS.md table for new patterns.
  When you find a fingerprint that is not in the dropdown yet, add
  it to `FINGERPRINTS.md` in the parent folder.
- It does not write back to Sentinel. The output is a clean view
  and a copy ready closeout, not an automated action.
- The dataset is whatever is in Log Analytics. If MDE streaming is
  filtered or delayed, the workbook reflects that.
