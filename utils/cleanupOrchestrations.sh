#!/bin/bash

rm -fr ../install-datastax-ubuntu-5.5.3
rm -fr ../5.5.3.zip

pwdFilePath=$1

oracle-compute discover orchestration $OPC_USER -p $pwdFilePath > orchestrations.txt
sed -e '1,1d' < orchestrations.txt  > orchestrationsWithoutHeader.txt

while read line
do
    oracle-compute stop orchestration $line --force
done < orchestrationsWithoutHeader.txt
sleep 180

while read line
do
    oracle-compute delete orchestration $line --force
done < orchestrationsWithoutHeader.txt
sleep 180

# Run this the second time to ensure all orchestrations will be gone
oracle-compute discover orchestration $OPC_USER -p $pwdFilePath > orchestrations.txt
sed -e '1,1d' < orchestrations.txt  > orchestrationsWithoutHeader.txt

while read line
do
    oracle-compute delete orchestration $line --force
done < orchestrationsWithoutHeader.txt
