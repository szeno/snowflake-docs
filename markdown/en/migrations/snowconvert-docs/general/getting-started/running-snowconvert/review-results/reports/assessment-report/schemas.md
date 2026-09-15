# SnowConvert AI - Schemas

Note

This page of the documentation is for Oracle only.

[![The Schemas section of the assessment report for Oracle.](/static/images/migrations/sc-assets/schemas.png "image")](/static/images/migrations/sc-assets/schemas.png)

## Number of Schemas Containing Objects

Represents the number of schemas that contain identified top-level objects. Each different schema name will only count as one single schema. In case an object does not have an explicit schema in its name, SnowConvert AI will count all of those names as one single schema because it is assumed that those objects are defined in the default schema of Oracle.

It is important to consider that this number will only be incremented by the names used to create the top-level objects, the references to the object names will not be counted in this assessment value.

Warning

The Database Link top-level object in Oracle is not defined under any schema, this top-level object does not apply to this assessment value.

### Sample

Copy code

```
CREATE TABLE schema1.table1 (col1 VARCHAR(255));
CREATE TABLE SCHEMA1.table2 (col1 VARCHAR(255));

CREATE TABLE schema2.table3 (col1 VARCHAR(255));

CREATE TABLE "SCHEMA3"."table4" (col1 VARCHAR(255));
CREATE TABLE "schema3"."table5" (col1 VARCHAR(255));

CREATE TABLE table6 (col1 VARCHAR(255));
CREATE TABLE table7 (col1 VARCHAR(255));
```

**Expected Number of Schemas Containing Objects:** 5

**Explanation:** Since `table1` and `table2` come from the same schema only one schema will be counted for those two objects. With the schema name of `table3` that will count as another different schema and finally. `table4` and `table5` have the schema names with double quotes and with uppercase and lowercase, this will make these two schemas count as different ones. `table6` and `table7` do not have an explicit schema name so SnowConvert AI will assume that both objects come from the same default schema.
