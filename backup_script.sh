#!/bin/sh
# keep last 30 backups and sleep for 10 seconds before retrying and try for max 3 attempts
/home/ubuntu/sales/backup.sh -k 30 -d /home/ubuntu/sales/dumps/ -r 3 -s 10 /home/ubuntu/sales/backend/db.sqlite3

