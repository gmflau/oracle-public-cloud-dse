# oracle-compute-dse [Work In Progress]
Scripts for deploying to Oracle Public Cloud (OPC)

These don't work yet, sorry.

These scripts will use the Oracle Public Cloud (OPC) CLI to deploy: https://docs.oracle.com/cloud-machine/latest/stcomputecs/ELUCL/GUID-A377A4D6-8A3E-43EF-B069-5C4EA50D7E6D.htm#ELACI115

 The [DataStax Enterprise Deployment Guide for Oracle Public Cloud - TBA] is a good place to start learning about these templates.

Directory | Description
--- | ---
[extensions](./extensions) | Common scripts that are used by OPC instance's bootstrapping process.  In OPC terminology these are referred to as "Automating Instance Configuration Using opc-init" a.k.a Linux OS bootstrapping.  You can learn more about this here - http://docs.oracle.com/cloud/latest/stcomputecs/STCSG/GUID-C63680F1-1D97-4984-AB02-285B17278CC5.htm#STCSG-GUID-C63680F1-1D97-4984-AB02-285B17278CC5 .
[root] (.) | Python and bash scripts to generate OPC CLI compliant json templates to stand up a DataStax DSE Cassandra environment.

