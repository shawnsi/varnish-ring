#!/bin/bash

echo
echo "New event: ${SERF_EVENT}. Data follows..."

while read line; do
  host=$(echo $line | awk '{ print $2 }')

  case $SERF_EVENT in
    member-join)
      echo curl -X PUT http://localhost:9190/members/${host}:6081
      ;;
    member-leave)
      echo curl -X DELETE http://localhost:9190/members/${host}:6081
      ;;
  esac
done
