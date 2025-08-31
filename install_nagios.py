import subprocess
import os
import platform

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    # Detect Linux distro
    with open("/etc/os-release") as f:
        os_info = f.read()

    if "Ubuntu" in os_info or "Debian" in os_info:
        print("Detected Ubuntu/Debian. Using apt...")
        run_cmd("sudo apt-get update -y")
        run_cmd("sudo apt-get install -y build-essential apache2 php libapache2-mod-php libgd-dev unzip curl wget tar openssl libssl-dev")

    elif "CentOS" in os_info or "Red Hat" in os_info or "Amazon Linux" in os_info:
        print("Detected RHEL/CentOS. Using yum...")
        run_cmd("sudo yum update -y")
        run_cmd("sudo yum install -y gcc glibc glibc-common wget unzip httpd php gd gd-devel perl postfix")

    else:
        print("Unsupported OS")
        return

    # Create nagios user/group
    run_cmd("sudo useradd nagios -m -s /bin/bash || true")
    run_cmd("sudo groupadd nagcmd || true")
    run_cmd("sudo usermod -a -G nagcmd nagios")
    run_cmd("sudo usermod -a -G nagcmd www-data")

    # Download and extract Nagios
    os.chdir("/tmp")
    run_cmd("wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.14.tar.gz")
    run_cmd("tar zxvf nagios-4.4.14.tar.gz")
    os.chdir("nagios-4.4.14")

    # Compile Nagios
    run_cmd("./configure --with-command-group=nagcmd")
    run_cmd("make all")
    run_cmd("sudo make install")
    run_cmd("sudo make install-init")
    run_cmd("sudo make install-commandmode")
    run_cmd("sudo make install-config")
    run_cmd("sudo make install-webconf")

    # Enable Apache and Nagios
    run_cmd("sudo a2enmod rewrite")
    run_cmd("sudo a2enmod cgi")
    run_cmd("sudo systemctl restart apache2")
    run_cmd("sudo systemctl enable nagios")
    run_cmd("sudo systemctl start nagios")

    print("✅ Nagios installation completed!")

if __name__ == "__main__":
    main()
