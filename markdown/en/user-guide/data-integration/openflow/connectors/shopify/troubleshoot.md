# Troubleshoot the Openflow Connector for Shopify

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to troubleshoot the Openflow Connector for Shopify.

## A table never appears or is empty

1. Confirm the `apiType` is listed in the **Objects to Sync** parameter and spelled correctly (matching is case-insensitive, but the value must correspond to a query root in the Shopify Admin GraphQL API).
2. Confirm the Shopify dev app has the matching read scope for that object type. For example, `orders` requires `read_orders`. A missing scope produces access errors or empty results for that object type only, without affecting other objects.
3. If you’re using a custom object definition, confirm the **Object Definitions Override** value is valid JSON and a top-level array. Then re-enable the controller services.
4. If you’re relying on auto-discovery, confirm **Enable Introspection** is set to `true`.

## Connector fails with `UnknownHostException` on OAuth2 token request

If the connector logs an error such as `OAuth2 access token request failed` caused by `java.net.UnknownHostException: <your_store>.myshopify.com`, the runtime can’t reach the Shopify domain. This means the External Access Integration (EAI) for the connector hasn’t been created, or USAGE on the EAI hasn’t been granted to the runtime’s execute-as role.

Follow the steps in [Creating network rules and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr#label-create-network-rules-and-external-access-integrations) to create the network rule and EAI, and grant the execute-as role USAGE on the integration. Add both required endpoints to the network rule’s `VALUE_LIST`, as described in the following section.

## Connector fails with `UnresolvedAddressException` when downloading bulk results

If the connector logs a `WebClientServiceException` with `java.net.ConnectException` or `java.nio.channels.UnresolvedAddressException` when accessing a `storage.googleapis.com` URL, the EAI network rule is missing `storage.googleapis.com:443` in its `VALUE_LIST`. After a bulk operation completes, Shopify returns a signed Google Cloud Storage URL for the result file, and the connector must be able to reach that host to download it.

`ALTER NETWORK RULE ... SET VALUE_LIST` overwrites the entire existing list, so as a precaution,
first check what’s already in the rule before changing it:

Copy code

```
DESCRIBE NETWORK RULE OPENFLOW_<RUNTIME_NAME>_NETWORK_RULE;
```

Then update the network rule to include the existing entries plus the two required endpoints:

Copy code

```
ALTER NETWORK RULE OPENFLOW_<RUNTIME_NAME>_NETWORK_RULE
  SET VALUE_LIST = (
    -- existing entries from the value_list column above,
    '<your_store>.myshopify.com:443',
    'storage.googleapis.com:443'
  );
```

## Connector fails with HTTP 401 Unauthorized

If the connector receives an HTTP 401 response with the error `[API] Invalid API key or access token (unrecognized login or wrong password)`, the OAuth2 access token is invalid or has been revoked. Check the following:

1. Confirm the **Shopify Client ID** and **Shopify Client Secret** parameters match the credentials in your app’s **Settings** » **Credentials** in the Dev Dashboard.
2. Confirm the app is installed on the store. If the app was uninstalled at any point, the existing token is revoked. Reinstall the app if needed, then restart the connector to obtain a new token.
3. Confirm the app has been released. Unreleased apps can’t authenticate.

## A query fails with `ACCESS_DENIED` on an object type

The connector can receive a GraphQL `ACCESS_DENIED` error on an object type for two reasons:

- **Missing scope:** The error message is `Access denied for <object> field.` The app doesn’t have the required read scope. Add the corresponding scope in the Dev Dashboard (for example, `read_orders` for `orders`), release the updated app version, and reinstall the app on your store.
- **Protected customer data not approved:** The error message is `This app is not approved to access the <Object> object.` The object requires Shopify’s protected customer data approval. Submit an access request through your app’s **API access** settings in the Dev Dashboard. For more information, see [Protected customer data](https://shopify.dev/docs/apps/launch/protected-customer-data) in the Shopify developer documentation.

If the error occurs on a single field rather than the entire object type, see [A query fails with an access-denied error on one field](#label-shopify-access-denied-one-field).

## A query fails with an access-denied error on one field

Some Shopify Admin GraphQL fields require a write scope to be read. For example, the customer marketing URL fields (`marketingUnsubscribeUrl`, `openTrackingUrl`) require `write_customers`. When the app lacks the required scope, the Shopify API returns an error for that field and the entire object’s query fails.

The fix is to remove the field from the query rather than grant a write scope. Note that `ignoredFields` matches only the leading name of top-level entries and doesn’t apply to nested sub-selections:

- **Top-level field** (a direct entry in `graphqlFields`): remove it from `graphqlFields`, or add its name to `ignoredFields`.
- **Nested field** (inside a sub-selection, for example `marketingUnsubscribeUrl` inside `defaultEmailAddress { ... }`): edit the parent entry’s sub-selection in `graphqlFields` to remove the offending field.

Supply the corrected definition through the **Object Definitions Override** parameter. For more information, see [Object definition overrides for the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/object-definitions).

## Orders are missing older history (only approximately 60 days present)

The `read_orders` scope limits access to orders created in the last 60 days by default. To backfill the full order history, your Shopify app must also be granted `read_all_orders`. This scope requires an access request through your app’s **API access** settings in the Dev Dashboard.

After granting `read_all_orders`, [reset the `orders` object state](/user-guide/data-integration/openflow/connectors/shopify/maintain#label-reload-a-specific-object) so the bulk load reruns and captures the full history.

## Connector won’t start or Object Registry service is INVALID

This is almost always caused by an invalid **Object Definitions Override** value. The value must be syntactically valid JSON and a top-level array. An invalid value or a non-array value prevents the `StandardShopifyObjectRegistryService` from enabling, and the connector fails to start.

To diagnose:

1. Open the **Controller Services** panel and select the `StandardShopifyObjectRegistryService`.
2. Check the service bulletin for the parse error, such as “Invalid JSON” or “Must be a JSON array of object definitions”.
3. Fix the JSON, re-apply the parameter, and re-enable the service.

You can validate the JSON before applying it:

Copy code

```
python3 -c "import json, sys; d = json.load(open('override.json')); sys.exit(0 if isinstance(d, list) else 1)"
```

## Bulk operation fails immediately

The following scenarios can cause a bulk operation to fail immediately or stall.

### Wrong sort key

An unsupported value in `sortKeys` fails the entire bulk operation. Remove the sort key from the object definition or correct it. Omitting `sortKeys` is always safe.

### Bulk operation already in progress

Shopify allows only one bulk operation per shop at a time. The processor retries automatically on the next cycle. If the in-flight operation never clears, another integration on the same shop may be holding the bulk slot.

### Too many or too deeply nested connections

The Shopify Bulk Operations API allows a maximum of 5 connections per query and 2 levels of nesting. If **Include Metafields** is enabled, it consumes one connection. Reduce or flatten child connections to stay within these limits.

### Bulk operation stuck with no progress

Very large datasets can take significant time to complete. If a bulk operation shows no progress after an extended period, it may be stalled. Check the Shopify admin for the status of the bulk operation, or [reset the affected object](/user-guide/data-integration/openflow/connectors/shopify/maintain#label-reload-a-specific-object) to resubmit.

## Duplicate or missing records in Snowflake

**Duplicates immediately after the initial load** are expected during the bulk-to-incremental handoff. The merge uses the compound key `(ID, SHOP_URL)`, so the target table converges after the first incremental run. No action is required.

**Records missing or not updating:** The incremental watermark may have advanced past the affected records. Inspect the per-object state to check the high watermark. If the watermark is incorrect, [reset the object](/user-guide/data-integration/openflow/connectors/shopify/maintain#label-reload-a-specific-object) to rerun the bulk load.

For `orders` specifically, also confirm that the 60-day order history window isn’t the cause. For more information, see [Orders are missing older history](#label-shopify-orders-history).

## Incremental processor routes to retry or failure on first run

The `GetShopifyIncremental` processor routes to retry or failure until the one-time bulk load for each object type completes. This is expected behavior on the first run. Let the bulk load finish before investigating further.

## Incremental fails with “Invalid search field: <name>”

This error appears in the `GetShopifyIncremental` bulletin when the object’s `incrementalField` exists on the returned type but isn’t accepted as a filter by the query root’s `query:` argument.

Fix: in the object’s **Object Definitions Override** entry, set `supportsIncremental` to `false` and `refreshStrategy` to `FULL_PERIODIC`. The object will perform a bulk load once and won’t poll incrementally. To refresh it, reset the object state.

Common objects affected: `codeDiscountNodes`, `automaticDiscountNodes`. For discount syncing with incremental support, use the `discountNodes` query root instead.

After editing the override JSON, re-enable the `StandardShopifyObjectRegistryService`.

## Schema changed in Shopify

Schema evolution isn’t supported. If a Shopify object’s fields change (fields added or removed), [reset the connector state for the affected object](/user-guide/data-integration/openflow/connectors/shopify/maintain#label-reload-a-specific-object) and drop the corresponding Snowflake table to re-snapshot with the updated schema.

## Deletes aren’t appearing in Snowflake

Check the following in order:

1. The object type must support delete detection. Only object types that emit destroy events in the Shopify Events API can be tracked. For more information, see [How deletes are handled](/user-guide/data-integration/openflow/connectors/shopify/about#label-shopify-how-deletes-are-handled).
2. The object type must be listed in the **Objects to Track for Deletes** parameter.
3. The initial bulk load for that object type must be complete before delete polling begins.
4. Delete events younger than the safety buffer (default 5 minutes) are intentionally deferred.
5. Delete polling yields when API credits fall below the rate limit threshold (default 500 points). Check the processor bulletin for messages indicating the connector is below the rate limit threshold and yielding.

## Error: “first cannot exceed 250”

This error occurs when a regular (incremental) query sets `first:` above Shopify’s hard limit of 250. The full error is: *“first cannot exceed 250. To query larger amounts of data with fewer limits, bulk operations should be used instead.”*

Check the **Page Size** parameter and the `pageSize` value in any `childFields` definitions in the **Object Definitions Override**. Both must be 250 or lower.

Note that this limit doesn’t apply to the initial bulk load: the Shopify Bulk Operations API ignores the `first:` argument and returns all records. For parent objects with more children than the `pageSize` value, only the initial bulk load captures the full child set; incremental runs are capped at `pageSize` per parent.

## Sustained throttling

High-volume stores with many objects can remain rate-limited for extended periods. To reduce API usage:

- Increase the **Sync Schedule** and **Deletes Schedule** intervals.
- Reduce the number of entries in **Objects to Sync**.
- Disable **Include Metafields** if metafield data isn’t required.

## StandardPrivateKeyService shows INVALID on SPCS or SNOWFLAKE\_MANAGED deployments

The `StandardPrivateKeyService` controller is only used for BYOC deployments with `KEY_PAIR` authentication. On SPCS deployments, and on BYOC deployments using `SNOWFLAKE_MANAGED` authentication, this controller is unused and may display an INVALID status.

This is expected behavior and has no impact on the connector. The connector works correctly regardless of this controller’s status. Deleting the controller causes local modifications to the flow definition, so Snowflake recommends leaving it in place.
