### Troubleshooting Device Control Issues

Device Installation Restrictions (DIR): These are Windows policies that control whether certain devices or drivers can be installed on a system. When DIR is enabled, it enforces restrictions such as:

1. Blocking installation of devices that are not explicitly allowed.    
2. Preventing installation of drivers from untrusted sources.    
3. Applying rules based on device IDs, classes, or setup classes.    

Even when using Intune Endpoint Security blade, Device Control policies only apply to removable storage classes (USB drives, WPD devices, CD/DVD, printers). Device control requires MDAV platform version 4.18.2103.3 or later (ideally the latest). Check the version with Get-MpComputerStatus in PowerShell. An MDE Plan 1 or Plan 2 license is required (included in Microsoft 365 E3/E5); verify via Intune compliance reporting.

### Devices that do not expose storage volumes IE: “Acme scanners without storage” cannot be controlled by MDE Device Control.
Navigate to: Endpoint Security > Attack Surface Reduction > Device Contrtol. 

### Add Hardware IDs or Instance IDs from Device Manager or via PowerShell:

```PS
Get-PnpDevice | Select InstanceId
```
### Configure rule evaluation in Intune (via included/excluded groups) to ensure allow/deny rules and exclusions are honored correctly 
You can run the following commands on an affected device to show whether DIR is enabled:
```PS
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceInstall\Restrictions /s
reg query HKLM\SYSTEM\DriverDatabase\Policies\Restrictions /s
```
### Getting Removal Device Information
The "DescriptorIdList" property specifies the attributes used to identify a USB removable storage device. Start by retrieving the "DeviceInstancePath" from Windows Device Manager: connect the device to a test machine, open Device Manager, expand Disk Drives, and find the device. Then, under the Details tab, select the Device instance path property.
<img width="1373" height="1110" alt="image" src="https://github.com/user-attachments/assets/83de9b1c-dfa5-4f54-b852-11bbc4654338" />

Copy this value as it will be used to derive the BusId, DeviceId, and the SerialNumberId attribute values. This is value from the device manager:
SCSI\DISK&VEN_SEAGATE&PROD_EXPANSION\8&2E0884B1&2&000000
<img width="1909" height="173" alt="image" src="https://github.com/user-attachments/assets/c01a8cd6-3761-4aa2-bcd5-4a1e14d95acc" />
Extract the BusId, DeviceId, and the SerialnumberId from this value:
```
PrimaryId - RemovableMediaDevices
InstancePathId - SCSI\DISK&VEN_SEAGATE&PROD_EXPANSION\8&2E0884B1&2&*
DeviceId - DISK&VEN_SEAGATE&PROD_EXPANSION
HardwareId - 
FriendlyNameId - 
BusId - SCSI
SerialNumberId - 8&2E0884B1&2
VID_PID -
```

### PrimaryId can be one of four values. This chart breaks down the differernce. 
| **PrimaryId**           | **Definition**                                                                                   | **Examples**                                      | **Intune/MDE Usage Notes**                                                                 |
|--------------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------|-------------------------------------------------------------------------------------------|
| `RemovableMediaDevices` | Removable storage media such as portable drives and flash storage.                             | USB flash drives, external HDDs, SD cards        | Used to apply allow/deny policies for removable storage. Combine with BusId/DeviceId for granular control. |
| `CdRomDevices`          | Optical drives that read/write CD/DVD media.                                                   | Internal/external CD/DVD drives                  | Controls access to CD/DVD drives. Can block read/write or execution from optical media.   |
| `WpdDevices`            | Windows Portable Devices that use WPD protocol for media and storage.                          | Smartphones, tablets, cameras                    | Restrict data transfer from portable devices. Often used to prevent data exfiltration.    |
| `PrinterDevices`        | Printers connected locally to the system, typically via USB or other direct interfaces.        | USB printers, locally attached printers          | Apply policies to block non-corporate printers or enforce corporate printer usage only.

### The HardwareId, FriendlyNameId, and VID_PID can be extracted from the device manager.
| **Device Manager Field** | **Device Control Attribute** | **Notes**                                                                 |
|---------------------------|-----------------------------|---------------------------------------------------------------------------|
| Hardware Ids             | HardwareId                 | Found under **Device Properties → Details → Property: Hardware Ids**.    |
| Friendly name            | FriendlyNameId             | Found under **Device Properties → Details → Property: Friendly Name**.   |
| Parent                   | VID_PID                    | Extract **VID_xxxx&PID_yyyy** from the **Parent** property in Device Manager. |
<img width="765" height="379" alt="image" src="https://github.com/user-attachments/assets/0a369ff8-7e4a-4445-9138-d319bc864d92" />
<img width="770" height="215" alt="image" src="https://github.com/user-attachments/assets/32075a08-d0f7-45c0-bc53-c6a11533a581" />
<img width="779" height="212" alt="image" src="https://github.com/user-attachments/assets/9dabebee-1a38-4fec-9043-e4eb92d6dd9b" />

The VID_PID extracted here would be "USB\VID_0BC2&PID_231A\MSFT30NA8R4YBW"

### Now that we have all possible values extracted, you can choose which of these you want to use as a matching identifier for the device. Remove trailing 0s for SerialNumberId because it changes when the device is unplugged/replugged.

| **Attribute**        | **Value**                                                                                   |
|-----------------------|-------------------------------------------------------------------------------------------|
| **PrimaryId**        | RemovableMediaDevices                                                                     |
| **InstancePathId**   | SCSI\DISK&VEN_SEAGATE&PROD_EXPANSION\8&2E0884B1&2&*                                       |
| **DeviceId**         | DISK&VEN_SEAGATE&PROD_EXPANSION                                                           |
| **HardwareId**       | SCSI\DiskSeagate_Expansion______0707                                                      |
| **FriendlyNameId**   | Seagate Expansion SCSI Disk Device                                                        |
| **BusId**            | SCSI                                                                                       |
| **SerialNumberId**   | 8&2E0884B1&2                                                                               |
| **VID_PID**          | VID_0BC2&PID_231A                                                                         |

### These represent all the identifiers you can use to match devices in your Device Control policy.

One important note: The final numeric segment in InstancePathId often corresponds to the USB port, which may change on reconnect—use a wildcard (*) to handle this.
```
Intune InstancePathId - SCSI\DISK&VEN_SEAGATE&PROD_EXPANSION\8&2E0884B1&2&*
```

### To investigate device control issue, you need the MDE Analyzer logs. reproduce the issue during the capture (Obtain the scanner and attempt to use it/plug it in during the capture).

1. Download the Client Analyzer from: https://aka.ms/Betamdeanalyzer.
2. Extract it to any folder on your computer.
3. Open an administrator PowerShell (Will not work with PowerShell ISE).           
4. Change directories to the same location you extracted the folder contents to.            
5. Run .\MDEClientAnalyzer.cmd -c -a -v        
6. Run the trace for 3 - 5 minutes (reproduce the problem during this time if one is occurring).              
7. Download/Upload the results.zip to support.          
8. Review AH and confirm whether you see Device control blocking the SID or device. Example:
```kql
DeviceEvents
| where ActionType == "DeviceControlBlocked"
| where AdditionalFields contains "USBSTOR"
| project Timestamp, DeviceName, InitiatingProcessAccountName, AdditionalFields
```
