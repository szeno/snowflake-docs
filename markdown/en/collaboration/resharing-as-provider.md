# Using resharing as a provider

As a provider, you can enable resharing on your listings so that consumers can reshare your data product with other accounts. This topic
describes how to set up and manage resharing as a provider.

## Enabling resharing on a listing

Before resharing listings, the provider must enable the `resharing` property in the
[listing manifest reference](/user-guide/collaboration/listings/organizational/org-listing-manifest-reference) or in Snowsight
when creating the listing.

To allow consumers to reshare your data product, set the `resharing.enabled` property to `true` in the listing manifest:

Copy code

```
resharing:
  enabled: true
```

To require that any consumer who reshares your listing can only reshare it to accounts within the consumer’s organization, also set
`resharing.only_within_organization` to `true` in the listing manifest:

Copy code

```
resharing:
  enabled: true
  only_within_organization: true
```

With this property set, your consumer can only reshare within their own organization. This holds at every level: no matter how many times the listing is reshared downstream, access to your data stays within the original consumer’s organization.

For the full listing manifest reference, see [Listing manifest reference](/progaccess/listing-manifest-reference).

## Default resharing behavior for organizational listings

For organizational listings, enabling resharing without specifying `only_within_organization` defaults to resharing within the
organization.
The following YAML shows this default behavior:

Copy code

```
resharing:
  enabled: true
```

## Disabling resharing

You can disable resharing at any time by setting `resharing.enabled` to `false` and republishing the listing. When you disable resharing,
downstream consumption breaks for all consumers of any reshared listings created from your listing.

## Supported governance policies

When resharing data that has governance policies applied, only the following policy types are supported. Note that policies are evaluated in
the context of the account doing the resharing, not by the downstream consumer:

- [Row access policy](/sql-reference/sql/create-row-access-policy)
- [Masking policy](/sql-reference/sql/create-masking-policy)

Important

If you apply an unsupported policy type on your shared data, resharing will be blocked. This happens even if `resharing.enabled` is set to
`true`. This will also revoke access for any downstream consumers who are already consuming reshared listings.

## Supported context functions

If your shared data uses context functions in governance policies or secure view definitions, only the following context functions are
supported for resharing. These functions return values as if they were executed by the account doing the resharing, not by the downstream
consumer:

- [CURRENT\_ACCOUNT](/sql-reference/functions/current_account)
- [CURRENT\_ACCOUNT\_NAME](/sql-reference/functions/current_account_name)
- [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session)
- [CURRENT\_ORGANIZATION\_NAME](/sql-reference/functions/current_organization_name)
- [CURRENT\_DATE](/sql-reference/functions/current_date)
- [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp)

If you add or change governance policies on your base tables that use [unsupported context functions](#label-resharing-supported-context-functions), resharers won’t be able to reshare
your data even if `resharing.enabled` is set to `true`. Downstream consumers of reshared listings will also lose access.

## Enabling cross-region resharing for your resharers

To support cross-region resharing, enable `change_tracking` on your tables. For more information, see
[Change tracking not enabled on base tables](/user-guide/dynamic-tables/troubleshoot-creation#label-dynamic-tables-and-change-tracking).
