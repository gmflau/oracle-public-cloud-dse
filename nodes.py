

def generateIPs(networkName):
    resource = {
          "name": networkName,
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


def generateInstanceNode(ocp_user, sshKey, vmType, securityList, hostname, boot_disk, app_data_disk, ip_label, seed_node_ip_addr, opscenter_ip_addr):
    resource = {
            "shape": vmType,
            "boot_order": [1],
            "label": hostname,
            "name": ocp_user + "/" + hostname,
            "attributes": {
                "userdata": {
                    "pre-bootstrap": {
                        "failonerror": "false",
                        "script": [
                            "cd /home/opc",
                            "curl https://raw.githubusercontent.com/DSPN/oracle-compute-cloud-dse/master/extensions/node.sh --output node.sh",
                            "chmod +x node.sh",
                            "./node.sh occ " + seed_node_ip_addr + " us2 " +  opscenter_ip_addr
                        ]
                    }
                }
            },
            "networking": {
                "eth0": {
                    "seclists": [ocp_user + "/" + securityList],
                    "nat": "ipreservation:" + ip_label
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


def generateInstanceOpsCenter(ocp_user, sshKey, vmType, securityList, hostname, boot_disk, app_data_disk, ip_label, seed_node_ip_addr):
    resource = {
            "shape": vmType,
            "boot_order": [1],
            "label": hostname,
            "name": ocp_user + "/" + hostname,
            "attributes": {
                "userdata": {
                    "pre-bootstrap": {
                        "failonerror": "false",
                        "script": [
                            "cd /home/opc",
                            "curl https://raw.githubusercontent.com/DSPN/oracle-compute-cloud-dse/master/extensions/opsCenter.sh --output opsCenter.sh",
                            "chmod +x opsCenter.sh",
                            "./opsCenter.sh occ " + seed_node_ip_addr
                        ]
                    }
                }
            },
            "networking": {
                "eth0": {
                    "seclists": [ocp_user + "/" + securityList],
                    "nat": "ipreservation:" + ip_label
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