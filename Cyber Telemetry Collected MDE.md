## Size of Cyber Telemetry Collected From Devices for MDE

## Question:
How does MDE work in a situation where devices are onboarded but intermittently on and off the internet. Would it still be monitored when it comes back online and catches up from when it was last connected to the internet? What are the limitations we are expecting?

## On the EPP side 
The AV engine continues to function (with the most recent signature it has), with the exception of cloud delivered protection not being available 
(which decreases the engines efficacy quite a bit).
 
## For EDR 
There is an on disk cache and it is 100MB. From the experimentations we did with the XXX, we observed cyber telemetry sent to the cloud service 
from a given machine ranged on average between 10-18MB in a 24 hour window. Some machines will send more cyber telemetry than others depending on how they are being used.
Based on the data collected from the experimentation a device can be offline and hold cyber telemetry (without data loss) for anywhere between 2-5 days 
(again depending on the machine, many variables). The EDR cache is FIFO so once the cache fills, older data is lost. The good news is once the connectivity is restored the
device will continue transmitting cyber telemetry.  The moral of the story is that EDR functions optimally when there is good connectivity
to the cloud service, this is why we have been pushing the department and other customers to next Gen connectivity such as starlink/starshield.

## KQL to Monitor for Cyber Telemetry
```kql
union isfuzzy=true
DeviceEvents,
DeviceProcessEvents,
DeviceNetworkEvents,
DeviceFileEvents,
DeviceRegistryEvents,
DeviceImageLoadEvents,
DeviceLogonEvents
| summarize EventCount = count() by DeviceName, bin(Timestamp, 1d)
| extend EstimatedDataMB = toreal(EventCount) * 1.0 / 1024.0  // Assuming 1 KB per event
| order by Timestamp desc, EstimatedDataMB desc
```

<img width="2351" height="1300" alt="image" src="https://github.com/user-attachments/assets/661beb26-8c24-4fc7-b44a-8d98f7018773" />



