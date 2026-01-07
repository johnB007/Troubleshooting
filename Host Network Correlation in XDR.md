# Host and Network Correlation in XDR

## Purpose

This page provides detailed guidance on correlating host-based activity with network-level and cross-domain signals across Microsoft XDR. It is intended for analyst training, SOC operations, and detection engineering, with an emphasis on practical investigation workflows.

<img width="2908" height="199" alt="image" src="https://github.com/user-attachments/assets/e2b99adc-7060-4917-9db6-55417173df8b" />

---

## Why Host and Network Correlation Matters

Modern attacks span multiple security planes and rarely remain isolated to a single telemetry source. Credential access, malware delivery, lateral movement, persistence, and command-and-control commonly involve a combination of endpoint execution, network communication, identity usage, and cloud application access.

Effective correlation enables analysts to:

- Attribute network activity to a specific process, user, and device
- Determine whether security controls prevented or observed malicious behavior
- Pivot from endpoint activity into identity, email, and cloud telemetry
- Reduce false positives by grounding detections in execution context

<img width="2286" height="366" alt="image" src="https://github.com/user-attachments/assets/6d903a29-4503-4f89-80bc-2ab7e7ddd263" />

---

## Core Telemetry Sources for Correlation

XDR correlation relies on layered telemetry that shares common identifiers such as device IDs, account context, and timestamps.

### Endpoint Host Telemetry

- DeviceProcessEvents  
  Process creation events including command lines and parent-child relationships
  
 <img width="2732" height="269" alt="image" src="https://github.com/user-attachments/assets/a94c63d2-07a1-46e1-b96c-baf39a40952c" />

- DeviceFileEvents  
  File creation, modification, download, and execution activity
  <img width="2790" height="423" alt="image" src="https://github.com/user-attachments/assets/4b1a3491-fa2c-4ed7-b3b8-47f818bd53ce" />

- DeviceEvents  
  Attack Surface Reduction rules, exploit protection, device control, Windows Firewall events, and behavioral detections
  <img width="2984" height="244" alt="image" src="https://github.com/user-attachments/assets/2296a5fd-1eb7-40d2-b827-f8857761b90f" />


----- screenshot needed -----

### Network Telemetry

- DeviceNetworkEvents  
  DNS queries, TCP and UDP connections, remote IPs, ports, and URLs

- Network Protection telemetry  
  Audited or blocked outbound connections based on reputation or indicators

- Windows Firewall telemetry  
  Allowed or blocked inbound and outbound traffic enforced by local firewall policy

<img width="2730" height="287" alt="image" src="https://github.com/user-attachments/assets/ce7b2c17-2fee-45d2-bdfd-e4c80d2da43d" />


### Cross-Domain XDR Telemetry

XDR correlation extends beyond the endpoint into identity, email, and cloud layers.

- Identity telemetry  
  Microsoft Entra ID sign-ins, token usage, risky sign-in events

- Email telemetry  
  Message delivery actions, attachments, URLs, phishing indicators

- Cloud application telemetry  
  API access, session activity, anomalous behavior in sanctioned and unsanctioned apps

- Alert and incident aggregation  
  Unified incidents combining signals from endpoint, identity, email, and cloud data

----- screenshot needed -----

---

## Shared Correlation Fields

| Field | Description |
|------|------------|
| DeviceId | Stable identifier for correlating activity across endpoint and network tables |
| Timestamp | Enables sequencing of execution, connectivity, and enforcement |
| InitiatingProcessFileName | Associates network activity with a specific executable |
| InitiatingProcessCommandLine | Provides execution context and attacker intent |
| InitiatingProcessId | Connects child, sibling, and follow-on activity |
| InitiatingProcessParent | Establishes origin of execution |
| AccountName / AccountUpn | Ties activity to a user or service identity |

----- screenshot needed -----

---

## Correlation via the Device Timeline

The Device Timeline provides a chronological view of execution, network activity, and security controls on a single endpoint.

Analyst focus areas include:

1. Initial process execution  
2. Follow-on DNS queries or outbound connections  
3. Enforcement or audit actions tied to the same process  

This approach reinforces that network activity must always be interpreted in host context.

----- screenshot needed -----

---

## Host and Network Correlation in Advanced Hunting

Advanced Hunting enables repeatable correlation using KQL across endpoint, network, and XDR datasets.

Example process-to-network correlation query:

```kql
DeviceProcessEvents
| where Timestamp > ago(30d)
| join kind=inner (
    DeviceNetworkEvents
) on DeviceId, InitiatingProcessId
| project Timestamp, DeviceName, AccountName,
          FileName, ProcessCommandLine,
          RemoteUrl, RemoteIP, RemotePort
| order by Timestamp desc
```

<img width="2872" height="792" alt="image" src="https://github.com/user-attachments/assets/9c67c743-cd9f-4955-a834-326340f1adb8" />
