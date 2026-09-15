# WaitForTableState 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Blocks incoming FlowFiles until the corresponding table state is not equal to accepted state. Blocked FlowFiles stay in the upstream queue. When table is in terminated state or table is removed from the state then all FlowFiles are routed to the ‘failure’ relationship.

## Tags

cdc, event, jdbc, mysql, postgresql, sql

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Accepted State | Blocks FlowFiles for a given SourceTableFQN until corresponding state is equal to the Accepted State |
| Table State Service | Manages the state of each replicated table |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles for tables in terminal states will be routed to this relationship |
| success | FlowFiles fulfilling a given condition will be routed to this relationship |

Expand

Show lessSee more
