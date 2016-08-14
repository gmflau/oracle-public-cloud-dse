#!/bin/bash

# Retrieve the public ssh-key's full filename
sshkey=$1

# Add public ssh-key to your Oracle Cloud environment
oracle-compute add sshkey $OPC_USER/dse_ocp_key $sshkey

# Building DataStax Cassandra cluster and OpsCenter
python preprocess.py
oracle-compute add orchestration generatedTemplateForIPs.json -f json -p pwdFile
oracle-compute start orchestration $OPC_USER/DataStax_IP_Reservation_Plan -p pwdFile
oracle-compute list ipreservation $OPC_USER -p pwdFile -F name,ip > ipListWithHeader.txt
sed -e '1,1d' < ipListWithHeader.txt > ipListWithoutHeader.txt

python main.py
oracle-compute add orchestration generatedTemplateForSecurityList.json -f json -p pwdFile
oracle-compute add orchestration generatedTemplateForSecurityRules.json -f json -p pwdFile
oracle-compute add orchestration generatedTemplateForStorage.json -f json -p pwdFile
oracle-compute add orchestration generatedTemplateForInstance.json -f json -p pwdFile
oracle-compute add orchestration generatedTemplateForMaster.json -f json -p pwdFile
oracle-compute start orchestration $OPC_USER/DataStax_Security_Lists_Plan -p pwdFile
oracle-compute start orchestration $OPC_USER/DataStax_Security_Rules_Plan -p pwdFile
oracle-compute start orchestration $OPC_USER/DataStax_Master_Plan -p pwdFile
