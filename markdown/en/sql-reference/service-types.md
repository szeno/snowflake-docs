# Service types

This topic contains the types of usage that can incur costs in Snowflake.

| Service type | Usage statement name | Description | Category | Unit |
| --- | --- | --- | --- | --- |
| AI\_FUNCTIONS | AI FUNCTIONS | Cortex AI functions invoked from SQL, including COMPLETE and other LLM-backed functions. | AI and Machine Learning | AI Credits |
| AI\_INFERENCE | AI INFERENCE | Credit-based usage for running AI models via the Cortex REST API. | AI and Machine Learning | AI Credits |
| AI\_INFERENCE\_TOOLS | AI INFERENCE TOOLS | Credit-based usage for inference AI tool calls invoked by AI workloads. | AI and Machine Learning | AI Credits |
| AI\_SENSITIVE\_DATA\_CLASSIFICATION | AI SENSITIVE DATA CLASSIFICATION | AI token credits for AI-enriched sensitive data classification. | Management and Governance | AI Credits |
| AI\_SERVICES | AI SERVICES | Usage of Snowflake AI and ML services including Cortex functions. | AI and Machine Learning | Credits |
| AI\_TRAINING | AI TRAINING | Compute used by AI Training jobs | AI and Machine Learning | AI Credits |
| ARCHIVE\_STORAGE\_COLD | ARCHIVE STORAGE COLD | Long-term cold archive storage for infrequently accessed data. | Storage | TiB-Months |
| ARCHIVE\_STORAGE\_COOL | ARCHIVE STORAGE COOL | Mid-tier archive storage for occasionally accessed data. | Storage | TiB-Months |
| ARCHIVE\_STORAGE\_DATA\_RETRIEVAL | ARCHIVE STORAGE DATA RETRIEVAL | Charges for retrieving data from archive storage tiers. | Databases | TiB |
| ARCHIVE\_STORAGE\_RETRIEVAL\_FILE\_PROCESSING | ARCHIVE STORAGE RETRIEVAL FILE PROCESSING | Processing charges for file retrieval operations from archive storage. | Databases | Credits |
| ARCHIVE\_STORAGE\_WRITE | ARCHIVE STORAGE WRITE | Charges for writing data to archive storage tiers. | Storage | Credits |
| AUTOMATED\_REFRESH\_AND\_DATA\_REGISTRATION | AUTOMATED REFRESH AND DATA REGISTRATION | Compute for automated refresh and data registration in Iceberg tables. | Databases | Credits |
| AUTO\_CLUSTERING | AUTOMATIC CLUSTERING | Serverless compute for automatic reclustering of tables. | Databases | Credits |
| BACKUP | BACKUP | Compute and storage for backup snapshots. | Storage | Credits |
| BATCH\_CORTEX\_SEARCH | BATCH CORTEX SEARCH | Batch indexing and storage for Cortex Search over large document sets. | AI and Machine Learning | AI Credits |
| BLOCK\_STORAGE | BLOCK STORAGE | Block storage used by Snowpark Container Services and Hybrid Tables. | Storage | TiB-Months |
| BLOCK\_STORAGE\_ADDITIONAL\_IOPS | BLOCK STORAGE ADDITIONAL IOPS | Additional IOPS provisioned beyond baseline for block storage. | Storage | Thousand IOPS-Months |
| BLOCK\_STORAGE\_ADDITIONAL\_THROUGHPUT | BLOCK STORAGE ADDITIONAL THROUGHPUT | Additional throughput provisioned beyond baseline for block storage. | Storage | GB/Second-Months |
| CLOUD\_SERVICES | CLOUD SERVICES | Always-on services including authentication, metadata, and query optimization. | Compute | Credits |
| COPY\_FILES | COPY FILES | Serverless compute for COPY FILES operations between stages. | Migration | Credits |
| CORTEX\_AGENTS | CORTEX AGENTS | Agent API that orchestrates tools, queries data, and executes multi-step tasks in Snowflake and via MCP powered by Cortex. | AI and Machine Learning | AI Credits |
| CORTEX\_AI\_GUARDRAILS | CORTEX AI GUARDRAILS | AI-powered guardrails for content safety and policy enforcement for Cortex Agents. | AI and Machine Learning | AI Credits |
| CORTEX\_CODE\_CLI\_SUBSCRIPTION | CORTEX CODE: CLI (SUBSCRIPTION) | Self-service Cortex Code command-line interface subscription. | AI and Machine Learning | N/A |
| CORTEX\_SEARCH | CORTEX SEARCH | Managed retrieval service for semantic and hybrid search over Snowflake data. | AI and Machine Learning | AI Credits |
| DATA\_QUALITY\_MONITORING | DATA QUALITY MONITORING | Serverless compute for data quality monitoring and metrics. | Management and Governance | Credits |
| DATA\_TRANSFER | DATA TRANSFER | Network egress charges for data transferred out of Snowflake. | Networking | TiB |
| EGRESS\_COST\_OPTIMIZER | EGRESS COST OPTIMIZER | Service that optimizes and reduces data egress costs. | Management and Governance | TiB-Months |
| EXTERNAL\_GOVERNANCE | EXTERNAL GOVERNANCE | Compute used for external-governance (data policy) enforcement. | Management and Governance | Credits |
| FAILSAFE\_RECOVERY | FAILSAFE RECOVERY | Charges for recovering data from Fail-safe storage. | Databases | Credits |
| HYBRID\_TABLE\_DEDICATED\_STORAGE\_MODE | HYBRID TABLE DEDICATED STORAGE MODE | Dedicated storage mode for Hybrid Tables. | Storage | Days |
| HYBRID\_TABLE\_STORAGE | HYBRID TABLE STORAGE | Storage used by Hybrid Tables for transactional data. | Storage | TiB-Months |
| INTERNAL\_DATA\_TRANSFER | INTERNAL DATA TRANSFER | Data transfer between Snowflake regions or cloud providers. | Networking | TiB |
| LOGGING | LOGGING | Storage and compute for event logging and audit trails. | Management and Governance | Credits |
| MATERIALIZED\_VIEW | MATERIALIZED VIEWS | Serverless compute for maintaining materialized views. | Compute | Credits |
| ONLINE\_FEATURE\_STORE\_AUTOSCALE\_COMPUTE | ONLINE FEATURE STORE AUTOSCALE COMPUTE | Compute used by Feature Store autoscale managed compute pools. | AI and Machine Learning | Credits |
| ONLINE\_FEATURE\_STORE\_COMPUTE | ONLINE FEATURE STORE COMPUTE | Compute used by Online Feature Store | AI and Machine Learning | Credits |
| ONLINE\_FEATURE\_STORE\_STORAGE | ONLINE FEATURE STORE STORAGE | Storage used by Online Feature Store | AI and Machine Learning | TiB-Months |
| OPENFLOW\_COMPUTE\_BYOC | OPENFLOW COMPUTE BYOC | Openflow compute using Bring Your Own Cloud resources. | Compute | Credits |
| OPENFLOW\_COMPUTE\_SNOWFLAKE | OPENFLOW COMPUTE SNOWFLAKE | Openflow compute managed by Snowflake infrastructure. | Compute | Credits |
| ORGANIZATION\_USAGE | ORGANIZATION USAGE | Compute for organization-level usage tracking and reporting. | Management and Governance | Credits |
| OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED | OUTBOUND PRIVATELINK DATA PROCESSED | Data processed through outbound private connectivity connections. | Networking | TiB |
| OUTBOUND\_PRIVATELINK\_ENDPOINT | OUTBOUND PRIVATELINK ENDPOINT | Endpoint charges for outbound private connectivity connections. | Networking | Thousand Hours |
| PIPE | SNOWPIPE | Serverless compute for continuous data ingestion via Snowpipe. | Migration | Credits |
| POSTGRES\_COMPUTE | POSTGRES COMPUTE | Compute for PostgreSQL-compatible interface workloads. | Compute | Credits |
| POSTGRES\_COMPUTE\_HA | POSTGRES COMPUTE HA | High-availability compute for PostgreSQL-compatible workloads. | Compute | Credits |
| POSTGRES\_STORAGE | POSTGRES STORAGE | Storage for PostgreSQL-compatible interface data. | Storage | TiB-Months |
| POSTGRES\_STORAGE\_HA | POSTGRES STORAGE HA | High-availability storage for PostgreSQL-compatible data. | Storage | TiB-Months |
| QUERY\_ACCELERATION | QUERY ACCELERATION | Serverless compute for accelerating eligible queries. | Compute | Credits |
| REPLICATION | REPLICATION | Compute and transfer for database and account replication. | Networking | Credits |
| SEARCH\_OPTIMIZATION | SEARCH OPTIMIZATION | Serverless compute for search optimization service maintenance. | Compute | Credits |
| SENSITIVE\_DATA\_CLASSIFICATION | SENSITIVE DATA CLASSIFICATION | Serverless compute for classifying sensitive data. | Management and Governance | Credits |
| SERVERLESS\_ALERTS | SERVERLESS ALERTS | Serverless compute for alert condition evaluation. | Management and Governance | Credits |
| SERVERLESS\_EXPERIMENTS | SERVERLESS EXPERIMENTS | Serverless compute for experiment execution. | Compute | Credits |
| SERVERLESS\_TASK | SERVERLESS TASKS | Serverless compute for scheduled task execution. | Compute | Credits |
| SERVERLESS\_TASKS\_FLEX | SERVERLESS TASKS FLEX | Flexible serverless compute for scheduled tasks. | Compute | Credits |
| SNOWFLAKE\_APP\_RUNTIME | SNOWFLAKE APP RUNTIME | Compute used to build and host Snowflake Application Services on managed compute pools. | Compute | Credits |
| SNOWFLAKE\_APP\_RUNTIME\_PREVIEW | SNOWFLAKE APP RUNTIME PREVIEW | Compute and memory used to preview Snowflake App Runtime on Workspaces. | Compute | Credits |
| SNOWFLAKE\_APP\_RUNTIME\_SERVERLESS | SNOWFLAKE APP RUNTIME SERVERLESS | Compute and memory used to build and host Snowflake Application Services on serverless compute. | Compute | Credits |
| SNOWFLAKE\_COCO | SNOWFLAKE COCO | AI-powered coding assistant consumption billed via canonical Cortex Code events. | AI and Machine Learning | AI Credits |
| SNOWFLAKE\_COCO\_CLI | SNOWFLAKE COCO: CLI | AI-powered coding assistant accessed via the command-line interface for local development. | AI and Machine Learning | AI Credits |
| SNOWFLAKE\_COCO\_DESKTOP | SNOWFLAKE COCO: DESKTOP | AI-powered coding assistant accessed through the desktop app. | AI and Machine Learning | AI Credits |
| SNOWFLAKE\_COCO\_SNOWSIGHT | SNOWFLAKE COCO: SNOWSIGHT | AI-powered coding assistant accessed through the browser-based IDE in Snowsight. | AI and Machine Learning | AI Credits |
| SNOWFLAKE\_COWORK | SNOWFLAKE COWORK | Natural language interface for asking questions about your Snowflake and MCP data. | AI and Machine Learning | AI Credits |
| SNOWPARK\_CONTAINER\_SERVICES | SNOWPARK CONTAINER SERVICES | Compute and resources for Snowpark Container Services workloads. | Compute | Credits |
| SNOWPIPE\_STREAMING | SNOWPIPE STREAMING | Serverless compute for low-latency streaming ingestion. | Migration | Credits |
| STORAGE | STORAGE | Compressed data storage including Time Travel and Fail-safe. | Storage | TiB-Months |
| STORAGE\_LIFECYCLE\_POLICY\_EXECUTION | STORAGE LIFECYCLE POLICY EXECUTION | Compute for executing storage lifecycle policies. | Management and Governance | Credits |
| STORAGE\_REQUEST | STORAGE REQUEST | Request-based charges for storage operations. | Databases | Million Requests |
| TABLE\_OPTIMIZATION | TABLE OPTIMIZATION | Serverless compute for automatic table optimization. | Compute | Credits |
| TELEMETRY\_DATA\_INGEST | TELEMETRY DATA INGEST | Ingestion of telemetry and observability data. | Management and Governance | Credits |
| TRUST\_CENTER | TRUST CENTER | Serverless compute for Trust Center security monitoring. | Management and Governance | Credits |
| WAREHOUSE\_METERING | COMPUTE | Virtual warehouse compute credits for query execution. | Compute | Credits |

Expand

Show lessSee more
