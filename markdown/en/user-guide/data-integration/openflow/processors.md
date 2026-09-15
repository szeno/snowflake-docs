# All processors (alphabetical)

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic provides a list of all Snowflake openflow processors in alphabetical order.
The list includes:

> - The name of each processor
> - A summary of each processor

## A

|  | Processor | Description |
| --- | --- | --- |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [AbortQueryJob](/user-guide/data-integration/openflow/processors/abortqueryjob) | Aborts a Query Job in Salesforce using the Bulk API 2. |
|  | [AttributesToCSV](/user-guide/data-integration/openflow/processors/attributestocsv) | Generates a CSV representation of the input FlowFile Attributes. |
|  | [AttributesToJSON](/user-guide/data-integration/openflow/processors/attributestojson) | Generates a JSON representation of the input FlowFile Attributes. |

Expand

Show lessSee more

## C

|  | Processor | Description |
| --- | --- | --- |
|  | [CalculateRecordStats](/user-guide/data-integration/openflow/processors/calculaterecordstats) | Counts the number of Records in a record set, optionally counting the number of elements per category, where the categories are defined by user-defined properties. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CaptureChangeMySQL](/user-guide/data-integration/openflow/processors/capturechangemysql) | Reads CDC events from a MySQL database. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CaptureChangePostgreSQL](/user-guide/data-integration/openflow/processors/capturechangepostgresql) | Reads CDC events from a PostgreSQL database. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CaptureChangeSqlServer](/user-guide/data-integration/openflow/processors/capturechangesqlserver) | Reads CDC events from a SQL Server database. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CaptureGoogleDriveChanges](/user-guide/data-integration/openflow/processors/capturegoogledrivechanges) | Captures changes to a Shared Google Drive and emits a FlowFile for each change that occurs. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CaptureMicrosoft365GroupsChanges](/user-guide/data-integration/openflow/processors/capturemicrosoft365groupschanges) | Captures Microsoft365 groups changes and emits a FlowFile for each change that occurs. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CaptureSharepointChanges](/user-guide/data-integration/openflow/processors/capturesharepointchanges) | Captures changes from a Sharepoint Document Library and emits a FlowFile for each change that occurs. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CheckMetaAdsReportReadiness](/user-guide/data-integration/openflow/processors/checkmetaadsreportreadiness) | Processor checking if the Meta Ads report is ready for download. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ChunkRecordText](/user-guide/data-integration/openflow/processors/chunkrecordtext) | Chunks text with options for recursively splitting by delimiters and max character length. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ChunkText](/user-guide/data-integration/openflow/processors/chunktext) | Chunks text with options for recursively splitting by delimiters and max character length. |
|  | [CompressContent](/user-guide/data-integration/openflow/processors/compresscontent) | Compresses or decompresses the contents of FlowFiles using a user-specified compression algorithm and updates the mime. |
|  | [ConnectWebSocket](/user-guide/data-integration/openflow/processors/connectwebsocket) | Acts as a WebSocket client endpoint to interact with a remote WebSocket server. |
|  | [ConsumeAMQP](/user-guide/data-integration/openflow/processors/consumeamqp) | Consumes AMQP Messages from an AMQP Broker using the AMQP 0. |
|  | [ConsumeAzureEventHub](/user-guide/data-integration/openflow/processors/consumeazureeventhub) | Receives messages from Microsoft Azure Event Hubs with checkpointing to ensure consistent event processing. |
|  | [ConsumeBoxEnterpriseEvents](/user-guide/data-integration/openflow/processors/consumeboxenterpriseevents) | Consumes Enterprise Events from Box admin\_logs\_streaming Stream Type. |
|  | [ConsumeBoxEvents](/user-guide/data-integration/openflow/processors/consumeboxevents) | Consumes all events from Box. |
|  | [ConsumeElasticsearch](/user-guide/data-integration/openflow/processors/consumeelasticsearch) | A processor that repeatedly runs a paginated query against a field using a Range query to consume new Documents from an Elasticsearch index/query. |
|  | [ConsumeGCPubSub](/user-guide/data-integration/openflow/processors/consumegcpubsub) | Consumes messages from the configured Google Cloud PubSub subscription. |
|  | [ConsumeIMAP](/user-guide/data-integration/openflow/processors/consumeimap) | Consumes messages from Email Server using IMAP protocol. |
|  | [ConsumeJMS](/user-guide/data-integration/openflow/processors/consumejms) | Consumes JMS Message of type BytesMessage, TextMessage, ObjectMessage, MapMessage or StreamMessage transforming its content to a FlowFile and transitioning it to ‘success’ relationship. |
|  | [ConsumeKafka](/user-guide/data-integration/openflow/processors/consumekafka) | Consumes messages from Apache Kafka Consumer API. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ConsumeKafka](/user-guide/data-integration/openflow/processors/consumekafka) | Consumes messages from Apache Kafka Consumer API. |
|  | [ConsumeKinesisStream](/user-guide/data-integration/openflow/processors/consumekinesisstream) | Reads data from the specified AWS Kinesis stream and outputs a FlowFile for every processed Record (raw) or a FlowFile for a batch of processed records if a Record Reader and Record Writer are configured. |
|  | [ConsumeMQTT](/user-guide/data-integration/openflow/processors/consumemqtt) | Subscribes to a topic and receives messages from an MQTT broker |
|  | [ConsumePOP3](/user-guide/data-integration/openflow/processors/consumepop3) | Consumes messages from Email Server using POP3 protocol. |
|  | [ConsumeSlack](/user-guide/data-integration/openflow/processors/consumeslack) | Retrieves messages from one or more configured Slack channels. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ConsumeSlackConversation](/user-guide/data-integration/openflow/processors/consumeslackconversation) | Retrieves messages from Slack conversations available to the App. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ConsumeSlackHistory](/user-guide/data-integration/openflow/processors/consumeslackhistory) | Fetches historical messages from all Slack channels available to the App. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ConsumeSnowflakeStream](/user-guide/data-integration/openflow/processors/consumesnowflakestream) | Fetches data from a Snowflake stream and writes it to a FlowFile. |
|  | [ConsumeTwitter](/user-guide/data-integration/openflow/processors/consumetwitter) | Streams tweets from Twitter’s streaming API v2. |
|  | [ControlRate](/user-guide/data-integration/openflow/processors/controlrate) | Controls the rate at which data is transferred to follow-on processors. |
|  | [ConvertCharacterSet](/user-guide/data-integration/openflow/processors/convertcharacterset) | Converts a FlowFile’s content from one character set to another |
|  | [ConvertRecord](/user-guide/data-integration/openflow/processors/convertrecord) | Converts records from one data format to another using configured Record Reader and Record Write Controller Services. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ConvertToJournalSchema](/user-guide/data-integration/openflow/processors/converttojournalschema) | Converts the incoming database schema into the appropriate schema for a Snowflake CDC Journal table. |
|  | [CopyAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/copyazureblobstorage_v12) | Copies a blob in Azure Blob Storage from one account/container to another. |
|  | [CopyS3Object](/user-guide/data-integration/openflow/processors/copys3object) | Copies a file from one bucket and key to another in AWS S3 |
|  | [CountText](/user-guide/data-integration/openflow/processors/counttext) | Counts various metrics on incoming text. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateAmazonAdsReport](/user-guide/data-integration/openflow/processors/createamazonadsreport) | Processor which creates report configuration for Amazon Ads connector. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateAzureOpenAiEmbeddings](/user-guide/data-integration/openflow/processors/createazureopenaiembeddings) | Uses Azure OpenAI to create embeddings for text. |
|  | [CreateBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/createboxfilemetadatainstance) | Creates a metadata instance for a Box file using a specified template with values from the flowFile content. |
|  | [CreateBoxMetadataTemplate](/user-guide/data-integration/openflow/processors/createboxmetadatatemplate) | Creates a Box metadata template using field specifications from the flowFile content. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateCohereEmbeddings](/user-guide/data-integration/openflow/processors/createcohereembeddings) | Uses Cohere to create embeddings for text. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateMetaAdsReport](/user-guide/data-integration/openflow/processors/createmetaadsreport) | Processor which creates report configuration for Meta Ads connector. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateOpenAiEmbeddings](/user-guide/data-integration/openflow/processors/createopenaiembeddings) | Uses OpenAI to create embeddings for text. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateSnowflakeEmbeddings](/user-guide/data-integration/openflow/processors/createsnowflakeembeddings) | Create vector embeddings using Snowflake Cortex Large Language Model functions |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [CreateVertexAIEmbeddings](/user-guide/data-integration/openflow/processors/createvertexaiembeddings) | Uses VertexAI to create embeddings for text. |
|  | [CryptographicHashContent](/user-guide/data-integration/openflow/processors/cryptographichashcontent) | Calculates a cryptographic hash value for the flowfile content using the given algorithm and writes it to an output attribute. |

Expand

Show lessSee more

## D

|  | Processor | Description |
| --- | --- | --- |
|  | [DebugFlow](/user-guide/data-integration/openflow/processors/debugflow) | The DebugFlow processor aids testing and debugging the FlowFile framework by allowing various responses to be explicitly triggered in response to the receipt of a FlowFile or a timer event without a FlowFile if using timer or cron based scheduling. |
|  | [DecryptContentAge](/user-guide/data-integration/openflow/processors/decryptcontentage) | Decrypt content using the age-encryption. |
|  | [DecryptContentPGP](/user-guide/data-integration/openflow/processors/decryptcontentpgp) | Decrypt contents of OpenPGP messages. |
|  | [DeduplicateRecord](/user-guide/data-integration/openflow/processors/deduplicaterecord) | This processor de-duplicates individual records within a record set. |
|  | [DeleteAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/deleteazureblobstorage_v12) | Deletes the specified blob from Azure Blob Storage. |
|  | [DeleteAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/deleteazuredatalakestorage) | Deletes the provided file from Azure Data Lake Storage |
|  | [DeleteBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/deleteboxfilemetadatainstance) | Deletes a metadata instance from a Box file using the specified template key |
|  | [DeleteByQueryElasticsearch](/user-guide/data-integration/openflow/processors/deletebyqueryelasticsearch) | Delete from an Elasticsearch index using a query. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DeleteDBFSResource](/user-guide/data-integration/openflow/processors/deletedbfsresource) | Delete a DBFS files and directories. |
|  | [DeleteDynamoDB](/user-guide/data-integration/openflow/processors/deletedynamodb) | Deletes a document from DynamoDB based on hash and range key. |
|  | [DeleteFile](/user-guide/data-integration/openflow/processors/deletefile) | Deletes a file from the filesystem. |
|  | [DeleteGCSObject](/user-guide/data-integration/openflow/processors/deletegcsobject) | Deletes objects from a Google Cloud Bucket. |
|  | [DeleteGridFS](/user-guide/data-integration/openflow/processors/deletegridfs) | Deletes a file from GridFS using a file name or a query. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DeleteMilvus](/user-guide/data-integration/openflow/processors/deletemilvus) | Deletes vectors from Milvus database from a collection by ID. |
|  | [DeleteMongo](/user-guide/data-integration/openflow/processors/deletemongo) | Executes a delete query against a MongoDB collection. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DeletePinecone](/user-guide/data-integration/openflow/processors/deletepinecone) | Deletes vectors from a Pinecone index. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DeleteQueryJob](/user-guide/data-integration/openflow/processors/deletequeryjob) | Deletes a Query Job in Salesforce using the Bulk API 2. |
|  | [DeleteS3Object](/user-guide/data-integration/openflow/processors/deletes3object) | Deletes a file from an Amazon S3 Bucket. |
|  | [DeleteSFTP](/user-guide/data-integration/openflow/processors/deletesftp) | Deletes a file residing on an SFTP server. |
|  | [DeleteSQS](/user-guide/data-integration/openflow/processors/deletesqs) | Deletes a message from an Amazon Simple Queuing Service Queue |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DeleteUnityCatalogResource](/user-guide/data-integration/openflow/processors/deleteunitycatalogresource) | Delete a Unity Catalog file or directory. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DescribeDataShare](/user-guide/data-integration/openflow/processors/describedatashare) | Describe the specified data share metadata in Salesforce Data Cloud. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [DescribeSFDCObject](/user-guide/data-integration/openflow/processors/describesfdcobject) | Describe the specified object metadata in Salesforce. |
|  | [DetectDuplicate](/user-guide/data-integration/openflow/processors/detectduplicate) | Caches a value, computed from FlowFile attributes, for each incoming FlowFile and determines if the cached value has already been seen. |
|  | [DistributeLoad](/user-guide/data-integration/openflow/processors/distributeload) | Distributes FlowFiles to downstream processors based on a Distribution Strategy. |
|  | [DuplicateFlowFile](/user-guide/data-integration/openflow/processors/duplicateflowfile) | Intended for load testing, this processor will create the configured number of copies of each incoming FlowFile. |

Expand

Show lessSee more

## E

|  | Processor | Description |
| --- | --- | --- |
|  | [EncodeContent](/user-guide/data-integration/openflow/processors/encodecontent) | Encode or decode the contents of a FlowFile using Base64, Base32, or hex encoding schemes |
|  | [EncryptContentAge](/user-guide/data-integration/openflow/processors/encryptcontentage) | Encrypt content using the age-encryption. |
|  | [EncryptContentPGP](/user-guide/data-integration/openflow/processors/encryptcontentpgp) | Encrypt contents using OpenPGP. |
|  | [EnforceOrder](/user-guide/data-integration/openflow/processors/enforceorder) | Enforces expected ordering of FlowFiles that belong to the same data group within a single node. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [EnrichAttributes](/user-guide/data-integration/openflow/processors/enrichattributes) | Looks up a value using the configured Lookup Service and adds the results to the FlowFile as one or more attributes. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [EnrichCdcStream](/user-guide/data-integration/openflow/processors/enrichcdcstream) | Enriches incoming FlowFiles that come from CaptureChangePostgreSQL, etc. |
|  | [EvaluateJsonPath](/user-guide/data-integration/openflow/processors/evaluatejsonpath) | Evaluates one or more JsonPath expressions against the content of a FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [EvaluateRagAnswerCorrectness](/user-guide/data-integration/openflow/processors/evaluateraganswercorrectness) | Evaluates the correctness of generated answers in a Retrieval-Augmented Generation (RAG) context by computing metrics such as F1 score, cosine similarity, and answer correctness. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [EvaluateRagFaithfulness](/user-guide/data-integration/openflow/processors/evaluateragfaithfulness) | Evaluates the faithfulness of generated answers in a Retrieval-Augmented Generation (RAG) system by analyzing responses using an LLM (e. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [EvaluateRagRetrieval](/user-guide/data-integration/openflow/processors/evaluateragretrieval) | Calculates retrieval metrics (Precision@N, Recall@N, FScore@N, MAP@N, MRR) for a RAG system using an LLM as a judge. |
|  | [EvaluateXPath](/user-guide/data-integration/openflow/processors/evaluatexpath) | Evaluates one or more XPaths against the content of a FlowFile. |
|  | [EvaluateXQuery](/user-guide/data-integration/openflow/processors/evaluatexquery) | Evaluates one or more XQueries against the content of a FlowFile. |
|  | [ExecuteGroovyScript](/user-guide/data-integration/openflow/processors/executegroovyscript) | Experimental Extended Groovy script processor. |
|  | [ExecuteProcess](/user-guide/data-integration/openflow/processors/executeprocess) | Runs an operating system command specified by the user and writes the output of that command to a FlowFile. |
|  | [ExecuteScript](/user-guide/data-integration/openflow/processors/executescript) | Experimental - Executes a script given the flow file and a process session. |
|  | [ExecuteSQL](/user-guide/data-integration/openflow/processors/executesql) | Executes provided SQL select query. |
|  | [ExecuteSQLRecord](/user-guide/data-integration/openflow/processors/executesqlrecord) | Executes provided SQL select query. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ExecuteSQLStatement](/user-guide/data-integration/openflow/processors/executesqlstatement) | Executes a SQL DDL or DML Statement against a database. |
|  | [ExecuteStreamCommand](/user-guide/data-integration/openflow/processors/executestreamcommand) | The ExecuteStreamCommand processor provides a flexible way to integrate external commands and scripts into NiFi data flows. |
|  | [ExtractAvroMetadata](/user-guide/data-integration/openflow/processors/extractavrometadata) | Extracts metadata from the header of an Avro datafile. |
|  | [ExtractEmailAttachments](/user-guide/data-integration/openflow/processors/extractemailattachments) | Extract attachments from a mime formatted email file, splitting them into individual flowfiles. |
|  | [ExtractEmailHeaders](/user-guide/data-integration/openflow/processors/extractemailheaders) | Using the flowfile content as source of data, extract header from an RFC compliant email file adding the relevant attributes to the flowfile. |
|  | [ExtractGrok](/user-guide/data-integration/openflow/processors/extractgrok) | Evaluates one or more Grok Expressions against the content of a FlowFile, adding the results as attributes or replacing the content of the FlowFile with a JSON notation of the matched content |
|  | [ExtractRecordSchema](/user-guide/data-integration/openflow/processors/extractrecordschema) | Extracts the record schema from the FlowFile using the supplied Record Reader and writes it to the ‘avro. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ExtractSchemaColumns](/user-guide/data-integration/openflow/processors/extractschemacolumns) | Extracts the record schema columns from the FlowFile using the supplied Record Reader and writes it to the ‘schema. |
|  | [ExtractStructuredBoxFileMetadata](/user-guide/data-integration/openflow/processors/extractstructuredboxfilemetadata) | Extracts metadata from a Box file using Box AI. |
|  | [ExtractText](/user-guide/data-integration/openflow/processors/extracttext) | Evaluates one or more Regular Expressions against the content of a FlowFile. |

Expand

Show lessSee more

## F

|  | Processor | Description |
| --- | --- | --- |
|  | [FetchAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/fetchazureblobstorage_v12) | Retrieves the specified blob from Azure Blob Storage and writes its content to the content of the FlowFile. |
|  | [FetchAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/fetchazuredatalakestorage) | Fetch the specified file from Azure Data Lake Storage |
|  | [FetchBoxFile](/user-guide/data-integration/openflow/processors/fetchboxfile) | Fetches files from a Box Folder. |
|  | [FetchBoxFileInfo](/user-guide/data-integration/openflow/processors/fetchboxfileinfo) | Fetches metadata for files from Box and adds it to the FlowFile’s attributes. |
|  | [FetchBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/fetchboxfilemetadatainstance) | Retrieves specific metadata instance associated with a Box file using template key and scope. |
|  | [FetchBoxFileRepresentation](/user-guide/data-integration/openflow/processors/fetchboxfilerepresentation) | Fetches a Box file representation using a representation hint and writes it to the FlowFile content. |
|  | [FetchDistributedMapCache](/user-guide/data-integration/openflow/processors/fetchdistributedmapcache) | Computes cache key(s) from FlowFile attributes, for each incoming FlowFile, and fetches the value(s) from the Distributed Map Cache associated with each key. |
|  | [FetchDropbox](/user-guide/data-integration/openflow/processors/fetchdropbox) | Fetches files from Dropbox. |
|  | [FetchFile](/user-guide/data-integration/openflow/processors/fetchfile) | Reads the contents of a file from disk and streams it into the contents of an incoming FlowFile. |
|  | [FetchFTP](/user-guide/data-integration/openflow/processors/fetchftp) | Fetches the content of a file from a remote FTP server and overwrites the contents of an incoming FlowFile with the content of the remote file. |
|  | [FetchGCSObject](/user-guide/data-integration/openflow/processors/fetchgcsobject) | Fetches a file from a Google Cloud Bucket. |
|  | [FetchGoogleDrive](/user-guide/data-integration/openflow/processors/fetchgoogledrive) | Fetches files from a Google Drive Folder. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchGoogleDriveFileComments](/user-guide/data-integration/openflow/processors/fetchgoogledrivefilecomments) | Fetches comments and their replies for a Google Drive file. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchGoogleDriveMetadata](/user-guide/data-integration/openflow/processors/fetchgoogledrivemetadata) | Fetches Google Drive file metadata. |
|  | [FetchGridFS](/user-guide/data-integration/openflow/processors/fetchgridfs) | Retrieves one or more files from a GridFS bucket by file name or by a user-defined query. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchJiraFields](/user-guide/data-integration/openflow/processors/fetchjirafields) | Retrieves comprehensive metadata for all fields available in the Jira Cloud instance using the REST API v3 /field endpoint. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchJiraIssues](/user-guide/data-integration/openflow/processors/fetchjiraissues) | Fetches issues from Jira Cloud using REST API v3 with configurable search options. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchMicrosoftDataverseTable](/user-guide/data-integration/openflow/processors/fetchmicrosoftdataversetable) | Fetch records from Microsoft Dataverse Tables |
|  | [FetchS3Object](/user-guide/data-integration/openflow/processors/fetchs3object) | Retrieves the contents of an S3 Object and writes it to the content of a FlowFile |
|  | [FetchSFTP](/user-guide/data-integration/openflow/processors/fetchsftp) | Fetches the content of a file from a remote SFTP server and overwrites the contents of an incoming FlowFile with the content of the remote file. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSharepointFile](/user-guide/data-integration/openflow/processors/fetchsharepointfile) | Fetches the contents of a file from a Sharepoint Drive, optionally downloading a PDF or HTML version of the file when applicable. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSharepointMetadata](/user-guide/data-integration/openflow/processors/fetchsharepointmetadata) | For each drive item retrieves its metadata and permissions and writes them as FlowFile attributes. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSlackConversationInfo](/user-guide/data-integration/openflow/processors/fetchslackconversationinfo) | Fetches Slack conversation info and member emails |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSlackFile](/user-guide/data-integration/openflow/processors/fetchslackfile) | Downloads a file shared on Slack. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSlackMessage](/user-guide/data-integration/openflow/processors/fetchslackmessage) | Fetches data about a single Slack message |
|  | [FetchSmb](/user-guide/data-integration/openflow/processors/fetchsmb) | Fetches files from a SMB Share. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSnowflakeTableProperties](/user-guide/data-integration/openflow/processors/fetchsnowflaketableproperties) | Reads properties from a table and stores them as flow file attributes. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchSourceTableSchema](/user-guide/data-integration/openflow/processors/fetchsourcetableschema) | Fetches the table schema (i. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FetchTableSnapshot](/user-guide/data-integration/openflow/processors/fetchtablesnapshot) | Fetches a snapshot of a table from a database. |
|  | [FilterAttribute](/user-guide/data-integration/openflow/processors/filterattribute) | Filters the attributes of a FlowFile by retaining specified attributes and removing the rest or by removing specified attributes and retaining the rest. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FindConfluencePages](/user-guide/data-integration/openflow/processors/findconfluencepages) | Processor for finding Confluence pages using space name and page name. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [FindSharepointDriveItem](/user-guide/data-integration/openflow/processors/findsharepointdriveitem) | Finds a Sharepoint Drive Item by its Drive ID and Item path. |
|  | [FlattenJson](/user-guide/data-integration/openflow/processors/flattenjson) | Provides the user with the ability to take a nested JSON document and flatten it into a simple key/value pair document. |
|  | [ForkEnrichment](/user-guide/data-integration/openflow/processors/forkenrichment) | Used in conjunction with the JoinEnrichment processor, this processor is responsible for adding the attributes that are necessary for the JoinEnrichment processor to perform its function. |
|  | [ForkRecord](/user-guide/data-integration/openflow/processors/forkrecord) | This processor allows the user to fork a record into multiple records. |

Expand

Show lessSee more

## G

|  | Processor | Description |
| --- | --- | --- |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GenerateAnswersFromContext](/user-guide/data-integration/openflow/processors/generateanswersfromcontext) | Generates synthetic answers for each question present in the incoming records using a Large Language Model (LLM). |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GenerateAnswersFromGroundTruth](/user-guide/data-integration/openflow/processors/generateanswersfromgroundtruth) | Generates synthetic answers for each question in the incoming records using an LLM. |
|  | [GenerateFlowFile](/user-guide/data-integration/openflow/processors/generateflowfile) | This processor creates FlowFiles with random data or custom content. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GenerateJSON](/user-guide/data-integration/openflow/processors/generatejson) | Produces a batch of JSON Objects with random field values based on a configurable JSON Schema. |
|  | [GenerateRecord](/user-guide/data-integration/openflow/processors/generaterecord) | This processor creates FlowFiles with records having random value for the specified fields. |
|  | [GenerateTableFetch](/user-guide/data-integration/openflow/processors/generatetablefetch) | Generates SQL select queries that fetch “pages” of rows from a table. |
|  | [GeoEnrichIP](/user-guide/data-integration/openflow/processors/geoenrichip) | Looks up geolocation information for an IP address and adds the geo information to FlowFile attributes. |
|  | [GeoEnrichIPRecord](/user-guide/data-integration/openflow/processors/geoenrichiprecord) | Looks up geolocation information for an IP address and adds the geo information to FlowFile attributes. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetAmazonAdsReport](/user-guide/data-integration/openflow/processors/getamazonadsreport) | Processor downloading report from Amazon Ads if ready. |
|  | [GetAwsPollyJobStatus](/user-guide/data-integration/openflow/processors/getawspollyjobstatus) | Retrieves the current status of an AWS Polly job. |
|  | [GetAwsTextractJobStatus](/user-guide/data-integration/openflow/processors/getawstextractjobstatus) | Retrieves the current status of an AWS Textract job. |
|  | [GetAwsTranscribeJobStatus](/user-guide/data-integration/openflow/processors/getawstranscribejobstatus) | Retrieves the current status of an AWS Transcribe job. |
|  | [GetAwsTranslateJobStatus](/user-guide/data-integration/openflow/processors/getawstranslatejobstatus) | Retrieves the current status of an AWS Translate job. |
|  | [GetAzureEventHub](/user-guide/data-integration/openflow/processors/getazureeventhub) | Receives messages from Microsoft Azure Event Hubs without reliable checkpoint tracking. |
|  | [GetAzureQueueStorage\_v12](/user-guide/data-integration/openflow/processors/getazurequeuestorage_v12) | Retrieves the messages from an Azure Queue Storage. |
|  | [GetBoxFileCollaborators](/user-guide/data-integration/openflow/processors/getboxfilecollaborators) | Retrieves all collaborators on a Box file and adds the collaboration information to the FlowFile’s attributes. |
|  | [GetBoxGroupMembers](/user-guide/data-integration/openflow/processors/getboxgroupmembers) | Retrieves members for a Box Group and writes their details in FlowFile attributes. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluenceAuditRecords](/user-guide/data-integration/openflow/processors/getconfluenceauditrecords) | Processor listing Confluence audit records. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluenceGroupUsers](/user-guide/data-integration/openflow/processors/getconfluencegroupusers) | Processor that downloads information about users belonging to a given Confluence group |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluencePageContent](/user-guide/data-integration/openflow/processors/getconfluencepagecontent) | Processor downloading Confluence pages. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluencePageIds](/user-guide/data-integration/openflow/processors/getconfluencepageids) | Downloads changed Confluence pages since the last sync and emits each as a FlowFile with metadata. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluencePagePermissions](/user-guide/data-integration/openflow/processors/getconfluencepagepermissions) | Processor downloading Confluence page permissions. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluenceSpaceIds](/user-guide/data-integration/openflow/processors/getconfluencespaceids) | Processor for retrieving Confluence space ids. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetConfluenceSpacePermissions](/user-guide/data-integration/openflow/processors/getconfluencespacepermissions) | Processor downloading Confluence space permissions. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetDataShareCredentials](/user-guide/data-integration/openflow/processors/getdatasharecredentials) | Describe the specified data share metadata in Salesforce Data Cloud. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetDataShareTables](/user-guide/data-integration/openflow/processors/getdatasharetables) | Describe the specified data share metadata in Salesforce Data Cloud. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetDBFSFile](/user-guide/data-integration/openflow/processors/getdbfsfile) | Read a DBFS file. |
|  | [GetDynamoDB](/user-guide/data-integration/openflow/processors/getdynamodb) | Retrieves a document from DynamoDB based on hash and range key. |
|  | [GetElasticsearch](/user-guide/data-integration/openflow/processors/getelasticsearch) | Elasticsearch get processor that uses the official Elastic REST client libraries to fetch a single document from Elasticsearch by \_id. |
|  | [GetFile](/user-guide/data-integration/openflow/processors/getfile) | Creates FlowFiles from files in a directory. |
|  | [GetFileResource](/user-guide/data-integration/openflow/processors/getfileresource) | This processor creates FlowFiles with the content of the configured File Resource. |
|  | [GetFTP](/user-guide/data-integration/openflow/processors/getftp) | Fetches files from an FTP Server and creates FlowFiles from them |
|  | [GetGcpVisionAnnotateFilesOperationStatus](/user-guide/data-integration/openflow/processors/getgcpvisionannotatefilesoperationstatus) | Retrieves the current status of an Google Vision operation. |
|  | [GetGcpVisionAnnotateImagesOperationStatus](/user-guide/data-integration/openflow/processors/getgcpvisionannotateimagesoperationstatus) | Retrieves the current status of an Google Vision operation. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetGoogleAdsReport](/user-guide/data-integration/openflow/processors/getgoogleadsreport) | A processor which can interact with Google Ads Reporting API. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetGoogleGroupMembers](/user-guide/data-integration/openflow/processors/getgooglegroupmembers) | Retrieves the members of one or more Google Groups, specified as a comma-separated list of group IDs that is given as a FlowFile attribute. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetGoogleSheets](/user-guide/data-integration/openflow/processors/getgooglesheets) | Processor responsible for fetching data from Google Sheets. |
|  | [GetHubSpot](/user-guide/data-integration/openflow/processors/gethubspot) | Retrieves JSON data from a private HubSpot application. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetHubSpotObject](/user-guide/data-integration/openflow/processors/gethubspotobject) | Get a HubSpot object and its associations by ID or unique value. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetHubSpotSchema](/user-guide/data-integration/openflow/processors/gethubspotschema) | Retrieves schema information for HubSpot object types including field names, types, and labels. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetLinkedInAdsReport](/user-guide/data-integration/openflow/processors/getlinkedinadsreport) | Processor downloading metrics from the LinkedIn Reporting APIs. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetMicrosoft365GroupMembers](/user-guide/data-integration/openflow/processors/getmicrosoft365groupmembers) | Retrieves Microsoft365 group members and emits a FlowFile for each change that occurs. |
|  | [GetMongo](/user-guide/data-integration/openflow/processors/getmongo) | Creates FlowFiles from documents in MongoDB loaded by a user-specified query. |
|  | [GetMongoRecord](/user-guide/data-integration/openflow/processors/getmongorecord) | A record-based version of GetMongo that uses the Record writers to write the MongoDB result set. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetQueryJobResult](/user-guide/data-integration/openflow/processors/getqueryjobresult) | Gets the results of a Query Job in Salesforce using the Bulk API 2. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetQueryJobStatus](/user-guide/data-integration/openflow/processors/getqueryjobstatus) | Gets the status of a Query Job in Salesforce using the Bulk API 2. |
|  | [GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata) | Check for the existence of an Object in S3 and fetch its Metadata without attempting to download it. |
|  | [GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags) | Check for the existence of an Object in S3 and fetch its Tags without attempting to download it. |
|  | [GetSFTP](/user-guide/data-integration/openflow/processors/getsftp) | Fetches files from an SFTP Server and creates FlowFiles from them |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetSharepointSiteGroupMembers](/user-guide/data-integration/openflow/processors/getsharepointsitegroupmembers) | Retrieves all members of a SharePoint site group. |
|  | [GetShopify](/user-guide/data-integration/openflow/processors/getshopify) | Retrieves objects from a custom Shopify store. |
|  | [GetSmbFile](/user-guide/data-integration/openflow/processors/getsmbfile) | Reads file from a samba network location to FlowFiles. |
|  | [GetSplunk](/user-guide/data-integration/openflow/processors/getsplunk) | Retrieves data from Splunk Enterprise. |
|  | [GetSQS](/user-guide/data-integration/openflow/processors/getsqs) | Fetches messages from an Amazon Simple Queuing Service Queue |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetUnityCatalogFile](/user-guide/data-integration/openflow/processors/getunitycatalogfile) | Read a Unity Catalog file up to 5 GiB. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [GetUnityCatalogFileMetadata](/user-guide/data-integration/openflow/processors/getunitycatalogfilemetadata) | Checks for Unity Catalog file metadata. |
|  | [GetWorkdayReport](/user-guide/data-integration/openflow/processors/getworkdayreport) | A processor which can interact with a configurable Workday Report. |
|  | [GetZendesk](/user-guide/data-integration/openflow/processors/getzendesk) | Incrementally fetches data from Zendesk API. |

Expand

Show lessSee more

## H

|  | Processor | Description |
| --- | --- | --- |
|  | [HandleHttpRequest](/user-guide/data-integration/openflow/processors/handlehttprequest) | Starts an HTTP Server and listens for HTTP Requests. |
|  | [HandleHttpResponse](/user-guide/data-integration/openflow/processors/handlehttpresponse) | Sends an HTTP Response to the Requestor that generated a FlowFile. |

Expand

Show lessSee more

## I

|  | Processor | Description |
| --- | --- | --- |
|  | [IdentifyMimeType](/user-guide/data-integration/openflow/processors/identifymimetype) | Attempts to identify the MIME Type used for a FlowFile. |
|  | [InvokeHTTP](/user-guide/data-integration/openflow/processors/invokehttp) | An HTTP client processor which can interact with a configurable HTTP Endpoint. |
|  | [InvokeScriptedProcessor](/user-guide/data-integration/openflow/processors/invokescriptedprocessor) | Experimental - Invokes a script engine for a Processor defined in the given script. |
|  | [ISPEnrichIP](/user-guide/data-integration/openflow/processors/ispenrichip) | Looks up ISP information for an IP address and adds the information to FlowFile attributes. |

Expand

Show lessSee more

## J

|  | Processor | Description |
| --- | --- | --- |
|  | [JoinEnrichment](/user-guide/data-integration/openflow/processors/joinenrichment) | Joins together Records from two different FlowFiles where one FlowFile, the ‘original’ contains arbitrary records and the second FlowFile, the ‘enrichment’ contains additional data that should be used to enrich the first. |
|  | [JoltTransformJSON](/user-guide/data-integration/openflow/processors/jolttransformjson) | Applies a list of Jolt specifications to either the FlowFile JSON content or a specified FlowFile JSON attribute. |
|  | [JoltTransformRecord](/user-guide/data-integration/openflow/processors/jolttransformrecord) | Applies a JOLT specification to each record in the FlowFile payload. |
|  | [JSLTTransformJSON](/user-guide/data-integration/openflow/processors/jslttransformjson) | Applies a JSLT transformation to the FlowFile JSON payload. |
|  | [JsonQueryElasticsearch](/user-guide/data-integration/openflow/processors/jsonqueryelasticsearch) | A processor that allows the user to run a query (with aggregations) written with the Elasticsearch JSON DSL. |

Expand

Show lessSee more

## L

|  | Processor | Description |
| --- | --- | --- |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListArchivedHubSpotData](/user-guide/data-integration/openflow/processors/listarchivedhubspotdata) | Lists archived data from HubSpot for the chosen object type and generates one FlowFile per listed object with the corresponding metadata as FlowFile attributes. |
|  | [ListAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/listazureblobstorage_v12) | Lists blobs in an Azure Blob Storage container. |
|  | [ListAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/listazuredatalakestorage) | Lists directory in an Azure Data Lake Storage Gen 2 filesystem |
|  | [ListBoxFile](/user-guide/data-integration/openflow/processors/listboxfile) | Lists files in a Box folder. |
|  | [ListBoxFileInfo](/user-guide/data-integration/openflow/processors/listboxfileinfo) | Fetches file metadata for each file in a Box Folder. |
|  | [ListBoxFileMetadataInstances](/user-guide/data-integration/openflow/processors/listboxfilemetadatainstances) | Retrieves all metadata instances associated with a Box file. |
|  | [ListBoxFileMetadataTemplates](/user-guide/data-integration/openflow/processors/listboxfilemetadatatemplates) | Retrieves all metadata templates associated with a Box file. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListConfluenceGroups](/user-guide/data-integration/openflow/processors/listconfluencegroups) | Processor listing Confluence groups. |
|  | [ListDatabaseTables](/user-guide/data-integration/openflow/processors/listdatabasetables) | Generates a set of flow files, each containing attributes corresponding to metadata about a table from a database connection. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListDBFSDirectory](/user-guide/data-integration/openflow/processors/listdbfsdirectory) | List file names in a DBFS directory and output a new FlowFile with the filename. |
|  | [ListDropbox](/user-guide/data-integration/openflow/processors/listdropbox) | Retrieves a listing of files from Dropbox (shortcuts are ignored). |
|  | [ListenFTP](/user-guide/data-integration/openflow/processors/listenftp) | Starts an FTP server that listens on the specified port and transforms incoming files into FlowFiles. |
|  | [ListenHTTP](/user-guide/data-integration/openflow/processors/listenhttp) | Starts an HTTP Server and listens on a given base path to transform incoming requests into FlowFiles. |
|  | [ListenOTLP](/user-guide/data-integration/openflow/processors/listenotlp) | Collect OpenTelemetry messages over HTTP or gRPC. |
|  | [ListenSlack](/user-guide/data-integration/openflow/processors/listenslack) | Retrieves real-time messages or Slack commands from one or more Slack conversations. |
|  | [ListenSyslog](/user-guide/data-integration/openflow/processors/listensyslog) | Listens for Syslog messages being sent to a given port over TCP or UDP. |
|  | [ListenTCP](/user-guide/data-integration/openflow/processors/listentcp) | Listens for incoming TCP connections and reads data from each connection using a line separator as the message demarcator. |
|  | [ListenUDP](/user-guide/data-integration/openflow/processors/listenudp) | Listens for Datagram Packets on a given port. |
|  | [ListenUDPRecord](/user-guide/data-integration/openflow/processors/listenudprecord) | Listens for Datagram Packets on a given port and reads the content of each datagram using the configured Record Reader. |
|  | [ListenWebSocket](/user-guide/data-integration/openflow/processors/listenwebsocket) | Acts as a WebSocket server endpoint to accept client connections. |
|  | [ListFile](/user-guide/data-integration/openflow/processors/listfile) | Retrieves a listing of files from the input directory. |
|  | [ListFTP](/user-guide/data-integration/openflow/processors/listftp) | Performs a listing of the files residing on an FTP server. |
|  | [ListGCSBucket](/user-guide/data-integration/openflow/processors/listgcsbucket) | Retrieves a listing of objects from a GCS bucket. |
|  | [ListGoogleDrive](/user-guide/data-integration/openflow/processors/listgoogledrive) | Performs a listing of concrete files (shortcuts are ignored) in a Google Drive folder. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListGoogleDriveFileInfo](/user-guide/data-integration/openflow/processors/listgoogledrivefileinfo) | Lists all files and folders in a specified Google Drive. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListGoogleGroups](/user-guide/data-integration/openflow/processors/listgooglegroups) | Lists all of the groups for a given domain in Google Workspace. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListHubSpotObjects](/user-guide/data-integration/openflow/processors/listhubspotobjects) | Fetches data from HubSpot for specified object types, and generates one FlowFile per listed object with the corresponding metadata as FlowFile attributes. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListMicrosoftDataverseTables](/user-guide/data-integration/openflow/processors/listmicrosoftdataversetables) | List Tables from Microsoft Dataverse environments |
|  | [ListS3](/user-guide/data-integration/openflow/processors/lists3) | Retrieves a listing of objects from an S3 bucket. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListSFDCDataShares](/user-guide/data-integration/openflow/processors/listsfdcdatashares) | List the available data shares in the organization that are available to the identified user. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListSFDCObjects](/user-guide/data-integration/openflow/processors/listsfdcobjects) | List the available objects in the organization that are available to the identified user. |
|  | [ListSFTP](/user-guide/data-integration/openflow/processors/listsftp) | Performs a listing of the files residing on an SFTP server. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListSharepointDrives](/user-guide/data-integration/openflow/processors/listsharepointdrives) | Emits a FlowFile for each Drive present in the specified Sharepoint Site. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListSharepointSiteGroups](/user-guide/data-integration/openflow/processors/listsharepointsitegroups) | Lists all SharePoint site groups available on a specified SharePoint site. |
|  | [ListSmb](/user-guide/data-integration/openflow/processors/listsmb) | Lists concrete files shared via SMB protocol. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListTableNames](/user-guide/data-integration/openflow/processors/listtablenames) | Fetches all source table names and matches them with one of the possible configurations: - regexp expression e. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ListUnityCatalogDirectory](/user-guide/data-integration/openflow/processors/listunitycatalogdirectory) | List file names in a Unity Catalog directory and output a new FlowFile with the filename. |
|  | [LogAttribute](/user-guide/data-integration/openflow/processors/logattribute) | Emits attributes of the FlowFile at the specified log level |
|  | [LogMessage](/user-guide/data-integration/openflow/processors/logmessage) | Emits a log message at the specified log level |
|  | [LookupAttribute](/user-guide/data-integration/openflow/processors/lookupattribute) | Lookup attributes from a lookup service |
|  | [LookupRecord](/user-guide/data-integration/openflow/processors/lookuprecord) | Extracts one or more fields from a Record and looks up a value for those fields in a LookupService. |

Expand

Show lessSee more

## M

|  | Processor | Description |
| --- | --- | --- |
|  | [MergeContent](/user-guide/data-integration/openflow/processors/mergecontent) | Merges a Group of FlowFiles together based on a user-defined strategy and packages them into a single FlowFile. |
|  | [MergeRecord](/user-guide/data-integration/openflow/processors/mergerecord) | This Processor merges together multiple record-oriented FlowFiles into a single FlowFile that contains all of the Records of the input FlowFiles. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [MergeSnowflakeJournalTable](/user-guide/data-integration/openflow/processors/mergesnowflakejournaltable) | Triggers a merge operation on changes from journal table to a destination table in Snowflake. |
|  | [ModifyBytes](/user-guide/data-integration/openflow/processors/modifybytes) | Discard byte range at the start and end or all content of a binary file. |
|  | [ModifyCompression](/user-guide/data-integration/openflow/processors/modifycompression) | Changes the compression algorithm used to compress the contents of a FlowFile by decompressing the contents of FlowFiles using a user-specified compression algorithm and recompressing the contents using the specified compression format properties. |
|  | [MonitorActivity](/user-guide/data-integration/openflow/processors/monitoractivity) | Monitors the flow for activity and sends out an indicator when the flow has not had any data for some specified amount of time and again when the flow’s activity is restored |
|  | [MoveAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/moveazuredatalakestorage) | Moves content within an Azure Data Lake Storage Gen 2. |

Expand

Show lessSee more

## N

|  | Processor | Description |
| --- | --- | --- |
|  | [Notify](/user-guide/data-integration/openflow/processors/notify) | Caches a release signal identifier in the distributed cache, optionally along with the FlowFile’s attributes. |

Expand

Show lessSee more

## O

|  | Processor | Description |
| --- | --- | --- |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [OpenAiTranscribeAudio](/user-guide/data-integration/openflow/processors/openaitranscribeaudio) | Transcribes audio into English text. |

Expand

Show lessSee more

## P

|  | Processor | Description |
| --- | --- | --- |
|  | [PackageFlowFile](/user-guide/data-integration/openflow/processors/packageflowfile) | This processor will package FlowFile attributes and content into an output FlowFile that can be exported from NiFi and imported back into NiFi, preserving the original attributes and content. |
|  | [PaginatedJsonQueryElasticsearch](/user-guide/data-integration/openflow/processors/paginatedjsonqueryelasticsearch) | A processor that allows the user to run a paginated query (with aggregations) written with the Elasticsearch JSON DSL. |
|  | [ParseEvtx](/user-guide/data-integration/openflow/processors/parseevtx) | Parses the contents of a Windows Event Log file (evtx) and writes the resulting XML to the FlowFile |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [ParseExcelCellReference](/user-guide/data-integration/openflow/processors/parseexcelcellreference) | Processor responsible for parsing Excel cell reference formula. |
|  | [ParseSyslog](/user-guide/data-integration/openflow/processors/parsesyslog) | Attempts to parses the contents of a Syslog message in accordance to RFC5424 and RFC3164 formats and adds attributes to the FlowFile for each of the parts of the Syslog message. |
|  | [ParseSyslog5424](/user-guide/data-integration/openflow/processors/parsesyslog5424) | Attempts to parse the contents of a well formed Syslog message in accordance to RFC5424 format and adds attributes to the FlowFile for each of the parts of the Syslog message, including Structured Data. |
|  | [PartitionRecord](/user-guide/data-integration/openflow/processors/partitionrecord) | Splits, or partitions, record-oriented data based on the configured fields in the data. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PerformSnowflakeCortexOCR](/user-guide/data-integration/openflow/processors/performsnowflakecortexocr) | Performs Optical Character Recognition (OCR) on PDF documents using Snowflake Cortex ML functions. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PickTablesForReplication](/user-guide/data-integration/openflow/processors/picktablesforreplication) | Accepts a list of fully qualified table names and determines if a table: - is new (is not replicated, but was added in the source) - is existing (is replicated and exists in the source) - is stale (is replicated but no longer exists in the source) Configuration is passed as a FlowFile attribute. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PromptAnthropicAI](/user-guide/data-integration/openflow/processors/promptanthropicai) | Sends a prompt to Anthropic, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PromptAzureOpenAI](/user-guide/data-integration/openflow/processors/promptazureopenai) | Sends a prompt to Azure’s OpenAI service, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PromptLLM](/user-guide/data-integration/openflow/processors/promptllm) | This processor sends a user defined prompt to a Large Language Model (LLM) to respond. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PromptOpenAI](/user-guide/data-integration/openflow/processors/promptopenai) | Sends a prompt to OpenAI, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PromptSnowflakeCortex](/user-guide/data-integration/openflow/processors/promptsnowflakecortex) | Sends a prompt to Snowflake Cortex, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PromptVertexAI](/user-guide/data-integration/openflow/processors/promptvertexai) | Sends a prompt to VertexAI, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. |
|  | [PublishAMQP](/user-guide/data-integration/openflow/processors/publishamqp) | Creates an AMQP Message from the contents of a FlowFile and sends the message to an AMQP Exchange. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PublishChangeDataSnowpipeStreaming](/user-guide/data-integration/openflow/processors/publishchangedatasnowpipestreaming) | Publishes change data as Newline Delimited JSON to Snowflake Database Pipes using Snowpipe Streaming High Availability with concurrency group serialization. |
|  | [PublishGCPubSub](/user-guide/data-integration/openflow/processors/publishgcpubsub) | Publishes the content of the incoming flowfile to the configured Google Cloud PubSub topic. |
|  | [PublishJMS](/user-guide/data-integration/openflow/processors/publishjms) | Creates a JMS Message from the contents of a FlowFile and sends it to a JMS Destination (queue or topic) as JMS BytesMessage or TextMessage. |
|  | [PublishKafka](/user-guide/data-integration/openflow/processors/publishkafka) | Sends the contents of a FlowFile as either a message or as individual records to Apache Kafka using the Kafka Producer API. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PublishKafka](/user-guide/data-integration/openflow/processors/publishkafka) | Sends the contents of a FlowFile as either a message or as individual records to Apache Kafka using the Kafka Producer API. |
|  | [PublishMQTT](/user-guide/data-integration/openflow/processors/publishmqtt) | Publishes a message to an MQTT topic |
|  | [PublishSlack](/user-guide/data-integration/openflow/processors/publishslack) | Posts a message to the specified Slack channel. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PublishSnowpipeStreaming](/user-guide/data-integration/openflow/processors/publishsnowpipestreaming) | Publishes Newline Delimited JSON to Snowflake Database Pipes using Snowpipe Streaming High Availability. |
|  | [PutAzureBlobStorage\_v12](/user-guide/data-integration/openflow/processors/putazureblobstorage_v12) | Puts content into a blob on Azure Blob Storage. |
|  | [PutAzureCosmosDBRecord](/user-guide/data-integration/openflow/processors/putazurecosmosdbrecord) | This processor is a record-aware processor for inserting data into Cosmos DB with Core SQL API. |
|  | [PutAzureDataExplorer](/user-guide/data-integration/openflow/processors/putazuredataexplorer) | Acts as an Azure Data Explorer sink which sends FlowFiles to the provided endpoint. |
|  | [PutAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/putazuredatalakestorage) | Writes the contents of a FlowFile as a file on Azure Data Lake Storage Gen 2 |
|  | [PutAzureEventHub](/user-guide/data-integration/openflow/processors/putazureeventhub) | Send FlowFile contents to Azure Event Hubs |
|  | [PutAzureQueueStorage\_v12](/user-guide/data-integration/openflow/processors/putazurequeuestorage_v12) | Writes the content of the incoming FlowFiles to the configured Azure Queue Storage. |
|  | [PutBigQuery](/user-guide/data-integration/openflow/processors/putbigquery) | Writes the contents of a FlowFile to a Google BigQuery table. |
|  | [PutBoxFile](/user-guide/data-integration/openflow/processors/putboxfile) | Puts content to a Box folder. |
|  | [PutCloudWatchMetric](/user-guide/data-integration/openflow/processors/putcloudwatchmetric) | Publishes metrics to Amazon CloudWatch. |
|  | [PutDatabaseRecord](/user-guide/data-integration/openflow/processors/putdatabaserecord) | The PutDatabaseRecord processor uses a specified RecordReader to input (possibly multiple) records from an incoming flow file. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutDatabricksSQL](/user-guide/data-integration/openflow/processors/putdatabrickssql) | Submit a SQL Execution using Databricks REST API then write the JSON response to FlowFile Content. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutDBFSFile](/user-guide/data-integration/openflow/processors/putdbfsfile) | Write FlowFile content to DBFS. |
|  | [PutDistributedMapCache](/user-guide/data-integration/openflow/processors/putdistributedmapcache) | Gets the content of a FlowFile and puts it to a distributed map cache, using a cache key computed from FlowFile attributes. |
|  | [PutDropbox](/user-guide/data-integration/openflow/processors/putdropbox) | Puts content to a Dropbox folder. |
|  | [PutDynamoDB](/user-guide/data-integration/openflow/processors/putdynamodb) | Puts a document from DynamoDB based on hash and range key. |
|  | [PutDynamoDBRecord](/user-guide/data-integration/openflow/processors/putdynamodbrecord) | Inserts items into DynamoDB based on record-oriented data. |
|  | [PutElasticsearchJson](/user-guide/data-integration/openflow/processors/putelasticsearchjson) | An Elasticsearch put processor that uses the official Elastic REST client libraries. |
|  | [PutElasticsearchRecord](/user-guide/data-integration/openflow/processors/putelasticsearchrecord) | A record-aware Elasticsearch put processor that uses the official Elastic REST client libraries. |
|  | [PutEmail](/user-guide/data-integration/openflow/processors/putemail) | Sends an e-mail to configured recipients for each incoming FlowFile |
|  | [PutFile](/user-guide/data-integration/openflow/processors/putfile) | Writes the contents of a FlowFile to the local file system |
|  | [PutFTP](/user-guide/data-integration/openflow/processors/putftp) | Sends FlowFiles to an FTP Server |
|  | [PutGCSObject](/user-guide/data-integration/openflow/processors/putgcsobject) | Writes the contents of a FlowFile as an object in a Google Cloud Storage. |
|  | [PutGoogleDrive](/user-guide/data-integration/openflow/processors/putgoogledrive) | Writes the contents of a FlowFile as a file in Google Drive. |
|  | [PutGridFS](/user-guide/data-integration/openflow/processors/putgridfs) | Writes a file to a GridFS bucket. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutHubSpot](/user-guide/data-integration/openflow/processors/puthubspot) | Upsert a HubSpot object. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutIcebergTable](/user-guide/data-integration/openflow/processors/puticebergtable) | Store records in Iceberg using configurable Catalog for managing namespaces and tables. |
|  | [PutKinesisFirehose](/user-guide/data-integration/openflow/processors/putkinesisfirehose) | Sends the contents to a specified Amazon Kinesis Firehose. |
|  | [PutKinesisStream](/user-guide/data-integration/openflow/processors/putkinesisstream) | Sends the contents to a specified Amazon Kinesis. |
|  | [PutLambda](/user-guide/data-integration/openflow/processors/putlambda) | Sends the contents to a specified Amazon Lambda Function. |
|  | [PutMongo](/user-guide/data-integration/openflow/processors/putmongo) | Writes the contents of a FlowFile to MongoDB |
|  | [PutMongoBulkOperations](/user-guide/data-integration/openflow/processors/putmongobulkoperations) | Writes the contents of a FlowFile to MongoDB as bulk-update |
|  | [PutMongoRecord](/user-guide/data-integration/openflow/processors/putmongorecord) | This processor is a record-aware processor for inserting/upserting data into MongoDB. |
|  | [PutRecord](/user-guide/data-integration/openflow/processors/putrecord) | The PutRecord processor uses a specified RecordReader to input (possibly multiple) records from an incoming flow file, and sends them to a destination specified by a Record Destination Service (i. |
|  | [PutRedisHashRecord](/user-guide/data-integration/openflow/processors/putredishashrecord) | Puts record field data into Redis using a specified hash value, which is determined by a RecordPath to a field in each record containing the hash value. |
|  | [PutS3Object](/user-guide/data-integration/openflow/processors/puts3object) | Writes the contents of a FlowFile as an S3 Object to an Amazon S3 Bucket. |
|  | [PutSalesforceObject](/user-guide/data-integration/openflow/processors/putsalesforceobject) | Creates new records for the specified Salesforce sObject. |
|  | [PutSFTP](/user-guide/data-integration/openflow/processors/putsftp) | Sends FlowFiles to an SFTP Server |
|  | [PutSmbFile](/user-guide/data-integration/openflow/processors/putsmbfile) | Writes the contents of a FlowFile to a samba network location. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutSnowflakeInternalStageFile](/user-guide/data-integration/openflow/processors/putsnowflakeinternalstagefile) | Puts files into a Snowflake internal stage. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutSnowpipeStreaming](/user-guide/data-integration/openflow/processors/putsnowpipestreaming) | Streams records into a Snowflake table. |
|  | [PutSNS](/user-guide/data-integration/openflow/processors/putsns) | Sends the content of a FlowFile as a notification to the Amazon Simple Notification Service |
|  | [PutSplunk](/user-guide/data-integration/openflow/processors/putsplunk) | Sends logs to Splunk Enterprise over TCP, TCP + TLS/SSL, or UDP. |
|  | [PutSplunkHTTP](/user-guide/data-integration/openflow/processors/putsplunkhttp) | Sends flow file content to the specified Splunk server over HTTP or HTTPS. |
|  | [PutSQL](/user-guide/data-integration/openflow/processors/putsql) | Executes a SQL UPDATE or INSERT command. |
|  | [PutSQS](/user-guide/data-integration/openflow/processors/putsqs) | Publishes a message to an Amazon Simple Queuing Service Queue |
|  | [PutSyslog](/user-guide/data-integration/openflow/processors/putsyslog) | Sends Syslog messages to a given host and port over TCP or UDP. |
|  | [PutTCP](/user-guide/data-integration/openflow/processors/puttcp) | Sends serialized FlowFiles or Records over TCP to a configurable destination with optional support for TLS |
|  | [PutUDP](/user-guide/data-integration/openflow/processors/putudp) | The PutUDP processor receives a FlowFile and packages the FlowFile content into a single UDP datagram packet which is then transmitted to the configured UDP server. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutUnityCatalogFile](/user-guide/data-integration/openflow/processors/putunitycatalogfile) | Write FlowFile content with max size of 5 GiB to Unity Catalog. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutVectaraDocument](/user-guide/data-integration/openflow/processors/putvectaradocument) | Generate and upload a JSON document to Vectara’s upload endpoint. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [PutVectaraFile](/user-guide/data-integration/openflow/processors/putvectarafile) | Upload a FlowFile content to Vectara’s index endpoint. |
|  | [PutWebSocket](/user-guide/data-integration/openflow/processors/putwebsocket) | Sends messages to a WebSocket remote endpoint using a WebSocket session that is established by either ListenWebSocket or ConnectWebSocket. |
|  | [PutZendeskTicket](/user-guide/data-integration/openflow/processors/putzendeskticket) | Create Zendesk tickets using the Zendesk API. |

Expand

Show lessSee more

## Q

|  | Processor | Description |
| --- | --- | --- |
|  | [QueryAzureDataExplorer](/user-guide/data-integration/openflow/processors/queryazuredataexplorer) | Query Azure Data Explorer and stream JSON results to output FlowFiles |
|  | [QueryDatabaseTable](/user-guide/data-integration/openflow/processors/querydatabasetable) | Generates a SQL select query, or uses a provided statement, and executes it to fetch all rows whose values in the specified Maximum Value column(s) are larger than the previously-seen maxima. |
|  | [QueryDatabaseTableRecord](/user-guide/data-integration/openflow/processors/querydatabasetablerecord) | Generates a SQL select query, or uses a provided statement, and executes it to fetch all rows whose values in the specified Maximum Value column(s) are larger than the previously-seen maxima. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [QueryMilvus](/user-guide/data-integration/openflow/processors/querymilvus) | Queries a given collection in a Milvus database using vectors. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [QueryPinecone](/user-guide/data-integration/openflow/processors/querypinecone) | Queries Pinecone for vectors that are similar to the input vector, or retrieves a vector by ID. |
|  | [QueryRecord](/user-guide/data-integration/openflow/processors/queryrecord) | Evaluates one or more SQL queries against the contents of a FlowFile. |
|  | [QuerySalesforceObject](/user-guide/data-integration/openflow/processors/querysalesforceobject) | Retrieves records from a Salesforce sObject. |
|  | [QuerySplunkIndexingStatus](/user-guide/data-integration/openflow/processors/querysplunkindexingstatus) | Queries Splunk server in order to acquire the status of indexing acknowledgement. |

Expand

Show lessSee more

## R

|  | Processor | Description |
| --- | --- | --- |
|  | [RemoveRecordField](/user-guide/data-integration/openflow/processors/removerecordfield) | Modifies the contents of a FlowFile that contains Record-oriented data (i. |
|  | [RenameRecordField](/user-guide/data-integration/openflow/processors/renamerecordfield) | Renames one or more fields in each Record of a FlowFile. |
|  | [ReplaceText](/user-guide/data-integration/openflow/processors/replacetext) | Updates the content of a FlowFile by searching for some textual value in the FlowFile content (via Regular Expression/regex, or literal value) and replacing the section of the content that matches with some alternate value. |
|  | [ReplaceTextWithMapping](/user-guide/data-integration/openflow/processors/replacetextwithmapping) | Updates the content of a FlowFile by evaluating a Regular Expression against it and replacing the section of the content that matches the Regular Expression with some alternate value provided in a mapping file. |
|  | [RetryFlowFile](/user-guide/data-integration/openflow/processors/retryflowfile) | FlowFiles passed to this Processor have a ‘Retry Attribute’ value checked against a configured ‘Maximum Retries’ value. |
|  | [RouteOnAttribute](/user-guide/data-integration/openflow/processors/routeonattribute) | Routes FlowFiles based on their Attributes using the Attribute Expression Language |
|  | [RouteOnContent](/user-guide/data-integration/openflow/processors/routeoncontent) | Applies Regular Expressions to the content of a FlowFile and routes a copy of the FlowFile to each destination whose Regular Expression matches. |
|  | [RouteText](/user-guide/data-integration/openflow/processors/routetext) | Routes textual data based on a set of user-defined rules. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [RunDatabricksJob](/user-guide/data-integration/openflow/processors/rundatabricksjob) | Triggers a pre-defined Databricks job to run with custom parameters. |
|  | [RunMongoAggregation](/user-guide/data-integration/openflow/processors/runmongoaggregation) | A processor that runs an aggregation query whenever a flowfile is received. |

Expand

Show lessSee more

## S

|  | Processor | Description |
| --- | --- | --- |
|  | [SampleRecord](/user-guide/data-integration/openflow/processors/samplerecord) | Samples the records of a FlowFile based on a specified sampling strategy (such as Reservoir Sampling). |
|  | [ScanAttribute](/user-guide/data-integration/openflow/processors/scanattribute) | Scans the specified attributes of FlowFiles, checking to see if any of their values are present within the specified dictionary of terms |
|  | [ScanContent](/user-guide/data-integration/openflow/processors/scancontent) | Scans the content of FlowFiles for terms that are found in a user-supplied dictionary. |
|  | [ScriptedFilterRecord](/user-guide/data-integration/openflow/processors/scriptedfilterrecord) | This processor provides the ability to filter records out from FlowFiles using the user-provided script. |
|  | [ScriptedPartitionRecord](/user-guide/data-integration/openflow/processors/scriptedpartitionrecord) | Receives Record-oriented data (i. |
|  | [ScriptedTransformRecord](/user-guide/data-integration/openflow/processors/scriptedtransformrecord) | Provides the ability to evaluate a simple script against each record in an incoming FlowFile. |
|  | [ScriptedValidateRecord](/user-guide/data-integration/openflow/processors/scriptedvalidaterecord) | This processor provides the ability to validate records in FlowFiles using the user-provided script. |
|  | [SearchElasticsearch](/user-guide/data-integration/openflow/processors/searchelasticsearch) | A processor that allows the user to repeatedly run a paginated query (with aggregations) written with the Elasticsearch JSON DSL. |
|  | [SegmentContent](/user-guide/data-integration/openflow/processors/segmentcontent) | Segments a FlowFile into multiple smaller segments on byte boundaries. |
|  | [SignContentPGP](/user-guide/data-integration/openflow/processors/signcontentpgp) | Sign content using OpenPGP Private Keys |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SnowflakeDetectDuplicate](/user-guide/data-integration/openflow/processors/snowflakedetectduplicate) | Checks if a FlowFile ‘s hash (provided as a FlowFile attribute) is already in a Snowflake table, and routes the FlowFile to’ duplicate ‘if found,’distinct ‘if not found, or’ failure’ on errors. |
|  | [SplitAvro](/user-guide/data-integration/openflow/processors/splitavro) | Splits a binary encoded Avro datafile into smaller files based on the configured Output Size. |
|  | [SplitContent](/user-guide/data-integration/openflow/processors/splitcontent) | Splits incoming FlowFiles by a specified byte sequence |
|  | [SplitExcel](/user-guide/data-integration/openflow/processors/splitexcel) | This processor splits a multi sheet Microsoft Excel spreadsheet into multiple Microsoft Excel spreadsheets where each sheet from the original file is converted to an individual spreadsheet in its own flow file. |
|  | [SplitJson](/user-guide/data-integration/openflow/processors/splitjson) | Splits a JSON File into multiple, separate FlowFiles for an array element specified by a JsonPath expression. |
|  | [SplitRecord](/user-guide/data-integration/openflow/processors/splitrecord) | Splits up an input FlowFile that is in a record-oriented data format into multiple smaller FlowFiles |
|  | [SplitText](/user-guide/data-integration/openflow/processors/splittext) | Splits a text file into multiple smaller text files on line boundaries limited by maximum number of lines or total size of fragment. |
|  | [SplitXml](/user-guide/data-integration/openflow/processors/splitxml) | Splits an XML File into multiple separate FlowFiles, each comprising a child or descendant of the original root element |
|  | [StartAwsPollyJob](/user-guide/data-integration/openflow/processors/startawspollyjob) | Trigger a AWS Polly job. |
|  | [StartAwsTextractJob](/user-guide/data-integration/openflow/processors/startawstextractjob) | Trigger a AWS Textract job. |
|  | [StartAwsTranscribeJob](/user-guide/data-integration/openflow/processors/startawstranscribejob) | Trigger a AWS Transcribe job. |
|  | [StartAwsTranslateJob](/user-guide/data-integration/openflow/processors/startawstranslatejob) | Trigger a AWS Translate job. |
|  | [StartGcpVisionAnnotateFilesOperation](/user-guide/data-integration/openflow/processors/startgcpvisionannotatefilesoperation) | Trigger a Vision operation on file input. |
|  | [StartGcpVisionAnnotateImagesOperation](/user-guide/data-integration/openflow/processors/startgcpvisionannotateimagesoperation) | Trigger a Vision operation on image input. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SubmitQueryJob](/user-guide/data-integration/openflow/processors/submitqueryjob) | Submits a Query Job to Salesforce using the Bulk API 2. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [SummarizeText](/user-guide/data-integration/openflow/processors/summarizetext) | This processor uses a Large Language Model (LLM) to summarize the content of a FlowFile. |

Expand

Show lessSee more

## T

|  | Processor | Description |
| --- | --- | --- |
|  | [TagS3Object](/user-guide/data-integration/openflow/processors/tags3object) | Adds or updates a tag on an Amazon S3 Object. |
|  | [TailFile](/user-guide/data-integration/openflow/processors/tailfile) | “Tails” a file, or a list of files, ingesting data from the file as it is written to the file. |
|  | [TransformXml](/user-guide/data-integration/openflow/processors/transformxml) | Applies the provided XSLT file to the FlowFile XML payload. |

Expand

Show lessSee more

## U

|  | Processor | Description |
| --- | --- | --- |
|  | [UnpackContent](/user-guide/data-integration/openflow/processors/unpackcontent) | Unpacks the content of FlowFiles that have been packaged with one of several different Packaging Formats, emitting one to many FlowFiles for each input FlowFile. |
|  | [UpdateAttribute](/user-guide/data-integration/openflow/processors/updateattribute) | Updates the Attributes for a FlowFile by using the Attribute Expression Language and/or deletes the attributes based on a regular expression |
|  | [UpdateBoxFileMetadataInstance](/user-guide/data-integration/openflow/processors/updateboxfilemetadatainstance) | Updates metadata template values for a Box file using the record in the given flowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateBulkJobState](/user-guide/data-integration/openflow/processors/updatebulkjobstate) | Updates the status of a Salesforce Bulk Job in the shared state service for a specific object type |
|  | [UpdateByQueryElasticsearch](/user-guide/data-integration/openflow/processors/updatebyqueryelasticsearch) | Update documents in an Elasticsearch index using a query. |
|  | [UpdateCounter](/user-guide/data-integration/openflow/processors/updatecounter) | This processor allows users to set specific counters and key points in their flow. |
|  | [UpdateDatabaseTable](/user-guide/data-integration/openflow/processors/updatedatabasetable) | This processor uses a JDBC connection and incoming records to generate any database table changes needed to support the incoming records. |
|  | [UpdateRecord](/user-guide/data-integration/openflow/processors/updaterecord) | Updates the contents of a FlowFile that contains Record-oriented data (i. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateSnowflakeDatabase](/user-guide/data-integration/openflow/processors/updatesnowflakedatabase) | Updates the definition of a Snowflake table based on the schema provided in the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateSnowflakeIcebergDatabase](/user-guide/data-integration/openflow/processors/updatesnowflakeicebergdatabase) | Updates the definition of a Snowflake Iceberg table. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateSnowflakeSchema](/user-guide/data-integration/openflow/processors/updatesnowflakeschema) | Creates Snowflake database schema if it does not exist. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateSnowflakeStream](/user-guide/data-integration/openflow/processors/updatesnowflakestream) | Manages Snowflake streams by creating, dropping, or replacing them based on the configured operation. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateSnowflakeTable](/user-guide/data-integration/openflow/processors/updatesnowflaketable) | Updates the definition of a Snowflake table based on the schema provided in the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateSnowflakeView](/user-guide/data-integration/openflow/processors/updatesnowflakeview) | Creates or replaces Snowflake views based on column mappings provided in the incoming FlowFile. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpdateTableState](/user-guide/data-integration/openflow/processors/updatetablestate) | Updates the state of a table in the Table State Service |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpsertMilvus](/user-guide/data-integration/openflow/processors/upsertmilvus) | Upserts vectors into Milvus database for a given collection |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpsertPinecone](/user-guide/data-integration/openflow/processors/upsertpinecone) | Publishes vectors, including metadata, and optionally text, to a Pinecone index. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [UpsertSFDCObjects](/user-guide/data-integration/openflow/processors/upsertsfdcobjects) | Upserts the records from the incoming FlowFile into Salesforce |

Expand

Show lessSee more

## V

|  | Processor | Description |
| --- | --- | --- |
|  | [ValidateCsv](/user-guide/data-integration/openflow/processors/validatecsv) | Validates the contents of FlowFiles or a FlowFile attribute value against a user-specified CSV schema. |
|  | [ValidateJson](/user-guide/data-integration/openflow/processors/validatejson) | Validates the contents of FlowFiles against a configurable JSON Schema. |
|  | [ValidateRecord](/user-guide/data-integration/openflow/processors/validaterecord) | Validates the Records of an incoming FlowFile against a given schema. |
|  | [ValidateXml](/user-guide/data-integration/openflow/processors/validatexml) | Validates XML contained in a FlowFile. |
|  | [VerifyContentMAC](/user-guide/data-integration/openflow/processors/verifycontentmac) | Calculates a Message Authentication Code using the provided Secret Key and compares it with the provided MAC property |
|  | [VerifyContentPGP](/user-guide/data-integration/openflow/processors/verifycontentpgp) | Verify signatures using OpenPGP Public Keys |

Expand

Show lessSee more

## W

|  | Processor | Description |
| --- | --- | --- |
|  | [Wait](/user-guide/data-integration/openflow/processors/wait) | Routes incoming FlowFiles to the ‘wait’ relationship until a matching release signal is stored in the distributed cache from a corresponding Notify processor. |
| [Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png) | [WaitForTableState](/user-guide/data-integration/openflow/processors/waitfortablestate) | Blocks incoming FlowFiles until the corresponding table state is not equal to accepted state. |

Expand

Show lessSee more
