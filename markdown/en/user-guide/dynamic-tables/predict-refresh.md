# Predict refresh behavior

You can ask Snowflake what a dynamic table’s next refresh will do before it happens. `EXPLAIN CHANGES`
generates metadata about the changes a statement would make, without actually running it. For a dynamic
table, that metadata includes details about its refresh behavior. There are two ways to get this
information:

- **Predict a refresh directly.** Prefix a manual refresh with `EXPLAIN CHANGES` to ask what the next
  refresh would do right now.
- **Predict the effect of a DDL change.** Prefix a statement that changes the table’s definition or
  properties with `EXPLAIN CHANGES` to ask what its next refresh would do after that change, without
  applying the change. See [Predict the next refresh](#label-dynamic-tables-predict-refresh-predict).

Both forms return the same kind of prediction, described in the rest of this page.

## Predict the next refresh

Prefix a DDL statement that targets a dynamic table with `EXPLAIN CHANGES`:

Copy code

```
EXPLAIN CHANGES [ USING {TABULAR | JSON | TEXT} ] <ddl_statement>
```

Copy code

```
EXPLAIN CHANGES ALTER DYNAMIC TABLE dt_orders SET TARGET_LAG = '5 minutes';
```

The result has an `effects` column. On the row whose `domain` is `DYNAMIC_TABLE`, that column
carries the refresh prediction:

```
[
  {
    "effect_type": "DYNAMIC_TABLE_REFRESH",
    "properties": {
      "refresh_mode": "ADAPTIVE",
      "effective_refresh_action": "INCREMENTAL",
      "is_expect_failure": false
    }
  }
]
```

The statement wasn’t applied, and `dt_orders` still has its original target lag. With rows in
`raw_orders` that `dt_orders` hasn’t processed yet, the prediction says that once you do apply the
change, the next refresh processes only the rows that changed.

Note

By default, `EXPLAIN CHANGES` returns a tabular result: a row for each object the statement touches,
with columns `operation`, `domain`, `name`, `changes`, and `effects`. For example:

```
operation    domain           name                            changes    effects
ALTER        DYNAMIC_TABLE    "MYDB"."MYSCHEMA"."DT_ORDERS"    []         [{"effect_type": "DYNAMIC_TABLE_REFRESH", "properties": {"refresh_mode": "ADAPTIVE", "effective_refresh_action": "INCREMENTAL", "is_expect_failure": false}}]
```

The `changes` column describes the set of changes the statement would make, which is outside the scope
of this page. For refresh behavior, read the `effects` column on the row whose `domain` is
`DYNAMIC_TABLE`.

## Read the prediction

Each `DYNAMIC_TABLE_REFRESH` effect carries a `properties` object:

| Property | Description |
| --- | --- |
| `effective_refresh_action` | What the next refresh action is. For the possible values, see [Refresh actions](#label-dynamic-tables-predict-refresh-actions). |
| `is_expect_failure` | `true` when the next refresh would fail. Always present. |
| `refresh_mode` | The refresh mode the table currently uses. Omitted when the prediction is a failure. |
| `refresh_mode_reason` | Why the dynamic table chooses this refresh mode. Omitted when the table’s refresh mode is INCREMENTAL, and when the prediction is a failure. See [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes). |
| `effective_refresh_action_reason` | Which change requires reinitialization. Present only when reinitialization is needed. This is the predicted form of the `REINIT_REASON` column in [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history). |
| `expect_failure_reason` | The error the refresh would return. Present only when `is_expect_failure` is `true`. |

Expand

Show lessSee more

## Refresh actions

`effective_refresh_action` uses the same vocabulary as the `REFRESH_ACTION` column in
[DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history): `NO_DATA`,
`REINITIALIZE`, `FULL`, `INCREMENTAL`, and `CUSTOM_INCREMENTAL`. Because it’s a prediction rather than
a completed refresh, `effective_refresh_action` also reports two values that `REFRESH_ACTION` doesn’t
have:

| Action | What it means |
| --- | --- |
| `CREATE` | The next refresh initializes a new instance of the table for the first time. Reported for statements that create the dynamic table or replace it. |
| `FAILURE` | The next refresh would fail. `is_expect_failure` is `true` and `expect_failure_reason` carries the error. A refresh that fails after it starts instead reports the action it attempted, along with its error, in refresh history. |

Expand

Show lessSee more

Note

The refresh mode is the configured refresh behavior of the dynamic table. The refresh action is the
effective action that the dynamic table will take to refresh. For example, ADAPTIVE is a refresh mode
that a dynamic table may have, but the effective action that an ADAPTIVE dynamic table takes depends on
what the refresh needs to do.

## Check whether a change reinitializes your dynamic table

General rules govern which changes force a dynamic table to reprocess all of its source data. For
the full list, see
[What triggers reinitialization](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).
Changing `REFRESH_MODE` is one such case: see
[Refresh mode transitions](/user-guide/dynamic-tables/modify#label-dynamic-tables-refresh-mode-transitions).

When the prediction is `REINITIALIZE`, `effective_refresh_action_reason` names which part of your
change caused it. For example, `dt_orders` has a
[frozen region](/user-guide/dynamic-tables/frozen-regions) covering its settled orders, and removing
it puts those rows back in scope:

Copy code

```
EXPLAIN CHANGES ALTER DYNAMIC TABLE dt_orders UNSET FROZEN WHERE;
```

```
[
  {
    "effect_type": "DYNAMIC_TABLE_REFRESH",
    "properties": {
      "refresh_mode": "ADAPTIVE",
      "effective_refresh_action": "REINITIALIZE",
      "is_expect_failure": false,
      "effective_refresh_action_reason": "Frozen region changed or removed."
    }
  }
]
```

## Limitations

`EXPLAIN CHANGES` predicts the refresh behavior of only the dynamic table the statement targets, not
other dynamic tables the statement’s query reads from.

The prediction reflects the state of the table and its source data at the moment `EXPLAIN CHANGES`
runs. It can change before you apply the statement, because it depends on the data that has arrived
so far and on the table’s current state.

## What’s next

- To see the general rules for which changes trigger reinitialization, see
  [Modify dynamic tables](/user-guide/dynamic-tables/modify).
- To understand the differences between INCREMENTAL, FULL, AUTO, ADAPTIVE, and CUSTOM\_INCREMENTAL
  refresh modes, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To confirm what a refresh actually did after you apply a change, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To understand the cost of reprocessing all source data, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
