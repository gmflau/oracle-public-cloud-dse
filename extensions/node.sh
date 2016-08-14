#!/bin/bash

# Install datastax cassandra node

cloud_type=$1
seed_node_ip_addr=$2
location=$3
opscenter_ip_addr=$4

echo "Input to node.sh is:"
echo cloud_type $cloud_type >> node.sh.out
echo seed_node_ip_addr $seed_node_ip_addr >> node.sh.out
echo opscenter_ip_addr $opscenter_ip_addr >> node.sh.out

curl -o 0.1.1.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/0.1.1
yum -y install unzip
unzip 0.1.1.zip
cd install-datastax-redhat-0.1.1/bin

./reach_install_dse.sh

./dse.sh $cloud_type $seed_node_ip_addr $location $opscenter_ip_addr

