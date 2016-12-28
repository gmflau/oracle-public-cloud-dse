import json
import copy
import nodes
import sys

# Get publicKeyPath
publicKeyPath = sys.argv[1]

ip_pool = []
ip_address_list = {}
storage_pool = {}


# Open file for reading pre-allocated static IP addresses
with open('cassandra_ip_pool.txt', 'r') as inputFile:
    ip_pool = json.load(inputFile)


# Open file for reading DSE cluster deployment template
with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)


# Setting deployment variables
locations = clusterParameters['locations']
vmType = clusterParameters['vmType']
nodeCount = clusterParameters['nodeCount']
OPC_USER = clusterParameters['OPC_USER']
OPC_DOMAIN = clusterParameters['OPC_DOMAIN']
networkPrefix = clusterParameters['networkPrefix']
osImage = clusterParameters['osImage']
securityList = clusterParameters['securityList']
securityRules = clusterParameters['securityRules']
sshKey = clusterParameters['sshKey']
bootDriveSizeInBytes = clusterParameters['bootDriveSizeInBytes']
appDataDriveSizeInBytes = clusterParameters['appDataDriveSizeInBytes']


# Retrieve IP addresses from Oracle Cloud and insert them into a dictionary
with open('ipListWithoutHeader.txt', 'r') as inputFile:
    for line in inputFile:
        splitLine = line.split()
        ip_address_list[splitLine[0]] = splitLine[1]


# We will use "dse_secList" as the security list
generatedTemplateForSecurityList = {
    "description": "Plan to create security list",
    "name": OPC_USER + "/DataStax_Security_Lists_Plan",
    "oplans": [
        {
            "label": "admin-seclists",
            "obj_type": "seclist",

            "objects": [
                {
                    "name": OPC_USER + "/" + securityList
                }
            ]
        }
    ]
}


# We will use "DSE_Rules" as the security Rules
generatedTemplateForSecurityRules = {
    "description": "Plan to create security rules",
    "name": OPC_USER + "/DataStax_Security_Rules_Plan",
    "oplans": [
        {
            "label": "DSE_Security_Rules",
            "obj_type": "secrule",
            "objects": [
                {
                    "name": OPC_USER + "/" + securityRules,
                    "application": "/oracle/public/all",
                    "src_list": "seciplist:/oracle/public/public-internet",
                    "dst_list": "seclist:" + OPC_USER + "/DSE_Seclist",
                    "action": "PERMIT"
                }
            ]
        }
    ]
}


# Boilerplate orchestration template for static IP address provisioning
generatedTemplateForIPs = {
    "description": "Plan to create static IP addresses for DataStax node",
    "name": OPC_USER + "/DataStax_IP_Reservation_Plan",
    "oplans": [
        {
            "label": "DSE IP Reservation",
            "obj_type": "ip/reservation",
            "objects": []
        }
    ]
}


# Boilerplate orchestration template for storage provisioning 
generatedTemplateForStorage = {
    "description": "Plan to create storage volumnes for DataStax node",
    "name": OPC_USER + "/DataStax_Storage_Plan",
    "oplans": [
        {
            "label": "DSE storage volumes",
            "obj_type": "storage/volume",
            "objects": []
        }

    ]
}


# Boilerplate orchestration template for instance provisioning
generatedTemplateForInstance = {
    "description": "Plan to deploy OCC instance for DataStax node",
    "name": OPC_USER + "/DataStax_Instance_Plan",
    "oplans": [
        {
            "obj_type": "launchplan",
            "ha_policy": "active",
            "label": "DataStax_Instance_Plan",
            "objects": [{"instances": []}]
        }
    ]

}


# Boilerplate orchestration template for Master orhcestration plan
# This will combine storage and instance provisioning in sequence
generatedTemplateForMaster = {
    "description": "Master plan to spin up a DataStax node",
    "name": OPC_USER + "/DataStax_Master_Plan",
    "relationships": [
        {
            "to_oplan": "DataStax_Storage_Plan",
            "oplan": "DataStax_Instance_Plan",
            "type": "depends"
        }
    ],
    "oplans": [
        {
            "label": "DataStax_Storage_Plan",
            "obj_type": "orchestration",
            "objects": [
                {
                    "name": OPC_USER + "/DataStax_Storage_Plan"
                }
            ]
        },
        {
            "label": "DataStax_Instance_Plan",
            "obj_type": "orchestration",
            "objects": [
                {
                    "name": OPC_USER + "/DataStax_Instance_Plan"
                }
            ]
        }
    ]
}


# Provision security lists
with open('generatedTemplateForSecurityList.json', 'w') as outputFile:
    json.dump(generatedTemplateForSecurityList, outputFile, indent=4, ensure_ascii=False)


# Provision security rules
with open('generatedTemplateForSecurityRules.json', 'w') as outputFile:
    json.dump(generatedTemplateForSecurityRules, outputFile, indent=4, ensure_ascii=False)



# Populate storage pool dictionary with item => (location: (boot_vol, app_data_vol))
for location, api_endpoint in locations.items():
    for nodeCounter in range(0, nodeCount):
        boot_vol_name = location + ".boot_vol." + str(nodeCounter)
        app_data_vol_name = location + ".app_data_vol." + str(nodeCounter)
        storage_pool[location] = storage_pool.get(location, []) + [[boot_vol_name, app_data_vol_name]]


#### Provision OpsCenter instance

# Provision OpsCenter storage volumes
boot_vol_name = "opscenter.boot_vol"
app_data_vol_name = "opscenter.app_data_vol"
storage_pool['opscenter'] = [[boot_vol_name, app_data_vol_name]]
resources = nodes.generateStorageVols(OPC_USER, osImage, boot_vol_name, app_data_vol_name,
                                      bootDriveSizeInBytes, appDataDriveSizeInBytes)
storageTemplate = copy.deepcopy(generatedTemplateForStorage)
storageTemplate['oplans'][0]['objects'].append(resources[0])
storageTemplate['oplans'][0]['objects'].append(resources[1])


# Provision cloud vm instance for OpsCenter
hostname = "dse.ent.host.opscenter"
opscenter_ip_label = ip_pool.pop()
opscenter_node_ip_addr = ip_address_list[opscenter_ip_label]
# Pick the first IP in ip_pool as the Cassandra seed node IP
seed_node_ip_addr = ip_address_list[ip_pool[0]]
resources = nodes.generateInstanceOpsCenter(OPC_DOMAIN, OPC_USER, sshKey, vmType, securityList, hostname,
                                            storage_pool['opscenter'][0][0], storage_pool['opscenter'][0][1],
                                            opscenter_ip_label, seed_node_ip_addr)

instanceTemplate = copy.deepcopy(generatedTemplateForInstance)
instanceTemplate['oplans'][0]['objects'][0]['instances'].append(resources)


# Set unique orchestration plans name for OpsCenter provisioning
ops_center_storage_plan = OPC_USER + "/DataStax_Storage_Plan_OpsCenter"
ops_center_instance_plan = OPC_USER + "/DataStax_Instance_Plan_OpsCenter"
ops_center_master_plan = OPC_USER + "/DataStax_Master_Plan_OpsCenter"
storageTemplate['name'] = ops_center_storage_plan
instanceTemplate['name'] = ops_center_instance_plan

# Generate storage orchestration plan for OpsCenter
with open('generatedTemplateForStorage_OpsCenter.json', 'w') as outputFile:
    json.dump(storageTemplate, outputFile, indent=4, ensure_ascii=False)

# Generate instance orchestration plan for OpsCenter
with open('generatedTemplateForInstance_OpsCenter.json', 'w') as outputFile:
    json.dump(instanceTemplate, outputFile, indent=4, ensure_ascii=False)

# Generate master orchestration plan to spin up the DataStax Enterprise OpsCenter
masterTemplate = copy.deepcopy(generatedTemplateForMaster)
masterTemplate['name'] = ops_center_master_plan
masterTemplate['oplans'][0]['objects'][0]['name'] = ops_center_storage_plan
masterTemplate['oplans'][1]['objects'][0]['name'] = ops_center_instance_plan
with open('generatedTemplateForMaster_OpsCenter.json', 'w') as outputFile:
    json.dump(masterTemplate, outputFile, indent=4, ensure_ascii=False)



#### Provision DSE nodes

# Provision cloud vm instance for DSE nodes
index = 0
for location, storage_vols in storage_pool.items():

    # there is only one opscenter in our environment
    storageTemplate = copy.deepcopy(generatedTemplateForStorage)
    instanceTemplate = copy.deepcopy(generatedTemplateForInstance)
    masterTemplate = copy.deepcopy(generatedTemplateForMaster) 

    if location != 'opscenter':

        for storage_disks in storage_vols:

	    ## Initialize orchestration templates and create unique plans
	    storageTemplate = copy.deepcopy(generatedTemplateForStorage)
	    instanceTemplate = copy.deepcopy(generatedTemplateForInstance)
	    masterTemplate = copy.deepcopy(generatedTemplateForMaster)
	    storage_plan = OPC_USER + "/DataStax_Storage_Plan_DSE_" + str(index)
	    instance_plan = OPC_USER + "/DataStax_Instance_Plan_DSE_" + str(index)
	    master_plan = OPC_USER + "/DataStax_Master_Plan_DSE_" + str(index)

            ## Generate a hostname
	    hostname = "dse.ent.host." + location + "." + str(index)

	    ## Create storage orchestration template
            boot_vol_name = storage_disks[0]
            app_data_vol_name = storage_disks[1]
	
            resources = nodes.generateStorageVols(OPC_USER, osImage, boot_vol_name, app_data_vol_name,
                                              bootDriveSizeInBytes, appDataDriveSizeInBytes)    
	    storageTemplate['oplans'][0]['objects'].append(resources[0])
            storageTemplate['oplans'][0]['objects'].append(resources[1])
	    storageTemplate['name'] = storage_plan

            # Generate storage orchestration plan 
	    with open('generatedTemplateForStorage_DSE_' + str(index) + '.json', 'w') as outputFile:
    	       json.dump(storageTemplate, outputFile, indent=4, ensure_ascii=False)


	    ## Create instance orchestratoin template
            resources = nodes.generateInstanceNode(OPC_DOMAIN, OPC_USER, location, sshKey, vmType, securityList,
                                                   hostname, storage_disks[0], storage_disks[1], ip_pool.pop(),
                                                   seed_node_ip_addr, opscenter_node_ip_addr, publicKeyPath, index, nodeCount)
            instanceTemplate['oplans'][0]['objects'][0]['instances'].append(resources)
	    instanceTemplate['name'] = instance_plan

            # Generate instance orchestration plan
	    with open('generatedTemplateForInstance_DSE_' + str(index) + '.json', 'w') as outputFile:
               json.dump(instanceTemplate, outputFile, indent=4, ensure_ascii=False)


	    ## Create master orchestration template
	    masterTemplate['name'] = master_plan
	    masterTemplate['oplans'][0]['objects'][0]['name'] = storage_plan
	    masterTemplate['oplans'][1]['objects'][0]['name'] = instance_plan

            # Generate master orchestration plan
	    with open('generatedTemplateForMaster_DSE_' + str(index) + '.json', 'w') as outputFile:
               json.dump(masterTemplate, outputFile, indent=4, ensure_ascii=False)

            index += 1


