#!/usr/bin/env bash

reset_server () {
    vagrant ssh $1 -- "docker-compose -f /vagrant/docker/docker-compose.${1}.yml kill"
    vagrant ssh $1 -- "sudo rm -rf /home/vagrant/mongo-data"
    vagrant up --provision $1
    python ./scripts/setup-roles.py $1
}

if [ $# -ne 1 ]; then
    me=`basename "$0"`
    echo "Usage: ${me} <first|second|all>"
else
    if [ $1 = "all" ]; then
        reset_server first
        reset_server second
    else
        reset_server $1
    fi
fi
