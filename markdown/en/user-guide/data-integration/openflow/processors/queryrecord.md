# QueryRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Evaluates one or more SQL queries against the contents of a FlowFile. The result of the SQL query then becomes the content of the output FlowFile. This can be used, for example, for field-specific filtering, transformation, and row-level filtering. Columns can be renamed, simple calculations and aggregations performed, etc. The Processor is configured with a Record Reader Controller Service and a Record Writer service so as to allow flexibility in incoming and outgoing data formats. The Processor must be configured with at least one user-defined property. The name of the Property is the Relationship to route data to, and the value of the Property is a SQL SELECT statement that is used to specify how input data should be transformed/filtered. The SQL statement must be valid ANSI SQL and is powered by Apache Calcite. If the transformation fails, the original FlowFile is routed to the ‘failure’ relationship. Otherwise, the data selected will be routed to the associated relationship. If the Record Writer chooses to inherit the schema from the Record, it is important to note that the schema that is inherited will be from the ResultSet, rather than the input Record. This allows a single instance of the QueryRecord processor to have multiple queries, each of which returns a different set of columns and aggregations. As a result, though, the schema that is derived will have no schema name, so it is important that the configured Record Writer not attempt to write the Schema Name as an attribute if inheriting the Schema from the Record. See the Processor Usage documentation for more information.

## Tags

aggregate, avro, calcite, csv, etl, filter, json, logs, modify, query, record, route, select, sql, text, transform, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Default Decimal Precision | When a DECIMAL/NUMBER value is written as a ‘decimal’ Avro logical type, a specific ‘precision’ denoting number of available digits is required. Generally, precision is defined by column data type definition or database engines default. However undefined precision (0) can be returned from some database engines. ‘Default Decimal Precision’ is used when writing those undefined precision numbers. |
| Default Decimal Scale | When a DECIMAL/NUMBER value is written as a ‘decimal’ Avro logical type, a specific ‘scale’ denoting number of available decimal digits is required. Generally, scale is defined by column data type definition or database engines default. However when undefined precision (0) is returned, scale can also be uncertain with some database engines. ‘Default Decimal Scale’ is used when writing those undefined numbers. If a value has more decimals than specified scale, then the value will be rounded-up, e.g. 1.53 becomes 2 with scale 0, and 1.5 with scale 1. |
| include-zero-record-flowfiles | When running the SQL statement against an incoming FlowFile, if the result has no data, this property specifies whether or not a FlowFile will be sent to the corresponding relationship |
| record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema |
| record-writer | Specifies the Controller Service to use for writing results to a FlowFile |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, the SQL statement contains columns not present in input data), the original FlowFile it will be routed to this relationship |
| original | The original FlowFile is routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records selected by the query |
| QueryRecord.Route | The relation to which the FlowFile was routed |

Expand

Show lessSee more

## Use cases

| Filter out records based on the values of the records’ fields |
| --- |
| Keep only specific records |
| Keep only specific fields in a a Record, where the names of the fields to keep are known |
| Route record-oriented data for processing based on its contents |

Expand

Show lessSee more
