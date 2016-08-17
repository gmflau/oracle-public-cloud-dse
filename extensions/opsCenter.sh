#!/usr/bin/env bash

cloud_type=$1
seed_node_ip_addr=$2

echo "Input to opscenter.sh is:"
echo cloud_type $cloud_type >> opsCenter.sh.out
echo seed_node_ip $seed_node_ip_addr >> opsCenter.sh.out

curl -o master.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/master
yum -y install unzip
unzip master.zip
cd install-datastax-redhat-master/bin

./opscenter.sh $cloud_type $seed_node_ip_addr