#!/bin/bash

echo "Ticket No: $1"

cd /var/lib/pgsql/sriram/

rm -rf temp/$1

mkdir -p temp/$1

echo `ls -l temp | grep $1`

cp -r /home/csadmin/sriram/fortisoar-logs.tar.gz temp/$1/fortisoar-logs.tar.gz

cd temp/$1/

pwd

for f in *.tar.gz; do tar -xvf "$f"; done

sudo find . -name "*.gz" | xargs gunzip
