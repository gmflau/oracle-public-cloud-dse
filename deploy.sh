#!/bin/bash

# Retrieve the public ssh-key's full filename
sshkey=$1

# Retrieve the full path of a file storing your Oracle CLI's password
# Make sure you do a "chmod 600" on it
pwdFilePath=$2

# Add public ssh-key to your Oracle Cloud environment
oracle-compute add sshkey $OPC_USER/dse_ocp_key $sshkey -p $pwdFilePath
sleep 10

# Building DataStax Cassandra cluster and OpsCenter

# Generate the IP reservation addresses for the DSE Cassandra cluster nodes
python preprocess.py
oracle-compute add orchestration generatedTemplateForIPs.json -f json -p $pwdFilePath
sleep 10
oracle-compute start orchestration $OPC_USER/DataStax_IP_Reservation_Plan -p $pwdFilePath
sleep 15
oracle-compute list ipreservation $OPC_USER -p $pwdFilePath -F name,ip > ipListWithHeader.txt
sleep 10
sed -e '1,1d' < ipListWithHeader.txt > ipListWithoutHeader.txt

# Generate storage, compute and master plan OPC CLI orchestration templates
python main.py

# Currently comment out the following two orchestrations as we are using default security list from your OPC account
#oracle-compute add orchestration generatedTemplateForSecurityList.json -f json -p $pwdFilePath
#oracle-compute add orchestration generatedTemplateForSecurityRules.json -f json -p $pwdFilePath
#oracle-compute start orchestration $OPC_USER/DataStax_Security_Lists_Plan -p $pwdFilePath
#oracle-compute start orchestration $OPC_USER/DataStax_Security_Rules_Plan -p $pwdFilePath

# Adding the templates to your OPC CLI environment and executing through the Master_Plan orchestration
oracle-compute add orchestration generatedTemplateForStorage.json -f json -p $pwdFilePath
oracle-compute add orchestration generatedTemplateForInstance.json -f json -p $pwdFilePath
oracle-compute add orchestration generatedTemplateForMaster.json -f json -p $pwdFilePath

# No need to run the following two orchestrations as we are using the default security list from your OPC env.
#oracle-compute start orchestration $OPC_USER/DataStax_Security_Lists_Plan -p $pwdFilePath
#oracle-compute start orchestration $OPC_USER/DataStax_Security_Rules_Plan -p $pwdFilePath

# Executing through the Master_Plan orchestration: invoke both storage and compute instance orchestrations in sequence
sleep 10
oracle-compute start orchestration $OPC_USER/DataStax_Master_Plan -p $pwdFilePath


