import json
#import opsCenter
#import nodes

with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

locations = clusterParameters['locations']
vmSize = clusterParameters['vmSize']
nodeCount = clusterParameters['nodeCount']

# This is the skeleton of the template that we're going to add resources to
generatedTemplate = {
}

# Create DSE nodes in each location
for datacenterIndex in range(0, len(locations)):
    1

# Create the OpsCenter node
# to do

with open('generatedTemplate.json', 'w') as outputFile:
    json.dump(generatedTemplate, outputFile, sort_keys=True, indent=4, ensure_ascii=False)
