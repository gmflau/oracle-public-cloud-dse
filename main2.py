import json
import copy
import nodes

OPC_USER = 'GML'


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



#### Provision OpsCenter instance

####### 
#               Need to make a copy of the json object .  how?#
#######


# Set unique orchestration plans name for OpsCenter provisioning
ops_center_storage_plan = OPC_USER + "/DataStax_Storage_Plan_OpsCenter"
ops_center_instance_plan = OPC_USER + "/DataStax_Instance_Plan_OpsCenter"
temp1 = copy.deepcopy(generatedTemplateForStorage)
temp2 = copy.deepcopy(generatedTemplateForInstance)

temp1['name'] = ops_center_storage_plan
temp2['name'] = ops_center_instance_plan

# Generate storage orchestration plan for OpsCenter
with open('generatedTemplateForStorage_OpsCenter.json', 'w') as outputFile:
    json.dump(temp1, outputFile, indent=4, ensure_ascii=False)

# Generate instance orchestration plan for OpsCenter
with open('generatedTemplateForInstance_OpsCenter.json', 'w') as outputFile:
    json.dump(temp2, outputFile, indent=4, ensure_ascii=False)

# Generate master orchestration plan to spin up the DataStax Enterprise OpsCenter
temp3 = copy.deepcopy(generatedTemplateForMaster)
temp3['oplans'][0]['objects'][0]['name'] = ops_center_storage_plan
temp3['oplans'][1]['objects'][0]['name'] = ops_center_instance_plan
with open('generatedTemplateForMaster_OpsCenter.json', 'w') as outputFile:
    json.dump(temp3, outputFile, indent=4, ensure_ascii=False)



# Set unique orchestration plans name for OpsCenter provisioning
dse_storage_plan = OPC_USER + "/DataStax_Storage_Plan_DSE"
dse_instance_plan = OPC_USER + "/DataStax_Instance_Plan_DSE"
temp1 = copy.deepcopy(generatedTemplateForStorage)
temp2 = copy.deepcopy(generatedTemplateForInstance)

temp1['name'] = dse_storage_plan
temp2['name'] = dse_instance_plan

# Generate storage orchestration plan for OpsCenter
with open('generatedTemplateForStorage_Dse.json', 'w') as outputFile:
    json.dump(temp1, outputFile, indent=4, ensure_ascii=False)

# Generate instance orchestration plan for OpsCenter
with open('generatedTemplateForInstance_Dse.json', 'w') as outputFile:
    json.dump(temp2, outputFile, indent=4, ensure_ascii=False)

# Generate master orchestration plan to spin up the DataStax Enterprise OpsCenter
temp3 = copy.deepcopy(generatedTemplateForMaster)
temp3['oplans'][0]['objects'][0]['name'] = dse_storage_plan
temp3['oplans'][1]['objects'][0]['name'] = dse_instance_plan
with open('generatedTemplateForMaster_Dse.json', 'w') as outputFile:
    json.dump(temp3, outputFile, indent=4, ensure_ascii=False)



