#!/bin/bash

echo "test"
echo $1
DOW=$(date +'%A')

echo $DOW
DOWNLOAD=$DOW-minecraft-.tar.gz
echo $DOWNLOAD

scp -i ~/minecraft-key-pair.pem -o "StrictHostKeyChecking no"  ubuntu@$1:/opt/temp/backup/$DOWNLOAD ../mc_backup/.
