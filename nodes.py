

def generateIPs(ocp_user, networkName):
    resource = {
          "name": ocp_user + "/" + networkName,
          "parentpool": "/oracle/public/ippool",
          "permanent": "true"
        }
    return resource


def generateStorageVols(ocp_user, osImage, boot_vol_name, app_data_vol_name):
    resource = [
        {
          "name": ocp_user + "/" + boot_vol_name,
          "bootable": "true",
          "imagelist": osImage,
          "properties": ["/oracle/public/storage/default"],
          "size": "4294967296"
        },
        {
          "name": ocp_user + "/" + app_data_vol_name,
          "properties": ["/oracle/public/storage/latency"],
          "size": "32212254720"
        }
    ]
    return resource
