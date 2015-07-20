#!/bin/bash

cat << EOF
upstream varnish {
EOF

for host in $(serf members | awk '{ print $2 }' | cut -d: -f1 | sort); do
        echo "  server ${host}:6081;"
done

cat << EOF
  hash $uri consistent;
}
EOF
