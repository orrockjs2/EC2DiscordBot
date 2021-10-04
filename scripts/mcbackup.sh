###########################################################
#
# Backup minecraft world to Scotty's Desktop
#
###########################################################

backup_files="minecraft"

dest="/C:/Users/SSH_USER/Documents/MC_backup"

temp_dest="/opt/temp/backup/"

day=$(date +%A)

archive_file="$day-$backup_files-.tar.gz"

cd /opt && tar -zcvf $temp_dest$archive_file $backup_files

echo "created tar in: $temp_dest$archive_file"
echo "running: sshpass -p '3p!cCr1nge' scp -P 6690 $temp_dest$archive_file SSH_USER@138.88.142.55:$dest"

sshpass -p '3p!cCr1nge' scp -P 6690 $temp_dest$archive_file SSH_USER@138.88.142.55:$dest

rm $temp_dest$archive_file
