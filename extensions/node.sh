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

curl -o master.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/master
yum -y install unzip
unzip master.zip
cd install-datastax-redhat-master/bin

./dse.sh $cloud_type $seed_node_ip_addr $location $opscenter_ip_addr

