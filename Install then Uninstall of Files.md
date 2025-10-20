## CX Wanted a way to determine when a specifc user installed and then unistalled a file by the exact time.

## KQL 


```KQL
DeviceProcessEvents
| where Timestamp > ago(180d)
| where DeviceName == "xxxxxx"//Replace with DeviceName
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
    // ✅ FIXED: User vs System detection (SIMPLE VERSION)
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
| project 
    LatestTimestamp, 
    DeviceName = "camslaptop007",
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

<img width="2968" height="1682" alt="image" src="https://github.com/user-attachments/assets/8fd9bb12-2681-49c9-a82b-b9bf82ac6946" />

## Device Inventory Only Shows Active Installed Software and not "Point in Time or Install/Uninstalled"

<img width="3164" height="1548" alt="image" src="https://github.com/user-attachments/assets/a0e6ac88-2856-4b1d-9ece-8a89a730f26c" />



