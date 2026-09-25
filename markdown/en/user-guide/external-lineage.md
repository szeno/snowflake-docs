# External lineage

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

External lineage extends Snowflake’s [native lineage](/user-guide/ui-snowsight-lineage) to include external data sources and
destinations, providing you with visibility into data flows across your entire data ecosystem. It captures lineage from external ETL tools
and source databases to create a unified view of how data moves through your data pipeline.

Lineage can be captured between a Snowflake object and an external object, and also between two external objects. Because an event isn’t
required to include a Snowflake object, a pipeline that moves data through several external systems is represented as a connected chain even
where no Snowflake object sits between them. External lineage captures lineage between individual columns as well as between objects.

[OpenLineage](https://openlineage.io) is an open standard for capturing and sharing data lineage information across diverse data
tools and platforms. Snowflake leverages this framework by accepting OpenLineage-compatible events through a REST endpoint. External tools
like dbt and Apache Airflow can use the endpoint to send lineage metadata to Snowflake, which then incorporates this information into the
native lineage graph displayed in Snowsight.

External lineage REST endpoint
:   Copy code

    ```
    /api/v2/lineage/external-lineage
    ```

Snowflake base URL for REST endpoints
:   Copy code

    ```
    https://<account_identifier>.snowflakecomputing.com
    ```

    Where `account_identifier` is the [account identifier](/user-guide/admin-account-identifier) of your Snowflake account. You
    can use either the account name format or the account locator format as your account identifier.

    For example, if your account identifier is `myorg-dev_account`, then the base URL of the external lineage
    endpoint is: `https://myorg-dev_account.snowflakecomputing.com`

## External lineage workflow

Implementing external lineage for a data tool consists of the following tasks:

1. [Grant the necessary privileges](#label-external-lineage-privilege) to the user who is authenticating to the external lineage
   endpoint, and make sure that user’s role can
   [access the Snowflake objects](#label-external-lineage-object-access) your lineage events reference.
2. [Configure your data tool](#label-external-lineage-configure) to send OpenLineage events to the Snowflake REST endpoint.
3. [Choose an authentication method](#label-external-lineage-auth) that works for Snowflake REST APIs, and then configure your data
   tool to use it to authenticate its requests to the external lineage endpoint.
4. Use your data tool as usual. OpenLineage events are sent to Snowflake automatically and appear in the native lineage graph in
   Snowsight.

If you want to test the external lineage endpoint before you configure a data tool to emit OpenLineage events, see
[Send manual requests to establish lineage](#label-external-lineage-configure-manual).

## View your data lineage

To view data lineage in Snowsight, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) with the [necessary privileges](/user-guide/ui-snowsight-lineage#label-lineage-privileges).
2. In the navigation menu, select **Catalog** » **Explorer**, and then select a [supported object](/user-guide/ui-snowsight-lineage#label-ui-lineage-supported-objects) such as a table or
   view.
3. Select the **Lineage** tab.

When a data tool sends lineage information to Snowflake, external objects appear in the Snowsight lineage graph and are
labeled as an external node. For example:

![Snowsight lineage graph with external objects](/static/images/governance/universal-lineage-external-source.png)

You can select an external object or the line connecting objects to obtain additional information just like you can with native lineage.

You can also query external lineage with SQL. External objects appear in the output of the
[GET\_LINEAGE](/sql-reference/functions/get_lineage-snowflake-core) function, and you can retrieve the lineage of an external object by
anchoring the query on it. For more information, see
[Lineage for objects outside Snowflake](/sql-reference/functions/get_lineage-snowflake-core#label-get-lineage-external-objects).

If you would rather retrieve lineage without using SQL, the external lineage endpoint returns the same edges. For more information, see
[Send requests to retrieve lineage](#label-external-lineage-retrieve).

## Lineage persistence when you recreate a Snowflake object

Whether an external lineage edge survives a Snowflake object being dropped and recreated (for example, with `CREATE OR REPLACE TABLE`, or
`DROP TABLE` followed by `CREATE TABLE`) depends on the direction of the edge, because recreating an object gives it a new internal
identifier even though its name doesn’t change:

- **A Snowflake object that is the source of an edge to an external target** (for example, a table that a BI tool reads) is tracked by its
  fully qualified name rather than its internal identifier. Most external systems reference Snowflake objects only by name; they have no
  way to reference Snowflake’s internal identifiers. Because Snowflake tracks the object by name in this direction, recreating it doesn’t
  break the lineage edge to the external object.
- **A Snowflake object that is the target of an edge from an external source** (for example, a table populated by a pipeline that sends
  lineage events) is tracked by its internal identifier. Recreating this object breaks the existing lineage edge, even though the object’s
  name is unchanged. The producing tool must send a new lineage event that references the recreated object to reestablish the edge.
- **An edge between two Snowflake objects that was captured through external lineage** (for example, from a data pipeline tool that emits
  OpenLineage events for a step that moves data between two Snowflake tables) is also tracked by internal identifier on both ends, and
  breaks the same way if either object is recreated.

## Lineage for externally managed Apache Iceberg™ tables

If an OpenLineage event describes a dataset in a storage namespace (for example, `s3://...`) whose `catalog` and `symlinks` facets identify
a Snowflake Apache Iceberg™ table, Snowflake resolves that dataset to the Snowflake table’s identity instead of recording it as a generic
external node. This applies to externally managed Iceberg tables backed by an external Iceberg REST catalog, not to tables that Snowflake
manages directly.

Resolution requires the `catalog` facet to specify `type: rest` and `framework: iceberg`. A facet naming a different catalog type, such as
AWS Glue, isn’t resolved, and the dataset remains an external node.

If the named table doesn’t resolve, for example because it doesn’t exist or the role sending the request can’t see it, Snowflake records
that one dataset as an external node instead of resolving it. The rest of the event, including any other datasets, is still recorded.

### Example: an OpenLineage event with catalog facets

The following payload sends lineage for a job that reads from one externally managed Iceberg table and writes to another. Both datasets
are in `s3://` namespaces, but their `catalog` and `symlinks` facets identify the Snowflake Iceberg tables backing them, so Snowflake
resolves both to their Snowflake identity instead of recording either as an external node:

Copy code

```
{
   "eventType": "COMPLETE",
   "eventTime": "2026-01-01T00:00:00.000Z",
   "producer": "https://github.com/OpenLineage/OpenLineage/blob/v1-0-0/client",
   "schemaURL": "https://openlineage.io/spec/1-0-0/OpenLineage.json",
   "job": {"namespace": "spark://spark-cluster", "name": "iceberg-etl-job"},
   "run": {"runId": "123e4567-e89b-12d3-a456-426614174000"},
   "inputs": [
      {
         "namespace": "s3://iceberg-lake-src",
         "name": "warehouse/src_events",
         "facets": {
            "catalog": {
               "framework": "iceberg",
               "type": "rest",
               "name": "SALES_CATALOG_DB",
               "metadataUri": "https://catalog.example.com/api/catalog"
            },
            "symlinks": {
               "identifiers": [
                  {"namespace": "https://catalog.example.com/api/catalog", "name": "PUBLIC.SRC_EVENTS", "type": "TABLE"}
               ]
            }
         }
      }
   ],
   "outputs": [
      {
         "namespace": "s3://iceberg-lake-tgt",
         "name": "warehouse/tgt_events",
         "facets": {
            "catalog": {
               "framework": "iceberg",
               "type": "rest",
               "name": "SALES_CATALOG_DB",
               "metadataUri": "https://catalog.example.com/api/catalog"
            },
            "symlinks": {
               "identifiers": [
                  {"namespace": "https://catalog.example.com/api/catalog", "name": "PUBLIC.TGT_EVENTS", "type": "TABLE"}
               ]
            }
         }
      }
   ]
}
```

The `catalog` facet’s `name` and the `symlinks` identifier’s `name` together form the Snowflake table identity that must match:
`<catalog name>.<symlink name>`, which is `SALES_CATALOG_DB.PUBLIC.SRC_EVENTS` for the input above. `SALES_CATALOG_DB` is the name of the
catalog-linked database (or, for a table registered directly with `CATALOG_TABLE_NAME`, the database that registration uses). If that
qualified name doesn’t match a Snowflake Iceberg table registered through the same external catalog, the dataset stays an external node.

### Effect on removing lineage

Resolving a dataset to Snowflake identity changes how you remove its lineage. Before resolution, an edge to or from the dataset is stored
and matched by its storage `namespace` and `name`. After resolution, the edge is stored and matched by the Snowflake table’s identity
instead.

A DELETE request that specifies the original storage `namespace` and `name` for a resolved endpoint doesn’t match the edge, and doesn’t
return an error. To remove lineage for a resolved endpoint, specify the Snowflake object’s database, schema, and table name instead. See
[Send requests to remove lineage](#label-external-lineage-remove).

This change applies only to edges recorded after resolution succeeds. An edge recorded before resolution, or one whose dataset never
resolved, continues to match on its original storage namespace and name.

## Grant Snowflake privileges

After a REST request is [authenticated](#label-external-lineage-auth), Snowflake checks whether the user associated with the request
is authorized to use external lineage. The user associated with the request must have a role that is granted the INGEST LINEAGE privilege
on the account.

For example, suppose you want requests sent by the service user `dbt_integration_user` to show up in Snowsight lineage. As an
administrator, run the following commands to create a dedicated role, grant it the necessary privilege, and then grant the role to the user:

Copy code

```
CREATE ROLE dbt_lineage_role;
GRANT INGEST LINEAGE ON ACCOUNT TO ROLE dbt_lineage_role;
GRANT ROLE dbt_lineage_role TO USER dbt_integration_user;
```

## Access to referenced Snowflake objects

The `INGEST LINEAGE` privilege authorizes a role to use external lineage, but it doesn’t grant access to the objects named in a lineage
event. The role sending the request must also be able to resolve every Snowflake object referenced in the `inputs` and `outputs` properties
of the payload. Snowflake resolves these objects when it receives the request, so the role needs the privileges required to see each object:
typically `USAGE` on the database and schema that contain it, along with a privilege such as `SELECT` on the object itself.

Snowflake resolves the objects using the role that is in effect for the request, which is the default role of the user associated with the
request. Granting the required privileges to a role that the user is granted, but that isn’t in effect for the request, isn’t sufficient. If
the user has no default role, or its default role isn’t the role you granted the privileges to, set the default role explicitly.

If any Snowflake object in the payload can’t be resolved, either because the object doesn’t exist or because the role can’t see it,
Snowflake rejects the whole event with a 400 HTTP status code and error code 394919, and stores no lineage from that event. Because a single
unresolvable object rejects the entire event, the other objects in the same event don’t produce lineage either.

Building on the previous example, the following commands make `dbt_lineage_role` the default role of the user and let it resolve the
objects in the `my_db.my_schema` schema:

Copy code

```
ALTER USER dbt_integration_user SET DEFAULT_ROLE = dbt_lineage_role;
GRANT USAGE ON DATABASE my_db TO ROLE dbt_lineage_role;
GRANT USAGE ON SCHEMA my_db.my_schema TO ROLE dbt_lineage_role;
GRANT SELECT ON ALL TABLES IN SCHEMA my_db.my_schema TO ROLE dbt_lineage_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA my_db.my_schema TO ROLE dbt_lineage_role;
```

Note

`CREATE OR REPLACE TABLE` replaces the object, and privileges granted directly on the previous object aren’t carried over to the new one
unless the statement includes `COPY GRANTS`. If a pipeline recreates the tables that it reports lineage for, grant the privileges at the
schema level using `GRANT SELECT ON FUTURE TABLES IN SCHEMA` as in the previous example, or include `COPY GRANTS` in the
`CREATE OR REPLACE TABLE` statement. Otherwise the role loses access each time a table is replaced, and subsequent lineage events for that
table are rejected.

## Configure your data tool

Note

Any data tool with an OpenLineage integration can be configured to send lineage data to Snowflake. For a full list of tools that have an
integration, see [OpenLineage Integrations](https://github.com/OpenLineage/OpenLineage/tree/main/integration#openlineage-integrations).

The following sections provide basic instructions for using external lineage with dbt and Apache Airflow.

- [Configure dbt to send lineage data to Snowflake](#label-external-lineage-configure-dbt)
- [Configure Airflow to send lineage data to Snowflake](#label-external-lineage-configure-airflow)

### Configure dbt to send lineage data to Snowflake

Note

Configuring dbt to emit OpenLineage events isn’t unique to Snowflake; the only thing specific to Snowflake is the endpoint and base URL
of external lineage.

The following steps provide the minimum configuration you need to set up your dbt environment. Consult the
[OpenLineage dbt documentation](https://openlineage.io/docs/integrations/dbt) and the [OpenLineage specification](https://openlineage.io/apidocs/openapi/) to configure your OpenLineage-dbt integration.

1. Install the [OpenLineage-dbt integration](https://pypi.org/project/openlineage-dbt/):

   Copy code

   ```
   pip3 install openlineage-dbt
   ```
2. Set your transport variables to specify the [base URL](/user-guide/external-lineage#label-external-lineage-base-url),
   [endpoint](/user-guide/external-lineage#label-external-lineage-endpoint), and [security token](#label-external-lineage-auth) for external lineage.

   For example, if the account identifier of your account is `MYORG-DEV_ACCOUNT`, define the following code in your YAML configuration
   file:

   Copy code

   ```
   transport:
   type: http
   url: https://MYORG-DEV_ACCOUNT.snowflakecomputing.com
   endpoint: /api/v2/lineage/external-lineage
   auth:
      type: api_key
      apiKey: eyJ0eXAiOiJKV1QiLsecuritytoken...
   compression: gzip
   ```
3. Replace `dbt` commands with `dbt-ol`. For example, change the `dbt run` command to `dbt-ol run`.

   These `dbt-ol` commands are required by the OpenLineage-dbt integration, and aren’t unique to Snowflake.

For more information about OpenLineage-dbt integrations, including other methods of setting variables, see the
[OpenLineage dbt documentation](https://openlineage.io/docs/integrations/dbt).

### Configure Airflow to send lineage data to Snowflake

Note

Configuring Apache Airflow to emit OpenLineage events isn’t unique to Snowflake; the only thing specific to Snowflake is the endpoint
and base URL of external lineage.

The following steps provide the minimum configuration you need to set up your Airflow environment for Airflow version 2.7+, which is the
preferred version for OpenLineage. Consult the [OpenLineage Airflow documentation](https://openlineage.io/docs/integrations/airflow) and the [OpenLineage specification](https://openlineage.io/apidocs/openapi/) to
configure your OpenLineage-Airflow integration.

1. Install the [OpenLineage Airflow integration](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/index.html#apache-airflow-providers-openlineage)
   for version 2.7+:

   Copy code

   ```
   pip install apache-airflow-providers-openlineage
   ```

   If you use an older version of Airflow, install `openlineage-airflow` instead.
2. Set your transport variables to specify the [base URL](/user-guide/external-lineage#label-external-lineage-base-url),
   [endpoint](/user-guide/external-lineage#label-external-lineage-endpoint), and [security token](#label-external-lineage-auth) for external lineage.

   For example, if the account identifier of your account is `MYORG-DEV_ACCOUNT`, define the following code in your YAML configuration
   file:

   Copy code

   ```
   transport:
   type: http
   url: https://MYORG-DEV_ACCOUNT.snowflakecomputing.com
   endpoint: /api/v2/lineage/external-lineage
   auth:
      type: api_key
      apiKey: eyJ0eXAiOiJKV1QiLsecuritytoken...
   compression: gzip
   ```

For more information about OpenLineage-Airflow integrations, including other methods of setting variables, see the
[OpenLineage Airflow documentation](https://openlineage.io/docs/integrations/airflow).

## Choose an authentication method

Snowflake provides multiple ways to authenticate requests to a Snowflake REST endpoint like the one used by external lineage. For a
complete list of authentication methods, see [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

After you select your preferred authentication method, you must generate a security token for a specific user. The token is used to
associate a user with the REST request so that Snowflake can authenticate the user and verify that the user is
[authorized to use external lineage](#label-external-lineage-privilege).

After successfully associating a user with a security token in Snowflake, you need to configure your data tool to authenticate its requests
with this token. For example, if you use a YAML configuration file to set OpenLineage transport variables, use the following code to
specify the security token that is sent in the header of the request:

Copy code

```
transport:
   auth:
      type: api_key
      apiKey: eyJ0eXAiOiJKV1QiLsecuritytoken...
```

For other methods of specifying a security token, see the OpenLineage documentation for your data tool.

## Send manual requests to establish lineage

External lineage works by accepting JSON payloads that conform to the OpenLineage specification for COMPLETE events. When integrated with a
data tool, the tool emits these COMPLETE events. But you can also construct a COMPLETE event, then send it to the endpoint by using any tool
or language that can send POST requests to an endpoint.

A valid request consists of the following method, [base URL](/user-guide/external-lineage#label-external-lineage-base-url), and [endpoint](/user-guide/external-lineage#label-external-lineage-endpoint):

Copy code

```
POST https://<account_identifier>.snowflakecomputing.com/api/v2/lineage/external-lineage
```

Where `account_identifier` is the [account identifier](/user-guide/admin-account-identifier) of your Snowflake account.

The following example shows how to use curl to send lineage information to external lineage:

Copy code

```
curl -i -X POST \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLsecuritytoken..." \
 -H "Accept: application/json" \
 -H "User-Agent: myApplicationName/1.0" \
 -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
 -d "@request_body.json" \
 "https://MYORG-DEV_ACCOUNT.snowflakecomputing.com/api/v2/lineage/external-lineage"
```

Where `request_body.json` conforms to the OpenLineage specification for COMPLETE events. For more information about this JSON payload, see [Payload requirements](#label-external-lineage-configure-manual-payload).

### Authentication and authorization of a manual request

The authentication and authorization of a manual request sent to the external lineage endpoint are the same as those in a request sent from
a data tool.

- The header of the request must include a security token from one of the
  [forms of authentication](/developer-guide/snowflake-rest-api/authentication) supported by Snowflake REST endpoints.
- The user associated with the security token must have the [proper privileges](#label-external-lineage-privilege).

### Payload requirements

When you send the JSON payload in a manual request to the external lineage endpoint, the payload must meet the following requirements:

- Must conform to the [OpenLineage specification](https://openlineage.io/apidocs/openapi/).
- Must be a COMPLETE event. That is, the `eventType` property must be `COMPLETE`. Events with any other `eventType` are rejected with a
  400 HTTP status code.
- The `inputs` property and `outputs` property can reference Snowflake objects, external objects, or both. Lineage between two external
  objects is supported; an event is no longer required to include at least one Snowflake object.
- Every Snowflake object referenced in the `inputs` and `outputs` properties must exist and must be visible to the role sending the
  request. See [Access to referenced Snowflake objects](#label-external-lineage-object-access).
- Must contain the following properties:

  - `inputs`
  - `outputs`
  - `eventType`
  - `eventTime`
  - `job`

  You can optionally include the `run` property, which is useful in identifying the job. The payload can contain additional
  properties, but Snowflake ignores them.

#### Minimal payload example

The following example shows a minimal payload that you can send to the external lineage endpoint:

Copy code

```
{
   "eventType": "COMPLETE",
   "eventTime": "2025-03-12T06:51:12.000Z",
   "job": {"namespace": "exampleNamespace", "name": "exampleJob"},
   "run": {"runId": "123e4567-e89b-12d3-a456-426614174000"},
   "producer": "https://github.com/OpenLineage/OpenLineage/blob/v1-0-0/client",
   "schemaURL": "https://openlineage.io/spec/0-0-1/OpenLineage.json",
   "inputs": [{"namespace": "snowflake://AXORG-AX_TEST_PP8", "name": "OL_TEST.OL_TEST_SCH.TEST_DEMO"}],
   "outputs": [{"namespace": "postgres://localhost:5432", "name": "PDB.SCH.OUTPUT"}]
}
```

#### Lineage between two external objects

Neither the input nor the output has to be a Snowflake object. The following example establishes lineage between two external systems, so a
pipeline that moves data between them is represented even though no Snowflake object is involved:

Copy code

```
{
   "eventType": "COMPLETE",
   "eventTime": "2025-03-12T06:51:12.000Z",
   "job": {"namespace": "exampleNamespace", "name": "exampleJob"},
   "run": {"runId": "123e4567-e89b-12d3-a456-426614174000"},
   "producer": "https://github.com/OpenLineage/OpenLineage/blob/v1-0-0/client",
   "schemaURL": "https://openlineage.io/spec/0-0-1/OpenLineage.json",
   "inputs": [{"namespace": "s3://example-bucket", "name": "raw/orders"}],
   "outputs": [{"namespace": "postgres://db.company.com:5432", "name": "public.orders_staging"}]
}
```

#### Specifying object types

Within the `outputs` array of the payload, you can use the `facets` field to specify the type of the object, which can be any
user-defined string. For example, the following snippet of the payload specifies that the object is of type VIEW:

Copy code

```
"outputs": [
    {
        "namespace": "postgres://db.company.com:5432",
        "name": "db.schema.view",
        "facets": {"datasetType": {"datasetType": "VIEW"}},
    },
],
```

If you don’t specify a `facets` field, the type of object defaults to `External Node`.

#### Specifying multiple inputs

If a payload includes more than one input, the resulting lineage shows the output as a downstream object of both inputs. For example, if a payload has input A and B along with an output C, then the lineage shows both A-C and B-C.

#### Specifying column lineage

External lineage captures lineage between individual columns as well as between objects. To establish column lineage, use the
`columnLineage` facet of an output dataset. The facet maps each output column to the input columns that it is derived from:

Copy code

```
"outputs": [
    {
        "namespace": "postgres://db.company.com:5432",
        "name": "db.schema.orders_summary",
        "facets": {
            "columnLineage": {
                "fields": {
                    "TOTAL_AMOUNT": {
                        "inputFields": [
                            {
                                "namespace": "snowflake://MYORG-DEV_ACCOUNT",
                                "name": "SALES_DB.PUBLIC.ORDERS",
                                "field": "AMOUNT"
                            }
                        ]
                    }
                }
            }
        }
    }
]
```

Each key in the `fields` object is the name of a column in the output dataset, and each entry in its `inputFields` array identifies a source
column by the `namespace` and `name` of its dataset plus the `field` name of the column.

Keep the following in mind when you specify column lineage:

- The `namespace` and `name` of each `inputFields` entry must match a dataset that is also listed in the `inputs` property of the same
  event. An entry that refers to a dataset outside the event’s `inputs` is ignored.
- Column mappings are captured on a best-effort basis. If a column can’t be resolved, Snowflake skips that mapping and continues. A column
  might not resolve because it was dropped or renamed, or because the role sending the request can’t see it. The event isn’t rejected, and
  the object-level lineage is still recorded.

## Send requests to retrieve lineage

You can retrieve lineage from the external lineage endpoint instead of querying it with SQL. The endpoint is backed by the same engine as
the [GET\_LINEAGE](/sql-reference/functions/get_lineage-snowflake-core) function, so it reports the same edges that `GET_LINEAGE` reports for
the same object, including edges between two Snowflake objects.

A valid request to retrieve lineage consists of the following method, [base URL](/user-guide/external-lineage#label-external-lineage-base-url), and endpoint:

Copy code

```
POST https://<account_identifier>.snowflakecomputing.com/api/v2/lineage/external-lineage:get
```

Note

Retrieving lineage uses the POST method and an endpoint that ends in `:get`, not the GET method. The request identifies the object to
retrieve lineage for in a JSON body, which a GET request can’t carry.

### Access control for retrieving lineage

The user sending a request to retrieve lineage must have the `VIEW LINEAGE` privilege on the account. If the request anchors on a Snowflake
object, the role must also be able to resolve that object, as described in
[Access to referenced Snowflake objects](#label-external-lineage-object-access).

### Request body

The body identifies the object to retrieve lineage for, called the anchor, and supports the following properties:

| Property | Description |
| --- | --- |
| `anchor` | Required. The object whose edges are returned. See [Anchor properties](#label-external-lineage-retrieve-anchor). |
| `filter` | Optional. Narrows the results to edges that connect the anchor to one specific object on the other side. Specify both `namespace` and `name`, and optionally `datasetType`. Specifying only one of them is rejected. |
| `maxDistance` | Optional. The number of hops from the anchor to return edges for. Only `1`, the default, is supported; any other value is rejected. |

Expand

Show lessSee more

#### Anchor properties

Identify the anchor by `namespace` and `name`, which are required together:

| Property | Description |
| --- | --- |
| `side` | Required. Whether the anchor is the source or the target of the edges to return. `SOURCE` returns the objects downstream of the anchor; `TARGET` returns the objects upstream of it. |
| `namespace` | Namespace of the anchor. Required together with `name`. |
| `name` | Name of the anchor. For a Snowflake object, use the fully qualified name. Required together with `namespace`. |
| `datasetType` | Optional type of the anchor, for example TABLE or VIEW. |
| `columnName` | Retrieves the lineage of a column of the anchor rather than of the anchor itself. Supported for objects that aren’t in Snowflake; to retrieve the lineage of a Snowflake column, use `GET_LINEAGE` with the COLUMN domain. Rejected if more than one column of the anchor has this name. |

Expand

Show lessSee more

### Response

The response contains an `edges` array. Each edge has a `source` object and a `target` object, which use the following properties, plus a
`process` object that describes how the lineage was established:

| Property | Description |
| --- | --- |
| `name` | Name of the object. For a column-level edge, this is the column’s parent object, and the column is in `columnName`. |
| `database` | Database that contains the object. Absent for objects that aren’t in Snowflake. |
| `schema` | Schema that contains the object. Absent for objects that aren’t in Snowflake. |
| `namespace` | Namespace of the object. |
| `datasetType` | Granular type of the object, for example TABLE or VIEW. |
| `domain` | Domain of the object. For an object that isn’t in Snowflake, this is EXTERNAL, or EXTERNAL\_COLUMN for one of its columns. |
| `columnName` | Name of the column. Present only on column-level edges. |
| `status` | Status of the object, for example ACTIVE or DELETED. |
| `version` | Version of the object. Present only for models and datasets. |
| `origin` | Where the object’s lineage came from: NATIVE for a Snowflake object, SNOWFLAKE\_CONNECTOR for one ingested by a connector, or OPEN\_LINEAGE for one you ingested. |
| `externalId` | Identifier of an object that isn’t in Snowflake. Absent for Snowflake objects. |

Expand

Show lessSee more

The values of these properties match the corresponding `SOURCE_*` and `TARGET_*` columns that `GET_LINEAGE` returns for the same edge. For
descriptions of those columns, see [GET\_LINEAGE](/sql-reference/functions/get_lineage-snowflake-core).

#### Example: Retrieve the lineage of a Snowflake table

The following example retrieves the objects immediately downstream of a Snowflake table, including objects that aren’t in Snowflake:

Copy code

```
curl -i -X POST \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLsecuritytoken..." \
 -H "Accept: application/json" \
 -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
 -d '{"anchor": {"side": "SOURCE", "namespace": "snowflake://MYORG-DEV_ACCOUNT", "name": "SALES_DB.PUBLIC.ORDERS"}}' \
 "https://MYORG-DEV_ACCOUNT.snowflakecomputing.com/api/v2/lineage/external-lineage:get"
```

The response is similar to the following:

Copy code

```
{
   "edges": [
      {
         "source": {
            "name": "ORDERS",
            "database": "SALES_DB",
            "schema": "PUBLIC",
            "domain": "TABLE",
            "origin": "NATIVE",
            "status": "ACTIVE"
         },
         "target": {
            "name": "public.orders_staging",
            "namespace": "postgres://db.company.com:5432",
            "domain": "EXTERNAL",
            "origin": "OPEN_LINEAGE"
         },
         "process": {"runId": "123e4567-e89b-12d3-a456-426614174000"}
      }
   ]
}
```

#### Example: Retrieve the lineage of an object outside Snowflake

To continue from an object that isn’t in Snowflake, anchor on it by passing its `namespace` along with its `name`. The following example
uses the target returned by the previous example to retrieve what that object feeds:

Copy code

```
curl -i -X POST \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLsecuritytoken..." \
 -H "Accept: application/json" \
 -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
 -d '{"anchor": {"side": "SOURCE", "namespace": "postgres://db.company.com:5432", "name": "public.orders_staging"}}' \
 "https://MYORG-DEV_ACCOUNT.snowflakecomputing.com/api/v2/lineage/external-lineage:get"
```

Repeat this pattern to follow a chain of objects outside Snowflake one step at a time.

#### Retrieving lineage considerations

Keep the following in mind when you retrieve lineage:

- The endpoint returns only the edges immediately connected to the anchor. To follow a longer chain, anchor a new request on an object from
  the previous response.
- If the anchor is a Snowflake object whose name no longer resolves to an existing object, the response contains an empty `edges` array
  rather than an error. Recreating an object can also break its existing edges. For more information, see
  [Lineage persistence when you recreate a Snowflake object](#label-external-lineage-object-identity).
- A request that specifies a `maxDistance` other than `1`, an anchor that is missing `side`, `namespace`, or `name`, or a partially
  specified `filter` is rejected with a 400 HTTP status code.

## Send requests to remove lineage

You can send a DELETE request to the external lineage endpoint to remove lineage that was established between a Snowflake object and an
external object.

- To break lineage between the source object and target object, use URL query parameters to specify details about the two objects.
- To break lineage between an object and all of its downstream objects, specify the source object without specifying a target object.
- To remove a target object from the lineage graph regardless of how many objects are upstream of it, specify the target object without
  specifying a source object.

A valid request to remove lineage consists of the following method, [base URL](/user-guide/external-lineage#label-external-lineage-base-url), and [endpoint](/user-guide/external-lineage#label-external-lineage-endpoint):

Copy code

```
DELETE https://<account_identifier>.snowflakecomputing.com/api/v2/lineage/external-lineage
```

| Query parameter | Description |
| --- | --- |
| `sourceNamespace={namespace}` | Namespace of the source dataset. |
| `sourceName={FQN}` | Fully qualified name of the source dataset. |
| `sourceDatasetType={dataset type}` | Type of the source dataset (for example, TABLE, VIEW, DATASET). By default, the value should be External Node. If you provided a value in the `facets` field of the payload when you sent a request to establish lineage, then specify the value that you sent in the payload, not External Node. |
| `targetNamespace={namespace}` | Namespace of the target dataset. |
| `targetName={FQN}` | Fully qualified name of the target dataset. |
| `targetDatasetType={dataset type}` | Type of the target dataset (for example, TABLE, VIEW, DATASET). By default, the value should be External Node (`External%20Node`). If you provided a value in the `facets` field of the payload when you sent a request to establish lineage, then specify the value that you sent in the payload, not External Node. |

Expand

Show lessSee more

Note

The values of the query parameters are case sensitive.

Important

These query parameters match an edge by its original storage `namespace` and `name`. If the dataset has since resolved to Snowflake
identity, for example an externally managed Iceberg table resolved through catalog facets, these parameters no longer match it. Specify
the Snowflake object’s database, schema, and table name instead. See
[Lineage for externally managed Apache Iceberg™ tables](#label-external-lineage-iceberg-catalog-resolution).

### Access control for removing lineage

The user sending a request to remove lineage between objects must have the DELETE LINEAGE privilege on the account.

## Limitations and considerations

- Snowflake doesn’t support OpenLineage version 2.
- The retention period for external lineage events is one year.
- Snowflake only accepts COMPLETE lineage events. Events with a different `eventType`, for example START or FAIL, are rejected with a 400
  HTTP status code. Data tools that emit a full event lifecycle therefore receive 400 responses for their non-COMPLETE events. This is
  expected and doesn’t indicate a problem with the COMPLETE events that the same tool sends.
- Every Snowflake object referenced in an event must exist and be visible to the role sending the request, or the event is rejected. See
  [Access to referenced Snowflake objects](#label-external-lineage-object-access).
- Dropping and recreating a Snowflake object can break its external lineage edges, depending on the direction of the edge. See
  [Lineage persistence when you recreate a Snowflake object](#label-external-lineage-object-identity).
- Resolving an externally managed Iceberg table to Snowflake identity changes how you remove its lineage. See
  [Lineage for externally managed Apache Iceberg™ tables](#label-external-lineage-iceberg-catalog-resolution).
- A request to retrieve lineage returns only the edges immediately connected to the anchor object. See
  [Send requests to retrieve lineage](#label-external-lineage-retrieve).
- The fully qualified name of a dataset — that is, the input or output — can’t exceed 1000 characters.
- A single event can’t produce more than 15,000 lineage edges. An event produces one edge for each combination of input and output, so an
  event with 100 inputs and 200 outputs produces 20,000 edges and is rejected.
- You can’t store more than 20,000 external lineage edges in the same account. If you reach this limit, you must delete edges before adding
  new ones.
