### Troubleshooting Device Control Issues


Device Installation Restrictions (DIR): These are Windows policies that control whether certain devices or drivers can be installed on a system. When DIR is enabled, it enforces restrictions such as:

Blocking installation of devices that are not explicitly allowed.
Preventing installation of drivers from untrusted sources.
Applying rules based on device IDs, classes, or setup classes.

Even when using Intune Endpoint Security blade, Device Control policies only apply to removable storage classes (USB drives, WPD devices, CD/DVD, printers).

Devices that do not expose storage volumes IE: “Acme scanners without storage” cannot be controlled by MDE Device Control.

For these devices, you must use Device Installation Restrictions (Intune or GPO) to block or allow based on Hardware IDs or Instance IDs.

Navigate to: Endpoint Security > Device Control > Device Installation Restrictions. 

Add Hardware IDs or Instance IDs from Device Manager or via PowerShell:

```PS
Get-PnpDevice | Select InstanceId
```
Enable layered evaluation in Intune for Allow/Prevent rules to ensure exclusions are honored correctly.
 
You can run the following commands on an affected device to show whether DIR is enabled:

reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceInstall\Restrictions /s

reg query HKLM\SYSTEM\DriverDatabase\Policies\Restrictions /s

What we’ll need going forward in order to investigate device control are the MDE Analyzer logs.

 1) Supply MDEA logs but reproduce the issue during the capture (Obtain the scanner and attempt to use it/plug it in during the capture)

1. Download the Client Analyzer from: https://aka.ms/Betamdeanalyzer
2. Extract it to any folder on your computer.
3. Open an administrator PowerShell (Will not work with PowerShell ISE).
4. Change directories to the same location you extracted the folder contents to.
5. Run .\MDEClientAnalyzer.cmd -c -a -v
6. Run the trace for 3 - 5 minutes (reproduce the problem during this time if one is occurring)
7. Upload the results.zip

 2) Review Advanced Hunting and confirm whether you see Device control blocking this SID or device. Example:

```kql
DeviceEvents
| where ActionType == "DeviceControlBlocked"
| where AdditionalFields contains "USBSTOR"
| project Timestamp, DeviceName, InitiatingProcessAccountName, AdditionalFields
```

<img width="1210" height="1722" alt="image" src="https://github.com/user-attachments/assets/46981af3-bfed-49a2-9246-96a087b26151" />
<img width="1611" height="509" alt="image" src="https://github.com/user-attachments/assets/da0ffb53-e083-4f44-a679-7f095604ad20" />
