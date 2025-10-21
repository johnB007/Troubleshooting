## MDAV Security Intelligence and Product Updates
Update your antivirus protection, even if Microsoft Defender Antivirus is running in passive mode. You can find the lates engine, platform, and signature date in Security intelligence updates for Microsoft Defender Antivirus and other Microsoft anti-malware.

<img width="2184" height="957" alt="image" src="https://github.com/user-attachments/assets/6e115b2f-05cd-46a3-9c0f-e150b98656d9" />


## Security intelligence updates

Microsoft Defender Antivirus uses cloud-delivered protection, also known as Microsoft Advanced Protection Service, or MAPS. Defender Antivirus periodically downloads dynamic security intelligence updates. These updates don't replace regular security intelligence updates. Engine updates are included with security intelligence updates and are released monthly.

<img width="2834" height="1346" alt="image" src="https://github.com/user-attachments/assets/31c85b30-25c1-4083-a3dd-eab2bfcb7972" />


Cloud-delivered protection is always on and requires an active connection to the internet to function. Security intelligence updates occur on a scheduled cadence which you can configure using a policy.

## Product updates or Plafrom Updates

Microsoft Defender Antivirus requires monthly updates (KB4052623) known as platform updates.

You can manage the distribution of updates using one of the following methods:

Windows Server Update Service (WSUS), Microsoft Configuration Manager, The usual methods you use to deploy Microsoft and Windows updates to endpoints in your network, or a UNC Share.

## Platform and engine releases

Updates contain:

Performance improvements, Serviceability improvements, and Integration improvements (Cloud, Microsoft Defender XDR).

## KQL for Endpoint Report

This query will identify the Microsoft Defender Antivirus Engine version and Microsoft Defender Antivirus Security Intelligence version (and timestamp), Product update version (aka Platform Update version) as well as the Microsoft Defender Antivirus Mode on the endpoint (Active, Passive, or EDR BLock ).

## KQL


```kusto
let avmodetable = DeviceTvmSecureConfigurationAssessment
| where ConfigurationId == "scid-2010" and isnotnull(Context)
| extend avdata=parsejson(Context)
| extend AVMode = iif(tostring(avdata[0][0]) == '0', 'Active' , iif(tostring(avdata[0][0]) == '1', 'Passive' ,iif(tostring(avdata[0][0]) == '4', 'EDR Blocked' ,'Unknown')))
| project DeviceId, AVMode;
DeviceTvmSecureConfigurationAssessment
| where ConfigurationId == "scid-2011" and isnotnull(Context)
| extend avdata=parsejson(Context)
| extend AVSigVersion = tostring(avdata[0][0])
| extend AVEngineVersion = tostring(avdata[0][1])
| extend AVSigLastUpdateTime = tostring(avdata[0][2])
| extend AVProductVersion = tostring(avdata[0][3]) 
| project DeviceId, DeviceName, OSPlatform, AVSigVersion, AVEngineVersion, AVSigLastUpdateTime, AVProductVersion, IsCompliant, IsApplicable
| join avmodetable on DeviceId
| project-away DeviceId1
```
<img width="2998" height="1324" alt="image" src="https://github.com/user-attachments/assets/6c8554ba-8eaa-4ebc-b845-0171e3b29e9b" />
