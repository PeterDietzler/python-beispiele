[Unit]
Description=smartmeter
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u smart.py
WorkingDirectory=/home/pi/smartmeter
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target