#!/usr/bin/env python3

#collect_metrics_agentless.py
#Agentless EC2 monitoring tool (Windows):
#- SSH into multiple EC2 hosts using key-based authentication
#- Collect: hostname, uptime, CPU load, disk usage, memory, failed logins, network errors
#- Generate JSON and CSV reports
#

import paramiko
import json
import pandas as pd
import traceback
from datetime import datetime
import os
import traceback
from datetime import datetime

# =======================
# Configuration
# =======================
HOSTS = [
    "3.148.186.129",
    "3.145.103.142"
]

user = "ec2-user"
key_path = r"C:\Desktop\.ssh\newkey.pem"
timeout = 20  # seconds

# Commands to run on remote host
COMMANDS = {
    "uptime": "uptime -p",
    "cpu": "top -bn1 | grep 'Cpu(s)' || mpstat 1 1 | tail -1",
    "disk": "df -h / | grep -E '^/dev/' | head -1",
    "failed_logins": "sudo bash -c 'grep \"Invalid user\" /var/log/secure | awk \"{for(i=1;i<=NF;i++) if (\\$i==\\\"from\\\") print \\$(i+1)}\" | sort | uniq -c | awk \"{print \\\"Failed logins from IP: \\\"\\$2\\\", count: \\\"\\$1}\"'"

,
    "network": "ping -c 4 8.8.8.8 | tail -1",
}



# =======================
# Collect metrics from one host
# =======================
def collect_metrics_one(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    result = {}
    result["host"] = host
    result["user"] = user
    result["collected_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        ssh.connect(hostname=host, username=user, key_filename=key_path, timeout=timeout)

        # Get hostname first
        stdin, stdout, stderr = ssh.exec_command("hostname")
        hostname_output = stdout.read().decode().strip()
        print(f"DEBUG: Hostname output from {host} = '{hostname_output}'")
        result["hostname"] = hostname_output if hostname_output else "Unknown"

        # Collect other metrics
        for label, cmd in COMMANDS.items():
            try:
                stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True, timeout=timeout)
                output = stdout.read().decode().strip()
                err = stderr.read().decode().strip()
                result[label] = output if output else (err if err else "")
            except Exception as cmd_e:
                result[label] = f"command error: {str(cmd_e)}"

    except Exception as e:
        print(f"    ! Error: {e}")
        traceback.print_exc()
        result["error"] = str(e)

    finally:
        try:
            ssh.close()
        except Exception:
            pass
    return result  # ← make sure this has exactly 4 spaces before it


# =======================
# Main function
# =======================
def main():
    print("=== Starting EC2 Monitoring ===\n")
    all_results = []

    for h in HOSTS:
        print(f"[+] Collecting from {h} (user={user})...")
        r = collect_metrics_one(h)
        if "error" in r:
            print(f"    ! Error: {r['error']}")
        all_results.append(r)

    # Save JSON
    json_filename = "global_status_report.json"
    with open(json_filename, "w") as f:
        json.dump(all_results, f, indent=4)
    print(f"\nJSON report saved as {json_filename}")

    # Save CSV
    df = pd.DataFrame(all_results)
    csv_filename = "global_status_report.csv"
    df.to_csv(csv_filename, index=False)
    print(f"CSV report saved as {csv_filename}\n")

    # Print JSON to console
    print("=== Global Status Report (JSON) ===")
    print(json.dumps(all_results, indent=4))


if __name__ == "__main__":
    main()
