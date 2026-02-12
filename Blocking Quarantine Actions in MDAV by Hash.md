##  Question on Exluding "File Quarantine Action" by Hash Only

We are seeing a false positive detection in Microsoft Defender Antivirus for a file that uses a generic name. Microsoft Defender for Endpoint supports creating custom indicators using SHA256 hashes, but Microsoft Defender Antivirus exclusions only allow path, folder, process, or file extension based exclusions, not hash based logic. What options are available for us to use.

## What the answer is

-MDAV exclusions are designed to be performance-efficient, which is why hash lookups (e.g., SHA256) are not available during real-time scans.   

-MDE supports hash-based Indicators of Compromise (IOCs), but these are used strictly for detection logic—not for exclusion or quarantine control.  

-You cannot use a file hash to prevent quarantine in MDAV, as MDAV does not honor hash-based IOCs when making quarantine decisions.    

-However, you can exclude the exact file path or the process that launches the file, and MDAV will skip scanning that file during real-time and scheduled scans.     

-Behavioral detections—such as those triggered by AMSI, heuristics, or script-based analysis—may still result in quarantine, even if the file path is excluded.     

## MDAV Only Supports Path/Process/Extension Exclusions   

The official Configure custom exclusions article lists only file/folder path, process, extension, or process-opened files as supported exclusion types—no mention of hash-based exclusions.

## These are the 4 Exclusion Types with	Description
1. Process:	Disables real-time scanning on files that are opened by specific processes, i.e., specified (source) process is not scanned.    
2. Path:	Excludes entire file paths from real-time/scheduled scans.
3. Extension:	Disables real-time/scheduled/custom scans on certain file extensions.
4. IpAddress:	Disables network packet inspection incoming from a certain IP.

##  Hash-Based Exclusions Are Not Supported by MDAV
No where in MSFT docs has hash based excludions listed.

## MDAV Does Not Use Hash IOCs for Quarantine Decisions

The Exclusions overview page reiterates that “exclusions mask files from protection logic,” but only path-based exclusions are honored. [learn.microsoft.com]
No MSM documentation shows MDAV retrieving or evaluating hashes to decide on quarantine—it skips excluded files entirely by path or process before hashes are evaluated.

## Exceptions and Edge Cases
There are scenarios where the file may still be quarantined:

Scheduled Scans:    

If exclusions are not applied to scheduled scans (depending on policy), the file may be scanned and quarantined.

Behavioral or Heuristic Detection:    

If the file exhibits suspicious behavior (e.g., via AMSI or script execution), MDAV may still quarantine it—even if excluded by path.

Incorrect or Partial Exclusion:   

If the file is moved, renamed, or executed from a different path or process than the one excluded, MDAV will scan it.

Tamper Protection or Policy Override:    

In enterprise environments, exclusions may be overridden by security policies or tamper protection settings.

<img width="1686" height="852" alt="image" src="https://github.com/user-attachments/assets/f07deed4-29a5-4930-b180-2ffa021cc56b" />
<img width="1600" height="207" alt="image" src="https://github.com/user-attachments/assets/7f28cc2e-7708-4e6f-a28e-a18ca1fde0a5" />



