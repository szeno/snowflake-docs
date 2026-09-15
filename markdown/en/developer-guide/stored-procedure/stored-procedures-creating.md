# Creating a stored procedure

You can create a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview) using any of several methods
available with Snowflake. These methods are described in this topic.

## Create a procedure

1. Write procedure logic as a handler using one of several supported languages, including Python, Java, and Scala.
2. Choose a tool or API to create the procedure with the handler you wrote.

   For more information about each of these, see [Tools for creating procedures](#label-procedure-creating-tools).

   |  |  |
   | --- | --- |
   | SQL | Use SQL and write logic in one of several languages. |
   | Snowpark | Use the Snowpark API for Java, Python, or Scala. |
   | Command line | Execute Snowflake CLI commands to create the procedure. |
   | Python API | Execute client-side Python commands to create the procedure. |
   | REST | Make requests to a RESTful API to create the procedure. |

   Expand

   Show lessSee more
3. [Execute the procedure](/developer-guide/stored-procedure/stored-procedures-calling) using one of several tools, depending on
   your needs.

## Tools for creating procedures

You can create a [procedure](/developer-guide/stored-procedure/stored-procedures-overview) using any of several methods available
with Snowflake, depending on the language and skill set you have available. Choose the tool that’s right for your needs from the
following table.

| Language | Approach |
| --- | --- |
| **SQL**  Execute a SQL command, such as by using Snowsight. | [Execute the SQL CREATE PROCEDURE command](#label-procedure-creating-sql) to create a procedure with handler code written in one of the following languages:   - [Java](/developer-guide/stored-procedure/java/procedure-java-overview) - [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript) - [Python](/developer-guide/stored-procedure/python/procedure-python-overview) - [Scala](/developer-guide/stored-procedure/scala/procedure-scala-overview) - [Snowflake Scripting](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting) |
| **Java, Python, or Scala**  Write code in one of the supported languages, then execute the code locally to perform operations in Snowflake. | Execute client code that uses Snowpark APIs in one of the following languages.   - [Java](/developer-guide/snowpark/java/creating-sprocs) - [Python](/developer-guide/snowpark/python/creating-sprocs) - [Scala](/developer-guide/snowpark/scala/creating-sprocs) |
| **Command line**  Create and manage Snowflake entities by executing commands from the command line. | Execute commands of the [Snowflake CLI](/developer-guide/snowflake-cli/objects/manage-objects#label-snowcli-object-create). |
| **Python**  On the client, write code that executes management operations on Snowflake. | Execute code that uses the [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures#label-snowflake-python-create-procedure). |
| **RESTful APIs** (language-agnostic)  Make requests of RESTful endpoints to create and manage Snowflake entities. | Make a request to create a procedure using the [Snowflake REST API](/developer-guide/snowflake-rest-api/procedure/procedure-introduction). |

Expand

Show lessSee more

## Key properties

The following describes some of the properties required or typically used when creating a procedure.

Procedure name:
:   The procedure name does not need to match the name of the handler. For more about name constraints and conventions, see
    [Naming and overloading procedures and UDFs](/developer-guide/udf-stored-procedure-naming-conventions).

Arguments:
:   For more information on requirements, see [Defining arguments for UDFs and stored procedures](/developer-guide/udf-stored-procedure-arguments).

Return type:
:   For information about how Snowflake maps SQL data types to handler data types, see
    [Data Type Mappings Between SQL and Handler Languages](/developer-guide/udf-stored-procedure-data-type-mapping).

Handler name:
:   When required, this is the name of the class or method containing code that executes when the procedure is called. You need specify a
    handler name only for handlers written in Java, Python, and Scala. For JavaScript and Snowflake Scripting handlers, all code specified
    in-line will be executed as the handler.

Dependencies:
:   For a handler written in Java, Python, or Scala, you might also need to specify the Snowpark library, such as when creating the procedure.

    For more about making dependencies available to your handler, see [Making dependencies available to your code](/developer-guide/upload-dependencies).

Handler language runtime:
:   When the handler language is Java, Python, or Scala, specify the runtime version to indicate which supported runtime version to use.
    Keep in mind that if you use the default version, that default will change over time.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE PROCEDURE | Schema | Required to create a permanent stored procedure. Not required when creating a temporary procedure that persists for only the duration of the session in which the procedure was created. |
| USAGE | Procedure | Granting the USAGE privilege on the newly created procedure to a role allows users with that role to call the procedure elsewhere in Snowflake. |
| USAGE | External access integration | Required on integrations, if any, specified when creating the procedure. For more information, see [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration). |
| READ | Secret | Required on secrets, if any, specified when creating the procedure. For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret) and [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf). |
| USAGE | Schema | Required on schemas containing secrets, if any, specified when creating the procedure. For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret) and [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

# All handler languages

- The definition for a stored procedure is limited to 1MB.
- Stored procedures support [overloading](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading). Two procedures can have the same
  name if they have a different number of parameters or different data types for their parameters.
- Stored procedures are not atomic; if one statement in a stored procedure fails, the other statements in the stored
  procedure are not necessarily rolled back. For information about stored procedures and transactions, see
  [Transaction management](/developer-guide/stored-procedure/stored-procedures-usage#label-stored-procedures-usage-transaction-management).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

Tip

If your organization uses a mix of caller’s rights and owner’s rights stored procedures, you might want to use a
naming convention for your stored procedures to indicate whether an individual stored procedure is a caller’s
rights stored procedure or an owner’s rights stored procedure.

- Setting LOG\_LEVEL or TRACE\_LEVEL as properties in a CREATE PROCEDURE statement is not supported. To set these properties
  on a procedure, use [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) after creating the procedure, or use
  [CREATE OR ALTER PROCEDURE](/sql-reference/sql/create-procedure#label-create-or-alter-procedure-syntax).

## Java

See the [known limitations](/developer-guide/stored-procedure/java/procedure-java-limitations).

## Javascript

A JavaScript stored procedure can return only a single value, such as a string (for example, a success/failure indicator)
or a number (for example, an error code). If you need to return more extensive information, you can return a
VARCHAR that contains values separated by a delimiter (such as a comma), or a semi-structured data type, such
as [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).

## Python

See the [known limitations](/developer-guide/stored-procedure/python/procedure-python-limitations).

## Scala

See the [known limitations](/developer-guide/stored-procedure/scala/procedure-scala-limitations).

## Create a stored procedure with SQL

You can create a stored procedure with SQL using the following steps.

Note

You can also create and call a procedure that isn’t stored for later use. Many of the properties for that kind of procedure are the same
as for a stored procedure. For more information, see [CALL (with anonymous procedure)](/sql-reference/sql/call-with).

1. Write handler code that executes when the procedure is called.

   You can use one of the supported handler languages. For more information, see [Supported languages and tools](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-handler-languages).
2. Choose whether you’ll keep the handler code in-line with the CREATE PROCEDURE SQL statement or refer to it on a stage.

   Each has its advantages. For more information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).
3. Execute a [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement in SQL, specifying properties of the procedure.

   Code in the following example creates a procedure called `myProc` with a in-line handler `MyClass.myMethod`. The
   handler language is Java, which (like procedure handlers written in Scala and Python) requires a Session object from the Snowpark
   library. Here, the PACKAGES clause refers to the Snowpark library included with Snowflake.

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE myProc(fromTable STRING, toTable STRING, count INT)
     RETURNS STRING
     LANGUAGE JAVA
     RUNTIME_VERSION = '11'
     PACKAGES = ('com.snowflake:snowpark:latest')
     HANDLER = 'MyClass.myMethod'
     AS
     $$
    import com.snowflake.snowpark_java.*;

    public class MyClass
    {
      public String myMethod(Session session, String fromTable, String toTable, int count)
      {
        session.table(fromTable).limit(count).write().saveAsTable(toTable);
        return "Success";
      }
    }
     $$;
   ```
