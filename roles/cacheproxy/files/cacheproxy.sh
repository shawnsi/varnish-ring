#!/bin/bash

BACKENDS=""

for host in $(serf members | awk '{ print $2 }' | cut -d: -f1 | sort); do
        BACKENDS="$BACKENDS ${host}:6081"
done

/tmp/bin/cacheproxy -p 80 $BACKENDS
