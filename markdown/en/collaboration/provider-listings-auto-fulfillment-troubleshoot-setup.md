# Troubleshoot auto-fulfillment setup issues

When you set up your listing, underlying issues with your data product can prevent auto-fulfillment.

- [A direct share with the same name already exists in the remote account](#label-laf-troubleshoot-database-exists)
- [A role is missing privileges on a share](#label-laf-troubleshoot-missing-share-privileges)
- [Auto-fulfillment failed during snapshot generation for multiple listings](#label-af-troubleshoot-snapshot-generation)
- [The database is larger than 10 terabytes](#label-laf-troubleshoot-database-too-large)
- [The data product contains a reference database](#label-laf-troubleshoot-database-reference)
- [The data product contains unsupported objects](#label-laf-troubleshoot-unsupported-objects)
- [The listing database is a primary database](#label-laf-troubleshoot-database-primary)
- [The listing database is a secondary database](#label-laf-troubleshoot-database-secondary)
- [Receiving an error that my account is not set up for auto-fulfillment](#label-laf-error-account-not-set-up)
- [The user is unable to share to accounts in other regions](#label-laf-troubleshoot-missing-laf-privileges)

## A direct share with the same name already exists in the remote account

Error:
:   Two or more providers within an organization can’t create a direct share with the same name.

Cause:
:   A direct share with the same name already exists in the secure share area used by Cross-Cloud Auto-Fulfillment. This can happen if a different account in your organization is using Cross-Cloud Auto-Fulfillment and has a direct share with the same name auto-fulfilled to that cloud region. The secure share area in a cloud region is shared across all provider accounts in your organization.

Solution:
:   Rename the direct share that contains the share attached to the listing that will be auto-fulfilled. Renaming the direct share doesn’t affect any downstream consumers.

## A role is missing privileges on a share

Error:
:   OWNERSHIP on the selected share is required to enable auto-fulfillment.

Cause:
:   Only the ACCOUNTADMIN role can set up auto-fulfillment. This error can occur when the ACCOUNTADMIN
    role is not granted and does not inherit the role that owns the share attached to the listing.

Solution:
:   Grant the role that owns the share to the ACCOUNTADMIN role. For example, run the following:

    Copy code

    ```
    GRANT ROLE SHARE_OWNER TO ROLE ACCOUNTADMIN;
    ```

## Auto-fulfillment failed during snapshot generation for multiple listings

Error:
:   Internal error occurs during auto-fulfillment for multiple listings.

Cause:
:   The error can occur if multiple listings use the same database for cross-region sharing and one of the listings contains or
    references an unsupported object type. This can impact the auto-fulfillment process for all listings that use that database.
    For example, let’s say a provider adds a new listing to be transferred across clouds or regions. The new listing shares objects from
    a database that other listings also use. The new listing includes a VIEW using a BUILD\_SCOPED\_FILE\_URL, a function that calls
    GET\_STAGE\_FILE to retrieve data from an external stage in S3. Because external stages are not supported for auto-fulfillment,
    and the objects in that database are transferred together as a group, the other listings get the same error. If no action is taken,
    existing consumers in remote regions will not get updates, and new customers will not be able to get the data product.

    Similar-looking errors can occur for other issues like network issues, authentication problems, or unsupported object types in
    certain operations (like replication).

Solution:
:   Starting with listings that were most recently added or updated, verify the following:

    - Verify that the listings in the group of listings that have errors include only
      supported object types for cross-region auto-fulfillment.
    - Verify that none of the objects make reference to unsupported object types. You might have to check multiple levels of
      dependencies to identify the root cause of the issue, for example, a view calling BUILD\_SCOPED\_FILE\_URL which itself calls
      GET\_STAGE\_FILE to retrieve data from an external stage.
    - Use separate databases for listings that require different object types to avoid cross-impact.
    - Remove or replace any unsupported objects to avoid auto-fulfillment errors.
    - Check for any potential network, authentication, or missing GRANTS issue.
    - Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if the issue persists or you need assistance.

## The database is larger than 10 terabytes

Error:
:   Auto-fulfillment is unavailable because the share is associated with a database larger than 10TB.

    Auto-fulfillment is unavailable because the data product is associated with a database larger than 10TB.

Cause:
:   The database that contains the objects in your share is larger than the 10TB limit for database replication and auto-fulfillment.
    The limit exists to prevent unexpectedly high costs resulting from auto-fulfillment or replication, but can be changed.

Solution:
:   Explore the cost ramifications for auto-fulfilling a database larger than 10TB to one or more regions. See [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

    If you accept the potential added cost, an account administrator (a user with the ACCOUNTADMIN role) can raise the limit for your account by setting the [LISTING\_AUTO\_FULFILLMENT\_INITIAL\_REFRESH\_SIZE\_LIMIT\_IN\_TB](/sql-reference/parameters#label-listing-auto-fulfillment-initial-refresh-size-limit-in-tb) parameter. For example:

    Copy code

    ```
    ALTER ACCOUNT SET LISTING_AUTO_FULFILLMENT_INITIAL_REFRESH_SIZE_LIMIT_IN_TB = 20.0;
    ```

    To remove the size limit, set the value to `0.0`.

Note

If you configured [object-level (SUB\_DATABASE) auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-object-level-auto-fulfillment), then the auto-fulfillment size safety check will only include shared dependencies and not the entire database.

## The data product contains a reference database

Error:
:   The reference database in the share is not supported for auto-fulfillment.

    The shared object references below are incompatible.

    The references below in the shared database are incompatible.

Cause:
:   The share attached to the listing contains a reference database or contains objects that reference a different database. Referencing objects
    in a different database is not supported for auto-fulfillment.

Solution:
:   You can do one of the following:

    > - Remove the reference database, and objects referring to the reference database, from the share.
    > - Use a different database that has all of the objects required for the share. You might need to recreate tables in the new database
    >   and update view and function definitions.
    > - Use manual fulfillment instead. Only some listings can be manually fulfilled. See [Manually replicate data to fulfill a listing request](https://other-docs.snowflake.com/en/collaboration/provider-listings-managing#label-manually-replicate-listing).

## The data product contains unsupported objects

Error:
:   The data product contains objects incompatible with cross-region sharing. Update the data product to share with accounts in other regions.

    The shared objects below are incompatible.

    The objects below in the shared database are incompatible.

Cause:
:   The database that contains the share contains objects unsupported by auto-fulfillment. Because the entire database gets auto-fulfilled,
    even if the share does not contain the objects, you might still encounter this issue.

    For an application package, you might see this issue if the data content included in the application or the referenced database contains
    objects unsupported by auto-fulfillment.

Solution:
:   Review the full list of supported objects for auto-fulfillment. See [Objects supported for auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-supported-objects).

    If the database contains objects that are not supported, you can do one of the following:

    > - Remove the unsupported objects from the database or application package to be shared.
    > - Use a different database that has all the objects required for the share, and no unsupported objects.

## The listing database is a primary database

Error:
:   The primary database in the share is not supported for auto-fulfillment.

    The primary database in the data product is not supported for auto-fulfillment.

    Cannot auto-fulfill listing: listing database is a global database, which is not supported.

Cause:
:   The share contains objects from a database that was previously used for database replication.

Solution:
:   You can do one of the following:

    - Convert the secondary and primary databases to use replication groups and set up a manual replication group if desired. See
      [Transitioning from database replication to group-based replication](/user-guide/account-replication-config#label-disabling-database-replication)
    - Use a different database that has all of the objects required for the share, and has not been previously replicated.

## The listing database is a secondary database

Error:
:   The secondary database in the share is not supported for auto-fulfillment. You will need to manually set up accounts in available regions,
    replicate the database to each account, create a secure share in each account, and attach those shares to this listing.

    The secondary database in the data product is not supported for auto-fulfillment. Please choose another data product.

Cause:
:   The database that contains the share is a secondary database, which is read-only and cannot be replicated or auto-fulfilled.

Solution:
:   You can do one of the following:

    > - Create your listing from the account where the database is the primary database.
    > - Stop replicating the database manually to other regions.

## Receiving an error that my account is not set up for auto-fulfillment

Error:
:   Cannot set replication schedule for listing <my\_listing>: account not set up for auto-fulfillment.

Cause:
:   Auto-fulfillment hasn’t been enabled for your account, or you’re using a trial account.

Solution:
:   - If you’re using a full (non-trial) account, you can enable auto-fulfillment on your account using the [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account) system function.

      You must use the [ORGADMIN](/user-guide/organization-administrators) role to call this system function. If you aren’t the organization administrator, contact your organization administrator to enable auto-fulfillment for your account.

      For more information, see [Enable auto-fulfillment for your account](/collaboration/provider-listings-auto-fulfillment-setup#label-listings-auto-fulfill-enable).
    - If you’re using a trial account, upgrade to a full account to enable auto-fulfillment.

## The user is unable to share to accounts in other regions

Error:
:   To share to accounts in other regions, please contact your organization administrator to delegate privileges to the ACCOUNTADMIN role in
    this account.

Cause:
:   Your role does not have permission to set up auto-fulfillment.

Solution:
:   Contact your organization administrator to [Manage privileges for auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges).
