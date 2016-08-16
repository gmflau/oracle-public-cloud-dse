#!/usr/bin/env bash

cloud_type=$1
seed_node_ip_addr=$2

echo "Input to opscenter.sh is:"
echo cloud_type $cloud_type >> opsCenter.sh.out
echo seed_node_ip $seed_node_ip_addr >> opsCenter.sh.out

curl -o 0.1.3.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/0.1.3
yum -y install unzip
unzip 0.1.3.zip
cd install-datastax-redhat-0.1.3/bin

./opscenter.sh $cloud_type $seed_node_ip_addr