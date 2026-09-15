# Python UDF limitations

This topic describes the limitations in place for handlers written in Python.

## General limitations

- Although your Python function can use modules and functions in the standard Python packages, Snowflake security
  constraints disable some capabilities. For details, see the section
  titled [Following good security practices](/developer-guide/udf/python/udf-python-designing#label-udf-python-security).
- Avoid code that assumes a specific operating system.
- Python UDFs are not sharable. Database objects that use Python UDFs are also not sharable. For example, you cannot:

  - Directly share a Python UDF.
  - Share a view that calls a Python UDF.
  - Share a function that calls a Python UDF.
  - Share a table with a masking or row access policy that calls a Python UDF.
- Granting USAGE privilege on a Python UDF might allow the recipient to see the contents of files imported by that UDF. If you grant the
  USAGE privilege on a Python UDF to a role, and if that role executes a statement that calls that Python UDF, then any Python UDF in the same
  statement could read the contents of any files imported by the Python UDF on which you granted USAGE privilege.
- Database [replication](/user-guide/account-replication-intro) is supported for in-line Python UDFs. However, replication is blocked if a Python UDF has a dependency on a file in a stage (i.e.
  a function created using the IMPORTS clause). This limitation might be removed in future versions.
- Snowflake uses the Python `zipimport` module to import Python code from stages. As a result, any `zipimport` limitations
  will also be present with UDFs. For more about `zipimport`, see the
  [zipimport reference](https://docs.python.org/3/library/zipimport.html).

## Limitations on cloning

A Python UDF can be cloned when the database or schema containing the Python UDF is cloned.
To be cloned, the Python UDF must meet the following condition(s):

- If the Python UDF references a stage, that stage must be
  outside the schema (or database) being cloned.

  You can keep a Python UDF and its referenced stage(s) in separate schemas (and/or separate databases) the following ways:

  - Wherever the Python UDF references a stage, use a qualified stage name (e.g. “my\_db.my\_schema.my\_stage()”)
    different from the schema or database of the Python UDF. If the cloning operation clones a database, the stage
    reference should include the database and schema. If the cloning operation clones a schema, the stage reference
    should include the schema (and optionally the database).
  - Create the referenced stage by using a non-qualified stage name (which implicitly uses the current session’s active
    database and schema), and create the Python UDF by using a qualified name that does not match the session’s
    current database and schema.
  - Use the user’s stage as the referenced stage (the user’s stage is separate from any database’s stage or schema’s stage).

If one or more Python UDFs in the schema or database do not meet the required conditions, the schema or database can
still be cloned, but the non-compliant Python UDFs are omitted from the clone without any error or warning message.

Each cloned Python UDF has the same definition as the original. That definition includes any references to stages.
The stage references in the Python UDF must be fully-qualified, and therefore are absolute, not relative to the
schema or database being cloned. Because both the original and the clone point to the same stage(s) and file(s):

- Dropping the stage or removing required files from the stage disables both the original and cloned UDF.
- Altering the stage or the files on the stage affects both the
  original and cloned UDF.
