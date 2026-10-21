Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$MIGRATE\_LEGACY\_EVENT\_ROUTING\_CONFIGURATION

Migrates the legacy event account configuration by creating a new event routing table with corresponding rules.
The function doesn’t activate the new table.

The resulting table has one rule for each region with an active event account. Each rule name uses the format
`<region_name>_RULE`, and the rule’s destination account is the event account configured for that region.

See also:
:   - [SYSTEM$SET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_set_event_sharing_account_for_region)
    - [SYSTEM$UNSET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_unset_event_sharing_account_for_region)
    - [CREATE EVENT ROUTING TABLE](/sql-reference/sql/create-event-routing-table)
    - [ALTER ORGANIZATION SET EVENT ROUTING TABLE](/sql-reference/sql/alter-organization-set-event-routing-table)

## Syntax

Copy code

```
SYSTEM$MIGRATE_LEGACY_EVENT_ROUTING_CONFIGURATION( '<table_name>' )
```

## Arguments

`table_name`
:   Specifies the name of the event routing table to create. The table name must be unique within the organization.

## Returns

Returns a message indicating whether the operation succeeded or failed.

## Usage notes

The migration fails if the legacy event-sharing configuration includes an event account for a region outside the
`PUBLIC` region group. For government or sovereign regions, continue using the legacy event-sharing configuration.

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this SQL function.

## Examples

Migrate the legacy event routing configuration to a new table named `my_table`:

Copy code

```
SELECT SYSTEM$MIGRATE_LEGACY_EVENT_ROUTING_CONFIGURATION('my_table');
```

After the function creates the table, activate it for application listings with
[ALTER ORGANIZATION SET EVENT ROUTING TABLE](/sql-reference/sql/alter-organization-set-event-routing-table):

Copy code

```
ALTER ORGANIZATION SET EVENT ROUTING TABLE my_table FOR ALL APPLICATION LISTINGS;
```
