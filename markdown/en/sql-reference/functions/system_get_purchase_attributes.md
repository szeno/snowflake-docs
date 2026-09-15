Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_PURCHASE\_ATTRIBUTES

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Identifies the behavior of a listing at runtime.

## Syntax

Copy code

```
SYSTEM$GET_PURCHASE_ATTRIBUTES()
```

## Arguments

None

## Returns

The function returns a value of type VARCHAR.

The returned string is in JSON format and contains the following name/value pairs:

`pricing_plan_identifier`
:   The identifier for the pricing plan associated with the listing.

`discount`
:   The pricing plan discount.

`offer_name`
:   The name of the private offer associated with the listing.

## Examples

Copy code

```
SELECT SYSTEM$GET_PURCHASE_ATTRIBUTES();
```

```
+-----------------------------------------------------------------------------------------+
| SYSTEM$GET_PURCHASE_ATTRIBUTES()                                                        |
|-----------------------------------------------------------------------------------------|
| {"pricing_plan_identifier":"TESTPLAN","discount":10.0,"offer_name":"TESTOFFER_WELE_RO"} |
+-----------------------------------------------------------------------------------------+
```
