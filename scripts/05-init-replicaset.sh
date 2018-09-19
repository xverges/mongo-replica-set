#!/usr/bin/env bash

scriptdir=`dirname "$BASH_SOURCE"`
template1=${scriptdir}/../docker/mongo-scripts/replicaset-init.template.js
target1=${scriptdir}/../docker/mongo-scripts/replicaset-init.js
template2=${scriptdir}/../docker/mongo-scripts/replicaset-add-additional.template.js
target2=${scriptdir}/../docker/mongo-scripts/replicaset-add-additional.js

/usr/local/opt/gettext/bin/envsubst < $template1 > $target1
/usr/local/opt/gettext/bin/envsubst < $template2 > $target2


mongodb_command() {
    echo Running "$2" on "$1"
    OUTPUT=$(vagrant ssh $1 -- "/usr/bin/docker exec docker_mongo_1 \
        /usr/bin/mongo \
        --username ${ROOT_USER} --password ${ROOT_PASSWORD} --authenticationDatabase admin $2 ")
    echo "$OUTPUT"
}

mongodb_command first "--eval='rs.status()'"
mongodb_command first '/mongo-scripts/replicaset-init.js'
while [[ $OUTPUT != *PRIMARY* ]]; do
    sleep 1
    mongodb_command first "--eval='rs.status()'"
done
mongodb_command first '/mongo-scripts/replicaset-add-additional.js'
mongodb_command second "--eval='rs.status()'"
