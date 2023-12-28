import os
import shutil
import zipfile
import boto3
from botocore.exceptions import NoCredentialsError

def backup_and_upload_to_s3(local_directory, s3_bucket_name):
    try:
        # Create a temporary directory for the backup
        backup_directory = "appdata_backup_temp"
        os.makedirs(backup_directory)

        # Copy the /home/ec2-user/appdata directory to the temporary backup directory
        appdata_backup_path = os.path.join(backup_directory, "appdata_backup")
        shutil.copytree(local_directory, appdata_backup_path)

        # Create a ZIP file of the backup
        zip_filename = "appdata_backup.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(appdata_backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, arcname=os.path.relpath(file_path, appdata_backup_path))

        # Upload the ZIP file to S3
        s3 = boto3.client('s3')
        s3.upload_file(zip_filename, s3_bucket_name, zip_filename)

        print("Backup and upload to S3 completed successfully!")

    except NoCredentialsError:
        print("Credentials not available or invalid. Please configure AWS credentials.")

    except Exception as e:
        print(f"Backup and upload to S3 failed: {e}")

    finally:
        # Clean up temporary files
        if os.path.exists(backup_directory):
            shutil.rmtree(backup_directory)
        if os.path.exists(zip_filename):
            os.remove(zip_filename)

# Replace 'your-s3-bucket-name' with your actual S3 bucket name
backup_and_upload_to_s3(local_directory='/home/ec2-user/appdata', s3_bucket_name='ec2backupproject')
