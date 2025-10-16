## When a File is Executed or Downloaded and Disapears, Where is the Info?

Look in (ActionType contains "SmartScreen" or ActionType contains "NetworkProtection" or ActionType contains "ControlledFolderAccess" or ActionType contains "Antivirus" or ActionType contains "Ioav" or ActionType contains "AppControl" or ActionType contains "AppLocker" or ActionType == "AntivirusDetection")

## KQL 

## TOP Machines With a List Query to Review Audits or Blocks

## KQL
```Kusto
DeviceEvents
//| where Timestamp > ago(7d) // Adjust time range as needed
| where ActionType contains "Asr" or ActionType contains "SmartScreen" or ActionType contains "NetworkProtection" or ActionType contains "ControlledFolderAccess" or ActionType contains "Antivirus" or ActionType contains "Ioav" or ActionType contains "AppControl" or ActionType contains "AppLocker" or ActionType == "AntivirusDetection"
| summarize 
    LastEDRSignalTime = max(Timestamp),
    ASR_Blocked = countif(ActionType contains "Asr" and ActionType contains "Block"),
    ASR_Audited = countif(ActionType contains "Asr" and ActionType contains "Audit"),
    SmartScreen_Blocks = countif(ActionType contains "SmartScreen" and ActionType contains "Block"),
    SmartScreen_Warns = countif(ActionType contains "SmartScreen" and ActionType has_any ("Warn", "Warning")),
    SmartScreen_Overrides = countif(ActionType contains "SmartScreen" and ActionType contains "UserOverride"),
    NetworkProtection_Blocked = countif(ActionType contains "NetworkProtection" and ActionType contains "Block"),
    NetworkProtection_Audited = countif(ActionType contains "NetworkProtection" and ActionType contains "Audit"),
    CFA_Blocked = countif(ActionType contains "ControlledFolderAccess" and ActionType contains "Block"),
    CFA_Audited = countif(ActionType contains "ControlledFolderAccess" and ActionType contains "Audit"),
    AV_Detections = countif(ActionType contains "Antivirus" or ActionType == "AntivirusDetection" or ActionType contains "Ioav"),
    WDAC_Blocked = countif(ActionType has_any (dynamic(["AppControl", "AppLocker"])))
    by DeviceName, DeviceId
| extend TotalBlocksOrAudits = ASR_Blocked + ASR_Audited + SmartScreen_Blocks + SmartScreen_Warns + SmartScreen_Overrides + NetworkProtection_Blocked + NetworkProtection_Audited + CFA_Blocked + CFA_Audited + AV_Detections + WDAC_Blocked
| where TotalBlocksOrAudits > 0
| project DeviceName, DeviceId, LastEDRSignalTime, ASR_Blocked, ASR_Audited, SmartScreen_Blocks, SmartScreen_Warns, SmartScreen_Overrides, NetworkProtection_Blocked, NetworkProtection_Audited, CFA_Blocked, CFA_Audited, AV_Detections, WDAC_Blocked, TotalBlocksOrAudits
| order by LastEDRSignalTime desc
```
<img width="2965" height="1553" alt="image" src="https://github.com/user-attachments/assets/7f9ae004-43e5-4b3c-8e05-16c7482eee69" />

## Machine with list of all blocks and audits

## KQL

```Kusto
DeviceEvents
//| where Timestamp > ago(7d) // Adjust time range as needed
| where DeviceId == "xxxxxxx" // Replace with your specific DeviceId
| where ActionType contains "Asr" or ActionType contains "SmartScreen" or ActionType contains "NetworkProtection" or ActionType contains "ControlledFolderAccess" or ActionType contains "Antivirus" or ActionType contains "Ioav" or ActionType contains "AppControl" or ActionType contains "AppLocker" or ActionType == "AntivirusDetection"
| project Timestamp, DeviceName, DeviceId, ActionType, FileName, InitiatingProcessFileName, InitiatingProcessCommandLine, AdditionalFields, 
    IsASRBlocked = iff(ActionType contains "Asr" and ActionType contains "Block", 1, 0),
    IsASRAudited = iff(ActionType contains "Asr" and ActionType contains "Audit", 1, 0),
    IsSmartScreenBlocked = iff(ActionType contains "SmartScreen" and ActionType contains "Block", 1, 0),
    IsSmartScreenWarned = iff(ActionType contains "SmartScreen" and ActionType has_any ("Warn", "Warning"), 1, 0),
    IsSmartScreenOverridden = iff(ActionType contains "SmartScreen" and ActionType contains "UserOverride", 1, 0),
    IsNetworkProtectionBlocked = iff(ActionType contains "NetworkProtection" and ActionType contains "Block", 1, 0),
    IsNetworkProtectionAudited = iff(ActionType contains "NetworkProtection" and ActionType contains "Audit", 1, 0),
    IsCFABlocked = iff(ActionType contains "ControlledFolderAccess" and ActionType contains "Block", 1, 0),
    IsCFAAudited = iff(ActionType contains "ControlledFolderAccess" and ActionType contains "Audit", 1, 0),
    IsAVDetection = iff(ActionType contains "Antivirus" or ActionType == "AntivirusDetection" or ActionType contains "Ioav", 1, 0),
    IsWDACBlocked = iff(ActionType has_any (dynamic(["AppControl", "AppLocker"])), 1, 0)
| summarize 
    LastEDRSignalTime = max(Timestamp),
    ASR_Blocked = sum(IsASRBlocked),
    ASR_Audited = sum(IsASRAudited),
    SmartScreen_Blocks = sum(IsSmartScreenBlocked),
    SmartScreen_Warns = sum(IsSmartScreenWarned),
    SmartScreen_Overrides = sum(IsSmartScreenOverridden),
    NetworkProtection_Blocked = sum(IsNetworkProtectionBlocked),
    NetworkProtection_Audited = sum(IsNetworkProtectionAudited),
    CFA_Blocked = sum(IsCFABlocked),
    CFA_Audited = sum(IsCFAAudited),
    AV_Detections = sum(IsAVDetection),
    WDAC_Blocked = sum(IsWDACBlocked),
    Events = make_list(pack("Timestamp", Timestamp, "ActionType", ActionType, "FileName", FileName, "InitiatingProcessFileName", InitiatingProcessFileName, "InitiatingProcessCommandLine", InitiatingProcessCommandLine, "AdditionalFields", AdditionalFields))
    by DeviceName, DeviceId
| extend TotalBlocksOrAudits = ASR_Blocked + ASR_Audited + SmartScreen_Blocks + SmartScreen_Warns + SmartScreen_Overrides + NetworkProtection_Blocked + NetworkProtection_Audited + CFA_Blocked + CFA_Audited + AV_Detections + WDAC_Blocked
| where TotalBlocksOrAudits > 0
| project DeviceName, DeviceId, LastEDRSignalTime, ASR_Blocked, ASR_Audited, SmartScreen_Blocks, SmartScreen_Warns, SmartScreen_Overrides, NetworkProtection_Blocked, NetworkProtection_Audited, CFA_Blocked, CFA_Audited, AV_Detections, WDAC_Blocked, TotalBlocksOrAudits, Events
| order by LastEDRSignalTime desc
```

<img width="2982" height="1680" alt="image" src="https://github.com/user-attachments/assets/3965b7a0-bba4-4e05-a037-82cbe048a36c" />
