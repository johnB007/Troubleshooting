## This is for creating a DCR for Ingestion Spike to Drop Certain Logs
These were created for certain 3rd Party vendors that caused a spike in Sentinel but can be used for any DCR.

## KQL

```Kusto
DeviceEvents
| where InitiatingProcessFolderPath !contains "Tanium"
| where InitiatingProcessFolderPath !contains "Trellix"
| where InitiatingProcessFolderPath !contains "McAfee" 
| where InitiatingProcessVersionInfoCompanyName !contains "Tanium"
| where InitiatingProcessVersionInfoCompanyName !contains "Trellix"
| where InitiatingProcessVersionInfoProductName !contains "Tanium"
| where InitiatingProcessVersionInfoProductName !contains "Trellix"
| where ProcessCommandLine !contains "Tanium"
| where FileName !contains "Tanium"  
| where ProcessCommandLine !contains "trellix"   
| where FileName !contains "trellix"  
| where InitiatingProcessCommandLine !contains "Tanium"
| where InitiatingProcessCommandLine !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Tanium"
```

```Kusto
DeviceProcessEvents
| where InitiatingProcessFolderPath !contains "Tanium"
| where InitiatingProcessFolderPath !contains "Trellix"
| where InitiatingProcessFolderPath !contains "McAfee" 
| where InitiatingProcessVersionInfoCompanyName !contains "Tanium"
| where InitiatingProcessVersionInfoCompanyName !contains "Trellix"
| where InitiatingProcessVersionInfoProductName !contains "Tanium"
| where InitiatingProcessVersionInfoProductName !contains "Trellix"
| where ProcessCommandLine !contains "Tanium"
| where FileName !contains "Tanium"  
| where ProcessCommandLine !contains "trellix"   
| where FileName !contains "trellix"  
| where InitiatingProcessCommandLine !contains "Tanium"
| where InitiatingProcessCommandLine !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Tanium"
```

```Kusto
DeviceRegistryEvents
| where InitiatingProcessFolderPath !contains "Tanium"
| where InitiatingProcessFolderPath !contains "Trellix"
| where InitiatingProcessFolderPath !contains "McAfee" 
| where InitiatingProcessVersionInfoCompanyName !contains "Tanium"
| where InitiatingProcessVersionInfoCompanyName !contains "Trellix"
| where InitiatingProcessVersionInfoProductName !contains "Tanium"
| where InitiatingProcessVersionInfoProductName !contains "Trellix"
| where ProcessCommandLine !contains "Tanium"
| where FileName !contains "Tanium"  
| where ProcessCommandLine !contains "trellix"   
| where FileName !contains "trellix"  
| where InitiatingProcessCommandLine !contains "Tanium"
| where InitiatingProcessCommandLine !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Tanium"
 ```

```Kusto
DeviceNetworkEvents
| where InitiatingProcessFolderPath !contains "Tanium"
| where InitiatingProcessFolderPath !contains "Trellix"
| where InitiatingProcessFolderPath !contains "McAfee" 
| where InitiatingProcessVersionInfoCompanyName !contains "Tanium"
| where InitiatingProcessVersionInfoCompanyName !contains "Trellix"
| where InitiatingProcessVersionInfoProductName !contains "Tanium"
| where InitiatingProcessVersionInfoProductName !contains "Trellix"
| where ProcessCommandLine !contains "Tanium"
| where FileName !contains "Tanium"  
| where ProcessCommandLine !contains "trellix"   
| where FileName !contains "trellix"  
| where InitiatingProcessCommandLine !contains "Tanium"
| where InitiatingProcessCommandLine !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Tanium"
```

```Kusto
DeviceFileEvents
| where InitiatingProcessFolderPath !contains "Tanium"
| where InitiatingProcessFolderPath !contains "Trellix"
| where InitiatingProcessFolderPath !contains "McAfee" 
| where InitiatingProcessVersionInfoCompanyName !contains "Tanium"
| where InitiatingProcessVersionInfoCompanyName !contains "Trellix"
| where InitiatingProcessVersionInfoProductName !contains "Tanium"
| where InitiatingProcessVersionInfoProductName !contains "Trellix"
| where ProcessCommandLine !contains "Tanium"
| where FileName !contains "Tanium"  
| where ProcessCommandLine !contains "trellix"   
| where FileName !contains "trellix"  
| where InitiatingProcessCommandLine !contains "Tanium"
| where InitiatingProcessCommandLine !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Trellix"
| where InitiatingProcessVersionInfoFileDescription !contains "Tanium"
```

## Pictures in Sentinel

<img width="3229" height="1882" alt="image" src="https://github.com/user-attachments/assets/722805de-4c7d-4c15-af23-d4cfcdd57070" />



