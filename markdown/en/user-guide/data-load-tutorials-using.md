# Using the tutorials

This topic provides general usage information for the data loading tutorials.

## Privileges for objects used in tutorials

### Practice databases and schemas

For convenience and to avoid mixing your data, we recommend that you create a separate database and/or schema for completing practice exercises, including Snowflake tutorials.

If you create a practice database/schema, make certain to grant the USAGE privilege on the database/schema to any roles for the users who will complete the tutorials. Also
grant the following schema privileges, which are required to create specific objects in the schema:

- CREATE FILE FORMAT
- CREATE STAGE
- CREATE TABLE

### Virtual warehouses

The tutorials also require an active warehouse to load data and execute queries. Grant the following virtual warehouse privileges to the same role:

- OPERATE
- USAGE

### Example

Copy code

```
grant usage on database mydb to role analyst;

grant usage, create file format, create stage, create table on schema mydb.public to role analyst;

grant operate, usage on warehouse mywh to role analyst;
```

## Credit usage

Each tutorial requires an estimated 30 minutes or less to complete, resulting in an average Snowflake credit usage of less than 1 credit (if an X-Small warehouse is used).
