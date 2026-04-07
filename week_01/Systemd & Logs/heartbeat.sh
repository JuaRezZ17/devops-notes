#!/bin/bash
while true
do
  echo "Heartbeat - $(date): RAM en uso: $(free -m | awk '/Mem:/ { print $3 }') MB"
  sleep 60
done