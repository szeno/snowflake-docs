# UpdateTableState 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Updates the state of a table in the Table State Service

## Tags

snowflake, state, table

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| CDC Schema Registry | When the state of the table is removed, the table will also be removed from the specified CDC Schema Registry. |
| Desired State | The desired state of the table |
| Overwrite Existing | Whether to overwrite the existing state of the table. If false, the state will only be updated if the state is currently unknown. |
| Schema Name | The name of the table’s schema |
| Table Name | The name of the table |
| Table State Service | The Table State Service to update |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms failure | A FlowFile is routed to this relationship if the table state could not be updated due to a communication failure with the Table State Service |
| state exists | A FlowFile is routed to this relationship if the table state was not updated because the state is already known for the table and the ‘Overwrite Existing’ property is set to ‘false’ |
| success | A FlowFile is routed to this relationship after the table state has been updated |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| table.state | The state of the table after updating the Table State Service |
| previous.table.state | The state of the table before the Table State Service was updated |

Expand

Show lessSee more
