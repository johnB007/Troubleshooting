Troubleshoot an endpoint using Live Response (LR) in MDE


1.	Run new LR session and connect.

<img width="975" height="222" alt="image" src="https://github.com/user-attachments/assets/84144684-572f-4a70-914d-ac3f4e98f340" />


2.	Upload both the MDEClientAnalyzerPreview.zip and the MDELiveAnalyzer.ps1 (from the .zip/tools folder) using the Upload file to library button.  Upload both separate and make sure you name them with a good description.

<img width="975" height="192" alt="image" src="https://github.com/user-attachments/assets/dc81cded-3c0e-4822-aa41-571dc8385b85" />
<img width="975" height="991" alt="image" src="https://github.com/user-attachments/assets/17f2b8c6-30e3-4971-9222-9f5207106eeb" />

3.	Run the following from the same LR session: Putfile MDEClientAnalyzerPreview.zip

<img width="975" height="238" alt="image" src="https://github.com/user-attachments/assets/b5e9718e-9539-41b3-9e8f-be8f4f54b45b" />

4.	Run the following:  Run MDELiveAnalyzer.ps1 . This will take several minutes, so be patient.

<img width="877" height="480" alt="image" src="https://github.com/user-attachments/assets/30b27a96-a842-431b-b25f-7de7b74d9ae4" />

5.	In the end It will show “succeeded” and then generating the health check..
<img width="975" height="560" alt="image" src="https://github.com/user-attachments/assets/a61d5fec-a542-46ec-8118-15cd4fd1168d" />

6.	Followed by the output path.
<img width="975" height="328" alt="image" src="https://github.com/user-attachments/assets/489b96f9-8d3b-43c8-9529-a28a5079b840" />
7.	Run the following: GetFile "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection\Downloads\MDECA\MDEClientAnalyzerResult.zip"
<img width="975" height="578" alt="image" src="https://github.com/user-attachments/assets/2c20bcf3-2f92-4698-94fc-ca1684da9f02" />
8.	Open the downloads folder to verify all files are present in the .zip. MDEClientAnalyzer.htm is the main file you need to open. Unzip all files into a new folder and view results.
<img width="975" height="301" alt="image" src="https://github.com/user-attachments/assets/5e5b1346-aa9f-4ba3-8022-c666d18610c6" />
9.	Look over the results to verify any issues.
<img width="975" height="593" alt="image" src="https://github.com/user-attachments/assets/5d5cbf7c-406a-4a6d-b0b0-e7a146e43df2" />
<img width="975" height="592" alt="image" src="https://github.com/user-attachments/assets/2ac1c82c-0f2a-4023-be51-8d90b86fa132" />














