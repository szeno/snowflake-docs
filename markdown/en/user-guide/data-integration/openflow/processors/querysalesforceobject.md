# QuerySalesforceObject 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-salesforce-nar

## Description

Retrieves records from a Salesforce sObject. Users can add arbitrary filter conditions by setting the ‘Custom WHERE Condition’ property. The processor can also run a custom query, although record processing is not supported in that case. Supports incremental retrieval: users can define a field in the ‘Age Field’ property that will be used to determine when the record was created. When this property is set the processor will retrieve new records. Incremental loading and record-based processing are only supported in property-based queries. It ‘s also possible to define an initial cutoff value for the age, filtering out all older records even for the first run. In case of’Property Based Query ‘this processor should run on the Primary Node only. FlowFile attribute’ record.count ‘indicates how many records were retrieved and written to the output. The processor can accept an optional input FlowFile and reference the FlowFile attributes in the query. When’Include Deleted Records ‘is true, the processor will include deleted records (soft-deletes) in the results by using the’ queryAll ‘API. The’IsDeleted’ field will be automatically included in the results when querying deleted records.

## Tags

query, salesforce, sobject, soql

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| age-delay | The ending timestamp of the time window will be adjusted earlier by the amount configured in this property. For example, with a property value of 10 seconds, an ending timestamp of 12:30:45 would be changed to 12:30:35. |
| age-field | The name of a TIMESTAMP field that will be used to filter records using a bounded time window. The processor will return only those records with a timestamp value newer than the timestamp recorded after the last processor run. |
| create-zero-record-files | Specifies whether or not to create a FlowFile when the Salesforce REST API does not return any records |
| custom-soql-query | Specify the SOQL query to run. |
| custom-where-condition | A custom expression to be added in the WHERE clause of the query |
| field-names | Comma-separated list of field names requested from the sObject to be queried. When this field is left empty, all fields are queried. |
| include-deleted-records | If true, the processor will include deleted records (IsDeleted = true) in the query results. When enabled, the processor will use the ‘queryAll’ API. |
| initial-age-filter | This property specifies the start time that the processor applies when running the first query. |
| oauth2-access-token-provider | Service providing OAuth2 Access Tokens for authenticating using the HTTP Authorization Header |
| query-type | Choose to provide the query by parameters or a full custom query. |
| read-timeout | Maximum time allowed for reading a response from the Salesforce REST API |
| record-writer | Service used for writing records returned from the Salesforce REST API |
| salesforce-api-version | The version number of the Salesforce REST API appended to the URL after the services/data path. See Salesforce documentation for supported versions |
| salesforce-url | The URL of the Salesforce instance including the domain without additional path information, such as <https://MyDomainName.my.salesforce.com> |
| sobject-name | The Salesforce sObject to be queried |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | When ‘Age Field’ is set, after performing a query the time of execution is stored. Subsequent queries will be augmented with an additional condition so that only records that are newer than the stored execution time (adjusted with the optional value of ‘Age Delay’) will be retrieved. State is stored across the cluster so that this Processor can be run on Primary Node only and if a new Primary Node is selected, the new node can pick up where the previous node left off, without duplicating the data. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The input flowfile gets sent to this relationship when the query fails. |
| original | The input flowfile gets sent to this relationship when the query succeeds. |
| success | For FlowFiles created as a result of a successful query. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer. |
| record.count | Sets the number of records in the FlowFile. |
| total.record.count | Sets the total number of records in the FlowFile. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.salesforce.PutSalesforceObject](/user-guide/data-integration/openflow/processors/putsalesforceobject)
