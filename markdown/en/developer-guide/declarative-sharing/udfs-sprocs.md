# User-Defined Functions and Stored Procedures in Declarative Shared Native Applications

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Declarative Native Apps can include [stored procedures](/developer-guide/stored-procedure/stored-procedures-overview) and [user-defined functions](/developer-guide/udf/udf-overview) (UDFs) to
query, visualize, and explore the data. This topic describes how to include
these logic objects in your app.

## Supported User-Defined Functions and Stored Procedures

You can share the following types of user-defined functions (UDFs) and stored
procedures (sprocs) in a Declarative Native App:

- Stored procedures that have owner’s rights or restricted caller’s rights.
  For more information, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
- All types of UDFs, except EXTERNAL functions
- Snowpark UDFs and stored procedures written in Python, Java, JavaScript, and
  Scala. Snowpark Container Service functions are not supported.

## Including User-Defined Functions and Stored Procedures in your application

To include UDFs and stored procedures in your Declarative Native App, add the
names of the objects and their permissions to the `manifest.yaml` file.
You don’t need to add the objects using separate files, as you do with
workspace files.

The following example shows how to include a UDF and a stored procedure in the
`manifest.yaml` file:

Copy code

```
manifest_version: 2

roles:
  - ANALYST:
      comment: "The ANALYST role provides access to logic objects."

shared_content:
  databases:
    - SNAF_POPULATION_DB:
        schemas:
          - LOGIC_SCHEMA:
              roles: [ANALYST]
              functions:
                - POPULATION_ANALYSIS_FUNCTION(NUMBER):
                    roles: [ANALYST]
              procedures:
                - POPULATION_ANALYSIS_PROCEDURE():
                    roles: [ANALYST]
```

In this example, the `POPULATION_ANALYSIS_FUNCTION` UDF and the
`POPULATION_ANALYSIS_PROCEDURE` stored procedure are included in the
`manifest.yaml` file. The `ANALYST` app role is granted access to
both objects.

## Accessing private (non-shared) objects using UDFs and stored procedures

You can use UDFs and stored procedures to access private (non-shared) tables and
views. For example, your database can have a view that isn’t visible to
consumers, but consumers can use a stored procedure to retrieve
data from that view.

To allow consumers to access private objects using UDFs and stored procedures,
mark the object with the `private: true` keyword in the
`manifest.yaml` file.

The following example shows how to allow a stored procedure to access a private
table in the `manifest.yaml` file:

Copy code

```
manifest_version: 2

roles:
  - VIEWER:
      comment: "The VIEWER role can access a stored procedure that retrieves data from a view, but not the underlying view."

shared_content:
  databases:
    - SNAF_POPULATION_DB:
        schemas:
          - DATA_SCHEMA:
              views: # This view is private as no roles are granted
                - COUNTRY_POP_BY_YEAR_2000:
                    private: true
          - LOGIC_SCHEMA:
              roles: [VIEWER]
              procedures:
                - POPULATION_DISPLAY_PROCEDURE():
                    roles: [VIEWER]
```

In the previous example, the `COUNTRY_POP_BY_YEAR_2000` view is private
because no roles are granted access to it, but the `private` parameter
allows logic objects to access it. The `VIEWER` app role can execute the
stored procedure, but it can’t query the private view directly. Note that the
tables that the `COUNTRY_POP_BY_YEAR_2000` view references don’t need to
be included in the `manifest.yaml` file for the view to access them.

## Limitations

Supported languages and types
:   Snowpark UDFs and stored procedures written in Python, Java, JavaScript, and
    Scala. Snowpark Container Service functions are not supported.

Schemas for data objects and logic objects
:   You must use separate schemas for data objects (tables and views) and logic
    objects (UDFs and stored procedures). For example, you can use a schema named
    `DATA_SCHEMA` for tables and views, and a schema named
    `LOGIC_SCHEMA` for UDFs and stored procedures.

Referencing private objects
:   Your UDFs and stored procedures must reference private objects by their
    schema-qualified names. Your logic objects can’t reference private objects by
    their fully-qualified names.

Object count
:   A Declarative Native App can include up to 100 UDFs and stored procedures. To
    raise this limit, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Dynamic tables
:   Referencing dynamic tables in UDFs and stored procedures is not supported.
