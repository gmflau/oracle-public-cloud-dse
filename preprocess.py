import json
import nodes

ip_pool = []

with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

locations = clusterParameters['locations']
nodeCount = clusterParameters['nodeCount']
OCP_USER = clusterParameters['OCP_USER']
networkPrefix = clusterParameters['networkPrefix']

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
for counter in range(0, len(locations)*nodeCount + 1):
    networkName = OCP_USER + "/" + networkPrefix + str(counter)
    resources = nodes.generateIPs(networkName)
    ip_pool.append(networkName)
    generatedTemplateForIPs['oplans'][0]['objects'].append(resources)

with open('generatedTemplateForIPs.json', 'w') as outputFile:
   json.dump(generatedTemplateForIPs, outputFile, indent=4, ensure_ascii=False)

with open('cassandra_ip_pool.txt', 'w') as outputFile:
   json.dump(ip_pool, outputFile)

