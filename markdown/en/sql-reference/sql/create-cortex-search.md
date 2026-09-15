# CREATE CORTEX SEARCH SERVICE

Creates a new [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) or replaces an existing one.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CORTEX SEARCH SERVICE [ IF NOT EXISTS ] <name>
  ON <search_column>
  [ PRIMARY KEY ( <col_name> [, ... ] ) ]
  ATTRIBUTES <col_name> [ , ... ]
  WAREHOUSE = <warehouse_name>
  TARGET_LAG = '<num> { seconds | minutes | hours | days }'
  [ EMBEDDING_MODEL = <embedding_model_name> ]
  [ REFRESH_MODE = { FULL | INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ FULL_INDEX_BUILD_INTERVAL_DAYS = <num> ]
  [ REQUEST_LOGGING = { TRUE | FALSE } ]
  [ AUTO_SUSPEND = <num_seconds> ]
  [ COMMENT = '<comment>' ]
AS <query>;

CREATE [ OR REPLACE ] CORTEX SEARCH SERVICE <name>
  TEXT INDEXES <text_column_name> [ , ... ]
  VECTOR INDEXES <column_specification> [ , ... ]
  [ PRIMARY KEY ( <col_name> [, ... ] ) ]
  ATTRIBUTES <col_name> [ , ... ]
  WAREHOUSE = <warehouse_name>
  TARGET_LAG = '<num> { seconds | minutes | hours | days }'
  [ REFRESH_MODE = { FULL | INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ FULL_INDEX_BUILD_INTERVAL_DAYS = <num> ]
  [ REQUEST_LOGGING = { TRUE | FALSE } ]
  [ AUTO_SUSPEND = <num_seconds> ]
  [ COMMENT = '<comment>' ]
AS <query>;
```

## Required parameters

`name`
:   String that specifies the identifier (that is, the name) for the Cortex Search service; must be unique for the schema in which the service is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ON search_column`
:   Specifies the text column in the base table that you wish to search on, for single-index Cortex Search. This column must be a text value.

`TEXT INDEXES text_column_name [, ... ]`
:   Specifies comma-separated text columns in the base table to search on, for multi-index Cortex Search. Columns must be text values.

`VECTOR INDEXES column_specification [ , ... ]`
:   Specifies columns for vector similarity searches. Column specifications include:

    - *Managed vector embeddings*: `text_column_name (model='embedding_model')`: Specifies a text column and the embedding model used for vector generation.
      Must use one of the [supported embedding models](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-regional-availability). If no model is specified,
      the default model `snowflake-arctic-embed-m-v1.5` is used.
    - *User-provided vector embeddings*: `vector_column_name`: Specifies a user-provided vector embedding column.
    - *User-provided vector embeddings with managed query embeddings*: `vector_column_name(query_model='embedding_model')`:
      Specifies a user-provided vector embedding column and the embedding model used for embedding text at query time.
      The `query_model` must be one of the [Snowflake-managed embedding models supported in Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-embedding-models).
      If no `query_model` is specified, then the user-provided vector column can only be used with a vector embedding query.

    For information on the behavior of vector embeddings, see [Usage Notes](#label-create-cortex-search-usage).

`ATTRIBUTES col_name [ , ... ]`
:   Specifies a comma-separated list of columns in the base table that you wish to filter on when issuing queries to the service.
    Attribute columns must be included in the source query, either via explicit enumeration or a wildcard (`*`).

`WAREHOUSE = warehouse_name`
:   Specifies the warehouse to use for running the source query, building the search index, and keeping it refreshed per the `TARGET_LAG` target.

`TARGET_LAG = 'num { seconds | minutes | hours | days }'`
:   Specifies the maximum amount of time that the Cortex Search service content should lag behind updates to the base tables specified in the source query.

    Note

    Ensure that the target lag is shorter than the data retention period of the source tables. If the target lag exceeds the data retention period, the service may be unable to detect changes in the source data and could require recreation. For more information, see [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days).

## Optional parameters

`PRIMARY KEY ( col_name [, ... ] )`
:   Specifies a set of columns that uniquely identify each row in the source query. The combination of values in the
    designated columns must be unique for each row; rows with duplicate primary key values are ignored in the resulting
    search index. Primary key columns must be of the [TEXT](/sql-reference/data-types-text) data type. Services
    with primary keys can make use of an optimized refresh path when the underlying data changes, resulting in significant
    reductions to the cost and latency of a refresh. For more information, see [Primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys).

`EMBEDDING_MODEL = <embedding_model_name>`
:   Optional parameter that specifies the embedding model to use in the Cortex Search Service. This property cannot be altered after you create the Cortex
    Search Service. To modify the property, recreate the Cortex Search Service with a CREATE OR REPLACE CORTEX SEARCH SERVICE command.

    Some embedding models are only available in certain cloud regions for Cortex Search.
    For an availability list by model by region, see
    [Cortex Search Regional Availability](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-regional-availability).

    Each model may incur a different cost per million input tokens processed.
    Refer to the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for each function’s cost in credits per million tokens.

    If the *EMBEDDING\_MODEL* is not specified, the default model is used. The default model is *snowflake-arctic-embed-m-v1.5*.

`REFRESH_MODE = { FULL | INCREMENTAL }`
:   Specifies the refresh mode for the Cortex Search Service.

    This property cannot be altered after you create the Cortex Search Service. To modify the property, recreate the Cortex Search
    Service with a CREATE OR REPLACE CORTEX SEARCH SERVICE command.

    > `FULL`
    > :   Enforces a full refresh of the Cortex Search Service. A full refresh recomputes all embeddings and rebuilds the index on every
    >     change to the underlying source data. Given the cost of recomputing embeddings, full refresh should only be considered if incremental
    >     refresh is not supported for your workload.
    >
    > `INCREMENTAL`
    > :   Enforces an incremental refresh of the Cortex Search Service. An incremental refresh applies only the changes since the
    >     last refresh, making it more efficient for large datasets with small updates. If the Cortex Search Service cannot perform
    >     an incremental refresh, service creation fails and displays an error message.
    >
    >     Incremental refresh requires change tracking to be enabled on all underlying objects. For more information, see
    >     [Change Tracking Requirements](#label-cortex-search-change-tracking-requirements).
    >
    > Default: `INCREMENTAL`

`INITIALIZE`
:   Specifies the behavior of the initial [refresh](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-refreshes) of the Cortex Search Service. This property cannot be
    altered after you create the service. To modify the property, replace the cortex search service with a CREATE OR REPLACE CORTEX SEARCH SERVICE command.

    > `ON_CREATE`
    > :   Refreshes the Cortex Search Service synchronously at creation. If this refresh fails, service creation fails and displays an error message.
    >
    > `ON_SCHEDULE`
    > :   Refreshes the Cortex Search Service at the next scheduled refresh.
    >
    >     The Cortex Search Service is populated when the refresh schedule process runs. No data is populated when the Cortex Search Service is created.
    >     If you try to query the service, you might see the following error because the first scheduled refresh has not yet occurred.
    >
    >     ```
    >     Your service has not yet been loaded into our serving system. Please retry your request in a few minutes.
    >     ```
    >
    > Default: `ON_CREATE`

`FULL_INDEX_BUILD_INTERVAL_DAYS = num`
:   Specifies the target interval, in days, between full index rebuilds for a Cortex Search service with
    [primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) defined. This property is only applicable to services that have primary keys set.

    Services with primary keys use an optimized refresh path where each refresh cycle (governed by `TARGET_LAG`) processes
    only the rows that changed since the last refresh, rather than re-embedding all data. Over time, these incremental
    updates accumulate fragmented index segments. A full index rebuild compacts these segments into a single optimized
    index. The rebuild does not re-embed unchanged data.

    This value is a soft target. Full index rebuilds may occur more frequently than the specified interval to optimize
    serving performance based on factors such as service target lag, change rate in the service source data, and overall
    service size.

    Default: 1

`REQUEST_LOGGING = { TRUE | FALSE }`
:   Enables or disables request logging for the Cortex Search Service. When enabled, the service records
    information about search requests, which you can query for monitoring and analysis purposes.
    For more information, see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor).

    Default: `FALSE`

`AUTO_SUSPEND = num_seconds`
:   Enables automatic suspension of the service’s serving compute after the specified number of
    seconds of query inactivity. The service automatically resumes when it receives a query.
    Minimum: `1800` (30 minutes). For more information, see
    [Auto-suspend serving on inactivity](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-auto-suspend-serving).

    Default: `NULL` (auto-suspend disabled)

`COMMENT = 'comment'`
:   Specifies a comment for the service.

`AS query`
:   Specifies a query defining the base table from which the service is created.

## Access Control Requirements

| Privilege | Object |
| --- | --- |
| CREATE CORTEX SEARCH SERVICE | Schema in which you are creating the search service. |
| SELECT | Tables and views that the service queries. |
| USAGE | Warehouse that refreshes the service. |

Expand

Show lessSee more

Attention

To create a Cortex Search Service, your role must have the required privileges to use the Cortex embedding functions.
This requires granting the [SNOWFLAKE.CORTEX\_USER](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user) database role
or the [SNOWFLAKE.CORTEX\_EMBED\_USER](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-embed-user) database
role to the service creator role.

## Usage Notes

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The size of the warehouse used to run the Cortex Search service source query does impact the speed and cost of each refresh. A
  larger warehouse decreases build and refresh time. However, during this preview, Snowflake recommends using a warehouse size no larger
  than MEDIUM for Cortex Search services.
- Snowflake recommends using a dedicated warehouse for each Cortex Search service so as to not interfere with other workloads.
- The search index is built as part of the create statement, which means the CREATE CORTEX SEARCH SERVICE statement may take longer to
  complete for larger datasets.
- When creating a multi-index search service, at least one column must be specified in the VECTOR INDEXES clause in order to ensure the highest quality of search results. Attempting to create a service with no vector indexes returns an error.
- A column can be specified in the TEXT INDEXES clause, the VECTOR INDEXES clause, or both:

  - Columns specified as text indexes can be used for keyword (lexical) search. When querying a text index,
    results are scored based on the degree of lexical similarity.
  - Columns specified as vector indexes can be used for vector (semantic) search. When querying a vector index,
    results are scored based on the degree of semantic similarity.
- Columns specified as both text and vector indexes are used for both types of search.
- Each vector index column employs one of three methods for managing embeddings:

  - **Managed vector embeddings**: Snowflake calculates the vector embeddings when a text column is specified
    either in the ON or VECTOR INDEXES clauses. Must use one of the [supported embedding models](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-regional-availability).
  - **User-provided vector embeddings**: You are responsible for computing the vector embeddings
    with a [Snowflake-provided vector embedding model](/user-guide/snowflake-cortex/vector-embeddings#label-cortex-create-llm-embed-text) or an externally hosted embedding model
    prior to ingestion by the Cortex Search Service, as well as for text inputs at query time.
  - **User-provided vector embeddings with managed query embeddings**: You are responsible for computing the vector embeddings
    with one of the [Snowflake-managed embedding models supported in Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-embedding-models)
    prior to ingestion by the Cortex Search Service. At query time, Cortex Search will embed text queries using the specified
    `query_model`.

## Change Tracking Requirements

When creating a Cortex Search Service, if change tracking is not already enabled on the tables that it queries, Snowflake
automatically attempts to enable change tracking on them. In order to support incremental refreshes, change tracking must be enabled with
[non-zero time travel retention](/sql-reference/parameters#label-data-retention-time-in-days) on all underlying objects used by a Cortex Search Service.

As base objects change, so does the Cortex Search Service. If you recreate a base object, you must re-enable change tracking.

For more information about enabling change tracking, see [Change tracking not enabled on base tables](/user-guide/dynamic-tables/troubleshoot-creation#label-dynamic-tables-and-change-tracking).

Note

For Cortex Search Services, the atomicity of `CREATE OR REPLACE` applies to the metadata transaction only. The search
index for the new service is built after the transaction commits, so the previous service’s data is no longer available
from the moment the statement commits until the new index finishes building.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create a Cortex Search service named `mysvc`
using the `snowflake-arctic-embed-l-v2.0` embedding model:

Copy code

```
CREATE OR REPLACE CORTEX SEARCH SERVICE mysvc
  ON transcript_text
  ATTRIBUTES region,agent_id
  WAREHOUSE = mywh
  TARGET_LAG = '1 hour'
  EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
AS (
  SELECT
      transcript_text,
      date,
      region,
      agent_id
  FROM support_db.public.transcripts_etl
);
```

Create a Cortex Search service named `mysvc`, with the first refresh
scheduled to run after one `TARGET_LAG` period (1 hour) has passed.

Copy code

```
CREATE OR REPLACE CORTEX SEARCH SERVICE mysvc
  ON transcript_text
  ATTRIBUTES region
  WAREHOUSE = mywh
  TARGET_LAG = '1 hour'
  INITIALIZE = ON_SCHEDULE
AS SELECT * FROM support_db.public.transcripts_etl;
```

Create a multi-index search service named `business_search_service` that searches the table `business_directory`, where:

- `name` and `address` are specified as text indexes, so they are searchable with keyword search only.
- `description` is specified as a vector index, so it is eligible for vector (semantic) search using
  managed vector embeddings and the `snowflake-arctic-embed-m-v1.5` model.

Copy code

```
-- Generate sample data
CREATE OR REPLACE TABLE business_directory (name TEXT, address TEXT, description TEXT);
INSERT INTO business_directory VALUES
    ('Joe''s Coffee', '123 Bean St, Brewtown','A cozy café known for artisan espresso and baked goods.'),
    ('Sparkle Wash', '456 Clean Ave, Sudsville', 'Eco-friendly car wash with free vacuum service.'),
    ('Tech Haven', '789 Circuit Blvd, Siliconia', 'Computer store offering the latest gadgets and tech repair services.'),
    ('Joe''s Wash n'' Fold', '456 Apple Ct, Sudsville', 'Laundromat offering coin laundry and premium wash and fold services.'),
    ('Circuit Town', '459 Electron Dr, Sudsville', 'Technology store selling used computer parts at discounted prices.')
;

-- Create the Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE business_search_service
    TEXT INDEXES name, address
    VECTOR INDEXES description (model='snowflake-arctic-embed-m-v1.5')
    WAREHOUSE = mywh
    TARGET_LAG = '1 hour'
    AS ( SELECT * FROM business_directory );
```

Create a multi-index Cortex Search service with custom vector embeddings called `custom_vector_search_service`. This service searches a table with a text column (`document_contents`) and a separate user-provided vector embedding column (`document_embedding`) that contains embeddings corresponding to the text column.

Note

This example uses mock embeddings for simplicity. In a production use case, vectors should be generated through a [Snowflake vector embedding model](/user-guide/snowflake-cortex/vector-embeddings#label-cortex-create-llm-embed-text) or an externally hosted embedding model.

Copy code

```
-- Generate sample data
CREATE OR REPLACE TABLE business_documents (
  document_contents VARCHAR,
  document_embedding VECTOR(FLOAT, 3)
);
INSERT INTO business_documents VALUES
  ('Quarterly financial report for Q1 2024: Revenue increased by 15%, with expenses stable. Highlights include strategic investments in marketing and technology.', [1, 1, 1]::VECTOR(float, 3)),
  ('IT manual for employees: Instructions for usage of internal technologies, including hardware and software guides and commonly asked tech questions.', [2, 2, 2]::VECTOR(float, 3)),
  ('Employee handbook 2024: Updated policies on remote work, health benefits, and company culture initiatives.', [2, 3, 2]::VECTOR(float, 3)),
  ('Marketing strategy document: Target audience segmentation for upcoming product launch.', [1, -1, -1]::VECTOR(float, 3))
;

-- Create the Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE custom_vector_search_service
  TEXT INDEXES (document_contents)
  VECTOR INDEXES (document_embedding)
  WAREHOUSE = mywh
  TARGET_LAG = '1 minute'
  AS SELECT * FROM business_documents;
```

Create a service `managed_vector_search_service` with user-managed vector embeddings and managed query embeddings:

Copy code

```
-- Generate sample data
CREATE OR REPLACE TABLE business_documents (
  document_contents VARCHAR
);

INSERT INTO business_documents VALUES
  ('Quarterly financial report for Q1 2024: Revenue increased by 15%, with expenses stable. Highlights include strategic investments in marketing and technology.'),
  ('IT manual for employees: Instructions for usage of internal technologies, including hardware and software guides and commonly asked tech questions.'),
  ('Employee handbook 2024: Updated policies on remote work, health benefits, and company culture initiatives.'),
  ('Marketing strategy document: Target audience segmentation for upcoming product launch.');

-- Add managed vector embeddings
ALTER TABLE business_documents ADD COLUMN document_embeddings VECTOR(FLOAT, 768);
UPDATE business_documents SET document_embeddings = AI_EMBED('snowflake-arctic-embed-m-v1.5', document_contents);

-- Create the Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE managed_vector_search_service
  TEXT INDEXES document_contents
  VECTOR INDEXES document_embedding(query_model='snowflake-arctic-embed-m-v1.5')
  WAREHOUSE = mywh
  TARGET_LAG = '1 minute'
  AS SELECT * FROM business_documents;
```
