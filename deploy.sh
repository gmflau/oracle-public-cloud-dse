#!/bin/bash


#### Archive files generated from previous deployments
timestamp_folder=./logs/$( date +"%Y-%m-%d-%H-%M-%S" )
echo $timestamp
mkdir $timestamp_folder
mv generatedTemplateFor*.json $timestamp_folder
mv cassandra_ip_pool.txt $timestamp_folder
mv ipListWithHeader.txt $timestamp_folder
mv ipListWithoutHeader.txt $timestamp_folder


##### Retrieve ssh public key name
sshKeyName=$1

##### Retrieve ssh public key's fullpath name
sshKeyFilePath=$2

##### Retrieve the full path of a file storing your Oracle CLI's password
# Make sure you "chmod 600" on it
pwdFilePath=$3

##### Add public ssh-key to your Oracle Cloud environment
oracle-compute add sshkey $OPC_USER/$sshKeyName $sshKeyFilePath -p $pwdFilePath


##### Building DataStax Cassandra cluster and OpsCenter
# Generate the IP reservation addresses for the DSE Cassandra cluster nodes
python preprocess.py

for i in generatedTemplateForIP_*.json; do
    echo $i
    oracle-compute add orchestration $i -f json -p $pwdFilePath
    sleep 2
done

COUNTER=0
for i in generatedTemplateForIP_*.json; do
    echo $i
    oracle-compute start orchestration $OPC_USER/DataStax_IP_Reservation_Plan_$COUNTER -p $pwdFilePath
    let COUNTER=COUNTER+1
    sleep 5
done

sleep 5
oracle-compute list ipreservation $OPC_USER -p $pwdFilePath -F name,ip > ipListWithHeader.txt
sed -e '1,1d' < ipListWithHeader.txt > ipListWithoutHeader.txt


# Generate storage, compute and master plan OPC CLI orchestration templates
python main.py
oracle-compute add orchestration generatedTemplateForSecurityList.json -f json -p $pwdFilePath
oracle-compute add orchestration generatedTemplateForSecurityRules.json -f json -p $pwdFilePath
oracle-compute start orchestration $OPC_USER/DataStax_Security_Lists_Plan -p $pwdFilePath
oracle-compute start orchestration $OPC_USER/DataStax_Security_Rules_Plan -p $pwdFilePath

# Adding the templates to your OPC CLI environment and executing through the Master_Plan orchestration
for i in generatedTemplateForStorage_*.json; do
    echo $i
    oracle-compute add orchestration $i -f json -p $pwdFilePath
    sleep 2
done

for i in generatedTemplateForInstance_*.json; do
    echo $i
    oracle-compute add orchestration $i -f json -p $pwdFilePath
    sleep 2
done

for i in generatedTemplateForMaster_*.json; do
    echo $i
    oracle-compute add orchestration $i -f json -p $pwdFilePath
    sleep 2
done
sleep 30

oracle-compute discover orchestration $OPC_USER -p $pwdFilePath | grep Master > generatedTemplateForMasterPlanWithHeader.txt
sed -e '1,1d' < generatedTemplateForMasterPlanWithHeader.txt  > generatedTemplateForMasterPlanWithoutHeader.txt
while read line
do
    oracle-compute start orchestration $line -p $pwdFilePath
    sleep 5
done < generatedTemplateForMasterPlanWithoutHeader.txt


