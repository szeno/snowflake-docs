# Listing share restrictions

Providers can enable share restrictions on listings at the listing level or at the account level.

## Introduction

Snowflake enforces share restrictions on direct shares by default for the following scenarios:

- Provider accounts in Business Critical or higher editions can’t share data with consumer accounts in lower editions. For example, a
  Business Critical provider account can’t share data with an Enterprise consumer account. For more information about Snowflake editions,
  see [Snowflake editions](/user-guide/intro-editions).
- HIPAA provider accounts can’t share data with non-HIPAA consumer accounts.

Listing share restrictions allow providers to enable these same restrictions on listings.

Note

- This feature supports private external listings, but not private external listings that target
  the entire organization. Organizational listings and public listings are also not supported.
- This feature is opt-in. Snowflake doesn’t enforce share restrictions on listings by default
  as it does with direct shares.
- For backward compatibility, enabling share restrictions on a listing doesn’t revoke access for
  consumers who have already imported the listing. Restrictions only apply to new listing requests
  and new database imports.
- Because this feature is opt-in, Snowflake doesn’t provide any approach to bypass the checks.
  If you want to disable the checks, you can opt out at the listing level or account level.
- This feature is independent of the share restrictions applied on direct shares.

## Share restrictions enablement

You can enable listing share restrictions at two levels:

### Account level

Enabling share restrictions at the account level enforces restrictions on all private external listings owned by the provider account.
Only the ACCOUNTADMIN role can enable or disable share restrictions at the account level.

To enable using Snowsight:

1. Open Provider Studio.
2. Select **Settings**.
3. In the **Share restrictions** section, turn on the toggle.

To enable using SQL:

Copy code

```
ALTER ACCOUNT SET ENABLE_LISTING_SHARE_RESTRICTIONS = TRUE;
```

To disable, set the parameter to `FALSE` or turn off the toggle in Provider Studio.

Note

When share restrictions are enabled at the account level, you can’t disable them for individual listings.

### Listing level

The listing owner role can control share restrictions for a specific listing using Snowsight or SQL.

To enable or disable using Snowsight:

1. Open the listing details page for the listing.
2. Select **Settings** (top right corner).
3. In the **Access** section, turn the **Share restrictions** toggle on or off.

To enable or disable using SQL, set
`share_restrictions = { TRUE | FALSE }` in the [listing manifest](/progaccess/listing-manifest-reference).

Copy code

```
CREATE EXTERNAL LISTING MYLISTING
SHARE MySHARE AS
$$
title: "MyListing"
subtitle: "Subtitle for MyListing"
description: "Description for MyListing"
listing_terms:
   type: "STANDARD"
targets:
    accounts: ["Org1.Account1"]
share_restrictions: TRUE
usage_examples:
    - title: "Sample SQL"
      description: "Simple example"
      query: "select *"
$$;
```

Note

If the `share_restrictions` field isn’t provided in the manifest during the listing update, Snowflake doesn’t change the existing
behavior, which means that the field value stays the same. This avoids accidentally disabling share restrictions if
you forget to set the field in every listing update. To opt out for a listing, explicitly set the field to `FALSE` in the
manifest.

### Observability

On the provider side, if the listing is a private external listing, the
[SHOW LISTINGS](/sql-reference/sql/show-listings) and
[DESCRIBE LISTING](/sql-reference/sql/desc-listing) commands display the share restrictions
field value in the result columns.

## Share restrictions checks

When share restrictions are enabled (either at the listing level or account level), Snowflake
enforces provider-side and consumer-side checks.

### Provider-side checks

**Create listing APIs**

If any of the target accounts violate the edition or HIPAA restrictions, then creating a listing fails.
This check covers all API paths and supports both listing target v1 and v2 formats.

**Alter listing APIs**

If any of the target accounts violate the edition or HIPAA restrictions, then altering a listing fails.
This check covers all API paths and supports both listing target v1 and v2 formats.

**Account upgrade**

If the provider upgrades their account (for example, to Business Critical or higher, or enabling HIPAA) and has
listings with share restrictions enabled, the upgrade fails if any target accounts would violate the new
restrictions. Remove those accounts from listing targets before upgrading.

### Consumer-side checks

**Request listing**

If the listing violates the provider-to-consumer edition or HIPAA restrictions, then requesting a listing fails.
This check saves cross-cloud auto-fulfillment costs if the listing hasn’t been fulfilled before in the
consumer region.

**Create database from listing**

If the listing violates the provider-to-consumer edition or HIPAA restrictions, then creating a database from a
listing fails.

**Account downgrade**

If the consumer downgrades their account (for example, from Business Critical, or disabling HIPAA) and has
imported listings from providers that have share restrictions enabled, the downgrade fails. Drop the imported
databases from those listings before downgrading.
