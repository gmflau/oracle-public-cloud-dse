import json
import nodes


# Generate IP address OCID


ip_pool = []


# Open DSE Cluster deployment environment file
with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)


# Retrieve information for the deployment file for IP createion orchestration
locations = clusterParameters['locations']
nodeCount = clusterParameters['nodeCount']
OCP_USER = clusterParameters['OPC_USER']
networkPrefix = clusterParameters['networkPrefix']


# Standard IP address orchestration template boiler plate
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


# Provision static IPs for the DataStax Cassandra cluster + OpCenter
for counter in range(0, len(locations) * nodeCount + 1):
    networkName = OCP_USER + "/" + networkPrefix + str(counter)
    resources = nodes.generateIPs(networkName)
    ip_pool.append(networkName)
    generatedTemplateForIPs['oplans'][0]['objects'].append(resources)
    with open('generatedTemplateForIP_' + str(counter) + '.json', 'w') as outputFile:
       json.dump(generatedTemplateForIPs, outputFile, indent=4, ensure_ascii=False)


# Output list of IP address OCIDs
with open('cassandra_ip_pool.txt', 'w') as outputFile:
    json.dump(ip_pool, outputFile)



