#!/bin/bash

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

# Infinite loop with a sleep of 20 minutes
while true; do
    sleep 1200  # 1200 seconds = 20 minutes
done