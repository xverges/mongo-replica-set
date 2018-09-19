#!/usr/bin/env bash



restore_server () {

    for database in db_1 db_2; do
        echo Restoring ${database} in $2 from $1
        vagrant ssh $1 -- "/usr/bin/docker exec docker_mongo_1 \
            /usr/bin/mongorestore \
            --host $2 --db ${database} \
            --username ${ROOT_USER} --password ${ROOT_PASSWORD} --authenticationDatabase admin \
            --gzip --archive=/mongo-backup/backup_${database}"
    done

}

if [ $# -ne 2 ]; then
    me=`basename "$0"`
    echo "Usage: ${me} origin_server_name target_server_ip"
    echo "   origin_server_name: first| second"
    echo "   target_server_ip: 0.0.0.0|192.168.100.10|192.168.100.11"

else
    restore_server $1 $2
fi

