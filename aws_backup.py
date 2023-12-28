# ssh_and_cron_script.py
import paramiko
import os

def ssh_and_schedule_cron(ssh_username, public_ip, private_key_file, cron_job_command):
    """Connects to a remote Linux server via SSH and schedules a cron job."""

    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=public_ip, username=ssh_username, key_filename=private_key_file)

        # Schedule the cron job on the remote VM
        _, stdout, stderr = ssh.exec_command(f"(crontab -l; echo '{cron_job_command}') | crontab -")

        # Display the result of the cron job scheduling
        print(stdout.read().decode())
        print(stderr.read().decode())

        print("Cron job scheduled successfully.")

    except Exception as e:
        print(f"SSH connection or cron job scheduling failed: {e}")

    finally:
        # Close SSH connection
        ssh.close()

if __name__ == "__main__":
    # Get user input for SSH connection parameters
    ssh_username = input("Enter SSH username: ")
    public_ip = input("Enter the remote VM public IP: ")
    private_key_file = input("Enter SSH private key file path: ")

    # Schedule the backup as a cron job (every day at 2:00 AM)
    cron_job_command = "* * * * * python3 /home/ec2-user/script/backupscript.py"

    # SSH into the remote VM and schedule the cron job
    ssh_and_schedule_cron(ssh_username, public_ip, private_key_file, cron_job_command)




