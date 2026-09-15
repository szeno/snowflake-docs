Categories:
:   [Table functions](/sql-reference/functions-table) (Object Modeling)

# GET\_OBJECT\_REFERENCES

Returns a list of objects that a specified object references. Input is currently limited to the name of a view.

The following table identifies which types of database objects are currently returned in the output:

| Object Type | Returned in Output? |
| --- | --- |
| Tables | Yes |
| Views (including secure views) | Yes |
| Materialized views | No |
| Named stages (internal or external) | No |
| Streams | No |
| User-defined functions (UDF) / user-defined table functions (UDTF) | No |

Expand

Show lessSee more

## Syntax

Copy code

```
GET_OBJECT_REFERENCES(
  DATABASE_NAME => '<string>'
  , SCHEMA_NAME => '<string>'
  , OBJECT_NAME => '<string>' )
```

## Arguments

`DATABASE_NAME => 'string'`
:   Name of the database in which the schema and object reside.

`SCHEMA_NAME => 'string'`
:   Name of the schema in which the object resides.

`OBJECT_NAME => 'string'`
:   Name of the object. Currently limited to the name of a view (secure or not secure).

## Returns

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATABASE\_NAME | TEXT | Name of the database that contains the queried object. |
| SCHEMA\_NAME | TEXT | Name of the schema that contains the queried object. |
| OBJECT\_NAME | TEXT | Name of the queried object. |
| REFERENCED\_DATABASE\_NAME | TEXT | Name of the database containing an object that the queried object references. |
| REFERENCED\_SCHEMA\_NAME | TEXT | Name of the schema containing an object that the queried object references. |
| REFERENCED\_OBJECT\_NAME | TEXT | Name of an object that the queried object references. |
| REFERENCED\_OBJECT\_TYPE | TEXT | Type of object identified in the REFERENCED\_OBJECT\_NAME column. Values include TABLE or VIEW. |

Expand

Show lessSee more

## Usage notes

- This function requires the following privileges:

  - SELECT on the view. To obtain references for a view, the role in use or a role granted to the role in use must have the SELECT
    privilege on the view. For details, refer to [Table privileges](/user-guide/security-access-control-privileges#label-table-privileges) and [View privileges](/user-guide/security-access-control-privileges#label-view-privileges).
  - OWNERSHIP on the secure view. If the dependency chain references any secure view, the role in use or a role granted to the role in
    use must have the OWNERSHIP privilege on the secure view. Otherwise, Snowflake returns this error message:

    Copy code

    ```
    Insufficient privileges to operate on view '<view_name>'
    ```
- The `DATABASE_NAME`, `SCHEMA_NAME`, and `OBJECT_NAME` values must be enclosed in single quotes. Also, if any of these names contains any spaces, mixed-case characters, or special characters, the name must be double-quoted within the single quotes (e.g. `'"My DB"'` vs `'mydb'`).
- If the view references stages, UDFs, or materialized views, this function returns an error, rather than returning
  a list of referenced tables and views.

## Examples

Return the list of references for a view:

> Copy code
>
> ```
> -- create a database
> create or replace database ex1_gor_x;
> use database ex1_gor_x;
> use schema PUBLIC;
>
> -- create a set of tables
> create or replace table x_tab_a (mycol int not null);
> create or replace table x_tab_b (mycol int not null);
> create or replace table x_tab_c (mycol int not null);
>
> -- create views with increasing complexity of references
> create or replace view x_view_d as
> select * from x_tab_a
> join x_tab_b
> using ( mycol );
>
> create or replace view x_view_e as
> select x_tab_b.* from x_tab_b, x_tab_c
> where x_tab_b.mycol=x_tab_c.mycol;
>
> --create a second database
> create or replace database ex1_gor_y;
> use database ex1_gor_y;
> use schema PUBLIC;
>
> -- create a table in the second database
> create or replace table y_tab_a (mycol int not null);
>
> -- create more views with increasing levels of references
> create or replace view y_view_b as
> select * from ex1_gor_x.public.x_tab_a
> join y_tab_a
> using ( mycol );
>
> create or replace view y_view_c as
> select b.* from ex1_gor_x.public.x_tab_b b, ex1_gor_x.public.x_tab_c c
> where b.mycol=c.mycol;
>
> create or replace view y_view_d as
> select * from ex1_gor_x.public.x_view_e;
>
> create or replace view y_view_e as
> select e.* from ex1_gor_x.public.x_view_e e, y_tab_a
> where e.mycol=y_tab_a.mycol;
>
> create or replace view y_view_f as
> select e.* from ex1_gor_x.public.x_view_e e, ex1_gor_x.public.x_tab_c c, y_tab_a
> where e.mycol=y_tab_a.mycol
> and e.mycol=c.mycol;
>
> -- retrieve the references for the last view created
> select * from table(get_object_references(database_name=>'ex1_gor_y', schema_name=>'public', object_name=>'y_view_f'));
>
> +---------------+-------------+-----------+--------------------------+------------------------+------------------------+------------------------+
> | DATABASE_NAME | SCHEMA_NAME | VIEW_NAME | REFERENCED_DATABASE_NAME | REFERENCED_SCHEMA_NAME | REFERENCED_OBJECT_NAME | REFERENCED_OBJECT_TYPE |
> |---------------+-------------+-----------+--------------------------+------------------------+------------------------+------------------------|
> | EX1_GOR_Y     | PUBLIC      | Y_VIEW_F  | EX1_GOR_Y                | PUBLIC                 | Y_TAB_A                | TABLE                  |
> | EX1_GOR_Y     | PUBLIC      | Y_VIEW_F  | EX1_GOR_X                | PUBLIC                 | X_TAB_B                | TABLE                  |
> | EX1_GOR_Y     | PUBLIC      | Y_VIEW_F  | EX1_GOR_X                | PUBLIC                 | X_TAB_C                | TABLE                  |
> | EX1_GOR_Y     | PUBLIC      | Y_VIEW_F  | EX1_GOR_X                | PUBLIC                 | X_VIEW_E               | VIEW                   |
> +---------------+-------------+-----------+--------------------------+------------------------+------------------------+------------------------+
> ```
