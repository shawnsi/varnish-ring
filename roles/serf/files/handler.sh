#!/bin/bash

echo
echo "New event: ${SERF_EVENT}. Data follows..."

while read line; do
  host=$(echo $line | awk '{ print $2 }')

  case $SERF_EVENT in
    member-join)
      curl -X PUT http://localhost:9190/members/${host}:6081
      ;;
    member-leave)
      curl -X DELETE http://localhost:9190/members/${host}:6081
      ;;
    member-failed)
      curl -X DELETE http://localhost:9190/members/${host}:6081
      ;;
    member-reap)
      curl -X DELETE http://localhost:9190/members/${host}:6081
      ;;
  esac
done
