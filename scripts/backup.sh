#!/usr/bin/env bash

backup_server () {

for database in db_1 db_2; do
    echo Backing up ${database} in $1
    vagrant ssh $1 -- "/usr/bin/docker exec docker_mongo_1 \
        /usr/bin/mongodump \
        --host 0.0.0.0 --db ${database} \
        --username ${ROOT_USER} --password ${ROOT_PASSWORD} --authenticationDatabase admin \
        --gzip --archive=/mongo-backup/backup_${database}"
done
}

backup_server first
backup_server second
