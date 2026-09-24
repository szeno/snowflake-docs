# Snowflake Data Clean Rooms: Troubleshooting external data connectors

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

This topic describes how to troubleshoot external data errors. It applies to Amazon Web Services, Microsoft Azure, and Google Cloud.

## Steps to follow to troubleshoot external data errors

1. Ensure the path URL/URI is correct. See the associated related topic for the correct URL/URI.
2. Ensure there is at least one file in the bucket or blob storage.
3. Ensure the file is in parquet format.
4. Ensure the parquet file is not empty.
5. Ensure the parquet file is not compressed using the Snappy format.
6. If none of the above resolves the issue, then debug with the following script:

> Copy code
>
> ```
> USE ROLE SAMOOHA_APP_ROLE;
> USE DATABASE SAMOOHA_BY_SNOWFLAKE_LOCAL_DB;
> USE SCHEMA PUBLIC;
>
> /*
>   Query the stage name from the connector configuration.
>   Use AWS_CONNECTOR_ID for AWS, GCP_CONNECTOR_ID for GCP and
>   AZURE_CONNECTOR_ID for Azure.
>
>   For example, if you are connecting to AWS, enter:
>
>   SELECT CONFIGURATION_ID, PARSE_JSON(CONFIGURATION) FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.CONNECTOR_CONFIGURATION WHERE CONNECTOR_ID = 'AWS_CONNECTOR_ID';
>
> /*
>   Note that the rest of this script relies on the output of this query so you
>   must save the output for use in the rest of the steps.
>
>   Next, check the storage integration. Replace <CONFIGURATION_ID> from the output
>   of the query.
> */
>
>   DESC STORAGE INTEGRATION SAMOOHA_STORAGE_INT_<CONFIGURATION_ID>;
>
> /*
>   List files in the stage. Replace <STAGE_NAME> from the output of the query.
> */
>
>   LIST @<STAGE_NAME>;
>
> /*
>   Check if you are able to query the files in the external stage. Replace
>   <STAGE_NAME> from the output of the query.
> */
>
>   SELECT * FROM @<STAGE_NAME> LIMIT 10;
>
> /*
>   Check if you are able to infer the schema from the files in the external
>   stage. Replace <STAGE_NAME> from the output of the query.
> */
>
>   SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
>   WITHIN GROUP (ORDER BY order_id)
>   FROM TABLE(
>     INFER_SCHEMA(
>       LOCATION=>'@<STAGE_NAME>',
>       FILE_FORMAT=>'SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PAR_FF'
>     )
>   );
>
> /*
>   Try to create a table from the external stage. Replace <STAGE_NAME> from
>   the output of the query.
> */
>
>   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.LIBRARY.CREATE_TABLE_FROM_STAGE('<STAGE_NAME>', 'EXT_INT_TEMP_TABLE');
>
> /*
>   Check data in the table.
> */
>
>   SELECT * FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.EXT_INT_TEMP_TABLE LIMIT 10;
> ```
