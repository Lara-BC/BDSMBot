#!/bin/bash
python bot.py
while [ $? -eq 11 ]; do
    echo "Server requested restart.  Respawning.." >&2
    git pull
    sleep 1
    python bot.py
done
