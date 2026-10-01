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

## Configuring policy enforcement mode

The `reshare_policy_enforcement` property controls how governance policies are evaluated when consumers access reshared data. Set this in the listing manifest alongside `resharing.enabled`.

Copy code

```
resharing:
  enabled: true
  only_within_organization: true
  reshare_policy_enforcement: CALLER   # or RESHARER (default)
```

The two modes are:

- **`RESHARER`** (default): Governance policies are evaluated in the resharer’s account context. Each consumer sees what the resharer can see from the provider’s data. Recommended for cross-organization resharing.
- **`CALLER`**: Governance policies are evaluated in each consumer’s account context. Consumers see only what they themselves are permitted to see from the provider’s data, regardless of what the resharer sees. Recommended for same-organization resharing where the provider wants to enforce per-consumer entitlements — for example, when base tables use `SYS_CONTEXT` to restrict access by org user group.

### When to use each mode

| Use case | Recommended mode |
| --- | --- |
| Resharing with accounts outside your organization | `RESHARER` |
| Resharing within your organization so that consumers see exactly what the resharer can access | `RESHARER` |
| Resharing within your organization with per-consumer policy enforcement | `CALLER` |

Expand

Show lessSee more

### Immutability

Important

Policy enforcement mode cannot be changed after a listing is published. To use a different mode, you must create a new listing.

### Limitations of CALLER mode

- **Same organization required**: All accounts involved in resharing — provider, resharer, and downstream consumers — must belong to the same Snowflake organization. Resharers can create secure views over the provider’s listing using either its Uniform Listing Locator (ULL) or an imported database; a ULL is not required.
- **CALLER mode propagates**: Once a listing in the resharing chain uses CALLER mode, all downstream reshared listings must also use CALLER mode. Downstream resharers cannot switch to RESHARER mode.
- **Auto-fulfillment required for cross-region**: If a downstream consumer reshares your data to a different region, your listing must have auto-fulfillment enabled and be visible to that target region.

### Objects supported for sharing and resharing

Sharing an object with a consumer does not necessarily mean that the consumer can reshare it. The following table compares objects in an
incoming share or listing when resharing is enabled. For tables, dynamic tables, and views, the resharer exposes the incoming data through
a secure view in their own database; they cannot attach an object from the imported database directly to an outgoing share.

| Object in the incoming data product | Sharing | Resharing a direct share (`RESHARER`) | Resharing a listing (`RESHARER`) | Resharing a listing (`CALLER`) |
| --- | --- | --- | --- | --- |
| Table | Supported | Supported through a secure view | Supported through a secure view | Supported through a secure view |
| Dynamic table | Supported | Supported through a secure view | Supported through a secure view | Supported through a secure view |
| View | Supported | Supported through a secure view | Supported through a secure view | Supported through a secure view |
| UDF or UDTF | Supported | Not supported | Not supported | Supported |

Expand

Show lessSee more

This table covers the object types supported for resharing, not every object type that can be shared. Resharing apps is not supported.
For direct-share restrictions, see [Resharing shares](/user-guide/data-share-consumers#resharing-shares). A `CALLER`-mode listing requires
all accounts in the resharing chain to belong to the same Snowflake organization.

Note

Resharing of direct shares (shares created with [CREATE SHARE](/sql-reference/sql/create-share)) always uses `RESHARER` enforcement mode regardless of any configuration. Only views, tables, and dynamic tables are supported for resharing from a direct share.

### Cross-region behavior

When using caller mode for cross-region resharing, Snowflake replicates the provider’s data directly to the consumer’s target region. Unlike resharer mode, no dynamic tables are created in the resharer’s account.

Note

If all downstream reshared listings are dropped, the provider’s remote share replica is not automatically cleaned up. To remove the replica, you can drop the listing, disable auto-fulfillment, or remove all target accounts from the listing’s visible regions.

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

When resharing data that has governance policies applied, only the following policy types are supported. With `RESHARER` enforcement,
policies are evaluated in the resharer’s account context; with `CALLER` enforcement, they are evaluated in the downstream consumer’s
account context:

- [Row access policy](/sql-reference/sql/create-row-access-policy)
- [Masking policy](/sql-reference/sql/create-masking-policy)

Important

If you apply an unsupported policy type on your shared data, resharing will be blocked. This happens even if `resharing.enabled` is set to
`true`. This will also revoke access for any downstream consumers who are already consuming reshared listings.

## Supported context functions

If your shared data uses context functions in governance policies or secure view definitions, only the following context functions are
supported for resharing. With `RESHARER` enforcement, functions resolve in the resharer’s context; with `CALLER` enforcement, they resolve
in the downstream consumer’s context:

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
