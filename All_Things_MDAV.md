## Microsoft Defender Antivirus Update Components: Security Intelligence, Platform, & Engine

For SOC, DFIR, and threat hunting teams, Microsoft Defender Antivirus (MDAV) is not merely an endpoint control; it is a **primary detection and evidence source** that directly impacts alert fidelity, investigative timelines, and response effectiveness. The reliability of MDAV depends on the currency of its **security intelligence, engine, and platform components**, regardless of whether it is operating in active or passive mode. These components are updated through **security intelligence releases multiple times per day**, **monthly platform updates (KB4052623)**, and **monthly engine updates**, which together ensure timely threat detection, consistent telemetry, and predictable detection behavior across the environment.

MDAV updates determine **what threats can be detected**, **how attacker behavior is interpreted**, and **what telemetry is generated during an incident**. Endpoints running outdated components may appear operational while silently introducing detection gaps, delayed alerts, or incomplete forensic artifacts that complicate root cause analysis and threat reconstruction.

Keeping MDAV fully updated ensures consistent detections, reliable telemetry, and predictable behavior across Defender and XDR workflows, all of which are critical during high tempo incident response.

<img width="2184" height="957" alt="image" src="https://github.com/user-attachments/assets/6e115b2f-05cd-46a3-9c0f-e150b98656d9" />
<img width="1992" height="199" alt="image" src="https://github.com/user-attachments/assets/803b17ab-3f63-42a3-86c0-4fe875df551e" />

## Security Intelligence Updates or SIU

Security Intelligence Updates (SIU) are the primary mechanism by which MDAV adapts to **live threat activity**. SIU combines **cloud delivered protection** via Microsoft Advanced Protection Service (MAPS) with **locally installed intelligence** to provide resilient, layered detection.

Cloud delivered protection enables MDAV to consume real time intelligence from the Microsoft security cloud, allowing new malware, attacker techniques, and behavioral patterns to be identified and mitigated without waiting for traditional signature releases. These signals continuously refine on endpoint detection logic and decision making.

In parallel, endpoints periodically download security intelligence updates containing malware definitions, heuristics, and behavioral detection improvements. This local intelligence ensures endpoints retain protection and detection capability during connectivity loss, restricted network conditions, or incident containment actions.

From a SOC and Threat Hunting perspective, SIU directly impacts **alert quality, detection timeliness, and zero day coverage**. Effective SIU reduces reliance on static signatures, improves behavioral detections, and ensures consistent protection across connected and disconnected environments.

<img width="2834" height="1346" alt="image" src="https://github.com/user-attachments/assets/31c85b30-25c1-4083-a3dd-eab2bfcb7972" />

Cloud delivered protection is always on and requires an active internet connection. Security intelligence updates are applied on a scheduled cadence that can be centrally configured by policy.

## Defender Platform Updates

Microsoft Defender Antivirus relies on **monthly platform updates (KB4052623)** to maintain the underlying antimalware framework. These updates refresh the core Defender components responsible for execution, scanning logic, remediation workflows, and telemetry generation.

From a SOC perspective, platform updates establish the **baseline capability** of Defender. They define how the antivirus stack functions, how events are generated, and how Defender interoperates with downstream security services such as Microsoft Defender XDR. Platform updates introduce foundational improvements that signatures and cloud intelligence cannot compensate for if the platform itself is outdated.

Because platform updates roll out in phases, it is normal for multiple platform versions to exist simultaneously across an environment. SOC and endpoint teams should account for this when evaluating detection consistency or investigating behavioral discrepancies across devices.

Organizations can control platform update deployment using standard enterprise mechanisms, including WSUS, Microsoft Configuration Manager, Windows Update, or controlled file-share distribution in restricted or disconnected environments.

## Engine and Runtime Behavior Updates

Engine updates focus on **runtime behavior and execution quality**. While platform updates establish Defender’s core capabilities, engine updates influence **how consistently and efficiently those capabilities are executed** during real-time operations.

These updates typically deliver:
- **Execution efficiency improvements** that reduce endpoint performance impact while sustaining detection coverage
- **Reliability and resilience fixes** that improve update success, component stability, and recovery behavior
- **Signal quality improvements** that enhance telemetry consistency and investigation fidelity across antivirus, EDR, and XDR workflows

For SOC operations, current engine versions are essential for predictable detections and consistent telemetry. Devices running older engines may remain protected but can exhibit uneven alert behavior or reduced investigative clarity compared to fully current systems.

Maintaining alignment between Defender platform and engine versions ensures endpoints behave consistently and that SOC analysts can rely on the accuracy and completeness of endpoint telemetry during investigations.

## KQL for Endpoint Report

This KQL pulls the latest MDAV signature, engine, product version, and mode (Active/Passive/EDR Blocked) for Windows, macOS, and Linux devices from Secure Configuration Assessment data. It normalizes the fields across platforms, joins Windows signature data with Windows AV mode data, and ensures each device returns only the most recent record. Finally, it unifies all device types into a single table and outputs a clean, sorted list of AV versioning and mode status per device for SOC visibility.

DISA STIG mandates that Microsoft Defender Antivirus virus and spyware definitions must not exceed 7 days, establishing the formal compliance threshold across DoD and federal environments.
Separately, Microsoft enforces a minimum supported AVSignatureDue value of 2 days (effective September 2025) to prevent false outdated signature alerts due to update timing, without altering STIG compliance requirements.

## KQL

```kusto
let win_sig = DeviceTvmSecureConfigurationAssessment
| where ConfigurationId == "scid-2011"
| where isnotnull(Context)
| extend avdata = parsejson(Context)
| extend AVSigVersion = tostring(avdata[0][0]),
        AVEngineVersion = tostring(avdata[0][1]),
        AVSigLastUpdateTime = todatetime(avdata[0][2]),
        AVProductVersion = tostring(avdata[0][3])
| summarize arg_max(Timestamp, *) by DeviceId
| project DeviceId, DeviceName, OSPlatform, AVSigVersion, AVEngineVersion,
          AVSigLastUpdateTime, AVProductVersion, IsCompliant, IsApplicable;

let win_mode = DeviceTvmSecureConfigurationAssessment
| where ConfigurationId == "scid-2010"
| where isnotnull(Context)
| extend avdata = parsejson(Context)
| extend AVMode = case(
    tostring(avdata[0][0]) == '0', 'Active',
    tostring(avdata[0][0]) == '1', 'Passive',
    tostring(avdata[0][0]) == '4', 'EDR Blocked',
    'Unknown')
| summarize arg_max(Timestamp, *) by DeviceId
| project DeviceId, AVMode;

let windows = win_sig
| join kind=leftouter win_mode on DeviceId
| project-away DeviceId1
| extend AVMode = coalesce(AVMode, 'Unknown');

let unix_sig = DeviceTvmSecureConfigurationAssessment
| where ConfigurationId in ("scid-5095", "scid-6095")
| where isnotnull(Context)
| extend avdata_raw = parsejson(Context)
| where array_length(avdata_raw) > 0
| extend avdata = avdata_raw[0] 
| extend AVSigVersion = tostring(avdata[0]),
        AVEngineVersion = tostring(avdata[1]),
        AVSigLastUpdateTime = todatetime(avdata[2]),
        AVProductVersion = tostring(avdata[3])
| extend AVMode = case(
    ConfigurationId == "scid-5095", "Active (macOS)",
    ConfigurationId == "scid-6095", "Active (Linux)",
    'Unknown')
| summarize arg_max(Timestamp, *) by DeviceId
| project DeviceId, DeviceName, OSPlatform, AVSigVersion, AVEngineVersion,
          AVSigLastUpdateTime, AVProductVersion, AVMode,
          IsCompliant, IsApplicable;

windows
| union unix_sig
| extend Priority = iif(isnotempty(AVSigVersion), 1, 0)
| summarize arg_max(Priority, *) by DeviceId
| project-away Priority
| order by DeviceName asc
```
<img width="3094" height="1097" alt="image" src="https://github.com/user-attachments/assets/829310f4-c7b4-47c2-9607-f66a8d937c0b" />

