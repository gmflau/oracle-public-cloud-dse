#!/bin/bash

# Install datastax cassandra node

#cloud_type="occ"
#seed_node_location=$1
#unique_string=$2
#data_center_name=$3
#opscenter_location=$4

echo "Input to node.sh is:"
#echo cloud_type $cloud_type
#echo seed_node_location $seed_node_location
#echo unique_string $unique_string
#echo opscenter_location $opscenter_location

#seed_node_dns_name=
#opscenter_dns_name=

echo "Calling dse.sh with the settings:"
#echo cloud_type $cloud_type
#echo seed_node_dns_name $seed_node_dns_name
#echo data_center_name $data_center_name
#echo opscenter_dns_name $opscenter_dns_name

curl -o 0.1.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/0.1
yum -y install unzip
unzip 0.1.zip
cd install-datastax-redhat-0.1/bin

#./dse2.sh $cloud_type $seed_node_dns_name $data_center_name $opscenter_dns_name

