#!/usr/bin/env bash

cloud_type=$1
seed_node_ip_addr=$2

echo "Input to opscenter.sh is:"
echo cloud_type $cloud_type >> opsCenter.sh.out
echo seed_node_ip $seed_node_ip_addr >> opsCenter.sh.out

# Will point to a specific release
curl -o master.zip https://codeload.github.com/DSPN/install-datastax-redhat/zip/master
yum -y install unzip
unzip master.zip
cd install-datastax-redhat-master/bin

#./opscenter.sh $cloud_type $seed_node_ip_addr

./os/install_java.sh

# occ currently supports OEL 6.x and has python 2.5 only
if [ "$cloud_type" == "occ" ]; then
  ./os/install_python27.sh
fi

./opscenter/install.sh $cloud_type

./opscenter/start.sh
