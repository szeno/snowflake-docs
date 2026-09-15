Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Configuring Private Key Authentication for Snowflake

The Kafka and Kinesis high-performance connectors use `PublishSnowpipeStreaming` to write data to Snowflake. By default they authenticate using `SNOWFLAKE_MANAGED` (session token). This page describes how to switch to key-pair authentication using an RSA private key.

Note

`SNOWFLAKE_MANAGED` is the recommended authentication strategy for both SPCS and BYOC deployments. Use Private Key authentication only when managed authentication is not suitable for your environment.

The steps below apply identically to the Kafka and Kinesis high-performance connectors.

## Prerequisites

### Generate an RSA key pair and assign it to a Snowflake user

Follow the official Snowflake guide to generate a key pair and assign the public key to your user: [Key-pair authentication and key-pair rotation](/en/user-guide/key-pair-auth).

Note

Both encrypted and unencrypted private keys are supported. If you generate an encrypted key (with a passphrase), set the **Key Password** property on the `StandardPrivateKeyService` controller service. The resulting `rsa_key.p8` file must begin with the header `-----BEGIN PRIVATE KEY-----` (unencrypted) or `-----BEGIN ENCRYPTED PRIVATE KEY-----` (encrypted).

## Step 1: Add a StandardPrivateKeyService controller service

1. Open the connector’s process group in the Openflow / NiFi UI.
2. Select **Configure** > **Controller Services** (gear icon).
3. Select **+** to add a new controller service.
4. Search for and select [StandardPrivateKeyService](/user-guide/data-integration/openflow/controllers/standardprivatekeyservice).
5. Select **Add**.

## Step 2: Upload the private key file

1. In the controller services list, select the **Edit** (pencil) icon on `StandardPrivateKeyService`.
2. Locate the **Key File** property.
3. Enable the **Reference asset** checkbox next to the field.
4. Select **Upload** and select your `rsa_key.p8` file. Openflow stores the file as an asset on the cluster so the key is never exposed in plain text in the configuration.
5. Leave **Key Password** blank for an unencrypted key, or provide the passphrase for an encrypted key.
6. Select **Apply**.

## Step 3: Enable the controller service

Select the **Enable** (lightning bolt) icon on `StandardPrivateKeyService` and wait until its status shows **Enabled**.

## Step 4: Configure PublishSnowpipeStreaming

1. Double-click the `PublishSnowpipeStreaming` processor to open its properties.
2. Set the following properties:

| Property | Value |
| --- | --- |
| **Authentication Strategy** | `KEY_PAIR` |
| **Account** | Your Snowflake account identifier, for example `myorg-myaccount` |
| **User** | Your Snowflake username |
| **Role** | Your Snowflake role |
| **Private Key Service** | Select the `StandardPrivateKeyService` created in [Step 1: Add a StandardPrivateKeyService controller service](#label-openflow-streaming-private-key-auth-step1) |

Expand

Show lessSee more

Note

**Account identifier format:** Use the organization-and-account format `<org_name>-<account_name>`, not the full hostname. For example, if your Snowflake URL is `https://myorg-myaccount.snowflakecomputing.com`, the account identifier is `myorg-myaccount`.

3. Select **Apply**.
4. Start the process group.

## Property reference

The [StandardPrivateKeyService](/user-guide/data-integration/openflow/controllers/standardprivatekeyservice) controller service accepts the following properties:

| Property | Description |
| --- | --- |
| `Key File` | Path to the PKCS8 PEM private key file. Use **Reference asset** to upload the file directly to the cluster. |
| `Key` | Inline PEM key content (alternative to `Key File`). |
| `Key Password` | Passphrase for an encrypted private key. Leave blank for unencrypted keys. |

Expand

Show lessSee more

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `PublishSnowpipeStreaming` shows validation errors after applying | `StandardPrivateKeyService` is not yet enabled — enable it before starting the processor. |
| Authentication failure at runtime | Verify the public key is correctly assigned to the Snowflake user (`DESC USER <username>` should show `RSA_PUBLIC_KEY` set). |
| `BEGIN ENCRYPTED PRIVATE KEY` in key file but auth fails | Encrypted key in use — ensure `Key Password` is set on `StandardPrivateKeyService`. |
| Wrong account identifier format | Use `<org>-<account>` without `.snowflakecomputing.com`. |

Expand

Show lessSee more
