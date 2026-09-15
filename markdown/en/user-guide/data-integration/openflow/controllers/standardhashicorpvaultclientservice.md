# StandardHashiCorpVaultClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A controller service for interacting with HashiCorp Vault.

## Tags

client, hashicorp, vault

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Configuration Strategy \* | configuration-strategy | direct-properties | - Direct Properties - Properties Files | Specifies the source of the configuration properties. |
| Vault Authentication \* | vault.authentication | TOKEN | - TOKEN - APPID - APPROLE - AWS\_EC2 - AZURE - CERT - CUBBYHOLE - KUBERNETES | Vault authentication method, as described in the Spring Vault Environment Configuration documentation (<https://docs.spring.io/spring-vault/docs/2.3.x/reference/html/#vault.core.environment-vault-configuration>). |
| Connection Timeout \* | vault.connection.timeout | 5 sec |  | The connection timeout for the HashiCorp Vault client |
| Vault Properties Files \* | vault.properties.files |  |  | A comma-separated list of files containing HashiCorp Vault configuration properties, as described in the Spring Vault Environment Configuration documentation (<https://docs.spring.io/spring-vault/docs/2.3.x/reference/html/#vault.core.environment-vault-configuration>). All of the Spring property keys and authentication-specific property keys are supported. |
| Read Timeout \* | vault.read.timeout | 15 sec |  | The read timeout for the HashiCorp Vault client |
| SSL Context Service | vault.ssl.context.service |  |  | The SSL Context Service used to provide client certificate information for TLS/SSL connections to the HashiCorp Vault server. |
| Vault URI \* | vault.uri |  |  | The URI of the HashiCorp Vault server (e.g., <http://localhost:8200>). Required if not specified in the Bootstrap HashiCorp Vault Configuration File. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
