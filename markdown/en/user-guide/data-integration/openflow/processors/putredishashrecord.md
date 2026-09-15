# PutRedisHashRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-redis-nar

## Description

Puts record field data into Redis using a specified hash value, which is determined by a RecordPath to a field in each record containing the hash value. The record fields and values are stored as key/value pairs associated by the hash value. NOTE: Neither the evaluated hash value nor any of the field values can be null. If the hash value is null, the FlowFile will be routed to failure. For each of the field values, if the value is null that field will be not set in Redis.

## Tags

hash, put, record, redis

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| charset | Specifies the character set to use when storing record field values as strings. All fields will be converted to strings using this character set before being stored in Redis. |
| data-record-path | This property denotes a RecordPath that will be evaluated against each incoming Record and the Record that results from evaluating the RecordPath will be sent to Redis instead of sending the entire incoming Record. The property defaults to the root ‘/’ which corresponds to a ‘flat’ record (all fields/values at the top level of the Record. |
| hash-value-record-path | Specifies a RecordPath to evaluate against each Record in order to determine the hash value associated with all the record fields/values (see ‘hset’ in Redis documentation for more details). The RecordPath must point at exactly one field or an error will occur. |
| record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema |
| redis-connection-pool |  |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles containing Records with processing errors will be routed to this relationship |
| success | FlowFiles having all Records stored in Redis will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| redis.success.record.count | Number of records written to Redis |

Expand

Show lessSee more
