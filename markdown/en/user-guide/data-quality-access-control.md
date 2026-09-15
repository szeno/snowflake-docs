# Access control for data quality

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The following sections describe the access control requirements for actions related to data quality and data metric functions (DMFs).

## Common tasks

Note

| Task | Required privileges/roles | Notes |
| --- | --- | --- |
| Associate a DMF with a table or view | EXECUTE DATA METRIC FUNCTION on the account | You can’t grant global privileges to database roles because database roles are scoped to the database in which they exist. If you have an object that is owned by a database role and you want to set a DMF on that object, you must transfer the OWNERSHIP privilege of the object to a custom role or system role. |
|  | USAGE privilege on the DMF | All users have USAGE on system DMFs [[1]](#footnote-1). For custom DMFs, see [Granting privileges on a custom DMF](#label-data-quality-access-control-custom-dmf). |
|  | One of the following:   - Role with the OWNERSHIP privilege on the table - Role that has the SELECT privilege on the table *and* is specified by the EXECUTE AS ROLE property. | For information about the EXECUTE AS ROLE property, see [Required privilege on the table or view](#label-data-quality-access-control-object-privilege). |
| View associations between objects and DMFs | USAGE privilege on the DMF | All users have USAGE on system DMFs [[1]](#footnote-1). For custom DMFs, see [Granting privileges on a custom DMF](#label-data-quality-access-control-custom-dmf). |
|  | SELECT privilege on the table or view associated with the DMF |  |
| Set the DMF schedule for a table | One of the following:   - OWNERSHIP on the table - Any privilege on the table *and* EXECUTE DATA METRIC FUNCTION on the account |  |
| Create a custom DMF | CREATE DATA METRIC FUNCTION privilege on the schema |  |
| Call a DMF manually | USAGE privilege on the DMF | All users have USAGE on system DMFs [[1]](#footnote-1). For custom DMFs, see [Granting privileges on a custom DMF](#label-data-quality-access-control-custom-dmf). |
|  | SELECT privilege on table or view specified in the call |  |

Expand

Show lessSee more

[1]
If you want to revoke the USAGE privilege on system DMFs, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Viewing data quality results

| Viewing option | Required privileges/roles | Notes |
| --- | --- | --- |
| DATA\_QUALITY\_MONITORING\_RESULTS\_RAW event table | SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN application role |  |
| DATA\_QUALITY\_MONITORING\_RESULTS view | One of the following:   - SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN application role - SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER application role |  |
| DATA\_QUALITY\_MONITORING\_RESULTS function | One of the following:   - SNOWFLAKE.DATA\_QUALITY\_MONITORING\_ADMIN application role - SNOWFLAKE.DATA\_QUALITY\_MONITORING\_VIEWER application role - SNOWFLAKE.DATA\_QUALITY\_MONITORING\_LOOKUP application role | The PUBLIC role is granted the DATA\_QUALITY\_MONITORING\_LOOKUP application role, which means a user can use any role to call the DATA\_QUALITY\_MONITORING\_RESULTS function. |
|  | USAGE privilege on the DMF | All users have USAGE on system DMFs [[2]](#footnote-2). For custom DMFs, see [Granting privileges on a custom DMF](#label-data-quality-access-control-custom-dmf). |
|  | OWNERSHIP or SELECT privilege on the table associated with the DMF |  |
|  | If the EXECUTE AS ROLE property of the association specifies a role, then that role must be active in your session. |  |

Expand

Show lessSee more

[2]
If you want to revoke the USAGE privilege on system DMFs, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Required privilege on the table or view

One of the access control requirements for associating a DMF with a table or view is having the appropriate privilege on that table or view.
To associate a DMF with an object your role must have one of the following privileges:

- OWNERSHIP privilege on the table or view
- SELECT privilege on the table or view

If you want roles with the SELECT privilege on an object to be able to associate DMFs with the object, you must set the EXECUTE AS ROLE
property when defining the association. This property specifies the role that the DMF runs with. For example, suppose the role
`analyst_role` has the SELECT privilege on table `t1`. To associate the `positive_number_count` DMF with table `t1` so it runs with
the `analyst_role` role, run the following command:

Copy code

```
ALTER TABLE t1
  ADD DATA METRIC FUNCTION governance.dfms.positive_number_count on (c1, c2, c3)
    EXECUTE AS ROLE analyst_role;
```

This command can be run by a user with the `analyst_role` role or by a user with a role that is higher in the role hierarchy (for example,
the ACCOUNTADMIN role).

If the EXECUTE AS ROLE property is not specified, the DMF runs with the role of the table owner. The role that the DMF runs with is important
because it can affect data governance policies that behave differently depending on the role of the current user.

### Benefits of the EXECUTE AS ROLE property

The EXECUTE AS ROLE property allows a non-owner to associate and run a DMF on a table or view. This makes it possible for a data governor to
create data quality checks without needing to own the table.

### Limitations

You cannot use the MODIFY DATA METRIC FUNCTION clause to change the role specified by the EXECUTE AS ROLE property. You must drop the
association, then re-create it with a new EXECUTE AS ROLE role.

## Granting privileges on a custom DMF

The GRANT and REVOKE commands require you to specify the arguments of the custom DMF that you create. For example:

Copy code

```
GRANT USAGE ON FUNCTION
  governance.dmfs.count_positive_numbers(TABLE(NUMBER, NUMBER, NUMBER))
  TO data_engineer;
```
