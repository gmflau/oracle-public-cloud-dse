import json
import sys

#import opsCenter
import nodes

ip_pool = []
storage_pool_boot_vol = {}
storage_pool_app_data_vol = {}


with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

locations = clusterParameters['locations']
vmSize = clusterParameters['vmSize']
nodeCount = clusterParameters['nodeCount']
OCP_USER = clusterParameters['OCP_USER']
networkPrefix = clusterParameters['networkPrefix']
osImage = clusterParameters['osImage']

# oracle-compute add ssh-public-key


# We will use "dse_secList" as the security list
generatedTemplateForSecurityList = {
  "name": OCP_USER + "/DSE_Security_Lists_Plan",
  "oplans": [
    {
      "label": "admin-seclists",
      "obj_type": "seclist",

      "objects": [
        {
          "name": OCP_USER + "/DSE_Seclist"
        }
      ]
    }
  ]
}

# We will use "DSE_Rules" as the security Rules
generatedTemplateForSecurityRules = {
  "name": OCP_USER + "/DSE_Security_Rules_Plan",
  "oplans": [
    {
      "label": "DSE_Security_Rules",
      "obj_type": "secrule",
      "objects": [
        {
          "name": OCP_USER + "/DSE_Rules",
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
    "Description": "Plan to create static IP addresses for DataStax node",
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
    "Description": "Plan to create storage volumnes for DataStax node",
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
    "description": "Orchestration plan to deploy OCC instance for DataStax node",
    "name": OCP_USER + "/DataStax_Instance_Plan",
    "oplans": [
        {
            "obj_type": "launchplan",
            "ha_policy": "active",
            "label": "DataStax_Instance_Plan",
            "objects": []
        }
    ]

}


generatedTemplateForMaster = {
    "description": "Master plan to spin up a DataStax node",
    "name": OCP_USER + "/DataStax_Master_Plan",
    "relationships": [
        {
            "oplan1": "DataStax_IP_Resv_Plan",
            "oplan2": "DataStax_Storage_Plan",
            "oplan3": "DataStax_Instance_Plan",
            "type": "depends"
        }
    ],
    "status": "ready",
    "oplans": [
        {
            "label": "DataStax_IP_Resv_Plan",
            "obj_type": "orchestration",
            "objects": [
                {
                    "name": OCP_USER + "/DataStax_IP_Reservation_Plan"
                }
            ]
        },
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

# Provision static IPs for the DataStax Cassandra cluster
for counter in range(0, len(locations)*nodeCount):
    networkName = networkPrefix + str(counter)
    resources = nodes.generateIPs(OCP_USER, networkName)
    ip_pool.append(networkName)
    generatedTemplateForIPs['oplans'][0]['objects'].append(resources)

with open('generatedTemplateForIPs.json', 'w') as outputFile:
   json.dump(generatedTemplateForIPs, outputFile, indent=4, ensure_ascii=False)

# Provision storage volumens for the DataStax Cassandra cluster
for locationCounter in range(0, len(locations)):
    for nodeCounter in range(0, nodeCount):
        location = locations[locationCounter]
        boot_vol_name = location + ".boot_vol." + str(nodeCounter)
        app_data_vol_name = location + ".app_data_vol." + str(nodeCounter)
        resources = nodes.generateStorageVols(OCP_USER, osImage, boot_vol_name, app_data_vol_name)
        print location
        print boot_vol_name
        storage_pool_boot_vol[location] = storage_pool_boot_vol.get(location, []) + [boot_vol_name]
        print storage_pool_boot_vol[location]
        storage_pool_app_data_vol[location] = storage_pool_app_data_vol.get(location, []) + [app_data_vol_name]
        generatedTemplateForStorage['oplans'][0]['objects'].append(resources)

with open('generatedTemplateForStorage.json', 'w') as outputFile:
    json.dump(generatedTemplateForStorage, outputFile, indent=4, ensure_ascii=False)




# Create DSE nodes in each location
#for datacenterIndex in range(0, len(locations)):
    #location = locations[datacenterIndex]

    #
   # resources

# Create the OpsCenter node
# to do

#with open('generatedTemplate.json', 'w') as outputFile:
 #  json.dump(generatedTemplate, outputFile, sort_keys=True, indent=4, ensure_ascii=False)

with open('generatedTemplateForInstance.json', 'w') as outputFile:
   json.dump(generatedTemplateForInstance, outputFile, sort_keys=True, indent=4, ensure_ascii=False)

with open('generatedTemplateForMaster.json', 'w') as outputFile:
   json.dump(generatedTemplateForMaster, outputFile, sort_keys=True, indent=4, ensure_ascii=False)
