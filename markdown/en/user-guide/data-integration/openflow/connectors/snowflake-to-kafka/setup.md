# Set up the Openflow Connector for Snowflake to Kafka

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Snowflake to Kafka.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Snowflake to Kafka](/user-guide/data-integration/openflow/connectors/snowflake-to-kafka/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. Create a Snowflake stream that will be queried for the changes.
4. Create a Kafka topic that will receive CDC messages from the Snowflake stream.

## Set up Snowflake account

As a Snowflake account administrator, perform the following tasks:

1. Create the database, source table, and the stream object that the connector will use for reading CDC events. For example:

   Copy code

   ```
   create database stream_db;
   use database stream_db;
   create table stream_source (user_id varchar, data varchar);
   create stream stream_on_table on table stream_source;
   ```
2. Create a new role or use an existing role, and grant the SELECT privilege on the stream
   and the source object for the stream. The connector will also need the USAGE privilege on the database and
   schema containing the stream and source object for the stream. For example:

   Copy code

   ```
   create role stream_reader;
   grant usage on database stream_db to role stream_reader;
   grant usage on schema stream_db.public to role stream_reader;
   grant select on stream_source to role stream_reader;
   grant select on stream_on_table to role stream_reader;
   ```
3. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property). For example:

   Copy code

   ```
   create user stream_user type = service;
   ```
4. Grant the Snowflake service user the role you created in the previous steps. For example:

   Copy code

   ```
   grant role stream_reader to user stream_user;
   ```
5. Configure [key-pair auth](/user-guide/key-pair-auth) for the Snowflake SERVICE user from step 3.
6. Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow, such as AWS, Azure, and HashiCorp,
   and store the public and private keys in the secret store. However, note that the private key generated in step 5 can be used
   directly as a configuration parameter for the connector configuration. In such a case, the private key is stored in Openflow runtime configuration.

   Note

   If for any reason, you do not wish to use a secrets manager, then you are responsible for safeguarding the
   public key and private key files used for key-pair authentication according to the security policies of your organization.

   1. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, it’s recommended that you use the
      EC2 instance role associated with Openflow, so that no other secrets have to be persisted.
   2. In Openflow, configure a Parameter Provider associated with this Secrets Manager, from the hamburger menu in the upper right.
      Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.
   3. At this point all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
7. Designate a warehouse for the connector to use. One connector can replicate a single table to a single Kafka topic.
   For this kind of processing, you can select the smallest warehouse.

## Set up the connector

As a data engineer, perform the following tasks to install and configure a connector:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find and choose the connector depending on what kind of Kafka broker instance the connector should communicate with.

   - mTLS version: Choose this connector if you are using the SSL (mutual TLS) security protocol, or if you are using
     the SASL\_SSL protocol and connecting to the broker that is using self-signed certificates.
   - SASL version: Choose this connector if you are using any other security protocol.
3. Select **Install**.
4. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list.
5. Select **Add**.
6. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
7. Authenticate to the runtime with your Snowflake account credentials.

   The Openflow canvas appears with the connector process group added to it.
8. Right-click on the imported process group and select **Parameters**.
9. Populate the required parameter values as described in [Flow parameters](#flow-parameters).

### Flow parameters

This section describes the flow parameters that you can configure based on the following parameter contexts:

- [Kafka Sink Source Parameters](#kafka-sink-source-parameters)
- [Kafka Sink Destination Parameters](#kafka-sink-destination-parameters)
- [Kafka Sink Ingestion Parameters](#kafka-sink-ingestion-parameters)

#### Kafka Sink Source Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name] where data will be persisted. | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Source Database | Source database. This database should contain the Snowflake Stream object that will be consumed. | Yes |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake Private Key File. | No |
| Snowflake Role | When using   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR** Authentication Strategy: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the user name used to connect to the Snowflake instance. | Yes |
| Snowflake Private Key | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the RSA private key used for authentication. The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either Snowflake Private Key File or Snowflake Private Key must be defined. | Yes |
| Snowflake Private Key File | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, upload the file that contains the RSA Private Key used for authentication to Snowflake, formatted according to PKCS8 standards and having standard PEM headers and footers. The header line begins with `-----BEGIN PRIVATE`. Select the **Reference asset** checkbox to upload the private key file. | No |
| Source Schema | The source schema. This schema should contain the Snowflake Stream object that will be consumed. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

#### Kafka Sink Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Kafka Bootstrap Servers | A comma-separated list of Kafka brokers to send data to. | Yes |
| Kafka SASL Mechanism | SASL mechanism used for authentication. Corresponds to the Kafka Client `sasl.mechanism` property. Possible values:   - `PLAIN` - `SCRAM-SHA-256` - `SCRAM-SHA-512` - `AWS_MSK_IAM` | Yes |
| Kafka SASL Username | The username to authenticate to Kafka. | Yes |
| Kafka SASL Password | The password to authenticate to Kafka. | Yes |
| Kafka Security Protocol | Security protocol used to communicate with brokers. Corresponds to the Kafka Client `security.protocol` property. Possible values:   - `PLAINTEXT` - `SASL_PLAINTEXT` - `SASL_SSL` - `SSL` | Yes |
| Kafka Topic | The Kafka topic where CDC messages from the Snowflake Stream will be sent. | Yes |
| Kafka Message Key Field | Specify the database column name that will be used as the Kafka message key. If not specified, the message key will not be set. If specified, the value of this column will be used as a message key. The value of this parameter is case-sensitive. | No |
| Kafka Keystore Filename | A full path to a keystore storing a client key and certificate for mTLS authentication method. Required for mTLS authentication and when the security protocol is SSL. | No |
| Kafka Keystore Type | The type of keystore. Required for mTLS authentication. Possible values:   - `PKCS12` - `JKS` - `BCFKS` | No |
| Kafka Keystore Password | The password used to secure the keystore file. | No |
| Kafka Key Password | A password for the private key stored in the keystore. Required for mTLS authentication. | No |
| Kafka Truststore Filename | A full path to a truststore storing broker certificates. The client will use the certificate from this truststore to verify broker identity. | No |
| Kafka Truststore Type | The type of truststore file. Possible values:   - `PKCS12` - `JKS` - `BCFKS` | No |
| Kafka Truststore Password | A password for the truststore file. | No |

Expand

Show lessSee more

#### Kafka Sink Ingestion Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Snowflake FQN Stream Name | Fully qualified Snowflake stream name. | Yes |

Expand

Show lessSee more

## Run the flow

1. Right-click on the canvas and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.
