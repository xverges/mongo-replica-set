#!/usr/bin/env bash

vagrant destroy --force first || true
vagrant destroy --force second || true
vagrant up first
vagrant up second
