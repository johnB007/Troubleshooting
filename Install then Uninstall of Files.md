### CX Wanted a way to determine when a specifc user installed and then unistalled a file by the exact time. A detection from Wave Browser was seen in the telemetry, but could not be found in MDVM.

### Device Inventory Only Shows Active Installed Software and not "Point in Time or Install/Uninstalled" w/ Timestamp - The Problem Statement

<img width="2908" height="1777" alt="image" src="https://github.com/user-attachments/assets/e093a599-f614-44a8-9144-68a98ecd2391" />

### This query can also be useful for:  

Auditing software changes on a device.  
Identifying unauthorized or automated installations (e.g., SYSTEM installs with silent flags).  
Tracking whether software is still installed or has been removed.  
Investigating the context of installations (e.g., command-line arguments, initiating account).   

## KQL 
Must place DeviceNmae in | where DeviceName == "" and at the bottom of | project DeviceName = "",
```KQL

DeviceProcessEvents
| where Timestamp > ago(180d)
| where DeviceName == "xxxx" // Replace with DeviceName
| where 
    // Direct installer files (.exe, .msi, etc.)
    FileName matches regex @"\.(exe|msi|msp|msu|appx|appxbundle|msix|msixbundle)$"
    or 
    // MSI via msiexec.exe
    (FileName == "msiexec.exe" and ProcessCommandLine matches regex @"\.msi")
    or 
    // MSU via wusa.exe
    (FileName == "wusa.exe" and ProcessCommandLine matches regex @"\.msu")
| where ProcessCommandLine has_any("/S", "/silent", "/quiet", "/passive", "install", "setup", "/i", "uninst", "uninstall", "/x", "remove")
| extend 
    // Installer file extraction
    InstallerFile = case(
        FileName matches regex @"\.(exe|msi|msp|msu|appx|appxbundle|msix|msixbundle)$", FileName,
        FileName == "msiexec.exe", extract(@"""([^""]+\.msi)""", 1, ProcessCommandLine),
        FileName == "wusa.exe", extract(@"""([^""]+\.msu)""", 1, ProcessCommandLine),
        FileName
    ),
    // Event type
    EventType = case(
        ProcessCommandLine has_any("uninst", "uninstall", "/uninstall", "/x", "remove"), "UNINSTALL",
        "INSTALL"
    ),
    InstalledBy = case(
        AccountName in~ ("SYSTEM", "NT AUTHORITY\\SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE"), "SYSTEM",
        ProcessCommandLine has_any("/qn", "/quiet", "/passive"), "SYSTEM",
        InitiatingProcessFileName in~ ("svchost.exe", "services.exe", "winlogon.exe"), "SYSTEM",
        "USER"
    )
| where isnotempty(InstallerFile)
| summarize 
    LatestTimestamp = max(Timestamp),
    LatestEventType = arg_max(Timestamp, EventType),
    LatestInstalledBy = arg_max(Timestamp, InstalledBy),
    LatestCommandLine = arg_max(Timestamp, ProcessCommandLine),
    LatestAccountName = arg_max(Timestamp, AccountName),
    InstallCount = countif(EventType == "INSTALL"),
    UninstallCount = countif(EventType == "UNINSTALL"),
    SystemInstalls = countif(EventType == "INSTALL" and InstalledBy == "SYSTEM"),
    UserInstalls = countif(EventType == "INSTALL" and InstalledBy == "USER")
    by InstallerFile
| extend 
    CurrentStatus = case(
        UninstallCount > 0, "UNINSTALLED",
        InstallCount > 0, "INSTALLED",
        "UNKNOWN"
    ),
    PrimaryInstaller = case(
        SystemInstalls > UserInstalls, "SYSTEM",
        UserInstalls > 0, "USER",
        "UNKNOWN"
    )
// >>> Only show entries where PrimaryInstaller == "USER"
| where PrimaryInstaller == "USER"
| project 
    LatestTimestamp, 
    DeviceName = "xxxxx", // Replace with DeviceName
    InstallerFile, 
    CurrentStatus,
    PrimaryInstaller,
    LatestInstalledBy,
    LatestEventType,
    SystemInstalls,
    UserInstalls,
    InstallCount,
    UninstallCount,
    LatestCommandLine, 
    LatestAccountName
| order by LatestTimestamp desc
```

## Screenshots of Device

<img width="2943" height="999" alt="image" src="https://github.com/user-attachments/assets/a0994524-54df-4e39-8e65-f9184e8bbe7a" />

### If no installation is returned in the results, you might have to run a seperate kql for when the .exe was created or seen on the device. Place the folders in the kql. You can find this information on the vendors webpage or by installing the actual software.

```
let device = "xxxxx";//Put device name here
let lookback = 365d;
DeviceFileEvents
| where Timestamp > ago(lookback)
| where DeviceName =~ device
| where FileName =~ "wavebrowser.exe"
   or FolderPath has @"\WaveBrowser\"
   or FolderPath has @"\Wave Browser\"
| summarize arg_min(Timestamp, *)  // earliest row (proxy for install time)
| project
    InstallEvidenceTime = Timestamp,
    DeviceName,
    ActionType,
    FileName,
    FolderPath,
    InitiatingProcessFileName,
    InitiatingProcessCommandLine,
    InitiatingProcessAccountName,
    InitiatingProcessParentFileName

```
<img width="2906" height="805" alt="image" src="https://github.com/user-attachments/assets/e78868c1-cdbf-443e-aad2-665317c092c2" />

### This is a commbined kql that targets wave browser install and uninstall. You might have to run all queries until you find exaclty what you need and then fine tune as needed. 

```

let device = "xxxx";//Replave with device name
let lookback = 365d;

DeviceProcessEvents
| where Timestamp > ago(lookback)
| where DeviceName =~ device
| where ProcessCommandLine has_any ("wavebrowser", "WaveBrowser", "Wave Browser")
   or FileName has_any ("wavebrowser", "SWUpdater", "setup", "installer", "uninstall")
| extend EventType = case(
    ProcessCommandLine has_any ("uninstall","/uninstall"," uninst","/x","remove"), "UNINSTALL",
    ProcessCommandLine has_any ("install","/i","/qn","/quiet","/passive","setup"), "INSTALL",
    "UNKNOWN"
)
| where EventType != "UNKNOWN"
| summarize arg_min(Timestamp, *) by EventType
| project
    EventType,
    EventTime = Timestamp,
    DeviceName,
    FileName,
    ProcessCommandLine,
    AccountName,
    InitiatingProcessFileName,
    InitiatingProcessCommandLine,
    InitiatingProcessAccountName
| order by EventTime asc
```

<img width="2920" height="1025" alt="image" src="https://github.com/user-attachments/assets/bcd1b4d4-5e6a-468a-b2ca-4d56876e3fcd" />

### This kql is very noisy, but can be modified for only user installs/uninstalls and specific file names. 

```
let device = "defcon30";
let lookback = 365d;
DeviceProcessEvents
| where Timestamp > ago(lookback)
| where DeviceName =~ device
| where AccountName != "system"
| where AccountName != ""
// Focus on common installers/package managers + uninstallers
| where FileName in~ (
    "msiexec.exe", "setup.exe", "update.exe", "installer.exe",
    "winget.exe", "choco.exe", "chocolatey.exe",
    "dism.exe", "wusa.exe", "appinstaller.exe", "powershell.exe", "cmd.exe"
)
or ProcessCommandLine has_any (
    "msiexec", "winget install", "winget uninstall",
    "choco install", "choco uninstall",
    "setup.exe", "installer", "uninstall", "/uninstall", " uninst",
    "/i", " /x", "/qn", "/quiet", "/passive", "remove"
)
// Classify event type more precisely (MSI / Winget / Choco / Generic)
| extend EventType = case(
    // MSI uninstall patterns
    FileName =~ "msiexec.exe" and ProcessCommandLine has_any ("/x", " /x ", "uninstall"), "UNINSTALL",
    // MSI install patterns
    FileName =~ "msiexec.exe" and ProcessCommandLine has_any ("/i", " /i ", ".msi"), "INSTALL",
    // Winget
    FileName =~ "winget.exe" and ProcessCommandLine has " uninstall", "UNINSTALL",
    FileName =~ "winget.exe" and ProcessCommandLine has " install", "INSTALL",
    // Chocolatey
    FileName in~ ("choco.exe","chocolatey.exe") and ProcessCommandLine has " uninstall", "UNINSTALL",
    FileName in~ ("choco.exe","chocolatey.exe") and ProcessCommandLine has " install", "INSTALL",
    // Generic keywords
    ProcessCommandLine has_any ("uninstall","/uninstall"," uninst","/x","remove"), "UNINSTALL",
    ProcessCommandLine has_any ("install","/i","/qn","/quiet","/passive","setup"), "INSTALL",
    "UNKNOWN"
)
| where EventType != "UNKNOWN"
| project
    Timestamp,
    EventType,
    DeviceName,
    FileName,
    ProcessCommandLine,
    AccountName,
    InitiatingProcessFileName,
    InitiatingProcessCommandLine,
    InitiatingProcessAccountName
| order by Timestamp asc
```

<img width="2808" height="940" alt="image" src="https://github.com/user-attachments/assets/cfc29d61-e46a-428d-8831-63ce03fa1de4" />








