# MongoDBLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a lookup service based around MongoDB. Each key that is specified will be added to a query as-is. For example, if you specify the two keys, user and email, the resulting query will be { “user”: “tester”, “email”: “[tester@test.com](mailto:tester@test.com)” }. The query is limited to the first result (findOne in the Mongo documentation). If no “Lookup Value Field” is specified then the entire MongoDB result document minus the \_id field will be returned as a record.

## Tags

lookup, mongo, mongodb, record

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Schema Access Strategy \* | Schema Access Strategy | infer | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Infer from Result | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Mongo Collection Name \* | mongo-collection-name |  |  | The name of the collection to use |
| Mongo Database Name \* | mongo-db-name |  |  | The name of the database to use |
| Client Service \* | mongo-lookup-client-service |  |  | A MongoDB controller service to use with this lookup service. |
| Projection | mongo-lookup-projection |  |  | Specifies a projection for limiting which fields will be returned. |
| Lookup Value Field | mongo-lookup-value-field |  |  | The field whose value will be returned when the lookup key(s) match a record. If not specified then the entire MongoDB result document minus the \_id field will be returned as a record. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
