#!/bin/bash

# Update and install necessary packages
echo "Updating system and installing necessary packages for NordVPN..."
sudo apt-get update && sudo apt-get install -y curl iptables apt-transport-https

# Download and run the NordVPN install script
echo "Running NordVPN installation script..."
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

# Add current user to the nordvpn group
USERNAME=$(whoami)
sudo usermod -aG nordvpn $USERNAME

# Reboot to apply changes
echo "NordVPN has been installed. Rebooting to take effect."
sudo reboot