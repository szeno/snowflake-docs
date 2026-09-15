Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

# Snowflake Openflow Connector for Kafka: Configuring mTLS Authentication

mTLS (mutual Transport Layer Security) authentication requires both the client and server to present certificates for mutual authentication.

## Prerequisites

Before configuring mTLS authentication, ensure you have:

1. Generated and configured the necessary certificates for both the connector and the Kafka broker.
2. Created a keystore containing the connector’s private key and certificate.
3. (Optional) Created a truststore containing the Kafka broker certificate or a certificate in the certification chain.
   This step is only required if the broker certificate is not signed by a trusted Certificate Authority (CA).
4. The supported keystore/truststore formats are PKCS12, JKS, and BCFKS.

## Step 1: Configure SSL Context Service

From the Openflow NiFi canvas, access the Controller Services configuration:

1. Double-click on the connector’s processing group.
2. Right-click on the canvas and select **Controller Services**.

Add a new **StandardSSLContextService**:

1. Select **+** to add a new controller service.
2. Select **StandardSSLContextService** from the list.
3. Select **Add**.

Configure the SSL Context Service properties:

| Property | Value |
| --- | --- |
| Keystore Filename | Full path to your keystore file (for example, `/path/to/client-keystore.p12`), or Asset reference |
| Keystore Password | Password for the keystore |
| Keystore Type | Keystore format (`PKCS12`, `JKS`, or `BCFKS`) |
| Key Password | Password for the private key (if the key is encrypted) |
| Truststore Filename | Full path to your truststore file (for example, `/path/to/client-truststore.p12`), or Asset reference |
| Truststore Password | Password for the truststore |
| Truststore Type | Truststore format (`PKCS12`, `JKS`, or `BCFKS`) |

Expand

Show lessSee more

Enable the SSL Context Service:

1. Select **Enable** for the service.
2. Confirm that the service status shows as **Enabled**.

## Configuring PEM-encoded SSL context

If your certificates and keys are in PEM format (`.pem`, `.crt`, `.key`) rather than in a JKS or PKCS12 keystore, use the `PEMEncodedSSLContextProvider` controller service instead of `StandardSSLContextService`.

1. In the **Controller Services** tab, select **+** to add a new controller service.
2. Select **PEMEncodedSSLContextProvider** from the list.
3. Select **Add**.
4. Configure the service properties:

| Property | Value |
| --- | --- |
| Certificate | Path to your PEM-encoded certificate file (`.pem`, `.crt`), or Asset reference (see [Ops parameters and assets](/user-guide/data-integration/openflow/ops-parameters-assets)) |
| Private Key | Path to your PEM-encoded private key file (`.key`), or Asset reference |
| CA Certificate | Path to the CA certificate file, or Asset reference. Required only if the broker certificate is not signed by a trusted CA. |

Expand

Show lessSee more

5. **Enable** the service.
6. In [Step 2](#label-openflow-kafka-mtls-auth-step2), set **SSL Context Service** to this `PEMEncodedSSLContextProvider` instead of the `StandardSSLContextService`.

## Step 2: Configure Kafka3Connection Service

1. In the same **Controller Services** tab, locate the [Kafka3Connection service](/user-guide/data-integration/openflow/controllers/kafka3connectionservice).
2. Configure the following properties:

| Property | Value |
| --- | --- |
| Security Protocol | `SSL` |
| SSL Context Service | Select the SSL Context Service you created in [Step 1: Configure SSL Context Service](#label-openflow-kafka-mtls-auth-step1) |

Expand

Show lessSee more

3. Keep all other [Kafka3Connection service](/user-guide/data-integration/openflow/controllers/kafka3connectionservice) settings unchanged.
4. Verify the Kafka3Connection service:
   1. Select **Verify** for the service.
   2. Confirm that the service status shows as **Verified**.
