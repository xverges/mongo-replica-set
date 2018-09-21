#!/usr/bin/env bash


read_replica() {
    vagrant ssh $1 -- "cd /vagrant/scripts && source guest-env.sh && ./update-replica.py $1"
}

if [ $# -ne 1 ]; then
    me=`basename "$0"`
    echo "Usage: ${me} server_name"
    echo "   server_name: first|second"

else
    read_replica $1
fi

