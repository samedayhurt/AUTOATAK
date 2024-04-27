import os

# ASCII art 
print("""
        ___ __      ___        
 /\ /  \ | /  \   /\ |  /\ |_/ 
/--\\__/ | \__/  /--\| /--\| \ 

""")

# Setup Dependencies
print("Setting up dependencies...")
os.system("sudo mkdir -p /etc/apt/keyrings")
os.system("sudo curl https://www.postgresql.org/media/keys/ACCC4CF8.asc --output /etc/apt/keyrings/postgresql.asc")
os.system("sudo sh -c 'echo \"deb [signed-by=/etc/apt/keyrings/postgresql.asc] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/postgresql.list'")
os.system("sudo apt update")

# Ask for TAK Server Debian package location
deb_location = input("What is the location of the TAK Server Debian package? ")
os.system("sudo apt install " + deb_location)

# Restart TAK Server
os.system("sudo systemctl daemon-reload")
os.system("sudo systemctl start takserver")

# Configure Metadata
print("Configuring metadata...")
os.chdir("/opt/tak/certs")
os.system("sudo su tak")
os.system("/opt/tak/certs/cert-metadata.sh")

# Create Certificates
print("Creating certificates...")
os.system("./makeRootCa.sh")
os.system("./makeCert.sh server takserver")
os.system("./makeCert.sh client admin")

# Ask if client certificates are needed
create_client_certs = input("Would you like to create client certificates? (yes/no) ")
if create_client_certs.lower() == "yes":
    client_name = input("Enter client name: ")
    os.system(f"./makeCert.sh client \"{client_name}\"")

# Restart TAK Server
os.system("sudo systemctl restart takserver")

# Set permissions
print("Setting permissions...")
os.system("sudo chmod 777 /opt/tak/certs/files/admin.pem")
os.system("sudo chmod 777 /opt/tak/certs/files/admin.p12")
os.system("sudo chmod 777 /opt/tak/certs/files/takserver.jks")
os.system("sudo apt update")

# Final instructions
print("Take the truststore-root.p12 and user.p12 files and copy them to your Android device. In ATAK, open Settings->General Settings->Network Settings")
print("In order to access the webui, You must import the admin certificate into FireFox. Go to Settings -> Security -> Certificates -> Import. It is located in /opt/tak/certs/files.")
print("When complete, TAKServer is accessible via Firefox at: https://localhost:8089")
