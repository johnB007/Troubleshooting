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

## Windows Feature Update wave (major version uplift)

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `services.exe` | `setuphost.exe` | Microsoft Corporation |
| `setuphost.exe` | `setupplatform.exe` | Microsoft Corporation |
| `svchost.exe` | `windowsupdatebox.exe` | Microsoft Corporation |
| `setupplatform.exe` | `dism.exe` | Microsoft Corporation |

**Shape**: multi day plateau, 2 to 4 days long, spanning
`DeviceFileEvents`, `DeviceProcessEvents`, and `DeviceRegistryEvents`
all at once. Distinct from monthly Patch Tuesday because the spike is
wider and includes `Windows.old` folder activity.

**Closeout language**:

> Spike aligns with a Windows feature update (major version uplift)
> rolling through the named device groups. Activity is concentrated
> on `setuphost.exe` and `setupplatform.exe` and will subside within
> the rollout window. No transform changes are required.

## Intune or Configuration Manager software deployment wave

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `IntuneManagementExtension.exe` | `msiexec.exe` | Microsoft Corporation |
| `CcmExec.exe` | `TSManager.exe` | Microsoft Corporation |
| `CcmExec.exe` | `cmtrace.exe` | Microsoft Corporation |
| `msiexec.exe` | vendor installer | varies |

**Shape**: scheduled to a maintenance window, sharp jump, returns to
baseline (or a new higher baseline if the deployed app is chatty).

**Closeout language**:

> Spike tracks an Intune or Configuration Manager software deployment
> wave for the named app. Volume returns to baseline once the
> deployment completes. If the deployed app keeps generating events
> at a new baseline, propose a transform filter scoped to the named
> binary.

## Microsoft Defender Antivirus scheduled scan wave

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `services.exe` | `MsMpEng.exe` | Microsoft Corporation |
| `MsMpEng.exe` | wide variety of scanned files | varies |

**Step 1 ActionType signals**: `AntivirusScanStarted`,
`AntivirusScanCompleted`, `AntivirusDetection`.

**Shape**: short, sharp spike (1 to 4 hours) that recurs on the
scheduled scan window. Fleet wide.

**Closeout language**:

> Spike matches the scheduled Microsoft Defender Antivirus scan
> window for the fleet. Activity is concentrated on `MsMpEng.exe`
> and is short lived. No transform changes are required.

## Backup agent run wave

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `services.exe` | `wbengine.exe` | Microsoft Corporation |
| `services.exe` | `obengine.exe` (Azure Backup MARS) | Microsoft Corporation |
| `services.exe` | `VeeamAgent.exe` | Veeam Software |
| `services.exe` | `cvd.exe` (Commvault) | Commvault |

**Step 1 ActionType signals**: heavy `FileCreated` and `FileOpened`
on volume snapshots.

**Shape**: recurring on the backup schedule (often nightly or
weekly), fleet wide, returns to baseline within hours of completion.

**Closeout language**:

> Spike aligns with the scheduled backup job for the named device
> groups. Activity tracks volume snapshot creation by the backup
> agent. No transform changes are required.

## Azure Arc agent rollout

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `services.exe` | `azcmagent.exe` | Microsoft Corporation |
| `services.exe` | `himdsagent.exe` | Microsoft Corporation |
| `azcmagent.exe` | `gcad.exe` | Microsoft Corporation |
| `services.exe` | `ExtensionService.exe` | Microsoft Corporation |

**Shape**: gradual ramp over days on server SKUs as the Arc rollout
reaches new groups.

**Closeout language**:

> Spike tracks the Azure Arc agent rollout for the named server
> fleet. Volume will plateau once all servers are connected. No
> transform changes are required.

## Sysmon configuration push

**Top rows in query 03 look like**: large jump in events whose
`InitiatingProcessFileName` matches the running Sysmon binary.

**Shape**: short spike on the day of the push. New baseline after
the push if the new config is more permissive than the previous one.

**Closeout language**:

> Spike matches a Sysmon configuration push to the named device
> groups. If volume remains elevated after the push completes,
> review the new Sysmon config for rules that generate more events
> than required.

## Microsoft Purview Endpoint DLP policy rollout

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `services.exe` | `MpDlpService.exe` | Microsoft Corporation |
| `MpDlpService.exe` | `endpointdlp.exe` | Microsoft Corporation |

**Step 1 ActionType signals**: any ActionType beginning with `Dlp`.

**Shape**: jump on the policy publish, then a new baseline if the
policy stays permissive.

**Closeout language**:

> Spike matches the rollout of a Microsoft Purview Endpoint DLP
> policy. Volume returns to a new baseline once the policy reaches
> all endpoints. If the policy is generating more events than
> required, scope the policy to a smaller location set.

## Certificate auto enrollment wave

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `gpsvc` | `certutil.exe` | Microsoft Corporation |
| `services.exe` | `certreq.exe` | Microsoft Corporation |

**Step 1 ActionType signals**: `CertificateImported`,
`CertificateExported`.

**Shape**: short spike coincident with a CA renewal or an auto
enrollment GPO change. Fleet wide on domain joined devices.

**Closeout language**:

> Spike matches a certificate auto enrollment wave from the
> Enterprise Certificate Authority. Activity is concentrated on
> `certutil.exe` and `certreq.exe`. Volume returns to baseline once
> enrollment completes.

## Group Policy or Intune policy refresh storm

**Top rows in query 03 look like**:

| ParentFileName | FileName | CompanyName |
|---|---|---|
| `svchost.exe` | `gpupdate.exe` | Microsoft Corporation |
| `services.exe` | `IntuneManagementExtension.exe` | Microsoft Corporation |

**Shape**: short, sharp spike (under an hour) after a published
policy change reaches the fleet.

**Closeout language**:

> Spike matches a Group Policy or Intune policy refresh storm
> following a published policy change. Activity is short lived and
> returns to baseline within hours. No transform changes are
> required.

## When nothing matches

Continue to step 5 and step 6 of the [playbook](PLAYBOOK.md). The
spike vs baseline output plus the process tree drill on a single
device is enough to write a defensible closeout even if the pattern
is new to you. Add the new fingerprint to this file once you have
resolved it.

=====

# Non Device* spike causes (Sentinel side)

The fingerprints above apply to the Microsoft Defender XDR `Device*`
tables. Enterprise tenants also see spikes in tables that this
workbook does not query. The patterns below are the most common
ones, with the table they hit and the usual fix.

## CommonSecurityLog explosion (firewall or proxy)

**Trigger**: verbosity flipped on a Palo Alto, Fortinet, Check Point,
Cisco ASA, or Zscaler appliance. Trust traffic logging or debug mode
turned on.

**Closeout**:

> Spike on `CommonSecurityLog` traces to verbosity change on the
> named appliance. Roll the appliance verbosity back, or add a DCR
> filter on the `DeviceVendor` and `DeviceProduct` fields to scope
> what reaches the workspace.

## Syslog explosion

**Trigger**: new chatty Linux source onboarded, or rsyslog facility
and severity widened by the platform team.

**Closeout**:

> Spike on `Syslog` traces to a widened facility or severity scope
> on the named hosts. Scope the AMA DCR back to the required
> facilities and severities.

## SecurityEvent surge

**Trigger**: AD audit policy widened to include more subcategories
(account management, directory service access, object access), or a
batch of DCs added to AMA collection at once.

**Closeout**:

> Spike on `SecurityEvent` traces to a widened audit policy or a new
> set of DCs onboarded. Scope the SecurityEvent collection tier in
> the DCR (Minimum, Common, All) to match what detections actually
> consume.

## AzureDiagnostics surge

**Trigger**: a new resource has a diagnostic setting forwarding all
categories instead of the categories the SOC actually needs.

**Closeout**:

> Spike on `AzureDiagnostics` traces to a new diagnostic setting on
> the named resource forwarding every category. Scope the diagnostic
> setting to the required categories only.

## Custom `*_CL` table doubling

**Trigger**: dual write from two collectors, or a chatty new app log
onboarded into a custom table.

**Closeout**:

> Spike on the named `*_CL` table traces to a duplicate collector or
> a newly onboarded application. Deduplicate the collectors, or add
> a DCR transform on the table to drop the noise.

## SecurityAlert surge

**Trigger**: a new analytics rule firing too often, or a Logic App
incident loop creating duplicate incidents.

**Closeout**:

> Spike on `SecurityAlert` traces to the named analytics rule (or
> playbook loop). Tune the rule, add suppression, or break the loop
> in the playbook.

## Heartbeat surge

**Trigger**: a new agent fleet onboarded (AMA or MMA).

**Closeout**:

> Spike on `Heartbeat` traces to the onboarding of the named agent
> fleet. Expected. Ride it out.

## W3CIISLog surge

**Trigger**: verbose IIS logging turned on, or a high traffic site
newly onboarded into collection.

**Closeout**:

> Spike on `W3CIISLog` traces to verbosity change or a new site in
> collection. Scope which sites forward via the AMA DCR.

## AADNonInteractiveUserSignInLogs surge

**Trigger**: a new application onboarded that polls Microsoft Graph
or another resource aggressively, generating one sign in per token
refresh.

**Closeout**:

> Spike on `AADNonInteractiveUserSignInLogs` traces to the named
> application identified by `AppDisplayName`. Usually expected
> behavior. If the volume is excessive, raise it with the application
> owner.

## Brand new table from a newly enabled connector

**Trigger**: another team enabled a connector without socializing it
with the SOC.

**Closeout**:

> The named table is new in the workspace as of the spike date.
> Trace the data connector that creates it and confirm whether the
> data is in scope for SOC retention. If not, disable the connector
> or move the table to the Lake tier.
