### For Red Team Validation before a test, make sure the settings for MDAV are complete. Also refernced are MDI settings in the end. 
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
Purpose
Displays the real-time operational state of Microsoft Defender: engine versions, signature freshness, whether real-time protection is actually running, tamper protection, last scans, etc.


| Property                          | Description                                      | Typical Values                |
|-----------------------------------|--------------------------------------------------|-------------------------------|
| AMEngineVersion                   | Scanning engine version                          | e.g. 1.1.xxxxx.xxxx           |
| AMProductVersion                  | Overall Defender build                           | e.g. 4.18.xxxxx.xxxx          |
| AMRunningMode                     | Current mode                                     | Normal / Passive / Disabled   |
| AMServiceEnabled                  | Service running                                  | True / False                  |
| AntispywareEnabled                | Antispyware active                               | True / False                  |
| AntispywareSignatureAge           | Days since last antispyware update               | 0 = current                   |
| AntispywareSignatureVersion       | Current antispyware definitions                  | e.g. 1.441.xxx.0              |
| AntispywareSignatureLastUpdated   | Last antispyware signature update timestamp      | DateTime                      |
| AntivirusEnabled                  | Antivirus active                                 | True / False                  |
| AntivirusSignatureAge             | Days since last AV update                        | 0 = current                   |
| AntivirusSignatureVersion         | Current AV definitions                           | e.g. 1.441.xxx.0              |
| AntivirusSignatureLastUpdated     | Last antivirus signature update timestamp        | DateTime                      |
| BehaviorMonitorEnabled            | Real-time behavior monitoring                    | True / False                  |
| ComputerID                        | Unique device ID (masked)                        | GUID                          |
| DefenderSignaturesOutOfDate       | Signatures outdated                              | True / False                  |
| DeviceControlState                | USB/removable storage policy                     | Disabled / Enforced / Audit   |
| FullScanAge                       | Days since last full scan                        | 0 = today                     |
| FullScanStartTime                 | Last full scan start time                        | DateTime                      |
| FullScanEndTime                   | Last full scan end time                          | DateTime                      |
| IoavProtectionEnabled             | Scan downloads & attachments                     | True / False                  |
| IsTamperProtected                 | Tamper Protection active                         | True / False                  |
| IsVirtualMachine                  | Running as VM                                    | True / False                  |
| NISEnabled                        | Network Inspection System (exploit protection)   | True / False                  |
| OnAccessProtectionEnabled         | Real-time file scanning                          | True / False                  |
| ProductStatus                     | Overall health (524288 = fully healthy)          | 524288 = good                 |
| QuickScanAge                      | Days since last quick scan                       | 0 = today                     |
| QuickScanStartTime                | Last quick scan start time                       | DateTime                      |
| QuickScanEndTime                  | Last quick scan end time                         | DateTime                      |
| RealTimeProtectionEnabled         | Real-time protection active                      | True / False                  |
| RebootRequired                    | Reboot needed for updates/remediation            | True / False                  |
| SmartAppControlState              | Smart App Control status                         | Off / On / Evaluation        | SmartAppControlState              | Smart App Control status                         | Off / On / Evaluation         |


### Section 2 – Get-MpPreference (Applied Policy & Configuration)
Purpose
Shows every policy setting enforced on the endpoint (Intune/GPO/local) — exclusions, scan behavior, cloud protection, Controlled Folder Access, PUA blocking, tamper protection, etc.

| Setting                                      | Description                                                  | Typical Values                              |
|----------------------------------------------|--------------------------------------------------------------|---------------------------------------------|
| EnableControlledFolderAccess                 | Controlled Folder Access (ransomware protection)            | 0=Off 1=Audit 2=Block                       |
| EnableNetworkProtection                      | Network Protection (SmartScreen for network)                | 0=Off 1=Audit 2=Block                       |
| PUAProtection                                | Block Potentially Unwanted Applications                     | 0=Off 1=Audit 2=Block                       |
| MAPSReporting                                | Telemetry level sent to Microsoft                           | 0=Off 1=Basic 2=Advanced                    |
| SubmitSamplesConsent                         | Auto-submit suspicious samples                              | 0=Never 1=Safe 2=Always                     |
| CloudBlockLevel                              | Cloud protection aggressiveness                             | 0=Default 2=High 4=High+ 6=ZeroTolerance    |
| PerformanceModeStatus                        | Lightweight performance mode                                | 0=Off 1=On                                  |
| EnableLowCpuPriority                         | Lower CPU priority for scans                                | True / False                                |
| ScanAvgCPULoadFactor                         | Max CPU % during scheduled scans                            | 5–100                                       |
| ScanOnlyIfIdleEnabled                        | Only scan when system is idle                               | True / False                                |
| RandomizeScheduleTaskTimes                   | Randomize scheduled scan times                              | True / False                                |
| SchedulerRandomizationTime                   | Randomization window (hours)                                | 0–23                                        |
| DisableCatchupFullScan                       | Prevent catch-up full scans                                 | True / False                                |
| DisableCatchupQuickScan                      | Prevent catch-up quick scans                                | True / False                                |
| DisableScanningNetworkFiles                  | Skip scanning network files                                 | True / False                                |
| DisableScanningMappedNetworkDrivesForFullScan| Skip mapped drives in full scans                            | True / False                                |
| DisableEmailScanning                         | Skip email file scanning                                    | True / False                                |
| DisableQuicParsing                           | Disable QUIC (HTTP/3) parsing                               | True / False                                |
| EnableDnsSinkhole                            | Use Microsoft malicious domain sinkhole                     | True / False                                |
| HideExclusionsFromLocalUsers                 | Hide exclusion list from local admins                       | True / False                                |
| DisableCpuThrottleOnIdleScans                | No CPU throttling when idle (aggressive scanning)           | True = no throttling                        |
| DisableArchiveScanning                       | Prevent scanning inside archive files                       | True / False                                |
| DisableRemovableDriveScanning                | Skip scanning removable drives                              | True / False                                |
| DisableScriptScanning                        | Prevent scanning scripts                                    | True / False                                |
| DisableRealtimeMonitoring                    | Disable real-time protection                                | True / False                                |
| DisableIOAVProtection                        | Disable scanning of downloaded files and attachments        | True / False                                |
| DisableBehaviorMonitoring                    | Disable behavior monitoring                                 | True / False                                |
| DisableBlockAtFirstSeen                      | Disable blocking of suspicious files at first sight         | True / False                                |
| DisablePrivacyMode                           | Disable privacy mode                                        | True / False                                |
| DisableTamperProtection                      | Allow local changes to Defender settings                    | True = disabled                             |
| ExclusionPath                                | Paths excluded from scanning                                | List                                        |
| ExclusionProcess                             | Processes excluded from real-time scanning                  | List                                        |
| ExclusionExtension                           | File extensions excluded                                    | List                                        |
| ControlledFolderAccessProtectedFolders       | Extra folders protected by CFA                              | List                                        |
| ControlledFolderAccessAllowedApplications    | Apps allowed in protected folders                           | List                                        |


### Missed Detection from MDAV
Make sure this was followed - [ Evaluate Microsoft Defender Antivirus - Microsoft Defender for Endpoint | Microsoft Learn](https://learn.microsoft.com/en-us/defender-endpoint/evaluate-microsoft-defender-antivirus)
## Obtain the following logs
Obtain the Defender AV configuration from the device used in the testing by running the following PowerShell cmdlets (Windows) or shell comamnds (Linux/MacOs) on the device and copy paste the output into a notepad file. This is the easiest, fastest, and smallest (file size) method to get this information from the customer and the .txt file can simply be emailed.

```PS
#Windows
Get-MpPreference
Get-MpPreference | select -expand AttackSurfaceReductionRules_Actions
Get-MpPreference | select -expand AttackSurfaceReductionRules_Ids
Get-MpPreference | select -expand ExclusionPath
Get-MpPreference | select -expand ExclusionProcess
Get-MpPreference | select -expand ExclusionIPAddress
Get-MpPreference | select -expand ControlledFolderAccessAllowedApplications
Get-MpComputerStatus
​
#Linux/MacOs
mdatp health
cat /etc/opt/microsoft/mdatp/managed/mdatp_managed.json
```

### MDI Missed Detections:    
    
TenantId - TenantId from the M365D portal    
OrgId- OrgId from the M365D portal    
WorkspaceId - WorkspaceId from the M365D portal under settings, Identities, General, About    
Timeframe - Request the exact timeframe window when the testing was performed, ensure the customer supplies the time zone    
Tools used - Specific list of tools used; i.e BRC4, AttackIQ, sharphound, bloodhound, CS, etc.     
Customer TTPs - Specific list of TTPs/CLI syntax used/performed for each missed detection, including a description, and any IoC      
Source computer - Hostname and IP address    
Source account - SamAccountName attribute value    
Target DC - Hostname and IP address    
Network setup - Is there any VPN / NAT / PROXY between the source computer and the target DC? If so - what are they and what is its IP address?    
MDI Config - Request information on how long the sensor has been installed and running, is the DC sized according to the sizing tool?     
MDI Deployment – Provide the output of the MDI readiness script: https://github.com/microsoft/Microsoft-Defender-for-Identity/tree/main/Test-MdiReadiness      
