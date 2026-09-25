# All controller services (alphabetical)

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic provides a list of all openflow controller services in alphabetical order.
The list includes:

> - Type of controller service (Snowflake or not)
> - The name of each controller service
> - A summary of each controller service

## A

|  | Controller | Description |
| --- | --- | --- |
|  | [ADLSCredentialsControllerService](/user-guide/data-integration/openflow/controllers/adlscredentialscontrollerservice) | Defines credentials for ADLS processors. |
|  | [ADLSCredentialsControllerServiceLookup](/user-guide/data-integration/openflow/controllers/adlscredentialscontrollerservicelookup) | Provides an ADLSCredentialsService that can be used to dynamically select another ADLSCredentialsService. |
|  | [AmazonGlueEncodedSchemaReferenceReader](/user-guide/data-integration/openflow/controllers/amazonglueencodedschemareferencereader) | Reads Schema Identifier according to AWS Glue Schema encoding as a header consisting of a two byte markers and a 16 byte UUID |
|  | [AmazonGlueSchemaRegistry](/user-guide/data-integration/openflow/controllers/amazonglueschemaregistry) | Provides a Schema Registry that interacts with the AWS Glue Schema Registry so that those Schemas that are stored in the Glue Schema Registry can be used in NiFi. |
|  | [AmazonMSKConnectionService](/user-guide/data-integration/openflow/controllers/amazonmskconnectionservice) | Provides and manages connections to AWS MSK Kafka Brokers for producer or consumer operations. Use this service for workload identity federation. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [AmazonMSKConnectionService](/user-guide/data-integration/openflow/controllers/amazonmskconnectionservice) | Deprecated. Doesn’t support workload identity federation. Use the service without the Snowflake badge instead. |
|  | [ApicurioSchemaRegistry](/user-guide/data-integration/openflow/controllers/apicurioschemaregistry) | Provides a Schema Registry that interacts with the Apicurio Schema Registry so that those Schemas that are stored in the Apicurio Schema Registry can be used in NiFi. |
|  | [AvroReader](/user-guide/data-integration/openflow/controllers/avroreader) | Parses Avro data and returns each Avro record as an separate Record object. |
|  | [AvroRecordSetWriter](/user-guide/data-integration/openflow/controllers/avrorecordsetwriter) | Writes the contents of a RecordSet in Binary Avro format. |
|  | [AvroSchemaRegistry](/user-guide/data-integration/openflow/controllers/avroschemaregistry) | Provides a service for registering and accessing schemas. |
|  | [AWSCredentialsProviderControllerService](/user-guide/data-integration/openflow/controllers/awscredentialsprovidercontrollerservice) | Defines credentials for Amazon Web Services processors. |
|  | [AzureBlobStorageFileResourceService](/user-guide/data-integration/openflow/controllers/azureblobstoragefileresourceservice) | Provides an Azure Blob Storage file resource for other components. |
|  | [AzureCosmosDBClientService](/user-guide/data-integration/openflow/controllers/azurecosmosdbclientservice) | Provides a controller service that configures a connection to Cosmos DB (Core SQL API) and provides access to that connection to other Cosmos DB-related components. |
|  | [AzureDataLakeStorageFileResourceService](/user-guide/data-integration/openflow/controllers/azuredatalakestoragefileresourceservice) | Provides an Azure Data Lake Storage (ADLS) file resource for other components. |
|  | [AzureEventHubRecordSink](/user-guide/data-integration/openflow/controllers/azureeventhubrecordsink) | Format and send Records to Azure Event Hubs |
|  | [AzureStorageCredentialsControllerService\_v12](/user-guide/data-integration/openflow/controllers/azurestoragecredentialscontrollerservice_v12) | Provides credentials for Azure Storage processors using Azure Storage client library v12. |
|  | [AzureStorageCredentialsControllerServiceLookup\_v12](/user-guide/data-integration/openflow/controllers/azurestoragecredentialscontrollerservicelookup_v12) | Provides an AzureStorageCredentialsService\_v12 that can be used to dynamically select another AzureStorageCredentialsService\_v12. |

Expand

Show lessSee more

## C

|  | Controller | Description |
| --- | --- | --- |
|  | [CEFReader](/user-guide/data-integration/openflow/controllers/cefreader) | Parses CEF (Common Event Format) events, returning each row as a record. |
|  | [ConfluentEncodedSchemaReferenceReader](/user-guide/data-integration/openflow/controllers/confluentencodedschemareferencereader) | Reads Schema Identifier according to Confluent encoding as a header consisting of a byte marker and an integer represented as four bytes |
|  | [ConfluentEncodedSchemaReferenceWriter](/user-guide/data-integration/openflow/controllers/confluentencodedschemareferencewriter) | Writes Schema Identifier according to Confluent encoding as a header consisting of a byte marker and an integer represented as four bytes |
|  | [ConfluentProtobufMessageNameResolver](/user-guide/data-integration/openflow/controllers/confluentprotobufmessagenameresolver) | Resolves Protobuf message names from Confluent Schema Registry wire format by decoding message indexes and looking up the fully qualified name in the schema definition For Confluent wire format reference see: <https://docs>. |
|  | [ConfluentSchemaRegistry](/user-guide/data-integration/openflow/controllers/confluentschemaregistry) | Provides a Schema Registry that interacts with the Confluent Schema Registry so that those Schemas that are stored in the Confluent Schema Registry can be used in NiFi. |
|  | [CSVReader](/user-guide/data-integration/openflow/controllers/csvreader) | Parses CSV-formatted data, returning each row in the CSV file as a separate record. |
|  | [CSVRecordLookupService](/user-guide/data-integration/openflow/controllers/csvrecordlookupservice) | A reloadable CSV file-based lookup service. |
|  | [CSVRecordSetWriter](/user-guide/data-integration/openflow/controllers/csvrecordsetwriter) | Writes the contents of a RecordSet as CSV data. |

Expand

Show lessSee more

## D

|  | Controller | Description |
| --- | --- | --- |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DatabaseLookup](/user-guide/data-integration/openflow/controllers/databaselookup) | A Lookup Service that allows for enrichment with a database using a user-specified SQL statement. |
|  | [DatabaseRecordLookupService](/user-guide/data-integration/openflow/controllers/databaserecordlookupservice) | A relational-database-based lookup service. |
|  | [DatabaseRecordSink](/user-guide/data-integration/openflow/controllers/databaserecordsink) | Provides a service to write records using a configured database connection. |
|  | [DBCPConnectionPool](/user-guide/data-integration/openflow/controllers/dbcpconnectionpool) | Provides Database Connection Pooling Service. |
|  | [DBCPConnectionPoolLookup](/user-guide/data-integration/openflow/controllers/dbcpconnectionpoollookup) | Provides a DBCPService that can be used to dynamically select another DBCPService. |
|  | [DeveloperBoxClientService](/user-guide/data-integration/openflow/controllers/developerboxclientservice) | Provides Box client objects through which Box API calls can be used. |
|  | [DistributedMapCacheLookupService](/user-guide/data-integration/openflow/controllers/distributedmapcachelookupservice) | Lets you choose a distributed map cache client to retrieve the value associated to a key. |

Expand

Show lessSee more

## E

|  | Controller | Description |
| --- | --- | --- |
|  | [ElasticSearchClientServiceImpl](/user-guide/data-integration/openflow/controllers/elasticsearchclientserviceimpl) | A controller service for accessing an Elasticsearch client, using the Elasticsearch (low-level) REST Client. |
|  | [ElasticSearchLookupService](/user-guide/data-integration/openflow/controllers/elasticsearchlookupservice) | Lookup a record from Elasticsearch Server associated with the specified document ID. |
|  | [ElasticSearchStringLookupService](/user-guide/data-integration/openflow/controllers/elasticsearchstringlookupservice) | Lookup a string value from Elasticsearch Server associated with the specified document ID. |
|  | [EmailRecordSink](/user-guide/data-integration/openflow/controllers/emailrecordsink) | Provides a RecordSinkService that can be used to send records in email using the specified writer for formatting. |
|  | [EmbeddedHazelcastCacheManager](/user-guide/data-integration/openflow/controllers/embeddedhazelcastcachemanager) | A service that runs embedded Hazelcast and provides cache instances backed by that. |
|  | [ExcelReader](/user-guide/data-integration/openflow/controllers/excelreader) | Parses a Microsoft Excel document returning each row in each sheet as a separate record. |
|  | [ExternalHazelcastCacheManager](/user-guide/data-integration/openflow/controllers/externalhazelcastcachemanager) | A service that provides cache instances backed by Hazelcast running outside of NiFi. |

Expand

Show lessSee more

## F

|  | Controller | Description |
| --- | --- | --- |
|  | [FreeFormTextRecordSetWriter](/user-guide/data-integration/openflow/controllers/freeformtextrecordsetwriter) | Writes the contents of a RecordSet as free-form text. |

Expand

Show lessSee more

## G

|  | Controller | Description |
| --- | --- | --- |
|  | [GCPCredentialsControllerService](/user-guide/data-integration/openflow/controllers/gcpcredentialscontrollerservice) | Defines credentials for Google Cloud Platform processors. |
|  | [GCSFileResourceService](/user-guide/data-integration/openflow/controllers/gcsfileresourceservice) | Provides a Google Compute Storage (GCS) file resource for other components. |
|  | [GrokReader](/user-guide/data-integration/openflow/controllers/grokreader) | Provides a mechanism for reading unstructured text data, such as log files, and structuring the data so that it can be processed. |

Expand

Show lessSee more

## H

|  | Controller | Description |
| --- | --- | --- |
|  | [HazelcastMapCacheClient](/user-guide/data-integration/openflow/controllers/hazelcastmapcacheclient) | An implementation of DistributedMapCacheClient that uses Hazelcast as the backing cache. |
|  | [HikariCPConnectionPool](/user-guide/data-integration/openflow/controllers/hikaricpconnectionpool) | Provides Database Connection Pooling Service based on HikariCP. |
|  | [HttpRecordSink](/user-guide/data-integration/openflow/controllers/httprecordsink) | Format and send Records to a configured uri using HTTP post. |

Expand

Show lessSee more

## I

|  | Controller | Description |
| --- | --- | --- |
|  | [IPLookupService](/user-guide/data-integration/openflow/controllers/iplookupservice) | A lookup service that provides several types of enrichment information for IP addresses. |

Expand

Show lessSee more

## J

|  | Controller | Description |
| --- | --- | --- |
|  | [JettyWebSocketClient](/user-guide/data-integration/openflow/controllers/jettywebsocketclient) | Implementation of WebSocketClientService. |
|  | [JettyWebSocketServer](/user-guide/data-integration/openflow/controllers/jettywebsocketserver) | Implementation of WebSocketServerService. |
|  | [JMSConnectionFactoryProvider](/user-guide/data-integration/openflow/controllers/jmsconnectionfactoryprovider) | Provides a generic service to create vendor specific javax. |
|  | [JndiJmsConnectionFactoryProvider](/user-guide/data-integration/openflow/controllers/jndijmsconnectionfactoryprovider) | Provides a service to lookup an existing JMS ConnectionFactory using the Java Naming and Directory Interface (JNDI). |
|  | [JsonConfigBasedBoxClientService](/user-guide/data-integration/openflow/controllers/jsonconfigbasedboxclientservice) | Provides Box client objects through which Box API calls can be used. |
|  | [JsonPathReader](/user-guide/data-integration/openflow/controllers/jsonpathreader) | Parses JSON records and evaluates user-defined JSON Path ‘s against each JSON object. |
|  | [JsonRecordSetWriter](/user-guide/data-integration/openflow/controllers/jsonrecordsetwriter) | Writes the results of a RecordSet as either a JSON Array or one JSON object per line. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [JsonTableColumnFilter](/user-guide/data-integration/openflow/controllers/jsontablecolumnfilter) | Provides a table column filter based on a JSON configuration. |
|  | [JsonTreeReader](/user-guide/data-integration/openflow/controllers/jsontreereader) | Parses JSON into individual Record objects. |
|  | [JWTBearerOAuth2AccessTokenProvider](/user-guide/data-integration/openflow/controllers/jwtbeareroauth2accesstokenprovider) | Provides OAuth 2. |

Expand

Show lessSee more

## K

|  | Controller | Description |
| --- | --- | --- |
|  | [Kafka3ConnectionService](/user-guide/data-integration/openflow/controllers/kafka3connectionservice) | Provides and manages connections to Kafka Brokers for producer or consumer operations. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [Kafka3ConnectionService](/user-guide/data-integration/openflow/controllers/kafka3connectionservice) | Provides and manages connections to Kafka Brokers for producer or consumer operations. |

Expand

Show lessSee more

## L

|  | Controller | Description |
| --- | --- | --- |
|  | [LoggingRecordSink](/user-guide/data-integration/openflow/controllers/loggingrecordsink) | Provides a RecordSinkService that can be used to log records to the application log (nifi-app. |

Expand

Show lessSee more

## M

|  | Controller | Description |
| --- | --- | --- |
|  | [MapCacheClientService](/user-guide/data-integration/openflow/controllers/mapcacheclientservice) | Provides the ability to communicate with a MapCacheServer. |
|  | [MapCacheServer](/user-guide/data-integration/openflow/controllers/mapcacheserver) | Provides a map (key/value) cache that can be accessed over a socket. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [MicrosoftClientCertificateOAuth2TokenProvider](/user-guide/data-integration/openflow/controllers/microsoftclientcertificateoauth2tokenprovider) | Provides OAuth2 access tokens for the Microsoft Graph API using client\_credentials with a client certificate. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [MicrosoftGraphAuthenticationProvider](/user-guide/data-integration/openflow/controllers/microsoftgraphauthenticationprovider) | Provides authentication for the Microsoft Graph API, which can be used for interacting with Microsoft 365 services. |
|  | [MongoDBControllerService](/user-guide/data-integration/openflow/controllers/mongodbcontrollerservice) | Provides a controller service that configures a connection to MongoDB and provides access to that connection to other Mongo-related components. |
|  | [MongoDBLookupService](/user-guide/data-integration/openflow/controllers/mongodblookupservice) | Provides a lookup service based around MongoDB. |

Expand

Show lessSee more

## P

|  | Controller | Description |
| --- | --- | --- |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ParquetIcebergWriter](/user-guide/data-integration/openflow/controllers/parqueticebergwriter) | Provides record serialization for Apache Iceberg using Apache Parquet formatting |
|  | [PEMEncodedSSLContextProvider](/user-guide/data-integration/openflow/controllers/pemencodedsslcontextprovider) | SSLContext Provider configurable using PEM Private Key and Certificate files. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PolarisIcebergCatalog](/user-guide/data-integration/openflow/controllers/polarisicebergcatalog) | Provides Apache Iceberg integration with Apache Polaris Catalog access over REST HTTP |
|  | [PropertiesFileLookupService](/user-guide/data-integration/openflow/controllers/propertiesfilelookupservice) | A reloadable properties file-based lookup service |
|  | [ProtobufReader](/user-guide/data-integration/openflow/controllers/protobufreader) | Parses a Protocol Buffers message from binary format. |

Expand

Show lessSee more

## R

|  | Controller | Description |
| --- | --- | --- |
|  | [ReaderLookup](/user-guide/data-integration/openflow/controllers/readerlookup) | Provides a RecordReaderFactory that can be used to dynamically select another RecordReaderFactory. |
|  | [RecordSetWriterLookup](/user-guide/data-integration/openflow/controllers/recordsetwriterlookup) | Provides a RecordSetWriterFactory that can be used to dynamically select another RecordSetWriterFactory. |
|  | [RecordSinkServiceLookup](/user-guide/data-integration/openflow/controllers/recordsinkservicelookup) | Provides a RecordSinkService that can be used to dynamically select another RecordSinkService. |
|  | [RedisConnectionPoolService](/user-guide/data-integration/openflow/controllers/redisconnectionpoolservice) | A service that provides connections to Redis. |
|  | [RedisDistributedMapCacheClientService](/user-guide/data-integration/openflow/controllers/redisdistributedmapcacheclientservice) | An implementation of DistributedMapCacheClient that uses Redis as the backing cache. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [RemoveFieldRecordReader](/user-guide/data-integration/openflow/controllers/removefieldrecordreader) | A wrapper for a RecordReaderFactory that supports filtering out specified fields from NiFi Records. |
|  | [RestLookupService](/user-guide/data-integration/openflow/controllers/restlookupservice) | Use a REST service to look up values. |

Expand

Show lessSee more

## S

|  | Controller | Description |
| --- | --- | --- |
|  | [S3FileResourceService](/user-guide/data-integration/openflow/controllers/s3fileresourceservice) | Provides an Amazon Web Services (AWS) S3 file resource for other components. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SalesforceDataCloudOAuthTokenProvider](/user-guide/data-integration/openflow/controllers/salesforcedatacloudoauthtokenprovider) | Retrieves an OAuth2 access token from Salesforce using the configured OAuth2 Access Token Provider and exchanges the token for a Data Cloud API token. |
|  | [ScriptedLookupService](/user-guide/data-integration/openflow/controllers/scriptedlookupservice) | Allows the user to provide a scripted LookupService instance in order to enrich records from an incoming flow file. |
|  | [ScriptedReader](/user-guide/data-integration/openflow/controllers/scriptedreader) | Allows the user to provide a scripted RecordReaderFactory instance in order to read/parse/generate records from an incoming flow file. |
|  | [ScriptedRecordSetWriter](/user-guide/data-integration/openflow/controllers/scriptedrecordsetwriter) | Allows the user to provide a scripted RecordSetWriterFactory instance in order to write records to an outgoing flow file. |
|  | [ScriptedRecordSink](/user-guide/data-integration/openflow/controllers/scriptedrecordsink) | Allows the user to provide a scripted RecordSinkService instance in order to transmit records to the desired target. |
|  | [SetCacheClientService](/user-guide/data-integration/openflow/controllers/setcacheclientservice) | Provides the ability to communicate with a SetCacheServer. |
|  | [SetCacheServer](/user-guide/data-integration/openflow/controllers/setcacheserver) | Provides a set (collection of unique values) cache that can be accessed over a socket. |
|  | [SimpleCsvFileLookupService](/user-guide/data-integration/openflow/controllers/simplecsvfilelookupservice) | A reloadable CSV file-based lookup service. |
|  | [SimpleDatabaseLookupService](/user-guide/data-integration/openflow/controllers/simpledatabaselookupservice) | A relational-database-based lookup service. |
|  | [SimpleKeyValueLookupService](/user-guide/data-integration/openflow/controllers/simplekeyvaluelookupservice) | Allows users to add key/value pairs as User-defined Properties. |
|  | [SimpleRedisDistributedMapCacheClientService](/user-guide/data-integration/openflow/controllers/simpleredisdistributedmapcacheclientservice) | An implementation of DistributedMapCacheClient that uses Redis as the backing cache. |
|  | [SimpleScriptedLookupService](/user-guide/data-integration/openflow/controllers/simplescriptedlookupservice) | Allows the user to provide a scripted LookupService instance in order to enrich records from an incoming flow file. |
|  | [SlackRecordSink](/user-guide/data-integration/openflow/controllers/slackrecordsink) | Format and send Records to a configured Channel using the Slack Post Message API. |
|  | [SmbjClientProviderService](/user-guide/data-integration/openflow/controllers/smbjclientproviderservice) | Provides access to SMB Sessions with shared authentication credentials. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SnowflakeConnectionService](/user-guide/data-integration/openflow/controllers/snowflakeconnectionservice) | Provides pooled database connections to Snowflake services |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SnowflakeDatabaseDialectService](/user-guide/data-integration/openflow/controllers/snowflakedatabasedialectservice) | Database Dialect Service supporting Snowflake. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SnowflakeSignJWTService](/user-guide/data-integration/openflow/controllers/snowflakesignjwtservice) | Provides OAuth2 access token using a JWT signed with a secret stored in Snowflake. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SnowflakeTableSchemaRegistry](/user-guide/data-integration/openflow/controllers/snowflaketableschemaregistry) | Uses Snowflake tables as the source of schema — utilises Snowpipe Streaming REST API. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardAnthropicLLMService](/user-guide/data-integration/openflow/controllers/standardanthropicllmservice) | A Controller Service that provides integration with Anthropic’s Claude AI models through their Messages API. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardAtlassianRequestRateManager](/user-guide/data-integration/openflow/controllers/standardatlassianrequestratemanager) | Provides rate limiting coordination for Atlassian API calls across processors to prevent cascading rate limit issues. |
|  | [StandardAzureCredentialsControllerService](/user-guide/data-integration/openflow/controllers/standardazurecredentialscontrollerservice) | Provide credentials to use with an Azure client. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardConfluenceClientService](/user-guide/data-integration/openflow/controllers/standardconfluenceclientservice) | Provides connection service to Confluence APIs |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardDatabricksWorkspaceClientService](/user-guide/data-integration/openflow/controllers/standarddatabricksworkspaceclientservice) | Databricks client. |
|  | [StandardDropboxCredentialService](/user-guide/data-integration/openflow/controllers/standarddropboxcredentialservice) | Defines credentials for Dropbox processors. |
|  | [StandardFileResourceService](/user-guide/data-integration/openflow/controllers/standardfileresourceservice) | Provides a file resource for other components. |
|  | [StandardHashiCorpVaultClientService](/user-guide/data-integration/openflow/controllers/standardhashicorpvaultclientservice) | A controller service for interacting with HashiCorp Vault. |
|  | [StandardHttpContextMap](/user-guide/data-integration/openflow/controllers/standardhttpcontextmap) | Provides the ability to store and retrieve HTTP requests and responses external to a Processor, so that multiple Processors can interact with the same HTTP request. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardHubSpotClientService](/user-guide/data-integration/openflow/controllers/standardhubspotclientservice) | HubSpot Controller Service to integrate with HubSpot HTTP api. |
|  | [StandardJsonSchemaRegistry](/user-guide/data-integration/openflow/controllers/standardjsonschemaregistry) | Provides a service for registering and accessing JSON schemas. |
|  | [StandardKustoIngestService](/user-guide/data-integration/openflow/controllers/standardkustoingestservice) | Sends batches of flowfile content or stream flowfile content to an Azure ADX cluster. |
|  | [StandardKustoQueryService](/user-guide/data-integration/openflow/controllers/standardkustoqueryservice) | Standard implementation of Kusto Query Service for Azure Data Explorer |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardMilvusConnectionService](/user-guide/data-integration/openflow/controllers/standardmilvusconnectionservice) | Provides connection service to a Milvus instance |
|  | [StandardOauth2AccessTokenProvider](/user-guide/data-integration/openflow/controllers/standardoauth2accesstokenprovider) | Provides OAuth 2. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardOCRService](/user-guide/data-integration/openflow/controllers/standardocrservice) | Provides integration to Openflow OCR Service |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardOpenAILLMService](/user-guide/data-integration/openflow/controllers/standardopenaillmservice) | A Controller Service that provides integration with OpenAI’s Chat Completion API. |
|  | [StandardPGPPrivateKeyService](/user-guide/data-integration/openflow/controllers/standardpgpprivatekeyservice) | PGP Private Key Service provides Private Keys loaded from files or properties |
|  | [StandardPGPPublicKeyService](/user-guide/data-integration/openflow/controllers/standardpgppublickeyservice) | PGP Public Key Service providing Public Keys loaded from files |
|  | [StandardPrivateKeyService](/user-guide/data-integration/openflow/controllers/standardprivatekeyservice) | Private Key Service provides access to a Private Key loaded from configured sources |
|  | [StandardProtobufReader](/user-guide/data-integration/openflow/controllers/standardprotobufreader) | Parses Protocol Buffers messages from binary format into NiFi Records. |
|  | [StandardProxyConfigurationService](/user-guide/data-integration/openflow/controllers/standardproxyconfigurationservice) | Provides a set of configurations for different NiFi components to use a proxy server. |
|  | [StandardRestrictedSSLContextService](/user-guide/data-integration/openflow/controllers/standardrestrictedsslcontextservice) | Restricted implementation of the SSLContextService. |
|  | [StandardS3EncryptionService](/user-guide/data-integration/openflow/controllers/standards3encryptionservice) | Adds configurable encryption to S3 Put and S3 Fetch operations. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardSalesforceBulkJobsStateService](/user-guide/data-integration/openflow/controllers/standardsalesforcebulkjobsstateservice) | Stores Salesforce Bulk Jobs state per object type at cluster scope |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardSalesforceClientService](/user-guide/data-integration/openflow/controllers/standardsalesforceclientservice) | Provides connection service to Salesforce APIs |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardSalesforceDataCloudClientService](/user-guide/data-integration/openflow/controllers/standardsalesforcedatacloudclientservice) | Provides connection service to Salesforce Data Cloud APIs |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardSlackRateLimiterService](/user-guide/data-integration/openflow/controllers/standardslackratelimiterservice) | Provides rate limiting coordination for Slack API calls across processors to prevent cascading rate limit issues |
|  | [StandardSSLContextService](/user-guide/data-integration/openflow/controllers/standardsslcontextservice) | Standard implementation of the SSLContextService. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardTableStateService](/user-guide/data-integration/openflow/controllers/standardtablestateservice) | A controller Service that provides and manages table state. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StandardVectaraClientService](/user-guide/data-integration/openflow/controllers/standardvectaraclientservice) | Vectara Controller Service to integrate with Vectara HTTP Api. |
|  | [StandardWebClientServiceProvider](/user-guide/data-integration/openflow/controllers/standardwebclientserviceprovider) | Web Client Service Provider with support for configuring standard HTTP connection properties |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [StateManagedCdcSchemaRegistry](/user-guide/data-integration/openflow/controllers/statemanagedcdcschemaregistry) | Uses the in-built NiFi State Management to store the hashes of table schemas. |
|  | [Syslog5424Reader](/user-guide/data-integration/openflow/controllers/syslog5424reader) | Provides a mechanism for reading RFC 5424 compliant Syslog data, such as log files, and structuring the data so that it can be processed. |
|  | [SyslogReader](/user-guide/data-integration/openflow/controllers/syslogreader) | Attempts to parses the contents of a Syslog message in accordance to RFC5424 and RFC3164. |

Expand

Show lessSee more

## U

|  | Controller | Description |
| --- | --- | --- |
|  | [UDPEventRecordSink](/user-guide/data-integration/openflow/controllers/udpeventrecordsink) | Format and send Records as UDP Datagram Packets to a configurable destination |

Expand

Show lessSee more

## V

|  | Controller | Description |
| --- | --- | --- |
|  | [VolatileSchemaCache](/user-guide/data-integration/openflow/controllers/volatileschemacache) | Provides a Schema Cache that evicts elements based on a Least-Recently-Used algorithm. |

Expand

Show lessSee more

## W

|  | Controller | Description |
| --- | --- | --- |
|  | [WindowsEventLogReader](/user-guide/data-integration/openflow/controllers/windowseventlogreader) | Reads Windows Event Log data as XML content having been generated by ConsumeWindowsEventLog, ParseEvtx, etc. |

Expand

Show lessSee more

## X

|  | Controller | Description |
| --- | --- | --- |
|  | [XMLFileLookupService](/user-guide/data-integration/openflow/controllers/xmlfilelookupservice) | A reloadable XML file-based lookup service. |
|  | [XMLReader](/user-guide/data-integration/openflow/controllers/xmlreader) | Reads XML content and creates Record objects. |
|  | [XMLRecordSetWriter](/user-guide/data-integration/openflow/controllers/xmlrecordsetwriter) | Writes a RecordSet to XML. |

Expand

Show lessSee more

## Y

|  | Controller | Description |
| --- | --- | --- |
|  | [YamlTreeReader](/user-guide/data-integration/openflow/controllers/yamltreereader) | Parses YAML into individual Record objects. |

Expand

Show lessSee more
