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


def generateInstanceNode(opc_domain, ocp_user, location, sshKey, vmType, securityList, hostname, boot_disk,
                         app_data_disk, ip_label, seed_node_ip_addr, opscenter_ip_addr):
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
                        "curl https://raw.githubusercontent.com/DSPN/oracle-public-cloud-dse/master/extensions/node.sh --output node.sh",
                        "chmod +x node.sh",
                        "mkfs -t ext3 /dev/xvdc",
                        "mkdir /mnt/data1",
                        "mount /dev/xvdc /mnt/data1",
                        "echo '/dev/xvdc\t\t/mnt/data1\t\text3\tdefault\t\t0 0' | tee -a /etc/fstab",
                        "./node.sh occ " + seed_node_ip_addr + " " + location + " " + opscenter_ip_addr
                    ]
                },
                "packages": ["wget"]
            }
        },
        "networking": {
            "eth0": {
                "seclists": [opc_domain + "/default/default"],
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


def generateInstanceOpsCenter(opc_domain, ocp_user, sshKey, vmType, securityList, hostname, boot_disk, app_data_disk,
                              ip_label, seed_node_ip_addr):
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
                        "curl https://raw.githubusercontent.com/DSPN/oracle-public-cloud-dse/master/extensions/opsCenter.sh --output opsCenter.sh",
                        "chmod +x opsCenter.sh",
                        "mkfs -t ext3 /dev/xvdc",
                        "mkdir /mnt/data1",
                        "mount /dev/xvdc /mnt/data1",
                        "echo '/dev/xvdc\t\t/mnt/data1\t\text3\tdefault\t\t0 0' | tee -a /etc/fstab",
                        "./opsCenter.sh occ " + seed_node_ip_addr
                    ]
                },
                "packages": ["wget"]
            }
        },
        "networking": {
            "eth0": {
                "seclists": [opc_domain + "/default/default"],
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
