#!/usr/bin/env python3
import os
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    # Update system
    run_cmd("sudo yum update -y")

    # Install dependencies
    run_cmd("sudo yum install -y gcc glibc glibc-common wget unzip httpd php gd gd-devel perl postfix")

    # Create Nagios user and group
    run_cmd("sudo useradd nagios")
    run_cmd("sudo groupadd nagcmd")
    run_cmd("sudo usermod -a -G nagcmd nagios")
    run_cmd("sudo usermod -a -G nagcmd apache")

    # Download Nagios Core
    run_cmd("wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.6.tar.gz -O /tmp/nagios.tar.gz")
    run_cmd("cd /tmp && tar zxvf nagios.tar.gz")

    # Compile and install
    run_cmd("cd /tmp/nagios-4.4.6 && ./configure --with-command-group=nagcmd")
    run_cmd("cd /tmp/nagios-4.4.6 && make all && sudo make install && sudo make install-init && sudo make install-config && sudo make install-commandmode")

    # Start httpd
    run_cmd("sudo systemctl enable httpd && sudo systemctl start httpd")

    print("✅ Nagios installation completed!")

if __name__ == "__main__":
    main()

