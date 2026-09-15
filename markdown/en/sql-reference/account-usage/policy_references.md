Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# POLICY\_REFERENCES view

This Account Usage view lists policy objects and their references in your account.

The view supports aggregation, feature, masking, network, projection, row access, and storage lifecycle policies.

The view is complementary to the Information Schema table function [POLICY\_REFERENCES](/sql-reference/functions/policy_references).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| POLICY\_DB | VARCHAR | The database in which the policy is set. |
| POLICY\_SCHEMA | VARCHAR | The schema in which the policy is set. |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the policy. |
| POLICY\_NAME | VARCHAR | The name of the policy. |
| POLICY\_KIND | VARCHAR(17) | The type of policy. |
| REF\_DATABASE\_NAME | VARCHAR | The name of the database containing an object that the queried object references. |
| REF\_SCHEMA\_NAME | VARCHAR | The name of the schema containing an object that the queried object references. |
| REF\_ENTITY\_NAME | VARCHAR | The name of the object (i.e. table\_name, view\_name, external\_table\_name) on which the policy is set. |
| REF\_ENTITY\_DOMAIN | VARCHAR | The object type (i.e. table, view) on which the policy is set. |
| REF\_COLUMN\_NAME | VARCHAR | The column name on which the policy is set. |
| REF\_ARG\_COLUMN\_NAMES | VARCHAR | Returns NULL for rows in the query result in which a Column-level Security masking policy is set. |
| TAG\_DATABASE | VARCHAR | The name of the database containing the tag that has a policy assigned to the tag or NULL if a policy is not assigned to the tag. |
| TAG\_SCHEMA | VARCHAR | The name of the schema containing the tag that has a policy assigned to the tag or NULL if a policy is not assigned to the tag. |
| TAG\_NAME | VARCHAR | The name of the tag that has a policy assigned to it or NULL if a policy is not assigned to the tag. |
| POLICY\_STATUS | VARCHAR | Specifies the status of the policy, which can be one of four possible values: `ACTIVE`, `MULTIPLE_MASKING_POLICY_ASSIGNED_TO_THE_COLUMN`, `COLUMN_IS_MISSING_FOR_SECONDARY_ARG`, or `COLUMN_DATATYPE_MISMATCH_FOR_SECONDARY_ARG`. |

Expand

Show lessSee more

Note the following for the POLICY\_STATUS column:

> `ACTIVE`
> :   Specifies that the column (i.e. REF\_COLUMN\_NAME) is only associated with a single policy.
>
> `MULTIPLE_MASKING_POLICY_ASSIGNED_TO_THE_COLUMN`
> :   Specifies that multiple masking policies are assigned to the same column.
>
> `COLUMN_IS_MISSING_FOR_SECONDARY_ARG`
> :   Specifies that the policy (i.e. POLICY\_NAME) is a conditional masking policy and the table (i.e. REF\_ENTITY\_NAME) does not have a
>     column with the same name.
>
> `COLUMN_DATATYPE_MISMATCH_FOR_SECONDARY_ARG`
> :   Specifies that the policy is a conditional masking policy and the table has a column with the same name but a different data type than
>     the data type in the masking policy signature.

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
