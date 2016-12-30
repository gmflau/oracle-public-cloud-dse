#!/bin/bash

# Install datastax cassandra node

cloud_type=$1

echo "Input to node.sh is:"
echo cloud_type $cloud_type >> node.sh.out

# Will point to a specific release
curl -o master.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/master
yum -y install unzip
unzip master.zip
cd install-datastax-redhat-master/bin

# Installing prerequisite software components for DSE 5.0.x
./os/install_java.sh
# occ currently supports OEL 6.x and has python 2.5 only
if [ "$cloud_type" == "occ" ]; then
  ./os/install_python27.sh
fi
./os/install_glibc_OEL6x.sh

# OpsCenter uses iostat
# OEL 6.7 does not have sysstat package pre-installed
yum -y install sysstat

# ./dse.sh $cloud_type $seed_node_ip_addr $location $opscenter_ip_addr

