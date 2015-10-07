#!/bin/bash

for host in $(serf members | awk '{ print $2 }' | cut -d: -f1 | sort); do
    curl -X PUT http://localhost:9190/members/${host}:6081
done
