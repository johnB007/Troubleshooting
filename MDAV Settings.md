### MDAV – Full Status & Policy Reference  for  Get-MpComputerStatus and Get-MpPreference

### Common Values Legend
| Value   | Meaning                                      |
|---------|----------------------------------------------|
| (blank) | Not configured / inherits default           |
| 0       | Disabled / Off / Never                       |
| 1       | Enabled / Audit mode                         |
| 2       | Block mode / Fully active / Auto-send        |

---

### Section 1 – Get-MpComputerStatus (Current Runtime Status)

**PowerShell command**  
```powershell
Get-MpComputerStatus
Purpose
Displays the real-time operational state of Microsoft Defender: engine versions, signature freshness, whether real-time protection is actually running, tamper protection, last scans, etc.
text| Property                     | Description                                      | Typical Values                | Sanitized Value     |
|------------------------------|--------------------------------------------------|-------------------------------|---------------------|
| AMEngineVersion              | Scanning engine version                          | e.g. 1.1.xxxxx.xxxx           | 1.1.25100.9002      |
| AMProductVersion             | Overall Defender build                           | e.g. 4.18.xxxxx.xxxx          | 4.18.25100.9008     |
| AMRunningMode                | Current mode                                     | Normal / Passive / Disabled   | Normal              |
| AMServiceEnabled             | Service running                                  | True / False                  | True                |
| AntispywareEnabled           | Antispyware active                               | True / False                  | True                |
| AntispywareSignatureAge      | Days since last antispyware update               | 0 = current                   | 0                   |
| AntispywareSignatureVersion  | Current antispyware definitions                  | e.g. 1.441.xxx.0              | 1.441.367.0         |
| AntivirusEnabled             | Antivirus active                                 | True / False                  | True                |
| AntivirusSignatureAge        | Days since last AV update                        | 0 = current                   | 0                   |
| AntivirusSignatureVersion    | Current AV definitions                           | e.g. 1.441.xxx.0              | 1.441.367.0         |
| BehaviorMonitorEnabled       | Real-time behavior monitoring                    | True / False                  | True                |
| ComputerID                   | Unique device ID (masked)                        | GUID                          | 010101…             |
| DefenderSignaturesOutOfDate  | Signatures outdated                              | True / False                  | False               |
| DeviceControlState           | USB/removable storage policy                     | Disabled / Enforced / Audit   | Disabled            |
| FullScanAge                  | Days since last full scan                        | 0 = today                     | 0                   |
| IoavProtectionEnabled        | Scan downloads & attachments                     | True / False                  | True                |
| IsTamperProtected            | Tamper Protection active                         | True / False                  | True                |
| IsVirtualMachine             | Running as VM                                    | True / False                  | True                |
| NISEnabled                   | Network Inspection System (exploit protection)  | True / False                  | True                |
| OnAccessProtectionEnabled    | Real-time file scanning                          | True / False                  | True                |
| ProductStatus                | Overall health (524288 = fully healthy)          | 524288 = good                 | 524288              |
| QuickScanAge                 | Days since last quick scan                       | 0 = today                     | 0                   |
| RealTimeProtectionEnabled    | Real-time protection active                      | True / False                  | True                |
| RebootRequired               | Reboot needed for updates/remediation           | True / False                  | False               |
| SmartAppControlState         | Smart App Control status                         | Off / On / Evaluation         | Off                 |
| TamperProtectionSource       | Managed by                                       | Intune / SCCM / Local         | Intune              |

Section 2 – Get-MpPreference (Applied Policy & Configuration)
PowerShell command
PowerShellGet-MpPreference
Purpose
Shows every policy setting enforced on the endpoint (Intune/GPO/local) — exclusions, scan behavior, cloud protection, Controlled Folder Access, PUA blocking, tamper protection, etc.
text| Setting                                      | Description                                                  | Typical Values                              | Sanitized Value             |
|----------------------------------------------|--------------------------------------------------------------|---------------------------------------------|-----------------------------|
| EnableControlledFolderAccess                 | Controlled Folder Access (ransomware protection)             | 0=Off 1=Audit 2=Block                       | 1 (Audit mode)              |
| EnableNetworkProtection                      | Network Protection (SmartScreen for network)                 | 0=Off 1=Audit 2=Block                       | 1 (Audit mode)              |
| PUAProtection                                | Block Potentially Unwanted Applications                      | 0=Off 1=Audit 2=Block                       | 2 (Block)                   |
| MAPSReporting                                | Telemetry level sent to Microsoft                            | 0=Off 1=Basic 2=Advanced                    | 2 (Advanced)                |
| SubmitSamplesConsent                         | Auto-submit suspicious samples                               | 0=Never 1=Safe 2=Always                     | 2 (Always)                  |
| CloudBlockLevel                              | Cloud protection aggressiveness                              | 0=Default 2=High 4=High+ 6=ZeroTolerance    | 0 (Default)                 |
| PerformanceModeStatus                        | Lightweight performance mode                                 | 0=Off 1=On                                  | 1 (On)                      |
| EnableLowCpuPriority                         | Lower CPU priority for scans                                 | True / False                                | True                        |
| ScanAvgCPULoadFactor                         | Max CPU % during scheduled scans                             | 5–100                                       | 25                          |
| ScanOnlyIfIdleEnabled                        | Only scan when system is idle                                | True / False                                | True                        |
| RandomizeScheduleTaskTimes                   | Randomize scheduled scan times                               | True / False                                | True                        |
| SchedulerRandomizationTime                   | Randomization window (hours)                                 | 0–23                                        | 2                           |
| DisableCatchupFullScan                       | Prevent catch-up full scans                                  | True / False                                | True                        |
| DisableCatchupQuickScan                      | Prevent catch-up quick scans                                 | True / False                                | True                        |
| DisableScanningNetworkFiles                  | Skip scanning network files                                  | True / False                                | True                        |
| DisableScanningMappedNetworkDrivesForFullScan| Skip mapped drives in full scans                             | True / False                                | True                        |
| DisableEmailScanning                         | Skip email file scanning                                     | True / False                                | True                        |
| DisableQuicParsing                           | Disable QUIC (HTTP/3) parsing                                | True / False                                | True                        |
| EnableDnsSinkhole                            | Use Microsoft malicious domain sinkhole                      | True / False                                | True                        |
| HideExclusionsFromLocalUsers                 | Hide exclusion list from local admins                        | True / False                                | True                        |
| DisableCpuThrottleOnIdleScans                | No CPU throttling when idle (aggressive scanning)            | True = no throttling                        | True                        |
| ExclusionPath                                | Paths excluded from scanning (sanitized)                     | List                                        | [Redacted corporate paths]  |
| ExclusionProcess                             | Processes excluded from real-time scanning (sanitized)       | List                                        | [Redacted scanner agents]   |
| ExclusionExtension                           | File extensions excluded                                     | List                                        | (none)                      |
| ControlledFolderAccessProtectedFolders       | Extra folders protected by CFA (sanitized)                   | List                                        | E:\ (data drive)            |
| ControlledFolderAccessAllowedApplications    | Apps allowed in protected folders (sanitized)                | List                                        | [Redacted EDR/AV agents]    |
| ScanScheduleDay                              | Scheduled scan day (0 = every day)                           | 0–8                                         | 0 (every day)               |
| ScanScheduleTime                             | Preferred scan time                                          | HH:MM:SS                                    | 03:00:00                    |
| SignatureUpdateInterval                      | Definition update check interval (hours)                     | 1–24                                        | 1 (hourly)                  |
| UILockdown                                   | Hide Defender UI from users                                  | True / False                                | False                       |
| DisableTamperProtection                      | Allow local changes to Defender settings                     | True = disabled                             | False (protected)           |
