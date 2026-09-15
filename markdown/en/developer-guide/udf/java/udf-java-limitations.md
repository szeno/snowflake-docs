# Java UDF limitations

This topic describes the limitations in place for handlers written in Java.

## General limitations

- Although your Java method can use classes and methods in the standard Java libraries, Snowflake security
  constraints disable some capabilities, such as writing to files. For details, see the section
  titled [Following good security practices](/developer-guide/udf/java/udf-java-designing#label-udf-java-security).
- Java UDFs are not sharable. Database objects that use Java UDFs are also not sharable. For example, you cannot:

  - Directly share a Java UDF.
  - Share a view that calls a Java UDF.
  - Share a function that calls a Java UDF.
  - Share a table with a masking or row access policy that calls a Java UDF.
- Granting USAGE privilege on a Java UDF might allow the recipient to see the contents of files imported by that UDF. If you grant the
  USAGE privilege on a Java UDF to a role, and if that role executes a statement that calls that Java UDF, then any Java UDF in the same
  statement could read the contents of any files imported by the Java UDF on which you granted USAGE privilege.
- [Replication](/user-guide/account-replication-intro) does not include external or internal stages yet.
  When you promote a secondary database to serve as the primary database, you must recreate stage objects and re-import any files missing
  in internal stages. The files should have the same path and filenames as in the original primary database.
- The maximum size for a Java UDF output row is 128 MB.

## Limitations on cloning

A Java UDF can be cloned when the database or schema containing the Java UDF is cloned.
To be cloned, the Java UDF must meet the following condition(s):

- If the Java UDF references a stage (for example, the stage that contains the UDF’s JAR file), that stage must be
  outside the schema (or database) being cloned.

  You can keep a Java UDF and its referenced stage(s) in separate schemas (and/or separate databases) the following ways:

  - Wherever the Java UDF references a stage, use a qualified stage name (e.g. “my\_db.my\_schema.my\_stage()”)
    different from the schema or database of the Java UDF. If the cloning operation clones a database, the stage
    reference should include the database and schema. If the cloning operation clones a schema, the stage reference
    should include the schema (and optionally the database).
  - Create the referenced stage by using a non-qualified stage name (which implicitly uses the current session’s active
    database and schema), and create the Java UDF by using a qualified name that does not match the session’s
    current database and schema.
  - Use the user’s stage as the referenced stage (the user’s stage is separate from any database’s stage or schema’s stage).

If one or more Java UDFs in the schema or database do not meet the required conditions, the schema or database can
still be cloned, but the non-compliant Java UDFs are omitted from the clone without any error or warning message.

Each cloned Java UDF has the same definition as the original. That definition includes any references to stages.
The stage references in the Java UDF must be fully-qualified, and therefore are absolute, not relative to the
schema or database being cloned. Because both the original and the clone point to the same stage(s) and file(s):

- Dropping the stage or removing required files from the stage disables both the original and cloned UDF.
- Altering the stage or the files on the stage (e.g. replacing the JAR file with a newer JAR file) affects both the
  original and cloned UDF.

For more information about cloning, see [Cloning considerations](/user-guide/object-clone).
