#!/bin/bash

# Proceed with NordVPN login using the provided token
echo "Logging into NordVPN with the provided token..."
nordvpn login --token e9f2ab533d0b7413e9fb8dbe9493419ac7993bc6e7d737c4ea447a47d7ea68e9

# Enable NordVPN's Meshnet
echo "Enabling NordVPN Meshnet..."
nordvpn set meshnet on

# --- mavp2p Setup ---

# Variables for mavp2p setup
RELEASE_URL="https://github.com/bluenviron/mavp2p/releases/download/v1.2.0/mavp2p_v1.2.0_linux_arm64v8.tar.gz"
RELEASE_TAR="mavp2p.tar.gz"
EXTRACTED_BIN="mavp2p"
INSTALL_DIR="/usr/local/bin"
FC_USB="/dev/ttyACM0"

# Download the specified release of mavp2p for arm64v8
echo "Downloading mavp2p from GitHub..."
curl -L $RELEASE_URL -o $RELEASE_TAR

# Extract the binary from the tarball
echo "Extracting mavp2p..."
tar -xzf $RELEASE_TAR

# Make mavp2p executable
chmod +x $EXTRACTED_BIN

# Move mavp2p to a global location
sudo mv $EXTRACTED_BIN $INSTALL_DIR/

# Check if the flight controller device exists
if [ ! -e $FC_USB ]; then
    echo "No flight controller detected at $FC_USB. Please make sure it is connected."
    exit 1
else
    echo "Flight controller detected at $FC_USB"
fi

# Prompt for IP address and port
read -p "Please enter the IP address to broadcast to (e.g., 100.86.68.139): " IP_ADDRESS
read -p "Please enter the port to broadcast to (e.g., 14550): " PORT

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/mavp2p.service"
echo "Creating systemd service at $SERVICE_FILE"

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=MAVLink Proxy
After=network.target

[Service]
ExecStart=$INSTALL_DIR/mavp2p serial:$FC_USB:57600 udpc:$IP_ADDRESS:$PORT
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable mavp2p.service
sudo systemctl start mavp2p.service

echo "mavp2p and NordVPN setup complete."