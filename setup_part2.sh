#!/bin/bash

# Proceed with NordVPN login using the provided token
echo "Logging into NordVPN with the provided token..."
nordvpn login --token e9f2ab8e143bea0ccd41f0cc2bad62339438490d3aa9c2d9faccf7370548a4c6

# Enable NordVPN's Meshnet
echo "Enabling NordVPN Meshnet..."
nordvpn set meshnet on