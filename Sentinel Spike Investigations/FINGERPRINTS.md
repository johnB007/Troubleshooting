# Fingerprints : known spike patterns

Quick reference card. After running
[03_spike_vs_baseline.kql](03_spike_vs_baseline.kql), match the top
rows against this list. If the pattern matches, jump straight to the
closeout language in the matching row.

## Windows Patch Tuesday (monthly, second Tuesday)

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `services.exe` | `tiworker.exe` | Microsoft Corporation |
| `svchost.exe` | `wuauclt.exe` | Microsoft Corporation |
| `svchost.exe` | `wuaucltcore.exe` | Microsoft Corporation |
| `svchost.exe` | `updateplatform.amd64fre.exe` | Microsoft Corporation |
| `services.exe` | `TrustedInstaller.exe` | Microsoft Corporation |

Often joined by `msiexec.exe`, `chrome.exe` and `onedrivesetup.exe`
deltas during the same window.

**Shape**: flat baseline through the Monday before Patch Tuesday, jump
on Tuesday, peak Wed through Fri, taper through the weekend, back to
baseline by the next Monday.

**Step 5 confirms**: fleet wide. Thousands of devices each with a
small fleet share.

**Closeout language**:

> Following the second Tuesday Patch Tuesday cycle, devices are
> applying servicing stack and Windows Update packages in a staged
> rollout. Volume is already trending back to baseline. No transform
> changes are required.

## Microsoft Defender platform and signature update

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `MsMpEng.exe` or `wuaucltcore.exe` | `MpSigStub.exe` | Microsoft Corporation |
| `MpSigStub.exe` | `AM_Delta_Patch_*.exe` | Microsoft Corporation |
| `services.exe` | `MsMpEng.exe` | Microsoft Corporation |

**Shape**: short, sharp bump (one to four hours) that recurs every few
days. Less spread than Patch Tuesday.

**Closeout language**:

> Spike is a Microsoft Defender platform and signature update rolling
> through the fleet. Activity is expected and short lived. No
> transform changes are required.

## MDE onboarding wave

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `MsSense.exe` | `SenseIR.exe` | Microsoft Corporation |
| `services.exe` | `MsSense.exe` | Microsoft Corporation |
| `wmiprvse.exe` | `mdeclientanalyzer.exe` | Microsoft Corporation |

**Shape**: gradual ramp over days as new device groups onboard. Not a
sudden spike. Confirm against the onboarding schedule before closing.

**Closeout language**:

> Volume increase tracks the scheduled MDE onboarding wave for the
> named device groups. Daily volume will plateau when the wave
> completes. No transform changes are required.

## Custom log or third party agent reinstall

**Top rows in query 03 look like**: unfamiliar binary names with
non Microsoft company names, often paired with `msiexec.exe` or a
vendor installer.

**Shape**: square wave. Volume jumps to a new plateau and stays
there.

**Closeout language**:

> Spike is the installation of vendor X on device group Y. The new
> baseline is expected. If the volume is excessive, propose a
> transform filter scoped to the named vendor binaries.

## When nothing matches

Continue to step 5 and step 6 of the [playbook](PLAYBOOK.md). The
spike vs baseline output plus the process tree drill on a single
device is enough to write a defensible closeout even if the pattern
is new to you. Add the new fingerprint to this file once you have
resolved it.
