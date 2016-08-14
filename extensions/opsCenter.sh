#!/usr/bin/env bash

#cloud_type="occ"
#seed_node_location=$1
#unique_string=$2

echo "Input to opscenter.sh is:"
#echo cloud_type $cloud_type
#echo seed_node_location $seed_node_location
#echo unique_string $unique_string

#seed_node_dns_name=""

echo "Calling opscenter.sh with the settings:"
#echo cloud_type $cloud_type
#echo seed_node_dns_name $seed_node_dns_name

wget https://github.com/DSPN/install-datastax-redhat/archive/0.1.zip
yum -y install unzip
unzip 0.1.zip
cd install-datastax-redhat-0.1/bin

#./opscenter2.sh $cloud_type $seed_node_dns_name