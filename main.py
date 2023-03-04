
import os
import time
import subprocess
from datetime import date
from netmiko import ConnectHandler



username="Enter Username"
password="Enter Password"

print("Please Wait a Moment ...")

today = date.today()
backup_dir = f'\\\\192.168.1.1\BackupDataStore/Cisco_Backup/{today.year}/{today.month:02d}/{today.day:02d}'

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def offline_device(ip_address):
    proc = subprocess.Popen(["ping", "-n", "2", "-4", ip_address], stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode()
    if "TTL" in output:
        return False
    else:
        return True

def do_something():
    time.sleep(1)

def do_another_something():
    time.sleep(1)

with open('\\\\192.168.1.1\BackupDataStore/Cisco_Troubled_Devices.txt', 'w') as f:
    f.truncate(0)

with open('devices.txt') as f:
    total_devices = sum([len(line.strip().split(':')[0].split(',')) for line in f])
    f.seek(0)
    current_device = 0

    for line in f:
        devices, port = line.strip().split(':')
        offline_devices = []
        current_device += 1

        for ip_address in devices.split(','): 
            if offline_device(ip_address):
                offline_devices.append(ip_address)
                ofline = (ip_address)

        if len(offline_devices) > 0:
            with open(f"\\\\192.168.1.1\BackupDataStore/Cisco_Troubled_Devices.txt", 'a') as f: 
                f.write(f"\nOffline_Devices {ofline}")
        else:


            for ip_address in devices.split(','): 
                
                try:
                    
                    print(f"Trying to Backup the Device : {ip_address} ({current_device}/{total_devices})")


                    device_connection = ConnectHandler(
                    device_type="cisco_ios",
                    ip=ip_address,
                    username=username,
                    password=password,
                    secret='Enter Secret Password',
                    )

                    device_connection.enable()

                    hostname = device_connection.send_command("show run | i hostname").split()[-1]

                    config_output = device_connection.send_command("show running-config")

                    with open(f"{backup_dir}/{hostname}.txt", "w") as f:
                        f.write(config_output)
                        print(f"Configuration saved for {hostname} ({ip_address})")
        
                    
                    device_connection.disconnect()
                    

                except Exception as e:
                    with open(f"\\\\192.168.1.1\BackupDataStore/Cisco_Troubled_Devices.txt", 'a') as d: 
                        d.write(f"\n{str(e)} {ip_address}")
                    continue

    with open(f"\\\\192.168.1.1\BackupDataStore/Cisco_Troubled_Devices.txt", 'a') as d: 
        d.write(f"\n\n\n         --- Powerd by @Mr_AhadiFar ---")

    print("Backups Completed Successfully.")

    print(f"""

    --- Powerd by @Mr_AhadiFar ---
    """)

        


#   --- Powerd by @Mr_AhadiFar ---   #