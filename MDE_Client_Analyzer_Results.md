
# MDE Client Analyzer Results.html Explained

**Script Version:** 27Jul2025  
**Script RunTime:** 16/10/2025 9:54:23 AM -04:00
<img width="3124" height="1889" alt="image" src="https://github.com/user-attachments/assets/182e2028-fde4-41fc-ae9a-898ef237eb47" />
<img width="3124" height="1891" alt="image" src="https://github.com/user-attachments/assets/ac3b487b-3871-494f-b2dc-fefa2eea769f" />

---

## Device Information

### General Device Details

| Field | Value | Explanation |
|-------|-------|------------|
| Device Host Name | Cyber-01101010 | The computer's network name. Useful for identifying the device. |
| Device Operating System | Microsoft Windows 11 Enterprise | The OS installed. Ensures compatibility with Defender features. |
| OS build number | Microsoft Windows NT 10.0.26200.0.6899 | Specific OS build. Important for troubleshooting OS-specific issues. |
| OS Edition | Client | Indicates it's a client OS, not server. |
| OS Architecture | 64-bit | Shows if the OS is 32 or 64-bit. Some features require 64-bit. |
| SystemBootTime | 10/16/2025 07:55:15 | Last time the device was booted. Useful for uptime checks. |
| Streamlined Connectivity Readiness (Preview) | READY | Indicates if the device is ready for streamlined Defender connectivity. |
| System-wide WinHTTP proxy | Direct access (no proxy server) | Shows if a proxy is configured. Direct means no proxy is used. |

### Device Configuration Management Details

| Field | Value | Explanation |
|-------|-------|------------|
| Enrollment Status | Device is managed by MDM Agent (3) | Shows if device is managed by Mobile Device Management (MDM). |
| Domain Joined | NO | Not joined to an on-premises Active Directory domain. |
| Azure AD Joined | YES | Joined to Azure Active Directory. Important for cloud management. |
| Workplace Joined | NO | Not joined to a workplace (legacy feature). |
| Azure AD Device ID | xxxxxxxxxxx | Unique identifier for the device in Azure AD. |
| MDM Enrollment state | (blank) | Enrollment state not specified. |

### AV Component Details

| Field | Value | Explanation |
|-------|-------|------------|
| Defender AV Service Status | Running | Antivirus service is running. |
| Windows Security Center Service Status | Running | Security Center service is running. |
| Windows Security Health Service Status | Running | Health monitoring service is running. |
| Defender AV SSLOptions configuration | False | SSL options not configured. |
| Defender AV mode | Active | Antivirus is actively protecting the device. |
| Defender Network Inspection Service | Running | Network threat inspection is active. |
| Defender Network Inspection Driver | Running | Driver for network inspection is loaded. |
| Defender AV Platform Version | 4.18.25090.3009 | Version of the Defender platform. |
| Defender AV Security Intelligence Version | 1.439.218.0 | Version of malware definitions. Outdated versions trigger warnings. |
| Defender AV engine Version | 1.1.25090.3001 | Core engine version. |
| Defender Is Tamper Protected | True | Tamper protection is enabled (prevents unauthorized changes). |
| Defender Tamper Protection Source | Intune | Tamper protection managed via Intune. |
| Defender Is Tamper Protection Exclusions Enabled | False | No exclusions for tamper protection. |
| Defender Network Protection Mode | Block Mode | Network threats are blocked. |
| DisableAntiSpyware | 0 | Anti-spyware is not disabled. |
| SmartLockerMode | 0 | SmartLocker is not enabled. |

### EDR Component Details

| Field | Value | Explanation |
|-------|-------|------------|
| Device ID | xxxxxxxxxxx | Unique device identifier for EDR. |
| Organization Id | xxxxxxxxxxx | Organization's unique ID. |
| Sense version | 10.8804.27858.1000 | Version of the EDR sensor. |
| Sense Configuration version | 10.8805.zv2.1_can.2025.09.30.03 | Configuration version for EDR. |
| DiagTrack (UTC) Service Status | Running | Diagnostic tracking service is running. |
| Microsoft Account Sign-in Assistant Start Type | Manual | Service starts manually. |
| Anti-Spoofing capability deployed | YES | Device supports anti-spoofing. |
| MachineAuth ID | xxxxxxxxxxx | Authentication ID for the device. |
| Anti-Spoofing State GUID | xxxxxxxxxxx | Unique identifier for anti-spoofing state. |
| Sense Service Discovered Proxy | Proxy config: Method=Direct, address= | Shows proxy configuration for EDR. |
| Device Datacenter Location | US | Location of the device's datacenter. |
| Device Onboarded via Streamlined Connectivity | NO | Not onboarded via streamlined connectivity. |
| Sense service Status | Running | EDR service is running. |
| Sense service StartType | Automatic | EDR service starts automatically. |


## Detailed Results

| Category      | Test Name                   | Results                                      | PS Remediation                                                                                     | Log Source                                                                 |
|---------------|-----------------------------|---------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| Configuration | SecurityIntelligenceVersion | Outdated security intelligence version reduces detection capability. | `Update-MpSignature`                                                                                | • Event Viewer → Microsoft → Windows → Windows Defender/Operational<br>• Event IDs: 2000–2006 |
| Configuration | AntiSpoofingStable          | Policy not configured; device falls back to camera/driver capability. | Check policy: `(gp 'HKLM:\SOFTWARE\Policies\Microsoft\Biometrics\FacialFeatures' -Name UseEnhancedAntiSpoofing -EA SilentlyContinue).UseEnhancedAntiSpoofing -eq 1` | • Event Viewer → Microsoft → Windows → DeviceGuard/Operational<br>• Microsoft → Windows → Biometrics/Operational |
| Connectivity  | EDRCloud CnC                | Cannot connect to Command & Control cloud service. | `Test-NetConnection winatp-gw.microsoft.com -Port 443`<br>`netsh winhttp show proxy`               | • System logs |
| Connectivity  | EDRCloud Cyber              | Cyber cloud endpoint unreachable.           | `Test-NetConnection winatp-gw.microsoft.com -Port 443`<br>`Test-NetConnection config.security.microsoft.com -Port 443`<br>`netsh winhttp show proxy` | • Sense logs |
| Connectivity  | EDRCloud AutoIR             | Auto Investigation & Response service unreachable. | `Test-NetConnection winatp-gw.microsoft.com -Port 443`<br>`Test-NetConnection config.security.microsoft.com -Port 443`<br>`netsh winhttp show proxy` | • Sense logs |
| Connectivity  | AVCloud SampleUpload        | Sample upload service blocked.              | `Test-NetConnection wdcp.microsoft.com -Port 443`                                                  | • Event Viewer → Microsoft → Windows → Sense/Operational<br>• Event IDs: 1, 2, 5 |
| Connectivity  | EDRCloud MdeConfigMgr       | Configuration Manager service unreachable.   | `Test-NetConnection config.security.microsoft.com -Port 443`                                       | • Sense logs |
| Connectivity  | AVCloud                     | Defender AV cloud unreachable.              | `Test-NetConnection winatp-gw.microsoft.com -Port 443`                                             | • Windows Defender logs |
| Connectivity  | Current Network Connection  | Network marked as metered or restricted.    | `Get-NetConnectionProfile`                                                                          | • System logs |
| Connectivity  | CertRevocation              | Certificate validation failed.              | `certutil -verifyCTL AuthRoot`<br>`Test-NetConnection winatp-gw.microsoft.com -Port 443 \| Select-Object ComputerName, TcpTestSucceeded` | • Sense logs and Windows Crypto logs |
| Environment   | CheckPPL                    | Protected Process Light (PPL) not enabled or Sense service not running. | `Get-Service Sense`<br>`Get-Process -Name Sense -ErrorAction SilentlyContinue`                     | • Windows Defender Operational logs |


---

# Troubleshooting Each Test Name

If any of these checks return **warnings or errors**, follow the steps below to remediate.

---

## Troubleshooting Guidance

- **Warnings:** These indicate potential misconfigurations or connectivity issues that could reduce protection or impact automated investigation  
- **Errors:** These represent critical failures where MDE cannot operate as intended—such as certificate validation failures, blocked cloud connectivity, or missing core services. Immediate remediation is required to ensure the device is protected and reporting correctly. 
- **Informational:** All connectivity and environment checks passed, indicating healthy Defender and EDR operation.

<img width="1216" height="281" alt="image" src="https://github.com/user-attachments/assets/6e199b95-af39-4b98-8d21-6ee7939a0ba8" />

