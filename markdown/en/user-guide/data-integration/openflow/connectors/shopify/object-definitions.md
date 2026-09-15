# Object definition overrides for the Openflow Connector for Shopify

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the **Object Definitions Override** parameter in detail, including the
full schema, promoted column and child field definitions, and a complete example.

The **Object Definitions Override** parameter accepts a JSON array of object definitions.
Each definition can add a new object type or fully replace an existing catalog entry.

## Object definition schema

Important

The **Object Definitions Override** value must be valid JSON. If the JSON is malformed,
the connector fails to start. Validate your JSON before applying the override.

The following fields are supported in each object definition:

| Field | Description |
| --- | --- |
| `apiType` | **(Required)** The query endpoint name in the Shopify Admin GraphQL API. This must match the root query field exactly (for example, `orders` for the [orders query](https://shopify.dev/docs/api/admin-graphql/2026-04/queries/orders), `products` for the [products query](https://shopify.dev/docs/api/admin-graphql/2026-04/queries/products)). Used as the key for lookup and override matching. |
| `tableName` | **(Required)** The Snowflake destination table name. |
| `gidTypeName` | The Shopify GID resource type (for example, `Order`, `Product`). Used for delete cascade and child record routing. |
| `additionalGidTypeNames` | Array of additional GID type names that also map to this object. Use when Shopify returns the same resource under more than one GID type name, so that records are routed to the correct table regardless of which GID type appears in the response. |
| `graphqlFields` | List of GraphQL selection fields. Each entry is a field name, a nested selection (for example, `"totalPriceSet { shopMoney { amount currencyCode } }"`), or an aliased field with arguments (for example, `"tier: metafield(key: \"custom.tier\") { value }"`). Aliases are useful for querying metafields by key. |
| `requiredQueryArgs` | Map of fixed GraphQL argument key-value pairs appended to every query for this object. Use for endpoints that require non-standard arguments that aren’t covered by the built-in query parameters (for example, `{"type": "SALES_CHANNEL"}`). |
| `supportsIncremental` | Whether the object supports incremental sync. Default: `true`. |
| `incrementalField` | The field used for watermark-based incremental queries (for example, `updatedAt`, `createdAt`). The field must both exist on the returned type **and** be accepted as a filter by the query root’s `query:` argument. A field that exists on the type but isn’t supported as a filter causes `GetShopifyIncremental` to fail with `Invalid search field: <name>`. If this happens, set `supportsIncremental` to `false` and `refreshStrategy` to `FULL_PERIODIC` instead. |
| `refreshStrategy` | Controls the sync mode. `INCREMENTAL` (default) uses watermark-based incremental queries. `FULL_PERIODIC` performs a complete re-sync on each run instead. `PARENT_PIGGYBACKED` means this object is extracted from another object’s query response and is not queried independently. |
| `supportsDeletes` | Whether the connector should track deletion events for this object. Default: `false`. |
| `promotedColumns` | Array of column definitions that extract values from the JSON payload into dedicated Snowflake columns. For more information, see [Promoted columns](#label-promoted-columns). |
| `childFields` | Array of child connection definitions that are extracted into separate tables. For more information, see [Child fields](#label-child-fields). |
| `ignoredFields` | List of field names to exclude from queries. Matches only on the leading name of each top-level entry in `graphqlFields`. For nested fields inside a sub-selection (for example, a field inside `defaultEmailAddress { ... }`), `ignoredFields` has no effect. Remove the field directly from the sub-selection in `graphqlFields` instead. |
| `supportsBulk` | Whether the object supports bulk queries through the Shopify Bulk Operations API. Default: `true`. |
| `sortKeys` | List of sort key values (from the object’s corresponding `SortKeys` enum) used to order results during bulk and incremental queries. For example, `["UPDATED_AT", "ID"]`. |
| `sortKeyStyle` | How sort key values are formatted in queries. `ENUM` (default) uses bare enum values (for example, `UPDATED_AT`). `STRING` uses quoted lowercase strings (for example, `"updated_at"`). Use `STRING` for object types that accept string sort keys, such as metaobjects. |

Expand

Show lessSee more

## Promoted columns

Promoted columns extract specific values from the raw JSON payload into dedicated typed
columns in the destination table. This makes frequently queried fields available as
first-class Snowflake columns for efficient filtering and aggregation.

Each promoted column has the following fields:

| Field | Description |
| --- | --- |
| `name` | The Snowflake column name (uppercase recommended). |
| `path` | A JSONPath expression pointing to the value in the raw record (for example, `$.email`, `$.totalPriceSet.shopMoney.amount`). |
| `type` | The Snowflake column type. The following values are supported:   | Value | Snowflake type | Notes | | --- | --- | --- | | `string` | `VARCHAR` | None | | `integer` | `NUMBER(38,0)` | None | | `boolean` | `BOOLEAN` | None | | `float` | `FLOAT` | None | | `money` | `NUMBER(38,4)` | Converts Shopify amount strings to numeric. | | `timestamp` | `TIMESTAMP_TZ` | ISO-8601 strings. | | `date` | `DATE` | None | | `id` | `NUMBER(38,0)` | Strips the `gid://shopify/*/` prefix and returns the numeric ID. | | `gid` | `VARCHAR` | Stores the full GID string. | | `json` | `VARIANT` | Stores sub-objects as VARIANT. | |

Expand

Show lessSee more

## Child fields

Child field definitions extract nested connections (such as order line items) into separate
Snowflake tables. Each child table includes a `__PARENT_ID` column linking records back
to the parent.

Each child field has the following fields:

| Field | Description |
| --- | --- |
| `fieldName` | The GraphQL connection field name in the parent object (for example, `lineItems`). |
| `tableName` | The Snowflake table name for the child records. |
| `gidTypeName` | The Shopify GID type for the child (for example, `LineItem`). |
| `connectionType` | `edges` (paginated connection) or `array` (inline array). Default: `edges`. |
| `pageSize` | The `first:` limit applied to this child connection in incremental queries. Default and maximum: `250`. |
| `graphqlFields` | Explicit GraphQL selection set for the child table. If omitted, the connector parses the child’s fields from the matching connection entry in the parent’s `graphqlFields` list. |
| `promotedColumns` | Array of promoted column definitions for the child table, using the same schema as top-level `promotedColumns`. |

Expand

Show lessSee more

Note

Shopify rejects `pageSize` values above 250 with a `first cannot exceed 250` error. This limit doesn’t apply to bulk loads: the Shopify Bulk Operations API ignores the `first:` argument and returns all child records. For more information, see [Limitations](/user-guide/data-integration/openflow/connectors/shopify/about#label-shopify-connector-limitations).

## Union types and GID routing

When a query root returns a union type, the records in the Shopify Bulk API response carry GID types that correspond to the **concrete wrapper node types**, not the query root name or the GraphQL union type name. The connector’s `PartitionShopifyByObject` processor routes records by GID type, so if the GID type isn’t registered in `gidTypeName` or `additionalGidTypeNames`, records are routed to failure.

For example, the `discountNodes` query root returns the `Discount` union. The records in the response carry GID types `DiscountCodeNode` and `DiscountAutomaticNode`, not `DiscountNode` or `Discount`. To route all records to the same table, set `gidTypeName` to one concrete type and list the others in `additionalGidTypeNames`.

The following example configures `discountNodes` correctly:

Copy code

```
[
  {
    "apiType": "discountNodes",
    "tableName": "DISCOUNTS",
    "gidTypeName": "DiscountCodeNode",
    "additionalGidTypeNames": ["DiscountAutomaticNode"],
    "graphqlFields": [
      "id",
      "discount { ... on DiscountCodeBasic { title status startsAt endsAt createdAt updatedAt } ... on DiscountAutomaticBasic { title status startsAt endsAt createdAt updatedAt } }"
    ]
  }
]
```

Note

When using `promotedColumns` on a union-type object, the JSON root after partitioning is the wrapper node (for example, `{ id, discount: { … } }`), not the inner union member. Promoted column `path` values must include the wrapper field, for example `$.discount.title`, not `$.title`.

For discount syncing with incremental support, use `discountNodes` rather than `codeDiscountNodes` or `automaticDiscountNodes`. The per-subtype query roots don’t accept `updated_at` as a filter, so they require `supportsIncremental: false` and `refreshStrategy: "FULL_PERIODIC"`.

To verify which GID types appear in a real response before writing the definition, run a small test bulk load or check the Shopify documentation for the concrete types returned by the query root.

## Example: Register a custom object type with promoted columns

The following override customizes an existing catalog entry to add scalar fields, nested object
selections, a metafield alias, and promoted columns. One promoted column extracts a value
directly from the aliased metafield.

Copy code

```
[
  {
    "apiType": "draftOrders",
    "tableName": "DRAFT_ORDERS",
    "gidTypeName": "DraftOrder",
    "supportsBulk": true,
    "supportsIncremental": true,
    "incrementalField": "updatedAt",
    "ignoredFields": [],
    "sortKeys": ["UPDATED_AT", "ID"],
    "supportsDeletes": false,
    "graphqlFields": [
      "id",
      "createdAt",
      "updatedAt",
      "name",
      "status",
      "email",
      "currencyCode",
      "totalQuantityOfLineItems",
      "customer { id }",
      "totalPriceSet { shopMoney { amount currencyCode } }",
      "billingAddress { address1 city countryCode zip }",
      "draft_po_number: metafield(key: \"custom.draft_po_number\") { key namespace compareDigest createdAt id jsonValue legacyResourceId updatedAt value definition { id description key pinnedPosition } }"
    ],
    "promotedColumns": [
      { "name": "STATUS", "path": "$.status", "type": "string" },
      { "name": "NAME", "path": "$.name", "type": "string" },
      { "name": "CUSTOMER_ID", "path": "$.customer.id", "type": "gid" },
      { "name": "TOTAL_PRICE_AMOUNT", "path": "$.totalPriceSet.shopMoney.amount", "type": "money" },
      { "name": "DRAFT_PO_NUMBER", "path": "$.draft_po_number.value", "type": "string" }
    ],
    "childFields": []
  }
]
```

## Example: Override an object with child fields

The following override customizes the `orders` object to extract line items and fulfillments
into separate tables. Line items use a paginated connection (`edges`); fulfillments are an
inline array in the parent response (`array`).

Copy code

```
[
  {
    "apiType": "orders",
    "tableName": "ORDERS",
    "gidTypeName": "Order",
    "graphqlFields": [
      "id",
      "createdAt",
      "updatedAt",
      "name",
      "email",
      "lineItems(first: 250) { edges { cursor node { id title quantity originalUnitPriceSet { shopMoney { amount currencyCode } } } } }",
      "fulfillments { id status createdAt }"
    ],
    "childFields": [
      {
        "fieldName": "lineItems",
        "tableName": "ORDER_LINE_ITEMS",
        "gidTypeName": "LineItem",
        "connectionType": "edges"
      },
      {
        "fieldName": "fulfillments",
        "tableName": "ORDER_FULFILLMENTS",
        "gidTypeName": "Fulfillment",
        "connectionType": "array"
      }
    ]
  }
]
```
