import json
import sys
import nodes

ip_pool = []
storage_pool = {}

with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

locations = clusterParameters['locations']
vmType = clusterParameters['vmType']
nodeCount = clusterParameters['nodeCount']
OCP_USER = clusterParameters['OCP_USER']
networkPrefix = clusterParameters['networkPrefix']
osImage = clusterParameters['osImage']
securityList = clusterParameters['securityList']
securityRules = clusterParameters['securityRules']
sshKey = clusterParameters['sshKey']
bootDriveSizeInBytes = clusterParameters['bootDriveSizeInBytes']
appDataDriveSizeInBytes = clusterParameters['appDataDriveSizeInBytes']


# We will use "dse_secList" as the security list
generatedTemplateForSecurityList = {
  "description": "Plan to create security list",
  "name": OCP_USER + "/DataStax_Security_Lists_Plan",
  "oplans": [
    {
      "label": "admin-seclists",
      "obj_type": "seclist",

      "objects": [
        {
          "name": OCP_USER + "/" + securityList
        }
      ]
    }
  ]
}

# We will use "DSE_Rules" as the security Rules
generatedTemplateForSecurityRules = {
  "description": "Plan to create security rules",
  "name": OCP_USER + "/DataStax_Security_Rules_Plan",
  "oplans": [
    {
      "label": "DSE_Security_Rules",
      "obj_type": "secrule",
      "objects": [
        {
          "name": OCP_USER + "/" + securityRules,
          "application": "/oracle/public/all",
          "src_list": "seciplist:/oracle/public/public-internet",
          "dst_list": "seclist:" + OCP_USER + "/DSE_Seclist",
          "action": "PERMIT"
        }
      ]
    }
  ]
}

generatedTemplateForIPs = {
    "description": "Plan to create static IP addresses for DataStax node",
    "name": OCP_USER + "/DataStax_IP_Reservation_Plan",
    "oplans": [
        {
            "label": "DSE IP Reservation",
            "obj_type": "ip/reservation",
            "objects": []
        }
    ]
}


generatedTemplateForStorage = {
    "description": "Plan to create storage volumnes for DataStax node",
    "name": OCP_USER + "/DataStax_Storage_Plan",
    "oplans": [
        {
            "label": "DSE storage volumes",
            "obj_type": "storage/volume",
            "objects": []
        }

    ]
}


# This is the skeleton of the template that we're going to add resources to
generatedTemplateForInstance = {
    "description": "Plan to deploy OCC instance for DataStax node",
    "name": OCP_USER + "/DataStax_Instance_Plan",
    "oplans": [
        {
            "obj_type": "launchplan",
            "ha_policy": "active",
            "label": "DataStax_Instance_Plan",
            "objects": [{"instances": []}]
        }
    ]

}


generatedTemplateForMaster = {
    "description": "Master plan to spin up a DataStax node",
    "name": OCP_USER + "/DataStax_Master_Plan",
    "relationships": [
        {
            "to_oplan": "DataStax_Storage_Plan",
            "oplan": "DataStax_Instance_Plan",
            "type": "depends"
        }
    ],
    "status": "ready",
    "oplans": [
        {
            "label": "DataStax_Storage_Plan",
            "obj_type": "orchestration",
            "objects": [
                {
                    "name": OCP_USER + "/DataStax_Storage_Plan"
                }
            ]
        },
        {
            "label": "DataStax_Instance_Plan",
            "obj_type": "orchestration",
            "objects": [
                {
                    "name": OCP_USER + "/DataStax_Instance_Plan"
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


# Provision static IPs for the DataStax Cassandra cluster + OpCenter
for counter in range(0, len(locations)*nodeCount + 1):
    networkName = networkPrefix + str(counter)
    resources = nodes.generateIPs(OCP_USER, networkName)
    ip_pool.append(networkName)
    generatedTemplateForIPs['oplans'][0]['objects'].append(resources)

with open('generatedTemplateForIPs.json', 'w') as outputFile:
   json.dump(generatedTemplateForIPs, outputFile, indent=4, ensure_ascii=False)


# Provision storage volumes for the DataStax Cassandra cluster
for location, api_endpoint in locations.items():
    for nodeCounter in range(0, nodeCount):
        boot_vol_name = location + ".boot_vol." + str(nodeCounter)
        app_data_vol_name = location + ".app_data_vol." + str(nodeCounter)
        resources = nodes.generateStorageVols(OCP_USER, osImage, boot_vol_name, app_data_vol_name,
                                            bootDriveSizeInBytes, appDataDriveSizeInBytes)
        storage_pool[location] = storage_pool.get(location, []) + [[boot_vol_name, app_data_vol_name]]
        generatedTemplateForStorage['oplans'][0]['objects'].append(resources[0])
        generatedTemplateForStorage['oplans'][0]['objects'].append(resources[1])

# Provision OpsCenter storage volumes
boot_vol_name = "opscenter.boot_vol"
app_data_vol_name = "opscenter.app_data_vol"
resources = nodes.generateStorageVols(OCP_USER, osImage, boot_vol_name, app_data_vol_name,
                                      bootDriveSizeInBytes, appDataDriveSizeInBytes)
storage_pool['opscenter'] = [[boot_vol_name, app_data_vol_name]]
generatedTemplateForStorage['oplans'][0]['objects'].append(resources[0])
generatedTemplateForStorage['oplans'][0]['objects'].append(resources[1])

with open('generatedTemplateForStorage.json', 'w') as outputFile:
    json.dump(generatedTemplateForStorage, outputFile, indent=4, ensure_ascii=False)


# Provision cloud vm instances for the DataStax Cassandra cluster and OpsCenter
for location, storage_vols in storage_pool.items():
    index = 0
    for storage_disks in storage_vols:
        hostname = "dse.host." + location + "." + str(index)
        resources = nodes.generateInstance(OCP_USER, sshKey, vmType, securityList, hostname,
                                           storage_disks[0], storage_disks[1], ip_pool.pop())
        generatedTemplateForInstance['oplans'][0]['objects'][0]['instances'].append(resources)
        index += 1

with open('generatedTemplateForInstance.json', 'w') as outputFile:
    json.dump(generatedTemplateForInstance, outputFile, indent=4, ensure_ascii=False)


# Generate master orchestration plan to spin up the DataStax Cassandra cluster
with open('generatedTemplateForMaster.json', 'w') as outputFile:
   json.dump(generatedTemplateForMaster, outputFile, indent=4, ensure_ascii=False)




