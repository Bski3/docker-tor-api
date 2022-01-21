#!/bin/bash

cat /var/lib/tor/hidden_service/hostname 
cat authorized_clients/torkey.auth_private && rm authorized_clients/torkey.auth_private
systemctl restart tor && service tor restart
python3 main.py