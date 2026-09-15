# Migrate from the legacy Snowflake data share target

With the introduction of the Snowflake V2 data share target, data shares linked to a legacy
Snowflake data share target must be migrated to Snowflake V2. Snowflake and Salesforce don’t
migrate existing data shares automatically — you need to complete the steps in this topic.

This migration is available in all Salesforce Data 360 editions.

Required permission in Salesforce: **Data Cloud Architect** permission set.

## Link the data share to the Snowflake V2 data share target

1. In Salesforce, go to **Data 360** » **Data Shares**.
2. Select a data share that’s linked to a legacy Snowflake data share target.
3. Link the data share to a Snowflake V2 data share target. See
   [Link the Data Share to the Data Share Target](/user-guide/data-integration/zero-copy/salesforce/setup-salesforce)
   for the linking steps.

Don’t unlink the data share from the legacy target yet.

## Verify the Snowflake V2 connection

Confirm that data is flowing to Snowflake through the new Zerocopy Connector before you touch
the legacy target:

- Use `SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES` to confirm the data share appears and its status
  is `MOUNTED` or `UNMOUNTED` as expected. See
  [List shared data products](/user-guide/data-integration/zero-copy/salesforce/explore-data-products).
- Query the catalog-linked database to confirm the shared data looks correct.

Important

Don’t unlink the data share from the legacy target before confirming the Snowflake V2 link is
working. Downstream processes in Snowflake may still reference the database created from the
legacy target.

## Swap to the Snowflake V2 database

Existing pipelines and dashboards reference the database created from the legacy target by
name. Rather than update every downstream reference, swap the V2 catalog-linked database into
that name. The swap is atomic and completes in under a minute.

Choose one of the following options.

### Option 1: Using a Cortex Code skill

If you have Cortex Code, install the `swap-databases` skill from
[Snowflake-Labs/coco-skills](https://github.com/Snowflake-Labs/coco-skills/tree/main/skills/swap-databases),
either with the command below or through the Snowflake UI:

Copy code

```
/swap-databases swap db_from_legacy db_from_v2
```

When prompted, choose **MODE C** to complete the migration.

The skill:

- Compares the legacy and V2 database structures and validates that the required V2 objects are
  present.
- Performs an atomic database-name swap so downstream references continue to resolve to the
  original production database name.

Confirm the schema names match between the two databases when the skill asks you to confirm.
If the names don’t match, drop the V2 catalog-linked database and remount it with
`LEGACY_SALESFORCE_SCHEMA_ALIAS = TRUE`.

Note

If you’re merging multiple data shares into a single catalog-linked database, tell the skill to
proceed even if the schema names don’t match.

### Option 2: Using a SQL function

If you don’t have Cortex Code, validate the databases and schemas yourself before and after
the swap, then run:

Copy code

```
SELECT SYSTEM$ZEROCOPY_SWAP_IMPORTED_DB_WITH_CLD('<imported_db_name>', '<cld_db_name>');
```

- `<imported_db_name>`: the database created from the legacy target.
- `<cld_db_name>`: the catalog-linked database created from the Zerocopy Connector (V2).

If you run into issues after the swap, you can roll back by swapping the databases back with
the same function.

## Unlink the data share from the legacy target

Once the swap is validated:

1. On the data share’s record home page, click **Link/Unlink Data Share Target**.
2. Deselect the legacy data share target.
3. Click **Save**.
