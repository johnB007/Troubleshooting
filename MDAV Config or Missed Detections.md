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
| AMServiceEnabled                  | Defender service running                         | True / False                  |
| AMServiceVersion                  | Defender service version                         | e.g. 4.18.xxxxx.xxxx          |
| AntispywareEnabled                | Antispyware component active                     | True / False                  |
| AntispywareSignatureAge           | Days since last antispyware update               | 0 = current                   |
| AntispywareSignatureVersion       | Current antispyware definitions                  | e.g. 1.443.xxx.0              |
| AntispywareSignatureLastUpdated   | Last antispyware signature update timestamp      | DateTime                      |
| AntivirusEnabled                  | Antivirus component active                       | True / False                  |
| AntivirusSignatureAge             | Days since last antivirus update                 | 0 = current                   |
| AntivirusSignatureVersion         | Current antivirus definitions                    | e.g. 1.443.xxx.0              |
| AntivirusSignatureLastUpdated     | Last antivirus signature update timestamp        | DateTime                      |
| BehaviorMonitorEnabled            | Real-time behavior monitoring                    | True / False                  |
| ComputerID                        | Unique device identifier (masked)                | GUID                          |
| ComputerState                     | Internal Defender state code                     | Integer                       |
| DefenderSignaturesOutOfDate       | Signatures are outdated                          | True / False                  |
| DeviceControlState                | Removable media / USB control state              | Enabled / Audit / Disabled    |
| DeviceControlDefaultEnforcement   | Default enforcement when no policy matches       | DefaultAllow / Deny           |
| DeviceControlPoliciesLastUpdated  | Last device control policy refresh               | DateTime                      |
| FullScanAge                       | Days since last full scan                        | Integer                       |
| FullScanStartTime                 | Last full scan start time                        | DateTime                      |
| FullScanEndTime                   | Last full scan end time                          | DateTime                      |
| FullScanOverdue                   | Full scan overdue                                | True / False                  |
| FullScanRequired                  | Full scan required                               | True / False                  |
| FullScanSignatureVersion          | Signature version used for last full scan        | e.g. 1.437.xxx.0              |
| InitializationProgress            | Service startup state                            | Status string                 |
| IoavProtectionEnabled             | Scan downloads and attachments                   | True / False                  |
| IsTamperProtected                 | Tamper Protection enforced                       | True / False                  |
| TamperProtectionSource            | Source enforcing tamper protection               | Intune / GPO / Local          |
| IsVirtualMachine                  | Device is a virtual machine                      | True / False                  |
| NISEnabled                        | Network Inspection System enabled                | True / False                  |
| NISEngineVersion                  | NIS engine version                               | e.g. 1.1.xxxxx.xxxx           |
| NISSignatureAge                   | Days since last NIS update                       | 0 = current                   |
| NISSignatureVersion               | Current NIS definitions                          | e.g. 1.443.xxx.0              |
| NISSignatureLastUpdated           | Last NIS signature update time                   | DateTime                      |
| OnAccessProtectionEnabled         | Real-time file system scanning                   | True / False                  |
| ProductStatus                     | Overall Defender health code                     | 524288 = Healthy              |
| QuickScanAge                      | Days since last quick scan                       | Integer                       |
| QuickScanStartTime                | Last quick scan start time                       | DateTime                      |
| QuickScanEndTime                  | Last quick scan end time                         | DateTime                      |
| QuickScanOverdue                  | Quick scan overdue                               | True / False                  |
| QuickScanSignatureVersion         | Signature version used for quick scan            | e.g. 1.443.xxx.0              |
| RealTimeProtectionEnabled         | Real-time protection active                      | True / False                  |
| RealTimeScanDirection             | RTP scan direction                               | 0=Both 1=Incoming 2=Outgoing  |
| RebootRequired                    | Reboot required for remediation                  | True / False                  |
| SmartAppControlState              | Smart App Control status                         | Off / On / Evaluation         |
| SmartAppControlExpiration         | Smart App Control expiration                     | DateTime / Empty              |
| LastFullScanSource                | Source of last full scan                         | Integer                       |
| LastQuickScanSource               | Source of last quick scan                        | Integer                       |
| TDTCapable                        | Intel Threat Detection capability                | True / False / N/A            |
| TDTMode                           | Intel TDT operating mode                         | Mode / N/A                    |
| TDTStatus                         | Intel TDT status                                 | Status / N/A                  |
| TDTSiloType                       | Intel TDT silo type                              | Type / N/A                    |
| TDTTelemetry                      | Intel TDT telemetry enabled                      | True / False / N/A            |
| TroubleShootingMode               | Defender troubleshooting mode                    | Enabled / Disabled            |
| TroubleShootingModeSource         | Source enabling troubleshooting                  | Service / Local / Intune      |
| TroubleShootingStartTime          | Troubleshooting start time                       | DateTime / N/A                |
| TroubleShootingEndTime            | Troubleshooting end time                         | DateTime / INFINITE           |
| TroubleShootingExpirationLeft     | Remaining troubleshooting duration               | INFINITE / Minutes            |
| TroubleShootingDailyMaxQuota      | Max daily troubleshooting quota (minutes)        | Integer                       |
| TroubleShootingDailyQuotaLeft     | Remaining troubleshooting quota                  | Integer                       |
| TroubleShootingQuotaResetTime     | Quota reset time                                 | DateTime / N/A                |



### Section 2 – Get-MpPreference (Applied Policy & Configuration)
Purpose
Shows every policy setting enforced on the endpoint (Intune/GPO/local) — exclusions, scan behavior, cloud protection, Controlled Folder Access, PUA blocking, tamper protection, etc.

| Setting                                      | Description                                                  | Typical Values                              |
|----------------------------------------------|--------------------------------------------------------------|---------------------------------------------|
| EnableControlledFolderAccess                 | Controlled Folder Access (ransomware protection)            | 0=Off 1=Audit 2=Block                       |
| EnableNetworkProtection                      | Network Protection (SmartScreen for network)                | 0=Off 1=Audit 2=Block                       |
| AllowNetworkProtectionOnWinServer            | Allow Network Protection on Windows Server                  | True / False                                |
| AllowNetworkProtectionDownLevel              | Allow Network Protection on down-level OS                   | True / False                                |
| PUAProtection                                | Block Potentially Unwanted Applications                     | 0=Off 1=Audit 2=Block                       |
| MAPSReporting                                | Telemetry level sent to Microsoft                           | 0=Off 1=Basic 2=Advanced                    |
| SubmitSamplesConsent                         | Auto-submit suspicious samples                              | 0=Never 1=Safe 2=Always                     |
| CloudBlockLevel                              | Cloud protection aggressiveness                             | 0=Default 2=High 4=High+ 6=ZeroTolerance    |
| CloudExtendedTimeout                         | Max cloud verdict wait time (seconds)                      | Integer                                    |
| PerformanceModeStatus                        | Lightweight performance mode                                | 0=Off 1=On                                  |
| EnableLowCpuPriority                         | Lower CPU priority for scans                                | True / False                                |
| ScanAvgCPULoadFactor                         | Max CPU % used during scheduled scans                      | 5–100                                       |
| ScanOnlyIfIdleEnabled                        | Only scan when system is idle                               | True / False                                |
| RandomizeScheduleTaskTimes                   | Randomize scheduled scan times                              | True / False                                |
| SchedulerRandomizationTime                   | Randomization window (hours)                                | 0–23                                        |
| DisableCatchupFullScan                       | Prevent catch-up full scans                                 | True / False                                |
| DisableCatchupQuickScan                      | Prevent catch-up quick scans                                | True / False                                |
| DisableScanningNetworkFiles                  | Skip scanning network files                                 | True / False                                |
| DisableScanningMappedNetworkDrivesForFullScan| Skip mapped drives during full scans                        | True / False                                |
| DisableEmailScanning                         | Skip scanning email content                                 | True / False                                |
| DisableArchiveScanning                       | Prevent scanning inside archive files                       | True / False                                |
| DisableRemovableDriveScanning                | Skip scanning removable media                               | True / False                                |
| DisableScriptScanning                        | Disable script scanning                                     | True / False                                |
| DisableRealtimeMonitoring                    | Disable real-time protection                                | True / False                                |
| DisableIOAVProtection                        | Disable scanning of downloaded content                     | True / False                                |
| DisableBehaviorMonitoring                    | Disable behavior monitoring                                 | True / False                                |
| DisableBlockAtFirstSeen                      | Disable block-at-first-sight                                | True / False                                |
| DisablePrivacyMode                           | Disable privacy mode                                        | True / False                                |
| DisableTamperProtection                     | Allow local changes to Defender settings                    | True = Disabled                             |
| EnableDnsSinkhole                            | Block malicious domains via Microsoft sinkhole              | True / False                                |
| DisableDnsParsing                            | Disable DNS inspection                                      | True / False                                |
| DisableDnsOverTcpParsing                     | Disable DNS-over-TCP inspection                              | True / False                                |
| DisableHttpParsing                           | Disable HTTP inspection                                     | True / False                                |
| DisableQuicParsing                           | Disable QUIC (HTTP/3) inspection                             | True / False                                |
| DisableSmtpParsing                           | Disable SMTP inspection                                     | True / False                                |
| DisableFtpParsing                            | Disable FTP inspection                                      | True / False                                |
| DisableSshParsing                            | Disable SSH inspection                                      | True / False                                |
| DisableTlsParsing                            | Disable TLS inspection                                      | True / False                                |
| DisableRdpParsing                            | Disable RDP inspection                                      | True / False                                |
| DisableCpuThrottleOnIdleScans                | Remove CPU throttling when system is idle                   | True = No throttling                        |
| HideExclusionsFromLocalUsers                 | Hide Defender exclusions from local admins                  | True / False                                |
| AttackSurfaceReductionRules_Ids              | ASR rule GUIDs applied                                      | List                                        |
| AttackSurfaceReductionRules_Actions          | ASR enforcement action per rule                             | 0=Disabled 1=Audit 2=Block                  |
| AttackSurfaceReductionOnlyExclusions         | Global ASR-only exclusions                                  | List                                        |
| AttackSurfaceReductionRules_RuleSpecificExclusions | Per-rule ASR exclusions                                | List                                        |
| ControlledFolderAccessDefaultProtectedFolders| Default folders protected by CFA                            | List                                        |
| ControlledFolderAccessProtectedFolders       | Additional CFA protected folders                            | List                                        |
| ControlledFolderAccessAllowedApplications    | Applications allowed through CFA                            | List                                        |
| ExclusionPath                                | Paths excluded from scanning                                | List                                        |
| ExclusionProcess                             | Processes excluded from scanning                            | List                                        |
| ExclusionExtension                           | File extensions excluded                                    | List                                        |
| ExclusionIpAddress                           | IP addresses excluded                                       | List                                        |
| DefinitionUpdatesChannel                     | AV definition update channel                                | Integer                                    |
| EngineUpdatesChannel                         | Defender engine update channel                              | Integer                                    |
| PlatformUpdatesChannel                       | Defender platform update channel                            | Integer                                    |
| MeteredConnectionUpdates                    | Allow updates over metered networks                        | True / False                                |
| SignatureScheduleDay                         | Scheduled signature update day                             | 0–8                                        |
| SignatureScheduleTime                        | Scheduled signature update time                            | HH:MM:SS                                   |
| SignatureUpdateInterval                      | Signature update frequency (hours)                         | Integer                                    |
| SignatureUpdateCatchupInterval               | Catch-up update interval (hours)                           | Integer                                    |
| ScanScheduleDay                              | Scheduled scan day                                         | 0–7                                        |
| ScanScheduleTime                             | Scheduled scan time                                        | HH:MM:SS                                   |
| ScanScheduleQuickScanTime                   | Scheduled quick scan time                                  | HH:MM:SS                                   |
| ScanScheduleOffset                           | Delay before scheduled scan (minutes)                     | Integer                                    |
| QuarantinePurgeItemsAfterDelay              | Days before quarantined items are purged                  | Integer                                    |
| ServiceHealthReportInterval                 | Service health reporting interval (minutes)              | Integer                                    |
| UILockdown                                  | Restrict Defender UI access                                | True / False                                |
| IntelTDTEnabled                             | Intel Threat Detection Technology                          | True / False                                |


### Missed Detection from MDAV
Make sure this was followed - [ Evaluate Microsoft Defender Antivirus - Microsoft Defender for Endpoint | Microsoft Learn](https://learn.microsoft.com/en-us/defender-endpoint/evaluate-microsoft-defender-antivirus)
## Obtain the following logs
Obtain the Defender AV configuration from the device used in the testing by running the following PowerShell cmdlets (Windows) or shell comamnds (Linux/MacOs).  Obtain only the output in a .txt file as thats the easiest, fastest, and smallest (file size) method to get this information from the customer. The following will run and then be available in the temp folder to email. 

```PS
#Windows
Start-Transcript -Path "C:\Temp\Defender_Output.txt"
Get-MpPreference
Get-MpPreference | select -expand AttackSurfaceReductionRules_Actions
Get-MpPreference | select -expand AttackSurfaceReductionRules_Ids
Get-MpPreference | select -expand ExclusionPath
Get-MpPreference | select -expand ExclusionProcess
Get-MpPreference | select -expand ExclusionIPAddress
Get-MpPreference | select -expand ControlledFolderAccessAllowedApplications
Get-MpComputerStatus
Stop-Transcript
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
