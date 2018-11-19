#!/usr/bin/env bash


for server in first second; do
    cmd="docker-compose -f /vagrant/docker/docker-compose.${server}-repl.yml up -d && cat /vagrant/docker/docker-compose.${server}-repl.yml"
    echo $cmd
    vagrant ssh ${server} -- $cmd 
done