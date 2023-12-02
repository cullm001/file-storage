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
- secret_key
- password
- rds-endpoint
- Bucket_Name
- individual_limit
- total_limit
4. Run the application
  ```bash
  python main.py
```

