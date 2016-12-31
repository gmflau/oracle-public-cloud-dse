import os

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
                         app_data_disk, ip_label, node_ip_addr, opscenter_ip_addr, sshKeyPath, index, nodeCount):

    publicKey = open(sshKeyPath, 'r').read()
    cmd = 'echo "' + publicKey + '" >> ~/.ssh/authorized_keys'

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

                        # Store the publicKey in /home/opc/.ssh/ folder
                        "cd /home/opc",
                        cmd,
                        "curl https://raw.githubusercontent.com/DSPN/oracle-public-cloud-dse/LCM/extensions/node.sh --output node.sh",
                        "chmod +x node.sh",
                        "./node.sh occ ",

                        "mkfs -t ext3 /dev/xvdc",
                        "mkdir /mnt/data1",
                        "mount /dev/xvdc /mnt/data1",
                        "echo '/dev/xvdc\t\t/mnt/data1\t\text3\tdefault\t\t0 0' | tee -a /etc/fstab",

                        # lcm -> addNode.py opscenter_ip_addr 'test_cluster' location unique_node_id private_ip_addr seed_node_ip_addr num_nodes_in_location
                        "rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm",
                        "yum -y install python setuptools python-pip",
                        "pip install requests",
                        "pip install argparse",
                        "git clone https://github.com/DSPN/amazon-cloudformation-dse",
                        "cd amazon-cloudformation-dse/lcm",
                        "./addNode.py --opsc-ip " + opscenter_ip_addr + " " + "--clustername test_cluster" + " --dcname " + location + " --nodeid " + str(index) + " --privip " +
                            "`hostname -I`" + " --pubip " + node_ip_addr + " --dcsize " + str(nodeCount)
                    ]
                },
                "packages": ["wget", "git"]
            }
        },
        "networking": {
            "eth0": {
                "seclists": [ ocp_user + "/" + securityList ],
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
                        "curl https://raw.githubusercontent.com/DSPN/oracle-public-cloud-dse/LCM/extensions/opsCenter.sh --output opsCenter.sh",
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
                "seclists": [ ocp_user + "/" + securityList ],
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
