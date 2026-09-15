# AzureStorageCredentialsControllerServiceLookup\_v12

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides an AzureStorageCredentialsService\_v12 that can be used to dynamically select another AzureStorageCredentialsService\_v12. This service requires an attribute named ‘azure.storage.credentials.name’ to be passed in, and will throw an exception if the attribute is missing. The value of ‘azure.storage.credentials.name’ will be used to select the AzureStorageCredentialsService\_v12 that has been registered with that name. This will allow multiple AzureStorageCredentialsServices\_v12 to be defined and registered, and then selected dynamically at runtime by tagging flow files with the appropriate ‘azure.storage.credentials.name’ attribute.

## Tags

azure, blob, cloud, credentials, microsoft, queue, storage

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
