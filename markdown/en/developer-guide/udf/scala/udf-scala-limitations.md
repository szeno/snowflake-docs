# Scala UDF limitations

This topic describes the limitations in place for handlers written in Scala.

## General limitations

- Although your Scala method can use classes and methods in the standard libraries, Snowflake security
  constraints disable some capabilities, such as writing to files. For details, see the section
  titled [Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices).
- Scala UDFs are not sharable. Database objects that use Scala UDFs are also not sharable. For example, you cannot:

  - Directly share a Scala UDF.
  - Share a view that calls a Scala UDF.
  - Share a function that calls a Scala UDF.
  - Share a table with a masking or row access policy that calls a Scala UDF.
- Granting USAGE privilege on a Scala UDF might allow the recipient to see the contents of files imported by that UDF. If you grant the
  USAGE privilege on a Scala UDF to a role, and if that role executes a statement that calls that Scala UDF, then any Scala UDF in the same
  statement could read the contents of any files imported by the Scala UDF on which you granted USAGE privilege.
- [Database replication](/user-guide/replication-intro) does not include external or internal stages yet.
  When you promote a secondary database to serve as the primary database, you must recreate stage objects and re-import any files missing
  in internal stages. The files should have the same path and filenames as in the original primary database.
- The maximum size for a Scala UDF output row is 128 MB.
- Concurrency is not supported. For example, from within your code, you cannot submit queries
  from multiple threads. Code that concurrently issues multiple queries will produce an error.
- If a query calls a UDF to access staged files, the operation fails with a user error if the SQL statement also queries a view that
  calls any UDF, regardless if the function in the view accesses staged files or not.
- UDFs currently process files serially. As a workaround, group rows in a subquery using the [GROUP BY](/sql-reference/constructs/group-by)
  clause.
- Currently, if the staged files referenced in a query are modified or deleted while the query is running, the function call fails with an
  error.

## Limitations on cloning

A Scala UDF can be cloned when the database or schema containing the Scala UDF is cloned.
To be cloned, the Scala UDF must meet the following condition(s):

- If the Scala UDF references a stage (for example, the stage that contains the UDF’s JAR file), that stage must be
  outside the schema (or database) being cloned.

  You can keep a Scala UDF and its referenced stage(s) in separate schemas (and/or separate databases) the following ways:

  - Wherever the Scala UDF references a stage, use a qualified stage name (such as `my_db.my_schema.my_stage`) different from the
    schema or database of the Scala UDF. If the cloning operation clones a database, the stage reference should include the database and
    schema. If the cloning operation clones a schema, the stage reference should include the schema (and optionally the database).
  - Create the referenced stage by using a non-qualified stage name (which implicitly uses the current session’s active database and
    schema), and create the Scala UDF by using a qualified name that does not match the session’s current database and schema.
  - Use the user’s stage as the referenced stage (the user’s stage is separate from any database’s stage or schema’s stage).

If one or more Scala UDFs in the schema or database do not meet the required conditions, the schema or database can still be cloned, but
the non-compliant Scala UDFs are omitted from the clone without any error or warning message.

Each cloned Scala UDF has the same definition as the original. That definition includes any references to stages. The stage references in
the Scala UDF must be fully-qualified, and therefore are absolute, not relative to the schema or database being cloned. Because both the
original and the clone point to the same stage(s) and file(s):

- Dropping the stage or removing required files from the stage disables both the original and cloned UDF.
- Altering the stage or the files on the stage (e.g. replacing the JAR file with a newer JAR file) affects both the original and cloned UDF.
