# Troubleshoot problems with auto-fulfilled data products

The following issues might occur for auto-fulfilled data products that are improperly configured.

- [Data is missing or out of sync for consumers](#label-laf-troubleshoot-missing-data)
- [Long delay getting data after requesting a listing](#label-laf-troubleshoot-long-delay)

## Data is missing or out of sync for consumers

Error:
:   Consumer reports that views from an auto-fulfillment listing are no longer visible.

Cause:
:   You re-created objects, such as tables or views, associated with your listing and either:

    - The objects were not re-granted to the share after being re-created
    - Or, the objects were re-granted but it has been less than 10 minutes. Changes to objects granted to shares are checked every 10 minutes,
      so if it has been less than 10 minutes, the updated objects have not yet been auto-fulfilled to the consumer’s region.

Solution:
:   Verify that the objects were re-granted to the share, and determine how much time has passed since the grant query was run.

    To confirm that all objects are granted to the share in your primary account, run the following:

    Copy code

    ```
    SHOW GRANTS to SHARE <share_name>;
    ```

    If needed, re-grant objects to the share:

    Copy code

    ```
    GRANT USAGE on DATABASE <db_name> to SHARE <share_name>;
    GRANT USAGE on SCHEMA <schema_name> to SHARE <share_name>;
    GRANT SELECT on TABLE <table_name> to SHARE <share_name>;
    GRANT SELECT on VIEW <view_name> to SHARE <share_name>;
    GRANT USAGE on FUNCTION <function_name(parameters)> to SHARE <share_name>;
    ```

    Allow up to 10 minutes after grants have been updated in the primary region, or after a database has been refreshed with new objects,
    for grants to apply in all remote regions.

## Long delay getting data after requesting a listing

Consumer reports that they requested a listing in their region, but after several days, they still don’t have access to the data product.

Error:
:   Data is replicating to your region…

Cause:
:   If the error message appears for several days with no change in status, it’s likely that an auto-fulfillment error occurred.

Solution:
:   As a provider, view the listing details to identify a specific error preventing auto-fulfillment of the data product, and refer to this
    troubleshooting guide to address the error.

    As a consumer, contact the provider to let them know that there is a problem auto-fulfilling their data product to your region.
