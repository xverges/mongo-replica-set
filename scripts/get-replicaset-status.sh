#!/usr/bin/env bash

mongodb_command() {
    vagrant ssh $1 -- "/usr/bin/docker exec docker_mongo_1 \
        /usr/bin/mongo --eval='$2' \
        --username ${ROOT_USER} --password ${ROOT_PASSWORD} --authenticationDatabase admin"
}

mongodb_command first 'rs.status()'
mongodb_command second 'rs.status()'
