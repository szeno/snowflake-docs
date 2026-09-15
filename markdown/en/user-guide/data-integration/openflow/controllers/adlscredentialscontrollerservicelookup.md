# ADLSCredentialsControllerServiceLookup

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides an ADLSCredentialsService that can be used to dynamically select another ADLSCredentialsService. This service requires an attribute named ‘adls.credentials.name’ to be passed in, and will throw an exception if the attribute is missing. The value of ‘adls.credentials.name’ will be used to select the ADLSCredentialsService that has been registered with that name. This will allow multiple ADLSCredentialsServices to be defined and registered, and then selected dynamically at runtime by tagging flow files with the appropriate ‘adls.credentials.name’ attribute.

## Tags

adls, azure, cloud, credentials, microsoft, storage

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
