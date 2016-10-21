#!/bin/bash


# Archive old orchestration related files 
#timestamp_folder=./logs/$( date +"%Y-%m-%d-%H-%M-%S" )
#echo $timestamp
#mkdir $timestamp_folder
#mv generatedTemplateForIP_*.json $timestamp_folder
#mv cassandra_ip_pool.txt $timestamp_folder


python preprocess.py

for i in generatedTemplateForIP_*.json; do
    echo $i 
done


for i in generatedTemplateForStorage_DSE_*.json; do
    echo $i
done


for i in generatedTemplateForInstance_DSE_*.json; do
    echo $i
done


for i in generatedTemplateForMaster_DSE_*.json; do
    echo $i
done





