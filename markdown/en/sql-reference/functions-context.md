# Context functions

This family of functions allows for the gathering of information about the context in which the statement is executed. These functions are evaluated
at most once per statement.

## List of functions

| Sub-category | Function | Notes |
| --- | --- | --- |
| General context | [CURRENT\_CLIENT](/sql-reference/functions/current_client) |  |
|  | [CURRENT\_DATE](/sql-reference/functions/current_date) |  |
|  | [CURRENT\_IP\_ADDRESS](/sql-reference/functions/current_ip_address) |  |
|  | [CURRENT\_REGION](/sql-reference/functions/current_region) |  |
|  | [CURRENT\_TIME](/sql-reference/functions/current_time) |  |
|  | [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) |  |
|  | [CURRENT\_VERSION](/sql-reference/functions/current_version) |  |
|  | [GETDATE](/sql-reference/functions/getdate) | Alias for CURRENT\_TIMESTAMP. |
|  | [LOCALTIME](/sql-reference/functions/localtime) | Alias for CURRENT\_TIME. |
|  | [LOCALTIMESTAMP](/sql-reference/functions/localtimestamp) | Alias for CURRENT\_TIMESTAMP. |
|  | [SYSDATE](/sql-reference/functions/sysdate) |  |
|  | [SYSTIMESTAMP](/sql-reference/functions/systimestamp) |  |
|  | [SYS\_CONTEXT](/sql-reference/functions/sys_context) |  |
| Session context | [ALL\_USER\_NAMES](/sql-reference/functions/all_user_names) |  |
|  | [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) | Returns account locator. |
|  | [CURRENT\_ACCOUNT\_NAME](/sql-reference/functions/current_account_name) | Returns account name. |
|  | [CURRENT\_ORGANIZATION\_NAME](/sql-reference/functions/current_organization_name) |  |
|  | [CURRENT\_ORGANIZATION\_USER](/sql-reference/functions/current_organization_user) |  |
|  | [CURRENT\_ROLE](/sql-reference/functions/current_role) |  |
|  | [CURRENT\_AVAILABLE\_ROLES](/sql-reference/functions/current_available_roles) |  |
|  | [CURRENT\_SECONDARY\_ROLES](/sql-reference/functions/current_secondary_roles) |  |
|  | [CURRENT\_SESSION](/sql-reference/functions/current_session) |  |
|  | [CURRENT\_STATEMENT](/sql-reference/functions/current_statement) |  |
|  | [CURRENT\_TRANSACTION](/sql-reference/functions/current_transaction) |  |
|  | [CURRENT\_USER](/sql-reference/functions/current_user) |  |
|  | [GETVARIABLE](/sql-reference/functions/getvariable) |  |
|  | [SET\_SYS\_CONTEXT](/sql-reference/functions/set_sys_context) |  |
|  | [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id) |  |
|  | [LAST\_TRANSACTION](/sql-reference/functions/last_transaction) |  |
| Session object context | [CURRENT\_DATABASE](/sql-reference/functions/current_database) |  |
|  | [CURRENT\_ROLE\_TYPE](/sql-reference/functions/current_role_type) |  |
|  | [CURRENT\_SCHEMA](/sql-reference/functions/current_schema) |  |
|  | [CURRENT\_SCHEMAS](/sql-reference/functions/current_schemas) |  |
|  | [CURRENT\_WAREHOUSE](/sql-reference/functions/current_warehouse) |  |
|  | [INVOKER\_ROLE](/sql-reference/functions/invoker_role) |  |
|  | [INVOKER\_SHARE](/sql-reference/functions/invoker_share) |  |
|  | [IS\_AGENT\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_agent_activated) |  |
|  | [IS\_DATABASE\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_database_role_activated) |  |
|  | [IS\_APPLICATION\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_application_role_activated) |  |
|  | [IS\_APPLICATION\_ROLE\_IN\_SESSION](/sql-reference/functions/is_application_role_in_session) |  |
|  | [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) |  |
|  | [IS\_GRANTED\_TO\_INVOKER\_ROLE](/sql-reference/functions/is_granted_to_invoker_role) |  |
|  | [IS\_INSTANCE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_instance_role_in_session) |  |
|  | [IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_role_activated) |  |
|  | [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session) |  |
|  | [POLICY\_CONTEXT](/sql-reference/functions/policy_context) |  |
| Alert context | [GET\_CONDITION\_QUERY\_UUID](/sql-reference/functions/get_condition_query_uuid) |  |
| Organization context | [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated) |  |
|  | [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_imported) |  |
|  | [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported) |  |

Expand

Show lessSee more

## Usage notes

- Context functions generally do not require arguments (except for [SYS\_CONTEXT](/sql-reference/functions/sys_context)).
- To comply with the ANSI standard, the following context functions can be called without parentheses
  in SQL statements:

  - CURRENT\_DATE
  - CURRENT\_TIME
  - CURRENT\_TIMESTAMP
  - CURRENT\_USER
  - LOCALTIME
  - LOCALTIMESTAMP

  Note

  If you are setting a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables)
  to an expression that calls one of these functions (for example, `my_var := <function_name>();`),
  you must include the parentheses.

## Examples

Display the current warehouse, database, and schema for the session:

Copy code

```
SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
```

```
+---------------------+--------------------+------------------+
| CURRENT_WAREHOUSE() | CURRENT_DATABASE() | CURRENT_SCHEMA() |
|---------------------+--------------------+------------------+
| MY_WAREHOUSE        | MY_DB              | PUBLIC           |
|---------------------+--------------------+------------------+
```

Display the current date, time, and timestamp (note that parentheses are not required to call these functions):

Copy code

```
SELECT CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP;
```

```
+--------------+--------------+-------------------------------+
| CURRENT_DATE | CURRENT_TIME | CURRENT_TIMESTAMP             |
|--------------+--------------+-------------------------------|
| 2024-06-07   | 10:45:15     | 2024-06-07 10:45:15.064 -0700 |
+--------------+--------------+-------------------------------+
```

In a Snowflake Scripting block, call the CURRENT\_DATE function without parentheses to set a variable in a
SQL statement:

Copy code

```
EXECUTE IMMEDIATE
$$
DECLARE
  currdate DATE;
BEGIN
  SELECT CURRENT_DATE INTO currdate;
  RETURN currdate;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| 2024-06-07      |
+-----------------+
```

In a Snowflake Scripting block, attempting to set a variable to an expression that calls the CURRENT\_DATE
function without parentheses results in an error:

Copy code

```
EXECUTE IMMEDIATE
$$
DECLARE
  today DATE;
BEGIN
  today := CURRENT_DATE;
  RETURN today;
END;
$$
;
```

```
000904 (42000): SQL compilation error: error line 5 at position 11
invalid identifier 'CURRENT_DATE'
```

The same block returns the current date when the function is called with the parentheses:

Copy code

```
EXECUTE IMMEDIATE
$$
DECLARE
  today DATE;
BEGIN
  today := CURRENT_DATE();
  RETURN today;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| 2024-06-07      |
+-----------------+
```
