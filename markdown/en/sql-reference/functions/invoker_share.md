Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# INVOKER\_SHARE

Returns the name of the share that directly accessed the table or view where the INVOKER\_SHARE function is invoked, otherwise the function returns NULL.

## Syntax

Copy code

```
INVOKER_SHARE()
```

## Arguments

None.

## Usage notes

- If using the INVOKER\_SHARE function with [masking policy](/user-guide/security-column-intro), verify that your Snowflake account is Enterprise Edition or higher.
- Use the INVOKER\_SHARE function in a policy that is attached to a table or view that is directly invoked by a share.
- If the INVOKER\_SHARE function is used inside a [User-defined functions overview](/developer-guide/udf/udf-overview) within a masking policy directly attached to a table or view, INVOKER\_SHARE returns NULL because the context of the INVOKER\_SHARE function is the UDF owner, not the share.
- To help determine if a table or view was directly or indirectly invoked by a share, consider using the [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) function in a masking policy. This function returns the Snowflake account for the user’s current session, which can help determine if the table or view is invoked from a data sharing consumer account.

## Examples

Consider a data sharing provider account that has a masking policy set on a column of a secure view. There are two different shares that
can access the secure view to support two different data sharing consumers.

The data sharing provider creates the following policy to use UDFs to identify which share is being accessed. If a user in the data sharing
consumer account attempts to query the data through either share, they see data based on how the UDFs are written, otherwise a fixed masked
value is seen.

> Copy code
>
> ```
> create or replace masking policy mask_share
> as (val string) returns string ->
> case
>   when invoker_share() in ('SHARE1') then mask1_function(val)
>   when invoker_share() in ('SHARE2') then mask2_function(val)
>   else '***MASKED***'
> end;
> ```
