#!/bin/bash



cp /home/kolibri/.kolibri/db.sqlite3 .

python export_users.py

sudo rm db.*
