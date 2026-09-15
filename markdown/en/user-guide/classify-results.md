# View and track sensitive data classification results

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes how you can view and track the results of sensitive data classification and how you can track classification tags to
monitor sensitive data.

## Use the Trust Center to view classification results

To view results of sensitive data classification in the Trust Center, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](/user-guide/classify-ui-trust-center#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Do one of the following:
   - If you want to gain high-level insights into the security of your sensitive data, select the **Dashboard** tab. For more information,
     see [Review the Dashboard page](#label-classify-trust-center-review-dashboard).
   - If you want to list all of the tables and views that have been classified as containing sensitive data, select the
     **Sensitive objects** tab.

     When the page opens, select a table to see which columns have sensitive data, the
     [semantic category](/user-guide/classify-intro#label-classify-categories) of those columns, and whether tags were applied to the columns.

### Review the Dashboard page

The **Dashboard** page provides high-level insights into the security of your sensitive data, such as how many databases and tables have been classified. The page contains the following tiles:

| Tile | Description |
| --- | --- |
| **Objects by compliance category** | Identifies the number of objects that contain data that might be subject to a regulation or other compliance standard, based on the type of information in the object.  Note  The mapping between a compliance category and semantic categories is not exhaustive. Only native semantic categories supported by Snowflake are mapped to a compliance category. For the complete mapping, see [Compliance categories and their semantic categories](#label-classify-trust-center-review-mapping).  You are solely responsible for determining which regulations or laws apply to your data and ensuring your compliance with the applicable regulations or laws. |
| **Objects by semantic category** | Identifies the most common semantic categories, and the number of objects that contain data that belongs to those categories. |
| **Databases monitored by auto-classification** | Identifies which databases are currently monitored by sensitive data classification. A database is partially monitored if someone used SQL to set a classification profile directly on a schema in the database rather than setting the profile at the database level. |
| **Classification status** | Identifies whether all databases currently being monitored for sensitive data have been classified. |
| **Sensitive data masking status** | Identifies whether sensitive data is protected by a [masking policy](/user-guide/security-column-ddm-intro). The masking policy can be a tag-based policy or one that was manually applied to the column.  A table is *fully masked* if every column that contains sensitive data has a masking policy associated with it. A table is *partially masked* if only some columns containing sensitive data are associated with a masking policy. |

Expand

Show lessSee more

### Compliance categories and their semantic categories

Note

You are solely responsible for determining which regulations or laws apply to your data and ensuring your compliance with the applicable
regulations or laws. The compliance categories within sensitive data classification are designed to give you an out-of-the-box toolkit to
aid your efforts, but are not exhaustive. Only [native semantic categories](/user-guide/classify-native) supported by Snowflake are
mapped to a compliance category.

Warning

HIPAA data requirements mandate that covered entities and business associates protect the confidentiality, integrity, and availability of
Protected Health Information (PHI) through strict administrative, physical, and technical safeguards. Non-compliance with HIPAA can lead
to significant penalties. Semantic categories related to PHI are included in [Sensitive information](/user-guide/classify-native#label-classify-sensitive-information).

Use the following table to understand the **Objects by compliance category** tile on the [Dashboard page](#label-classify-trust-center-review-dashboard).

| Compliance category | Native semantic category | Locale |
| --- | --- | --- |
| Digital Personal Data Protection Act (DPDPA) | DATE\_OF\_BIRTH | n/a |
|  | DRIVERS\_LICENSE | India (IN) |
|  | EMAIL | n/a |
|  | NAME | n/a |
|  | NATIONAL\_IDENTIFIER | India (IN) |
|  | PHONE\_NUMBER | n/a |
|  | STREET\_ADDRESS | n/a |
|  | TAX\_IDENTIFIER | India (IN) |
| General Data Protection Regulation (GDPR) | AGE | n/a |
|  | DRIVERS\_LICENSE | Austria (AT), Belgium (BE), Bulgaria (BG), Croatia (HR), Cyprus (CY), Czech Republic (CZ), Denmark (DK), Estonia (EE), Finland (FI), France (FR), Germany (DE), Greece (GR), Hungary (HU), Ireland (IE), Italy (IT), Latvia (LV), Lithuania (LT), Luxembourg (LU), Malta (MT), Netherlands (NL), Poland (PL), Portugal (PT), Romania (RO), Slovakia (SK), Slovenia (SI), Spain (ES), Sweden (SE) |
|  | EMAIL | n/a |
|  | ETHNICITY | n/a |
|  | GENDER | n/a |
|  | IBAN | n/a |
|  | IMEI | n/a |
|  | IP\_ADDRESS | n/a |
|  | NAME | n/a |
|  | NATIONAL\_IDENTIFIER | Austria (AT), Belgium (BE), Bulgaria (BG), Croatia (HR), Cyprus (CY), Czech Republic (CZ), Denmark (DK), Estonia (EE), Finland (FI), France (FR), Germany (DE), Greece (GR), Hungary (HU), Ireland (IE), Latvia (LV), Lithuania (LT), Luxembourg (LU), Malta (MT), Netherlands (NL), Poland (PL), Portugal (PT), Romania (RO), Slovakia (SK), Slovenia (SI), Spain (ES), Sweden (SE), United Kingdom (UK) |
|  | PASSPORT | Austria (AT), Belgium (BE), Bulgaria (BG), Croatia (HR), Cyprus (CY), Czech Republic (CZ), Denmark (DK), Estonia (EE), Finland (FI), France (FR), Germany (DE), Greece (GR), Hungary (HU), Ireland (IE), Italy (IT), Latvia (LV), Lithuania (LT), Luxembourg (LU), Malta (MT), Netherlands (NL), Poland (PL), Portugal (PT), Romania (RO), Slovakia (SK), Slovenia (SI), Spain (ES), Sweden (SE) |
|  | PAYMENT\_CARD | n/a |
|  | PHONE\_NUMBER | n/a |
|  | SALARY | n/a |
|  | TAX\_IDENTIFIER | Austria (AT), Cyprus (CY), France (FR), Germany (DE), Greece (GR), Hungary (HU), Italy (IT), Malta (MT), Netherlands (NL), Poland (PL), Portugal (PT), Slovenia (SI), Spain (ES), Sweden (SE) |
|  | VIN | n/a |
| Gramm-Leach-Bliley Act (GLBA) | BANK\_ACCOUNT | United States (US) |
|  | DRIVERS\_LICENSE | United States (US) |
|  | NAME | United States (US) |
|  | NATIONAL\_IDENTIFIER | United States (US) |
|  | PASSPORT | United States (US) |
|  | PAYMENT\_CARD | n/a |
|  | STREET\_ADDRESS | United States (US) |
|  | TAX\_IDENTIFIER | United States (US) |
| Health Insurance Portability and Accountability Act (HIPAA) | ADMINISTRATIVE\_AREA\_1 | United States (US) |
|  | ADMINISTRATIVE\_AREA\_2 | United States (US) |
|  | AGE | n/a |
|  | CITY | United States (US) |
|  | DATE\_OF\_BIRTH | n/a |
|  | EMAIL | n/a |
|  | ETHNICITY | n/a |
|  | IMEI | n/a |
|  | IP\_ADDRESS | n/a |
|  | MEDICAL\_DATA | n/a |
|  | MEDICAL\_SPECIALTY | n/a |
|  | NAME | n/a |
|  | NATIONAL\_IDENTIFIER | United States (US) |
|  | PHONE\_NUMBER | United States (US) |
|  | POSTAL\_CODE | United States (US) |
|  | STREET\_ADDRESS | United States (US) |
|  | URL | n/a |
|  | VIN | n/a |
| Payment Card Industry (PCI) | PAYMENT\_CARD | n/a |
| Personally identifiable information (PII) | DATE\_OF\_BIRTH | n/a |
|  | DRIVERS\_LICENSE | n/a |
|  | EMAIL | n/a |
|  | NAME | n/a |
|  | NATIONAL\_IDENTIFIER | n/a |
|  | PHONE\_NUMBER | n/a |
|  | STREET\_ADDRESS | n/a |
|  | TAX\_IDENTIFIER | n/a |

Expand

Show lessSee more

## Use SQL to view classification results

You can use SQL to view the results of data classification by calling a system function or querying an Account Usage view.

### Retrieve classification results for a specific table

Call the [SYSTEM$GET\_CLASSIFICATION\_RESULT](/sql-reference/functions/system_get_classification_result) function to view results for a specific table.

Copy code

```
CALL SYSTEM$GET_CLASSIFICATION_RESULT('mydb.sch.t1');
```

Results aren’t available until the classification process is complete. The automatic classification process doesn’t start until one hour after setting the classification profile on the database.

### Query the latest classification results

To view the latest classification results, query the [DATA\_CLASSIFICATION\_LATEST](/sql-reference/account-usage/data_classification_latest) view. Classification results before the latest are not shown. For example,
you can use a role that has been granted the SNOWFLAKE.GOVERNANCE\_VIEWER database role. Other privileges can also provide access,
such as using ACCOUNTADMIN or having IMPORTED PRIVILEGES on the SNOWFLAKE database.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_CLASSIFICATION_LATEST;
```

Results might not appear until three hours after classification is complete. To view previous classification results, see [Query the classification history](#label-classify-view-history-sql).

### Query the classification history

To view all classification events over the last 365 days, query the [DATA\_CLASSIFICATION\_HISTORY](/sql-reference/account-usage/data_classification_history) view. For example, you can use a role that has been granted the SNOWFLAKE.GOVERNANCE\_VIEWER
database role. Other privileges can also provide access, such as using ACCOUNTADMIN or having IMPORTED PRIVILEGES on the SNOWFLAKE
database.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_CLASSIFICATION_HISTORY;
```

Use the following examples to query classification history:

- [Filter classification history by database, schema, and table name](#filter-classification-history-by-database-schema-and-table-name)
- [Filter by table ID](#filter-by-table-id)
- [Count classification events in the last seven days](#count-classification-events-in-the-last-seven-days)
- [Compare classification runs for one table](#compare-classification-runs-for-one-table)

#### Filter classification history by database, schema, and table name

The following example returns all classification events for a specific table by filtering on database name, schema name, and table name, ordered from most recent to oldest:

Copy code

```
SELECT
    database_id,
    database_name,
    schema_id,
    schema_name,
    table_id,
    table_name,
    trigger_type,
    classified_on,
    table_deleted_on,
    result
  FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_CLASSIFICATION_HISTORY
  WHERE database_name = 'MY_DB'
    AND schema_name = 'MY_SCHEMA'
    AND table_name = 'EMPLOYEES'
  ORDER BY classified_on DESC;
```

The output shows two classification events for the same EMPLOYEES table: a manual classification from February 2025 that identified the EMAIL column, and a later auto classification from March 2025 that identified both the EMAIL and SSN columns. The results are ordered from most recent to oldest, showing how classification results can evolve over time.

```
+-------------+---------------+-----------+-------------+----------+------------+---------------------+---------------------------+----------------+--------------------------------+
| DATABASE_ID | DATABASE_NAME | SCHEMA_ID | SCHEMA_NAME | TABLE_ID | TABLE_NAME | TRIGGER_TYPE        | CLASSIFIED_ON             | TABLE_DELETED_ON | RESULT                         |
+-------------+---------------+-----------+-------------+----------+------------+---------------------+---------------------------+----------------+--------------------------------+
| 10          | MY_DB         | 100       | MY_SCHEMA   | 1234     | EMPLOYEES  | AUTO CLASSIFICATION | 2025-03-01 08:00:00 -0800 | NULL           | {"EMAIL": {...}, "SSN": {...}} |
| 10          | MY_DB         | 100       | MY_SCHEMA   | 1234     | EMPLOYEES  | MANUAL              | 2025-02-15 14:30:00 -0800 | NULL           | {"EMAIL": {...}}               |
+-------------+---------------+-----------+-------------+----------+------------+---------------------+---------------------------+----------------+--------------------------------+
```

#### Filter by table ID

The following example filters the classification history by the table ID to return all classification events for a specific table, ordered
by most recent first:

Note

Filtering by the ID can be useful if the table was renamed after classification.

Copy code

```
SELECT
    database_id,
    database_name,
    schema_id,
    schema_name,
    table_id,
    table_name,
    trigger_type,
    classified_on,
    table_deleted_on,
    result
  FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_CLASSIFICATION_HISTORY
  WHERE table_id = 1234
  ORDER BY classified_on DESC;
```

The output shows two classification events for the same table (ID 1234), even though the table was renamed from EMPLOYEES to EMPLOYEES\_NEW between events. Because the query filters by table ID rather than name, both events are returned regardless of the name change.

```
+-------------+---------------+-----------+-------------+----------+---------------+---------------------+---------------------------+----------------+--------------------------------+
| DATABASE_ID | DATABASE_NAME | SCHEMA_ID | SCHEMA_NAME | TABLE_ID | TABLE_NAME    | TRIGGER_TYPE        | CLASSIFIED_ON             | TABLE_DELETED_ON | RESULT                         |
+-------------+---------------+-----------+-------------+----------+---------------+---------------------+---------------------------+----------------+--------------------------------+
| 10          | MY_DB         | 100       | MY_SCHEMA   | 1234     | EMPLOYEES_NEW | AUTO CLASSIFICATION | 2025-03-01 08:00:00 -0800 | NULL           | {"EMAIL": {...}, "SSN": {...}} |
| 10          | MY_DB         | 100       | MY_SCHEMA   | 1234     | EMPLOYEES     | MANUAL              | 2025-02-15 14:30:00 -0800 | NULL           | {"EMAIL": {...}}               |
+-------------+---------------+-----------+-------------+----------+---------------+---------------------+---------------------------+----------------+--------------------------------+
```

#### Count classification events in the last seven days

The following example shows the number of classification events in the last seven days:

Copy code

```
SELECT
    COUNT(*) AS classification_count
  FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_CLASSIFICATION_HISTORY
  WHERE classified_on >= DATEADD(DAY, -7, CURRENT_TIMESTAMP());
```

```
+----------------------+
| CLASSIFICATION_COUNT |
+----------------------+
| 42                   |
+----------------------+
```

#### Compare classification runs for one table

The following example compares the two most recent classification runs for a table and returns only the columns whose
classification changed between the runs. Each row in the result includes a `change_type` column with one of the
following values:

- `ADDED`: The column was not classified in the previous run. The `PREV_*` columns are NULL.
- `REMOVED`: The column was classified in the previous run but not in the current run. The `CURR_*` columns are NULL.
- `CHANGED`: The column exists in both runs but its semantic or privacy category differs.

Columns whose classification was identical across both runs are excluded from the results.

Copy code

```
WITH ranked AS (
    SELECT
        table_id,
        database_id,
        schema_id,
        database_name,
        schema_name,
        table_name,
        classified_on,
        trigger_type,
        result,
        ROW_NUMBER() OVER (PARTITION BY table_id ORDER BY classified_on DESC) AS rn
      FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_CLASSIFICATION_HISTORY
      WHERE table_id = 1234
    ),
  curr_cols AS (
      SELECT r.table_id, r.database_id, r.schema_id,
          r.database_name, r.schema_name, r.table_name,
          r.classified_on, r.trigger_type,
          c.key AS column_name, c.value AS column_result
        FROM ranked r, LATERAL FLATTEN(input => r.result) c
        WHERE r.rn = 1
  ),
  prev_cols AS (
      SELECT r.table_id,
          r.classified_on, r.trigger_type,
          c.key AS column_name, c.value AS column_result
        FROM ranked r, LATERAL FLATTEN(input => r.result) c
        WHERE r.rn = 2
  )
  SELECT
      curr.database_id,
      curr.database_name,
      curr.schema_id,
      curr.schema_name,
      curr.table_id,
      curr.table_name,
      prev.classified_on AS previous_classified_on,
      curr.classified_on AS current_classified_on,
      COALESCE(curr.column_name, prev.column_name) AS column_name,
      CASE
        WHEN prev.column_name IS NULL THEN 'ADDED'
        WHEN curr.column_name IS NULL THEN 'REMOVED'
        ELSE 'CHANGED'
      END AS change_type,
      prev.column_result:recommendation.semantic_category::STRING AS prev_semantic_category,
      curr.column_result:recommendation.semantic_category::STRING AS curr_semantic_category,
      prev.column_result:recommendation.privacy_category::STRING AS prev_privacy_category,
      curr.column_result:recommendation.privacy_category::STRING AS curr_privacy_category
    FROM curr_cols curr
    FULL OUTER JOIN prev_cols prev
      ON curr.table_id = prev.table_id
      AND curr.column_name = prev.column_name
    WHERE prev.column_name IS NULL
      OR curr.column_name IS NULL
      OR curr.column_result:recommendation.semantic_category != prev.column_result:recommendation.semantic_category
      OR curr.column_result:recommendation.privacy_category != prev.column_result:recommendation.privacy_category
    ORDER BY column_name;
```

The output shows three columns whose classification changed between the two most recent runs: DATE\_OF\_BIRTH and SSN were newly identified (ADDED) in the current run, while PHONE was classified in the previous run but no longer appears in the current run (REMOVED). Columns whose classification remained the same across both runs, such as EMAIL, are excluded from the results.

```
+-------+---------+-----------+-------------+----------+------------+---------------------+---------------------+---------------+-------------+---------------+---------------+--------------+------------------+
| DB_ID | DB_NAME | SCHEMA_ID | SCHEMA_NAME | TABLE_ID | TABLE_NAME | PREV_CLASSIFIED_ON  | CURR_CLASSIFIED_ON  | COLUMN_NAME   | CHANGE_TYPE | PREV_SEMANTIC | CURR_SEMANTIC | PREV_PRIVACY | CURR_PRIVACY     |
+-------+---------+-----------+-------------+----------+------------+---------------------+---------------------+---------------+-------------+---------------+---------------+--------------+------------------+
| 10    | MY_DB   | 100       | MY_SCHEMA   | 1234     | EMPLOYEES  | 2025-02-15 14:30:00 | 2025-03-01 08:00:00 | DATE_OF_BIRTH | ADDED       | NULL          | DATE_OF_BIRTH | NULL         | QUASI_IDENTIFIER |
| 10    | MY_DB   | 100       | MY_SCHEMA   | 1234     | EMPLOYEES  | 2025-02-15 14:30:00 | 2025-03-01 08:00:00 | PHONE         | REMOVED     | PHONE_NUMBER  | NULL          | IDENTIFIER   | NULL             |
| 10    | MY_DB   | 100       | MY_SCHEMA   | 1234     | EMPLOYEES  | 2025-02-15 14:30:00 | 2025-03-01 08:00:00 | SSN           | ADDED       | NULL          | US_SSN        | NULL         | IDENTIFIER       |
+-------+---------+-----------+-------------+----------+------------+---------------------+---------------------+---------------+-------------+---------------+---------------+--------------+------------------+
```

## View classification results for JSON columns

Snowflake can classify columns of type ARRAY, VARIANT, or OBJECT when the semi-structured data is in JSON format. The result of this
classification has the following characteristics:

- The results object contains an `object_path_results` field. This field lists objects, where each object corresponds to
  a field in the semi-structured data that was classified into a native semantic category.
- If a field in the semi-structured data contains sensitive data, then the semantic category of the *column* is `MULTIPLE`. To obtain
  the semantic category of fields in the semi-structured data, use the `object_path_results` field in the results.

As an example, suppose Snowflake classifies the following table:

```
+-----------------------------------------------------------+---------------+-----------------------------------------------------+
| ARRAY_COL                                                 | FIRST_NAME    | OBJECT_COL                                          |
+-----------------------------------------------------------+---------------+-----------------------------------------------------+
| [ { "email": "alice@example.com" }, { "email": "b..." } ] | "Joe"         | { "email": "jane@domain.com", "phone": "206-..." }  |
+-----------------------------------------------------------+---------------+-----------------------------------------------------+
```

The classification result might look like the following:

Copy code

```
{
  "ARRAY_COL": {
    "object_path_results": {
      "ARRAY_COL:[$$].email": {
        "alternates": [],
        "recommendation": {
          "confidence": "HIGH",
          "coverage": 1,
          "details": [],
          "privacy_category": "IDENTIFIER",
          "semantic_category": "EMAIL"
        }
      }
    },
    "recommendation": {
      "confidence": "HIGH",
      "details": [],
      "privacy_category": "IDENTIFIER",
      "semantic_category": "MULTIPLE"
    },
    "valid_value_ratio": 1
  },
  "FIRST_NAME": {
    "alternates": [],
    "recommendation": {
      "confidence": "HIGH",
      "coverage": 1,
      "details": [],
      "privacy_category": "IDENTIFIER",
      "semantic_category": "NAME"
    },
    "valid_value_ratio": 1
  },
  "OBJECT_COL": {
    "object_path_results": {
      "OBJECT_COL:email": {
        "alternates": [],
        "recommendation": {
          "confidence": "HIGH",
          "coverage": 1,
          "details": [],
          "privacy_category": "IDENTIFIER",
          "semantic_category": "EMAIL"
        }
      },
      "OBJECT_COL:phone": {
        "alternates": [],
        "recommendation": {
          "confidence": "HIGH",
          "coverage": 1,
          "details": [
            {
              "coverage": 1,
              "semantic_category": "US_PHONE_NUMBER"
            },
            {
              "coverage": 1,
              "semantic_category": "JP_PHONE_NUMBER"
            }
          ],
          "privacy_category": "IDENTIFIER",
          "semantic_category": "PHONE_NUMBER"
        }
      }
    },
    "recommendation": {
      "confidence": "HIGH",
      "details": [],
      "privacy_category": "IDENTIFIER",
      "semantic_category": "MULTIPLE"
    },
    "valid_value_ratio": 1
  }
}
```

## Use tags to track sensitive data

When Snowflake classifies sensitive data, it suggests or automatically applies system-defined and user-defined tags to the columns that
contain sensitive data. Because columns with sensitive data are assigned these tags, you can monitor the sensitive data by running queries
and calling functions to track the tags.

For example, to list all of the columns that were classified and assigned a semantic category, you can run the following query:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
  WHERE TAG_NAME = 'SEMANTIC_CATEGORY'
  ORDER BY object_database, object_schema, object_name, column_name;
```

If you want to determine which semantic category was assigned to the `fname` column of the `hr_data` table, you can run the following
query to obtain the value of the SEMANTIC\_CATEGORY tag:

Copy code

```
SELECT SYSTEM$GET_TAG(
    'SNOWFLAKE.CORE.SEMANTIC_CATEGORY',
    'hr_data.fname',
    'COLUMN'
    );
```

For information about the different ways that you can track tags, see [Monitor object tags](/user-guide/object-tagging/monitor).
