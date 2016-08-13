

def generateIPs(ocp_user, networkName):
    resource = {
          "name": ocp_user + "/" + networkName,
          "parentpool": "/oracle/public/ippool",
          "permanent": "true"
        }
    return resource


def generateStorageVols(ocp_user, osImage, boot_vol_name, app_data_vol_name, boot_vol_size, data_vol_size):
    resource = [
        {
          "name": ocp_user + "/" + boot_vol_name,
          "bootable": "true",
          "imagelist": osImage,
          "properties": ["/oracle/public/storage/default"],
          "size": boot_vol_size
        },
        {
          "name": ocp_user + "/" + app_data_vol_name,
          "properties": ["/oracle/public/storage/latency"],
          "size": data_vol_size
        }
    ]
    return resource


def generateInstance(ocp_user, sshKey, vmType, securityList, hostname, boot_disk, app_data_disk, ip_label):
    resource = {
            "shape": vmType,
            "boot_order": [1],
            "label": hostname,
            "attributes": {
                "userdata": {
                    "pre-bootstrap": {
                        "failonerror": "true",
                        "script": [
                            "mkdir /containership3"
                        ]
                    },
                    "packages": ["git"]
                }
            },
            "networking": {
                "eth0": {
                    "seclists": [ocp_user + "/" + securityList],
                    "nat": "ipreservation:" + ocp_user + "/" + ip_label
                }
            },
            "sshkeys": [ocp_user + "/" + sshKey],
            "storage_attachments": [
                {
                    "index": 1,
                    "volume": ocp_user + "/" + boot_disk
                },
                {
                    "index": 2,
                    "volume": ocp_user + "/" + app_data_disk
                }
            ]
    }
    return resource