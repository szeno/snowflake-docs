# May 25, 2026: Openflow Connector for Oracle: Multi-PDB replication from a CDB

The Openflow Connector for Oracle now supports replicating data from multiple Pluggable Databases
(PDBs) in a single connector instance when connected to a Container Database (CDB).
Previously, replicating tables from multiple PDBs required a separate connector
instance for each PDB.

To enable multi-PDB replication, grant the connector’s connect user two additional
Oracle privileges that allow the CDB-level user to switch between containers and
access data dictionary objects across all PDBs.

For more information, see
[Openflow Connector for Oracle: Configure the Oracle database](/user-guide/data-integration/openflow/connectors/oracle/setup-oracledb).
