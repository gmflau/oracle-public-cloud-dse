#!/bin/bash

# Retrieve the public ssh-key's full filename
sshkey=$1

# Add public ssh-key to Oracle Cloud environment
oracle-compute add sshkey $OPC_USER/dse_ocp_key $sshkey

# This uses clusterParameters.json as input and writes output to generatedTemplate.json (orchestration.json)
python main.py $OPC_USER

# Adding OCC orchestrations to spin up a DataStax Cassandra cluster in Oracle Cloud
oracle-compute add orchestration generatedTemplateForSecurityList.json -f json
oracle-compute add orchestration generatedTemplateForSecurityRules.json -f json
oracle-compute add orchestration generatedTemplateForIPs.json -f json
oracle-compute add orchestration generatedTemplateForStorage.json -f json

# Firing off OCC orchestrations to spin up a DataStax Cassandra cluster in Oracle Cloud
oracle-compute start orchestration $OPC_USER//DSE_Security_Lists_Plan
oracle-compute start orchestration $OPC_USER//DSE_Security_Rules_Plan
oracle-compute start orchestration $OPC_USER/DataStax_IP_Reservation_Plan
oracle-compute start orchestration $OPC_USER//DataStax_Storage_Plan


