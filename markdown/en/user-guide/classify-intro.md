# Introduction to sensitive data classification

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

It’s critical to know where your sensitive data resides and if it’s adequately protected. This isn’t just a best practice; it’s
a vital requirement across many industries to maintain compliance with regulations. Snowflake provides a solution that automatically
discovers sensitive data and makes it easy to apply governance controls like tags and masking policies.

Snowflake classifies sensitive data into [native categories](/user-guide/classify-native) like name and national identifier, but you
can also create your own [custom categories](/user-guide/classify-custom) to detect sensitive data that is specific to your
organization or domain.

## Get started

Snowflake provides a web interface to configure sensitive data classification and to view the governance posture of sensitive data.

To get started, do one of the following:

- To set up sensitive data classification, see [Use the Trust Center to set up sensitive data classification](/user-guide/classify-ui-trust-center).
- To view the results of sensitive data classification, see [Use the Trust Center to view classification results](/user-guide/classify-results#label-classify-trust-center-review).

Note

This recommendation is rolling out in phases to all customers.

Snowflake is also introducing recommendations on Snowsight (**Database details** and **Trust Center** pages) for databases that are likely to contain
sensitive data. The recommendation uses table metadata to flag those databases and includes a one-click option to enable
classification. For details, see [Sensitive data classification recommendations in Snowsight](/user-guide/classify-ui-trust-center#label-classify-trust-center-sensitive-data-banner).

## Core concepts of sensitive data classification

- [About classification categories](#about-classification-categories)
- [About classification tags](#about-classification-tags)
- [About classification profiles](#about-classification-profiles)

### About classification categories

With sensitive data classification, every column that is identified as containing sensitive data is assigned two categories: a semantic
category and a privacy category.

- A **semantic category** identifies the *type* of personal attribute. Snowflake provides
  [native categories](/user-guide/classify-native) for common attributes such as names and addresses. If your sensitive data doesn’t
  fit into a native category, you can create a [custom category](/user-guide/classify-custom) for it.
- A **privacy category** identifies the *sensitivity* of a personal attribute. It can be IDENTIFIER, QUASI\_IDENTIFIER, or SENSITIVE (a generic, non-identifier category for things such as medical/health data or salary).

### About classification tags

A [tag](/user-guide/object-tagging/introduction) is a Snowflake object that can be assigned to a column. Snowflake uses
the following system-defined tags to identify columns that it has classified as containing sensitive data.

- SNOWFLAKE.CORE.SEMANTIC\_CATEGORY: Tag used to identify the native or custom category of the data in a column.
- SNOWFLAKE.CORE.PRIVACY\_CATEGORY: Tag used to identify the privacy category of the data in a column.

You can map user-defined tags to system-defined classification tags. For example, you can set up a tag map so that every time the system tag
`SNOWFLAKE.CORE.SEMANTIC_CATEGORY = 'NAME'` is applied to a column, the user-defined tag `tag_db.sch.pii = 'Highly confidential'`
is also applied.

### About classification profiles

When you use the Trust Center web interface to specify classification settings, those settings are saved as a *classification profile*. This
classification profile can be edited later to change the settings that control how data is classified. In the web interface, the
classification profile also controls which databases are being classified with the profile’s settings.

You can also [use SQL commands](/user-guide/classify-auto) to create and modify a classification profile. If you are using SQL,
associating the classification profile with a database to start the classification process is a separate step.

### AI mode

[Preview Feature](/release-notes/preview-features) — Open

Available to Enterprise Edition or higher.

A classification profile can optionally use **AI mode** to use LLMs to identify additional semantic categories beyond those identified by
standard classification. When AI mode is enabled, Snowflake uses the `openai-gpt-5-mini` model to augment classification results and improve
accuracy.

You can enable AI mode when you [set up classification with advanced settings](/user-guide/classify-ui-trust-center#label-classify-trust-center-advanced)
in the Trust Center, or by using [SQL commands](/user-guide/classify-auto#label-classify-auto-ai-mode) to create or update a classification
profile.

## Protecting sensitive data

Snowflake provides the governance tools you need to track and protect your sensitive data.

- You can configure the classification process so Snowflake automatically assigns system and user-defined
  [tags](/user-guide/object-tagging/introduction) to data that it classifies as sensitive. You can then track the data within your
  data estate by tracking the tags.
- You can assign a [masking policy](/user-guide/security-column-ddm-intro) to columns that contain sensitive data to selectively mask
  the data at query time.
- You can combine tagging and masking policies to automatically mask data that is classified as sensitive. If you use
  [tag-based masking](/user-guide/tag-based-masking-policies) to associate a masking policy with a user-defined tag, the data will be
  automatically masked when Snowflake applies the tag as part of the classification process. As new data is added to a database, the
  tag-based masking policies are automatically assigned to the columns that contain sensitive data.

## Determine which databases are being classified

You can determine what data is being monitored for sensitive data classification by listing the databases that are
associated with a [classification profile](#label-classify-classification-profiles). If a database is associated with a classification
profile, all the tables and views in that database are being automatically classified according to the criteria defined in the profile.

To determine which databases are being classified:

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](/user-guide/classify-ui-trust-center#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Select the **Dashboard** tab.
5. Find the **Databases monitored by classification** tile. To list the databases being classified, select **Monitored** or
   **Partially monitored**.

Note

A database is partially monitored if someone used SQL to set a classification profile directly on a schema in the database rather
than setting the profile at the database level.

Use the [SYSTEM$SHOW\_SENSITIVE\_DATA\_MONITORED\_ENTITIES](/sql-reference/functions/system_show_sensitive_data_monitored_entities) function to list the databases that are
associated with a classification profile.

Copy code

```
SELECT SYSTEM$SHOW_SENSITIVE_DATA_MONITORED_ENTITIES('DATABASE');
```

## Cost considerations

Sensitive data classification consumes credits as it uses [serverless compute resources](/user-guide/cost-understanding-compute#label-serverless-credit-usage) to
classify tables in the database.

When you enable [AI mode](#label-classify-ai-mode) on a classification profile, you also incur token charges for LLM usage in addition to these compute charges.

For more information about pricing for this consumption, see Table 5 in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Note

Classifying views can cost more than classifying tables. The additional cost depends on the complexity of the query that created
the view. Materialized views don’t incur these additional costs. By default, views are excluded from classification.

### View costs in Snowsight

To explore the cost of sensitive data classification:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to cost and usage data](/user-guide/cost-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select a warehouse to use to view the usage data. Snowflake recommends using an XS warehouse for this purpose.
5. Select **Consumption**.
6. From the **Usage Type** drop-down, select **Compute**.
7. From the **Service Type** drop-down, select **Sensitive Data Classification**.

### Use SQL to query costs

You can query views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas to determine how much was spent on automatically classifying
sensitive data. To monitor credit consumption, query the following views:

METERING\_HISTORY view (ACCOUNT\_USAGE)
:   Lets you retrieve the hourly cost of automatic classification by focusing on `SENSITIVE_DATA_CLASSIFICATION` in the
    `SERVICE_TYPE` column. For example:

    Copy code

    ```
    SELECT
      service_type,
      start_time,
      end_time,
      entity_id,
      name,
      credits_used_compute,
      credits_used_cloud_services,
      credits_used,
      budget_id
      FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
      WHERE service_type = 'SENSITIVE_DATA_CLASSIFICATION';
    ```

METERING\_DAILY\_HISTORY view (ACCOUNT\_USAGE and ORGANIZATION\_USAGE)
:   Lets you retrieve the daily cost of automatic classification by focusing on `SENSITIVE_DATA_CLASSIFICATION` in the
    `SERVICE_TYPE` column. For example:

    Copy code

    ```
    SELECT
      service_type,
      usage_date,
      credits_used_compute,
      credits_used_cloud_services,
      credits_used
      FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
      WHERE service_type = 'SENSITIVE_DATA_CLASSIFICATION';
    ```

USAGE\_IN\_CURRENCY\_DAILY (ORGANIZATION\_USAGE)
:   Lets you retrieve the daily cost of automatic classification by focusing on `SENSITIVE_DATA_CLASSIFICATION` in the
    `SERVICE_TYPE` column. Use this view to determine the cost in currency, not credits.

## Supported objects

Snowflake supports classifying data stored in the following types of tables and views:

Tables:

- [Snowflake tables](/user-guide/tables-micro-partitions)
- [External tables](/user-guide/tables-external-intro)
- [Managed and unmanaged Apache Iceberg™ tables](/user-guide/tables-iceberg)
- [Dynamic tables](/user-guide/dynamic-tables/overview)
- [Event tables](/developer-guide/logging-tracing/event-table-setting-up)

Views:

- [Snowflake views](/user-guide/views-introduction)
- [Materialized views](/user-guide/views-materialized)
- [Secure views](/user-guide/views-secure)

Note

Although views can be classified, classifying a view can cost significantly more than classifying the underlying
tables directly, because of the complexity of the query that created the view. For more information, see [Cost considerations](#label-classify-auto-cost).

Note that Snowflake does not support classification on [shared tables](/user-guide/data-sharing-intro) and shared schemas from the
consumer’s side. If a table is created by the provider and placed into the provider’s outbound share, the classification only works if it is
called from the provider’s side.

## Supported data types

You can classify table and view columns for all supported [data types](/sql-reference-data-types) except for the following
data types:

- BINARY
- DECFLOAT
- GEOGRAPHY
- UUID
- VECTOR

Note

- Unstructured data like long text stored in columns is not supported.
- JSON is the only semi-structured data that is supported.

## Limitations and considerations

- Classification profiles cannot be set on a reader account.
- A classification profile cannot be set on more than 1,000 databases.
- A classification profile cannot be *directly* set on more than 10,000 schemas.
- A maximum of 100 million tables can be classified in a schema.
- You cannot automatically classify a table if it has any of the following characteristics:
  - More than 10,000 columns.
  - A column with a name that has more than 255 characters.
  - A column with a name that includes the `$` character.
- When [AI mode](#label-classify-ai-mode) is enabled on a classification profile:
  - Columns of type VARIANT, OBJECT, or ARRAY are not evaluated in AI mode classification.
  - Tables with more than 300 columns are not passed for AI enrichment.
  - AI mode is only available with the OpenAI GPT-5 Mini model (`openai-gpt-5-mini`).
  - To use AI mode, you might need to [enable cross-region inference](/user-guide/snowflake-cortex/cross-region-inference)
    on your account.
