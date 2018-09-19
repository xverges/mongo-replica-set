#!/usr/bin/env bash


for server in first second; do
    vagrant ssh ${server} -- "docker-compose -f /vagrant/docker/docker-compose.${server}-repl.yml up -d"
done