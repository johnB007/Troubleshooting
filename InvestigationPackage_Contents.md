
# Investigation Package Contents for Windows Devices
Purpose: Forensic snapshot collected during active incident response to identify the current state of a device and understand tools and techniques used by an attacker. 

When to Use: During or after a security incident, When investigating alerts or suspicious activity, As part of the investigation or response process, Take response actions on a device in Microsoft, When you need a point-in-time forensic snapshot, or deep troubleshooting from an EDR perspective. 

<img width="2505" height="414" alt="image" src="https://github.com/user-attachments/assets/3b22e53e-2b0d-4543-a146-5ca77373466d" />
<img width="2206" height="381" alt="image" src="https://github.com/user-attachments/assets/18e15e82-a98b-4fc0-a8e2-78a3b595f784" />
<img width="2547" height="1608" alt="image" src="https://github.com/user-attachments/assets/198f010c-059d-4d07-a8a3-07c315ab132c" />

For Windows devices, the package contains the folders described in the following table:

## Folder Structure

| Folder | Description |
|--------|-------------|
| **📁 Autoruns** | Contains a set of files that each represent the content of the registry of a known auto start entry point (ASEP) to help identify attacker's persistency on the device.<br><br>If the registry key isn't found, the file contains the following message: "ERROR: The system was unable to find the specified registry key or value." |
| **📁 Installed programs** | This .CSV file contains the list of installed programs that can help identify what is currently installed on the device. For more information, see [Win32_Product class](https://docs.microsoft.com/windows/win32/cimwin32prov/win32-product). |
| **📁 Network connections** | This folder contains a set of data points related to the connectivity information that can help in identifying connectivity to suspicious URLs, attacker's command and control (C&C) infrastructure, any lateral movement, or remote connections.<br><br>- **📁 ActiveNetConnections.txt**: Displays protocol statistics and current TCP/IP network connections. Enables you to look for suspicious connectivity made by a process.<br>- **📁 Arp.txt**: Displays the current address resolution protocol (ARP) cache tables for all interfaces. ARP cache can reveal other hosts on a network that were compromised or suspicious systems on the network that might be used to run an internal attack.<br>- **📁 DnsCache.txt**: Displays the contents of the DNS client resolver cache, which includes both entries preloaded from the local Hosts file and any recently obtained resource records for name queries resolved by the computer. This can help in identifying suspicious connections.<br>- **📁 IpConfig.txt**: Displays the full TCP/IP configuration for all adapters. Adapters can represent physical interfaces, such as installed network adapters, or logical interfaces, such as dial-up connections.<br>- **📁 FirewallExecutionLog.txt and pfirewall.log**: The pfirewall.log file must exist in `%windir%\system32\logfiles\firewall\pfirewall.log`, so it's included in the investigation package. For more information on creating the firewall log file, see [Configure the Windows Firewall with Advanced Security Log](https://docs.microsoft.com/windows/security/threat-protection/windows-firewall/configure-windows-firewall-log). |
| **📁 Prefetch files** | Windows Prefetch files are designed to speed up the application startup process. It can be used to track all the files recently used in the system and find traces for applications that might be deleted but can still be found in the prefetch file list.<br><br>- **📁 Prefetch folder**: Contains a copy of the prefetch files from `%SystemRoot%\Prefetch`. We recommend downloading a prefetch file viewer to view the prefetch files.<br>- **📁 PrefetchFilesList.txt**: Contains the list of all the copied files that can be used to track if there were any copy failures to the prefetch folder. |
| **📁 Processes** | Contains a .CSV file listing the running processes and provides the ability to identify current processes running on the device. This can be useful when identifying a suspicious process and its state. |
| **📁 Scheduled tasks** | Contains a .CSV file listing the scheduled tasks, which can be used to identify routines performed automatically on a chosen device to look for suspicious code that was set to run automatically. |
| **📁 Security event log** | Contains the security event log, which contains records of sign-in or sign-out activity, or other security-related events specified by the system's audit policy.<br><br>Open the event log file using Event viewer. |
| **📁 Services** | Contains a .CSV file that lists services and their states. |
| **📁 Windows Server Message Block SMB sessions** | Lists shared access to files, printers, and serial ports and miscellaneous communications between nodes on a network. This can help identify data exfiltration or lateral movement.<br><br>Contains files for SMBInboundSessions and SMBOutboundSession. If there are no sessions (inbound or outbound), you get a text file that tells you that there are no SMB sessions found. |
| **📁 System Information** | Contains a SystemInformation.txt file that lists system information such as OS version and network cards. |
| **📁 Temp Directories** | Contains a set of text files that lists the files located in `%Temp%` for every user in the system. This can help to track suspicious files that an attacker might have dropped on the system.<br><br>If the file contains the following message: "The system cannot find the path specified", it means that there's no temp directory for this user, and might be because the user didn't sign in to the system. |
| **📁 Users and Groups** | Provides a list of files that each represent a group and its members. |
| **📁 WdSupportLogs** | Provides the MpCmdRunLog.txt and MPSupportFiles.cab. This folder is only created on Windows 10, version 1709 or later with February 2020 update rollup. |
| **📁 CollectionSummaryReport.xls** | This file is a summary of the investigation package collection, it contains the list of data points, the command used to extract the data, the execution status, and the error code if there's failure. You can use this report to track if the package includes all the expected data and identify if there were any errors. |

## WdSupportLogs

### Detailed Breakdown of Files in the Support Folder/MPSupportFiles.cab

Each .cab file is a compressed archive containing logs and diagnostics. Here's what some of the common ones include:

| File Name | Category | Description |
|-----------|----------|-------------|
| **📁 ACPIN.txt** | System and Component Status | ACPI (Advanced Configuration and Power Interface) information dump, detailing power management and hardware enumeration relevant to Defender's system scanning and performance. Useful for troubleshooting boot-sector or low-level hardware-related scan issues. |
| **📁 AppAccLauncherDLLInjection.log** | Command and Tracing Files | Logs DLL injections attempted by application access launchers, tracking potential security events or misconfigurations in app execution. Helps investigate injection-based threats or Defender's real-time protection responses. |
| **📁 AppEvent.txt** | Event and Operational Logs | Application event logs from Defender's monitoring of app behaviors, including starts, stops, and errors. Mirrors subsets of Event Viewer for app-specific telemetry; key for correlating app crashes with Defender actions. |
| **📁 AppEvent.xml** | Event and Operational Logs | XML-formatted application event data, providing structured details on app interactions with Defender (e.g., blocked executions). Exportable for parsing in tools like PowerShell; useful for automated analysis. |
| **📁 CacheFileNamedump...** | System and Component Status | Dump of cached filenames from Defender's scan cache, listing hashed or temporary files observed during scans. Aids in reconstructing recent file activity and optimizing scan performance reviews. |
| **📁 Cbs.log** | System and Component Status | Component-Based Servicing (CBS) log from Windows, capturing system file repairs and updates that may impact Defender components. Essential for diagnosing update failures or corrupted Defender binaries. |
| **📁 CbsDNList...** | System and Component Status | CBS dependency network list, detailing inter-component relationships for servicing. Helps trace why Defender updates or features fail due to missing dependencies. |
| **📁 customDNList** | Custom Configuration | Custom DNS list entry (part 1), logging user-defined or policy-applied DNS exclusions/blocklists for Defender's network filtering. Useful for verifying custom network protection rules. |
| **📁 customDNList...** | Custom Configuration | Timestamped custom DNS list, containing applied DNS resolutions and blocks. Key for troubleshooting network-based threats or false positives in custom setups. |
| **📁 customSettings** | Custom Configuration | Custom settings snapshot (instance 2), exporting user or policy-defined configurations like exclusions or scan parameters. Compare across instances to detect changes. |
| **📁 customSettingsCA...** | Custom Configuration | Detailed custom settings log with hashes, showing effective vs. intended configs. Vital for auditing policy application in enterprise environments. |
| **📁 customSupportedURIs** | Custom Configuration | Custom supported URIs list (instance 4), tracking allowed or monitored web resources. Helps investigate web protection bypasses or custom allowlists. |
| **📁 customSupportedURIs...** | Custom Configuration | Timestamped custom URI support data, including resolution logs. Useful for network protection troubleshooting, e.g., blocked legitimate sites. |
| **📁 customSupportedURIs...** | Custom Configuration | Additional custom URI mappings, focusing on historical supports. Cross-reference with network logs for evasion attempts. |
| **📁 DpRegistry.txt** | Registry and Configuration | Registry dump for Data Protection (DP) components in Defender, covering encryption and secure storage keys. Critical for issues with quarantined file handling or secure data features. |
| **📁 DpSR.txt** | Registry and Configuration | Data Protection Secure Remote (SR) registry export, detailing remote access policies for protected data. Aids in cloud-integrated protection diagnostics. |
| **📁 DeviceControlInfo.txt** | System and Component Status | Information on device control policies (e.g., USB restrictions), including enabled rules and enforcement logs. Essential for endpoint DLP or peripheral threat investigations. |
| **📁 FileVersions.txt** | System and Component Status | List of file versions for Defender binaries and dependencies (e.g., .exe, .dll). Use to verify update integrity and version mismatches causing errors. |
| **📁 FileVersions.txt Mitiga** | System and Component Status | Mitigated file versions log, flagging vulnerable or patched files. Helps prioritize vulnerability assessments in Defender scans. |
| **📁 FlTMgrInfo.txt** | System and Component Status | Filter Manager (FltMgr) information, logging file system mini-filter drivers like WdFilter.sys. Key for real-time protection troubleshooting, e.g., filter load failures. |
| **📁 FltUtilJournalInfo.txt** | System and Component Status | Filter Utility journal for file system operations, detailing journaling events filtered by Defender. Useful for deep-dive into I/O monitoring and performance impacts. |
| **📁 IEFT.txt** | Registry and Configuration | Internet Explorer Feature Table (IEFT) dump, covering legacy browser security settings integrated with Defender. Relevant for older web threat detections. |
| **📁 IEO.txt** | Registry and Configuration | Internet Explorer Options export, including zone settings and security levels. Helps correlate browser-based threats with Defender's web protection. |
| **📁 MpCmdRun.log** | Command and Tracing Files | Primary log of MpCmdRun.exe executions, capturing commands, outputs, and errors (e.g., scans, updates). Core for reproducing diagnostic collection steps. |
| **📁 MpCmdRunLocalService.log** | Command and Tracing Files | MpCmdRun logs under LocalService context, focusing on service-level operations like background scans. Isolate service-specific failures. |
| **📁 MpCmdRunNetworkService.log** | Command and Tracing Files | NetworkService-context MpCmdRun logs, detailing network-dependent tasks (e.g., signature downloads). Crucial for connectivity issues. |
| **📁 MpCmdRunNetworkService.log.bak** | Command and Tracing Files | Backup of NetworkService MpCmdRun log, preserving prior session data for comparison. Use for historical analysis. |
| **📁 MpCmdRunSystemTemp.log** | Command and Tracing Files | System temporary context MpCmdRun logs, tracking temp file handling during scans. Helps debug temp-related errors or cleanups. |
| **📁 MpCmdRunSystemTemp.log.bak** | Command and Tracing Files | Backup of SystemTemp MpCmdRun log, for rollback analysis of temp operations. |
| **📁 MPDetection.log** | Detection and Threat History | Timestamped detection log, listing threats with paths, hashes (SHA1/MD5), timestamps, and actions (e.g., quarantine). Primary for threat forensics. |
| **📁 MPDeviceControl...** | Detection and Threat History | Device control detection events, logging blocked/allowed devices (e.g., USB). Ties into DLP policy enforcement reviews. |
| **📁 MPOperationalEvents.txt** | Event and Operational Logs | Export of Operational channel events from Windows Defender Event Log, including scan starts/completions, detections, and errors (e.g., Event ID 1000-1024). Mirrors Event Viewer for comprehensive timelines. |
| **📁 MPOperationalEvents.txt.bak** | Event and Operational Logs | Backup of operational events, preserving pre-collection state for delta analysis. |
| **📁 MPRegistry.txt** | Registry and Configuration | Full Defender registry export (e.g., `HKLM\SOFTWARE\Microsoft\Windows Defender`), showing settings, exclusions, and policies. Essential for config mismatch diagnostics. |
| **📁 MPSCAN.log** | Event and Operational Logs | Timestamped scan log, detailing full/quick/custom scan progress, files checked, and results. Use to verify scan efficacy and coverage. |
| **📁 MPSigUpdate.log** | Update and Signature Files | Signature update log, tracking download attempts, versions, and failures from Microsoft Update. Critical for outdated definitions issues. |
| **📁 MPStateInfo.txt** | System and Component Status | Current Defender state snapshot (e.g., enabled features, service health). Quick health check for onboarding or runtime problems. |
| **📁 MPLog.log** | Event and Operational Logs | Verbose MP (Malware Protection) operational log, with timestamps, file paths, hashes, scan results, and telemetry (e.g., cloud queries). Core artifact for behavioral and real-time events. |
| **📁 MPLog.log** | Event and Operational Logs | Additional verbose MP log instance, focusing on prior session details. Compare with current for trend analysis. |
| **📁 MPSupportEffectiveConfig.json** | Registry and Configuration | JSON export of effective support configurations, merging GPO/MDM/local settings. Parse for policy conflicts. |
| **📁 MPSupportProtectionSettings.ecc...** | Registry and Configuration | Protection settings dump with hash, detailing real-time/behavioral toggles. Useful for feature enablement verification. |
| **📁 NetworkProtectionSettings** | Network Protection | Base network protection settings file, listing mode (block/audit), scopes, and indicators. Foundation for web threat troubleshooting. |
| **📁 NetworkProtectionSettings** | Network Protection | Instance 5 of network settings, capturing runtime applications. Track changes over collections. |
| **📁 NetworkProtectionSettings.....** | Network Protection | Timestamped network settings, including proxy integrations. Key for false positive blocks. |
| **📁 NetworkProtectionSettings..ecc...** | Network Protection | Versioned network protection config, with ECC (error-correcting code?) details. Aids in advanced network filtering reviews. |
| **📁 NetworkProtectionState.txt** | Network Protection | Current state of network protection (e.g., active blocks, connections). Real-time status for incident response. |
| **📁 PrinterInfo.txt** | System and Component Status | Printer configuration and security info, relevant if print spooler threats are suspected. Logs potential peripheral vectors. |
| **📁 SecurityHealthApp.txt** | System and Component Status | Health report from Security Health App (e.g., Windows Security), summarizing Defender status and recommendations. Quick overview for compliance. |
| **📁 SecurityHealthRegistry.txt** | Registry and Configuration | Registry keys for security health monitoring, tracking app integrations. Useful for third-party AV conflicts. |
| **📁 SenseIRTraceLogger...** | Command and Tracing Files | Sense (Defender sensor) IR (Incident Response) trace log, detailing endpoint sensor data uploads to cloud. For EDR telemetry analysis. |
| **📁 SenseIRTraceLogger...** | Command and Tracing Files | Additional Sense IR trace, focusing on behavioral signals. Parse for advanced persistent threat indicators. |
| **📁 SetupAct.log** | System and Component Status | Setup activation log from Windows setup, capturing Defender installation events. Diagnose onboarding failures. |
| **📁 Setuperr.log** | System and Component Status | Setup error log, listing failures during Defender or Windows updates. Correlate with update issues. |
| **📁 SHff...** | System and Component Status | Shim (compatibility layer) hash log, tracking file shims for legacy app compatibility with Defender scans. For version-specific bugs. |
| **📁 SHff...** | System and Component Status | Additional shim hash data, aiding in compatibility troubleshooting. |
| **📁 SinkholeCache** | Network Protection | Cache of sinkholed (blocked) domains/IPs by Defender's network protection. Review for evasion attempts or misconfigs. |
| **📁 SinkholeCache....** | Network Protection | Timestamped sinkhole cache, listing resolved bad domains. Forensic gold for phishing/pharming investigations. |
| **📁 SnapshotInfo.txt...** | System and Component Status | System snapshot info with hash, capturing state at collection time (e.g., processes, modules). Baseline for anomaly detection. |
| **📁 supportedConnections** | Network Protection | List of supported network connections, including protocols and ports monitored by Defender. Config validation tool. |
| **📁 supportedConnections** | Network Protection | Instance 6 of connection supports, with runtime data. Track dynamic changes. |
| **📁 supportedConnections....** | Network Protection | Timestamped supported connections log. Useful for bandwidth or proxy issues. |
| **📁 supportedConnections....** | Network Protection | Additional connection mapping, focusing on historical supports. |
| **📁 supportedURIs** | Custom Configuration | Base list of supported URIs for web/cloud integrations. Foundation for URI-based protections. |
| **📁 supportedURIs** | Custom Configuration | Instance 7 of URI supports, capturing policy-applied lists. Compare for drifts. |
| **📁 System.evt** | Event and Operational Logs | Legacy system event log (.evt format), including Defender-related system events pre-Win10. For historical analysis on upgraded systems. |
| **📁 SystemInfo.txt** | System and Component Status | General system info dump (OS version, hardware, Defender build). Essential onboarding and compatibility check. |
| **📁 TaskSchedulerInfoInternal.log** | System and Component Status | Internal Task Scheduler log for Defender tasks (e.g., scheduled scans). Diagnose missed scans or task failures. |
| **📁 TaskSchedulerInfoWindows.xml** | System and Component Status | XML export of Windows Task Scheduler defs for Defender (e.g., MpCmdRun tasks). Parse for misconfigurations. |
| **📁 topTraffic** | Network Protection | Top network traffic summary, ranking connections by volume. Identify anomalous traffic blocked by Defender. |
| **📁 topTraffic** | Network Protection | Instance 8 of top traffic, with metrics. Trend analysis for performance impacts. |
| **📁 topTraffic.** | Network Protection | Timestamped top traffic log (638041746094982), detailing high-volume endpoints. Forensic for data exfil attempts. |
| **📁 topTraffic.** | Network Protection | Duplicate/timestamped variant of top traffic, for multi-session captures. |
| **📁 UICache** | System and Component Status | User Interface cache for Defender apps (e.g., Windows Security), storing UI state and preferences. Minor, but useful for UI glitch troubleshooting. |
| **📁 UICache.log** | System and Component Status | Log of UI cache operations, tracking refreshes and errors. |
| **📁 WamStateCache** | System and Component Status | Windows Audio Manager (Wam) state cache, potentially tied to audio file scans or mitigations. Niche for multimedia threats. |
| **📁 WdAtpInfo.txt** | System and Component Status | Windows Defender Advanced Threat Protection (ATP, now EDR) info, including sensor status and onboarding details. Core for MDE connectivity issues. |
| **📁 WfpState.xml** | Network Protection | Windows Filtering Platform (WFP) state XML, exporting firewall and filter rules applied by Defender. Deep network stack diagnostics. |
| **📁 WindowsProxy.txt** | Network Protection | Proxy configuration dump for Windows/Defender traffic, including PAC files and settings. Troubleshoot update or cloud submission failures. |
| **📁 WSCInfo.txt** | System and Component Status | Windows Security Center (WSC) info, detailing AV registration and health signals. Verify Defender's AV role and alerts. |
| **📁 WSCRegistry.txt** | Registry and Configuration | WSC registry export, covering security provider registrations. For integration with other security tools. |
| **📁 diag.xml** | Diagnostic and Misc | General diagnostic XML report, summarizing collection metadata and errors. Overview file for CAB integrity. |
| **📁 diagwn.xml** | Diagnostic and Misc | Windows-specific diagnostic XML, focusing on network and Defender diagnostics. Complements network logs. |
| **📁 FlTMgrSoft.txt Mitiga** | System and Component Status | Mitigated Filter Manager software list, flagging risky filters. Enhances vulnerability scans. |
| **📁 MicrosoftWindowsSecurityMitiga...** | Registry and Configuration | Partial registry dump for Microsoft Security Mitigation (Mitiga), covering exploit guards. For ASR rule troubleshooting. |
| **📁 MitigationPolicies...** | Registry and Configuration | Timestamped mitigation policies log, detailing applied protections (e.g., CFG, DEP). Key for exploit prevention reviews. |
| **📁 MPWppCoreTracing...** | Command and Tracing Files | Windows Software Trace Preprocessor (WPP) core tracing log (binary/text mix), for low-level Defender engine traces. Advanced debugging for crashes. |
| **📁 MPWppTracing...** | Command and Tracing Files | Additional WPP tracing instance, capturing performance and error traces. Requires tools like TraceFmt for full decode. |
| **📁 rt.log** | Event and Operational Logs | Real-time (RT) protection log, logging on-access scans and blocks. High-volume; grep for threats. |
| **📁 setuact.log** | System and Component Status | Setup activity log variant, focusing on activation events. Similar to SetupAct but more granular. |
| **📁 setuper.log** | System and Component Status | Setup error log variant, with extended details. Pair with Setuperr for full picture. |
| **📁 SnapshotInfo.txt** | System and Component Status | Base snapshot info, capturing process/module state. Baseline without hash suffix. |
