# Creating and calling stored procedures

You can use the SQL API to create and call stored procedures. The following is an example of the body of a POST request that
creates a new stored procedure that passes in the name of a table and returns the number of rows in that table:

Copy code

```
{
  "statement": "create or replace procedure sql_api_stored_proc(table_name varchar) returns varchar language javascript as $$var sql_command = \"select count(*) from \" + TABLE_NAME; var rs = snowflake.execute({sqlText: sql_command}); rs.next(); var rowCount = rs.getColumnValue(1); return rowCount; $$;",
  "role": "MY_ROLE",
  "warehouse": "MY_WAREHOUSE",
  "database": "MY_DB",
  "schema": "MY_SCHEMA"
}
```

The following is an example of the body of the response for this request:

Copy code

```
{
  "resultSetMetaData": {
    "numRows": 1,
    "format": "jsonv2",
    "rowType": [ {
      "name": "status",
      "database": "",
      "schema": "",
      "table": "",
      "type": "text",
      "byteLength": 16777216,
      "scale": null,
      "precision": null,
      "nullable": true,
      "collation": null,
      "length": 16777216
    } ]
  },
  "data": [ [ "Function SQL_API_STORED_PROC successfully created." ] ],
  "code": "090001",
  "statementStatusUrl": "/api/v2/statements/019c9f28-0502-f257-0000-438300e0a02a?requestId=...",
  "sqlState": "00000",
  "statementHandle": "019c9f28-0502-f257-0000-438300e0a02a",
  "message": "Statement executed successfully.",
  "createdOn": 1622494569592
}
```

The following is an example of the body of a POST request that calls the stored procedure, passing in the table name “prices”:

Copy code

```
{
  "statement": "call sql_api_stored_proc('prices');",
  "role": "MY_ROLE",
  "warehouse": "MY_WAREHOUSE",
  "database": "MY_DB",
  "schema": "MY_SCHEMA"
}
```

The following is an example of the body of the response for this request:

Copy code

```
{
  "resultSetMetaData": {
    "numRows": 1,
    "format": "jsonv2",
    "rowType": [ {
      "name": "SQL_API_STORED_PROC",
      "database": "",
      "schema": "",
      "table": "",
      "type": "text",
      "byteLength": 16777216,
      "length": 16777216,
      "scale": null,
      "precision": null,
      "nullable": true,
      "collation": null
    } ]
  },
  "data": [ [ "4" ] ],
  "code": "090001",
  "statementStatusUrl": "/api/v2/statements/019c9f2a-0502-f244-0000-438300e04496?requestId=...",
  "sqlState": "00000",
  "statementHandle": "019c9f2a-0502-f244-0000-438300e04496",
  "message": "Statement executed successfully.",
  "createdOn": 1622494718694
}
```
