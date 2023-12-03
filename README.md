# Cloud-Based File Storage

## Overview
This is a full stack file storage web application. It features user authentication and authorization and multiple AWS service integrations. The goal of this project was to design a system to allow users to manage and store files in the cloud.

## Built With
- **Backend:** Python, Flask
- **Frontend:** HTML, Bootstrap
- **Database:** MySQL, AWS RDS
- **Cloud Storage:** AWS S3

## How to Install
1. Clone the repository
```bash
   git clone https://github.com/cullm001/file-storage.git
   cd file-storage
```
2. Install required libraries
```bash
  pip install -r requirements.txt
```
3. Edit the following variables 
- secret_key (flask secret key)
- password (MySQL password)
- rds-endpoint (The endpoint for AWS RDS instance)
- Bucket_Name (Name of AWS S3 bucket)
- individual_limit (Size limit of individual file)
- total_limit (Size limit of total bucket)
4. Install the AWS CLI and enter AWS credentials using
```bash
  aws configure
```
5. Run the application
```bash
  python main.py
```
## How to use
1. Enter your information and click Sign Up
<img width="1437" alt="Screen Shot 2023-12-02 at 3 23 01 PM" src="https://github.com/cullm001/file-storage/assets/102619047/42bb58a7-1c64-4ad6-b75b-40ec826e7be9">
2. If you are a returning user, click Login at the top left and enter your credentials
<img width="1440" alt="Screen Shot 2023-12-02 at 3 24 40 PM" src="https://github.com/cullm001/file-storage/assets/102619047/ca391e15-5806-4ad5-8498-50870f376039">
3. If you want to upload a file, click on the "Choose File for Upload" button and submit a file
<img width="1440" alt="Screen Shot 2023-12-02 at 3 26 43 PM" src="https://github.com/cullm001/file-storage/assets/102619047/d7adb7b5-9062-4e11-adcf-e6c1bfdc8834">
4. Now you can perform actions with the buttons in the respective row as your button
<img width="1439" alt="Screen Shot 2023-12-02 at 3 27 52 PM" src="https://github.com/cullm001/file-storage/assets/102619047/f4723f7f-88ff-4b34-8054-72f904995efa">
5. Use the dropdown button on the top right to reorder your files
<img width="1440" alt="Screen Shot 2023-12-02 at 3 32 03 PM" src="https://github.com/cullm001/file-storage/assets/102619047/03baac70-93ac-42f0-a6b2-855c62f2edba">


