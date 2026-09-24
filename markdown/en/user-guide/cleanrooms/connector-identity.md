# Snowflake Data Clean Rooms: Identity and data provider connectors

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

Important

Third-party connectors are not offered by Snowflake and may be subject to additional terms. These integrations are made available for
your convenience, but you are responsible for any content sent to or received from the integrations.

Customers are responsible for obtaining any necessary consents in connection with their use of Snowflake Data Clean Rooms. Please ensure
that you are complying with applicable laws and regulations when using Snowflake Data Clean Rooms, including in connection with
third-party connectors for activation purposes.

## Overview

Identity connectors can be used to resolve and join entities between tables when different values refer to the same entity. For example,
if an identity provider knows that two different emails refer to the same person, if Table1 uses email 1 and Table2 uses email 2, using
an identity connector will enable you to join on those two different emails as the same entity.

For an identity connector to be available for use in a clean room, an administrator must first
[configure the clean room to make that connector available to clean room creators](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-admin-customize-connectors).

## TransUnion TruAudience Identity connector

TransUnion TruAudience Identity provides consumer data hygiene, enrichment, and matching solutions using online and offline identifiers.
It matches rows in your table with a TransUnion identity, which can be used to join rows in your collaborator’s tables.

Keep the following in mind when using the TransUnion integration:

- Snowflake does not consider the TransUnion score filter when matching identities. All matches are included.
- When the provider, not the consumer, is running an analysis like the Overlap Audience Analysis, the distinct collaboration IDs are based
  on the consumer’s count, not the provider’s count.
- You cannot use the SQL Query template to aggregate on the collaboration ID.

Configuration guideUser guide

This section describes how to configure the connector for TransUnion TruAudience Identity. You must have the MANAGE\_DCR\_CONNECTORS
role to install and configure this connector.

After you configure the connector, Snowflake maintains a cache that maps TransUnion collaborator IDs to values that uniquely identify
records in the source table. As an administrator, you can [manage this cache](#label-dcr-transunion-cache), for example, by
deleting specific records from the cache.

**Prerequisites**
:   The following must be completed before configuring the TransUnion TruAudience Identity connector in the clean room environment:

    Step 1: Install the TransUnion native app
    :   Use the Snowflake Marketplace to install the native app for TransUnion TruAudience Identity.

    Step 2: Grant privileges to the clean rooms native app
    :   After the TransUnion native app has been installed, but before a clean room administrator configures the connector, the owner
        of the TransUnion native app must follow these steps:

        1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
        2. Assume a role that has ownership rights to the TransUnion native app. For example, if the `tu_admin_role` role is the
           owner of the
           TransUnion native app, execute:

           Copy code

           ```
           USE ROLE tu_admin_role;
           ```
        3. Grant Snowflake Data Clean Rooms access to the TransUnion application role and the TransUnion table installed in step 1:

           Copy code

           ```
           GRANT APPLICATION ROLE <transunion_app_database>.tru_app_public
           TO ROLE SAMOOHA_APP_ROLE;

           GRANT SELECT, INSERT
           ON TABLE SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS
           TO ROLE SAMOOHA_APP_ROLE;
           ```

    Step 3: Ensure the required stored procedure exists
    :   The TransUnion connector relies on a stored procedure, which might not exist in some clean room environments. To ensure that
        the stored procedure exists, execute the following command as a user with the ACCOUNTADMIN role:

        Copy code

        ```
        USE ROLE ACCOUNTADMIN;

        DESCRIBE PROCEDURE SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.GRANT_EXTERNAL_APP_ROLE;
        ```

        If you receive an error that the procedure does not exist, you must use the following commands to define the procedure:

        Copy code

        ```
        USE ROLE ACCOUNTADMIN;

        CREATE OR REPLACE PROCEDURE SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.GRANT_EXTERNAL_APP_ROLE(APP_ROLE string, APPLICATION string)
           RETURNS string
           LANGUAGE SQL
           EXECUTE AS OWNER
           AS
           $$
           GRANT APPLICATION ROLE IDENTIFIER(:APP_ROLE) TO APPLICATION IDENTIFIER(:APPLICATION);
           $$;

        GRANT USAGE ON PROCEDURE SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.GRANT_EXTERNAL_APP_ROLE(string, string)
          TO ROLE SAMOOHA_APP_ROLE;
        ```

**Configuring the connector**

To configure the TransUnion TruAudience Identity connector:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors**.
3. Select the **Identity & Data Providers** tab.
4. Expand **TransUnion - TruAudience Identity**.
5. In the **Application Database** field, enter the name of the application database that was installed by the TransUnion native
   app.
6. In the **Collaboration Key** field, enter the collaboration key received from TransUnion for authorization.
7. Select a warehouse that is used when clean room users integrate a table with TransUnion TruAudience Identity.

   If you want to complete the process of matching identities within an hour, use the following guidelines to help select the right
   warehouse size:

   | Number of rows | Warehouse size |
   | --- | --- |
   | < 100k | Large |
   | 1 million | XLarge |
   | 5-10 million with addresses | 3X-Large |
   | > 10 million | 3X-Large |

   Expand

   Show lessSee more
8. Select **Authenticate**.

This section describes how to use the TransUnion TruAudience Identity connector in the clean rooms UI.

To enrich your data with TransUnion connector:

1. Start the clean room creation or installation process.
2. When you get to the **Specify Join Policies** step, expand **Identity Hub**.
3. Select **TransUnion (TruAudience Identity)**.
4. In the **Table** field, select the table that contains the data you want to enhance with TransUnion collaboration IDs.
5. In the **Unique Record Column** field, select the column that uniquely identifies a record in the table, for example, a
   system-generated user ID.
6. Use the **User Identifiers** section to associate TransUnion identity types with columns in the table. These columns are used to
   match TransUnion identities. The values in these columns should conform to the following requirements.

   > | Identity type | Format requirements |
   > | --- | --- |
   > | Address | - Address Line — Single input. For addresses with lines 1 and 2, combine the two values into a single value. - City — String. - State — Two-character abbreviation. - Zip — Zip code or Zip code+4. Exclude special characters such as spaces or hyphens. |
   > | Date of Birth | yyyy-mm-dd format. |
   > | Device ID | Either IDs with hyphens (36 character length raw Device IDs/MAIDs/IFAs) or IDs without hyphens (32 & 40 character long hashed Device IDs/MAIDs/IFAs). |
   > | Email | Plain text or SHA256-hashed lowercase strings. |
   > | First Name | Upper or lowercase names, including nicknames. Exclude titles and suffixes. |
   > | IP Address | IPv4 addresses in dot notation or integer format. You can use the [PARSE\_IP](/sql-reference/functions/parse_ip) function to obtain the integer format. |
   > | Last Name | Upper or lowercase names. Exclude middle initials. |
   > | Phone | Ten digits without special characters like spaces and hyphens. |
   >
   > Expand
   >
   > Show lessSee more

**Matched TransUnion Identities**

When Snowflake matches records in the table with TransUnion identities, the collaborator IDs are added to the table in a new column
`TCUID`. When your collaborator adds the column to one of their own tables, you can match records based on the TransUnion
collaborator ID.

### Cache for TransUnion TruAudience Identity

Snowflake maintains a cache that maps TransUnion collaborator IDs to values in the source table that uniquely identify records. For
example,
the cache might map each collaborator ID to a value in the `user_id` column of the source table. The cache is
stored in the SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.SAMOOHA\_INTERNAL\_TRANSUNION\_ID\_GENERATION\_RECORDS table. This table contains the
following columns:

> | Column | Data type | Description |
> | --- | --- | --- |
> | `inputid` | VARCHAR | Value from the column selected as the **Unique Record Column** during the integration. |
> | `collaborationid` | VARCHAR | TransUnion collaboration ID generated based on the input ID and other integration parameters. |
> | `lastprocessed` | TIMESTAMP\_NTZ | Timestamp when TransUnion generated the collaboration ID. |
>
> Expand
>
> Show lessSee more

You can perform the following actions on a cache:

Delete the cache
:   Copy code

    ```
    TRUNCATE SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS;
    ```

Delete specific records from the cache
:   You can delete specific records from the cache by specifying them as a comma-separated list of single-quoted values. For example, to
    delete the records with input IDs of `123456` and `abcedf`, execute:

    Copy code

    ```
    DELETE FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS
      WHERE inputid IN ('123456', 'abcedf');
    ```

Delete multiple records based on input IDs in a separate dataset
:   You can delete multiple records from the cache when the input IDs are present in a column of another table. For example, if the input IDs
    to be deleted are listed in the `user_id` column of the `my_db.my_schema.ref_table` table, execute:

    Copy code

    ```
    DELETE FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS
      WHERE INPUTID IN (
        SELECT user_id as INPUTID
        FROM my_db.my_schema.ref_table
      );
    ```

Add all records from a batch
:   You can add all of the records from a batch that is present in TransUnion’s view to the cache.

    Copy code

    ```
    INSERT INTO SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS (
      INPUTID,
      COLLABORATIONID,
      LASTPROCESSED
    SELECT
      INPUTID,
      COLLABORATIONID,
      LASTPROCESSED
    FROM <TRANSUNION_APPLICATION_DATABASE>.SHARE_SCHEMA.REF_MATCHING_OUTPUT_VIEW
    WHERE BATCHID = '<BATCH_ID>';
    ```

Merge all records from a batch
:   You can merge all of the records from a batch that is present in TransUnion’s view to the cache by overwriting existing input ID records
    with the corresponding new collaboration IDs and new last-processed timestamps.

    Copy code

    ```
    MERGE INTO SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS CT
    USING <TRANSUNION_APPLICATION_DATABASE>.SHARE_SCHEMA.REF_MATCHING_OUTPUT_VIEW OT
      ON
        CT.INPUTID = OT.INPUTID
        AND OT.BATCHID = '<BATCH_ID>'
    WHEN MATCHED THEN
      UPDATE SET
        CT.COLLABORATIONID = OT.COLLABORATIONID,
        CT.LASTPROCESSED = OT.LASTPROCESSED
    WHEN NOT MATCHED THEN
      INSERT (
        INPUTID,
        COLLABORATIONID,
        LASTPROCESSED
      ) VALUES (
          OT.INPUTID,
          OT.COLLABORATIONID,
          OT.LASTPROCESSED
      );
    ```

Add collaborator IDs for input ID records
:   You can add collaborator IDs for input ID records present as a column in a dataset and also present in a specific batch.

    Copy code

    ```
    INSERT INTO SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.SAMOOHA_INTERNAL_TRANSUNION_ID_GENERATION_RECORDS (
      INPUTID,
      COLLABORATIONID,
      LASTPROCESSED
    )
      SELECT
        INPUTID,
        COLLABORATIONID,
        LASTPROCESSED
      FROM <TRANSUNION_APPLICATION_DATABASE>.SHARE_SCHEMA.REF_MATCHING_OUTPUT_VIEW
      WHERE INPUTID IN (
        SELECT <column_name_containing_input_ids_to_be_added> as INPUTID
        FROM <dataset_fqtn_containing_input_ids_to_be_added>
        )
        AND BATCHID = '<BATCH_ID>';
    ```
