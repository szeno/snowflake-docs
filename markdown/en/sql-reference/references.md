# Using references to authorize access on objects

A reference can be used to authorize access on objects to a stored procedure, Snowflake Native App, or class instance
that does not have access to those objects by default.

## Introduction

A reference is a string that can be used as an identifier. The identifier resolves to the object being referenced.

A reference encapsulates the following:

- The object name.
- The active role used to create the object reference and any active secondary role(s) if applicable.
- The privilege(s) on the object that are specified when the reference is created.

Some scenarios where a reference might be required include:

- An [owner’s rights stored procedure](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state-owners) requires access to insert data in a table
  owned by a different role.
- An application performs data analytics and requires read access to data in tables.
- An instance of the SNOWFLAKE.ML.ANOMALY\_DETECTION class requires read access to a view for training the anomaly detection ML model.

### Objects identified by name

A reference identifies an object *by name*. This means if an object is renamed after a reference is created, the reference is
invalid. However, if a new object with the same name is created, the reference *might* be valid. For example, a role
`my_role` creates a reference `my_ref1` for table `my_table1` with the SELECT
privilege. After the reference is created, table `my_table1` is dropped and a *new* table named `my_table1` is created.
The reference `my_ref1` identifies a table with the name `my_table1`. In this case, it identifies the *new*
table `my_table1`.

If the role used to create the reference, and the privilege(s) granted on `my_table1` are still valid, access to
the new `my_table1` is authorized when using the reference.

If the role and privilege(s) encapsulated in the reference are no longer valid, access to table `my_table1` cannot
be authorized and a new reference must be created for the new table.

### Privileges verified at execution time

The privileges granted to the role that created the reference are verified at the time the reference is used. For example, a role
`my_role` creates a reference to a table `t1` with the SELECT privilege. If `my_role` is dropped or
the SELECT privilege on table `t1` is revoked from `my_role`, the privileges encapsulated in the reference are no
longer valid. When the reference is passed to a stored procedure that requires the SELECT privilege on
the table, the stored procedure fails with a permissions error.

### Types of references and reference lifespan

The lifespan of a reference can be specified at creation time.

- A *transient reference* has a limited lifespan, either for the duration of the call in which the reference is passed, or
  for the duration of the session.

- A *persistent reference* has an unlimited lifespan. The reference remains valid until the object it references is dropped,
  the reference is unset, or the reference becomes invalid.

  For examples of unsetting references, see [Unset a persistent reference for an application](#label-unset-persistent-reference).

  A reference can become invalid for any of the following reasons:

  - The object it references is renamed.
  - The role that created the reference is dropped.
  - The role that created the reference no longer has privileges on the object.

  For more information, see [Objects identified by name](#label-references-objects-identified-by-name) and [Privileges verified at execution time](#label-references-privileges-at-execution-time).

### References for owner’s rights stored procedures

An [owner’s rights stored procedure](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state-owners) executes with the privileges of the *owner*
rather than the privileges of the *caller* who executes the stored procedure. In order to perform actions on a table, view, or
function that the caller has privileges to access, the caller must pass a reference to the table, view, or function. The reference
enables the stored procedure to perform actions on the object that the reference identifies with the privileges of the
creator of the reference (in this case, the caller).

### References for applications and classes

By design, applications and classes *do not* have access to objects in the account where the application is installed or
an instance of a class is created. Users can authorize access on objects to an application or class instance by creating a reference.

#### Providers and consumers of applications and classes

A *provider* creates an application and a *consumer* installs and uses an application in the consumer account. In the case of
[Snowflake classes](/sql-reference/snowflake-db-classes), Snowflake is the *provider*, and a user with a Snowflake account who creates an instance
of a class is the *consumer*.

Providers can create applications and classes that request and use references in their code. For more information, see
[References for providers](#label-references-for-providers).

Consumers can create and pass references to applications that they install in their account or to instances
of Snowflake classes. For more information, see [References for consumers](#label-references-for-consumers).

## Supported targets for references

The targets for a reference can be an object or a query. If the target of the reference is an object, privilege(s) on the object
are required for the reference.

### Supported object types and privileges for references

The following table lists the object types that a reference can include, the type of reference that can be created,
and the privileges allowed for each object:

| Object type | Transient | Persistent | Privileges allowed | Default privilege |
| --- | --- | --- | --- | --- |
| AI GATEWAY | ✔ |  | [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all accounts.  APPLYBUDGET, USAGE | USAGE |
| API INTEGRATION |  | ✔ | USAGE | USAGE |
| CATALOG INTEGRATION |  | ✔ | USAGE | USAGE |
| COMPUTE POOL | ✔ |  | APPLYBUDGET |  |
| CORTEX AGENT | ✔ |  | USAGE | USAGE |
| DATABASE | ✔ |  | APPLYBUDGET |  |
| EXTERNAL ACCESS INTEGRATION |  | ✔ | USAGE |  |
| EXTERNAL VOLUME |  | ✔ | USAGE |  |
| EXTERNAL TABLE |  | ✔ | SELECT, REFERENCES | SELECT |
| FUNCTION | ✔ | ✔ | USAGE | USAGE |
| GIT REPOSITORY |  | ✔ | READ | READ |
| MATERIALIZED VIEW | ✔ |  | APPLYBUDGET |  |
| PIPE | ✔ |  | APPLYBUDGET | APPLYBUDGET |
| POLICY | ✔ |  | MANAGE POLICY |  |
| PROCEDURE | ✔ | ✔ | USAGE | USAGE |
| ROW ACCESS POLICY | ✔ |  | APPLY |  |
| SCHEMA | ✔ |  | APPLYBUDGET |  |
| SECRET |  | ✔ | USAGE, READ |  |
|  | ✔ |  | READ |  |
| SNOWFLAKE INTELLIGENCE | ✔ |  | USAGE | USAGE |
| STAGE |  | ✔ | READ, WRITE | READ |
| TABLE | ✔ |  | APPLYBUDGET, REBUILD, EVOLVESCHEMA |  |
|  | ✔ | ✔ | SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES | SELECT |
| TAG | ✔ |  | APPLYBUDGET |  |
| TASK | ✔ |  | APPLYBUDGET | APPLYBUDGET |
| VIEW | ✔ | ✔ | SELECT, REFERENCES | SELECT |
| WAREHOUSE | ✔ |  | APPLYBUDGET |  |
|  |  | ✔ | MODIFY, MONITOR, OPERATE, USAGE | USAGE |

Expand

Show lessSee more

### Query references

A *query reference* is a type of transient reference. It references a SELECT statement that can be used in the FROM clause of
another SQL statement in a stored procedure. You can create a query reference by using the
[SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) function or the TABLE keyword.

For more information, see [Using query references](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-query-references) and [Using the TABLE keyword to create a reference to a table, view, or query](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-table-keyword).

## References for providers

You can create applications as a provider by using the [Snowflake Native App Framework](/developer-guide/native-apps/native-apps-about).
For detailed information on requesting references from a consumer of your application, see
[Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

## References for consumers

You can create a reference by using the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function. You can pass the string identifier
that the function returns to a stored procedure, application, or class instance. Alternatively, you can pass in the statement that
creates the reference in place of the string identifier.

Note

If you are passing a reference to a stored procedure, you can use the TABLE keyword (rather than calling the SYSTEM$REFERENCE
function) to create the reference. See [Using the TABLE keyword to create a reference to a table, view, or query](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-table-keyword).

### Examples

Create a transient reference with session scope to table `t1` with the SELECT privilege:

Copy code

```
SELECT SYSTEM$REFERENCE('TABLE', 't1', 'SESSION', 'SELECT');
```

To create a reference to the same table for the lifetime of the scope in which it is referenced (for example, if you pass it to
a stored procedure, its lifetime would be that of the outermost block of the stored procedure), execute the following statement:

Copy code

```
SELECT SYSTEM$REFERENCE('TABLE', 't1', 'CALL', 'SELECT');
```

Create a persistent reference to a table `t1` with the INSERT privilege to pass to an application:

Copy code

```
SELECT SYSTEM$REFERENCE('TABLE', 't1', 'PERSISTENT', 'INSERT');
```

Create a query reference to pass to a stored procedure. The lifetime of this transient reference is for the outermost block of
the stored procedure to which you pass the reference to:

Copy code

```
SELECT SYSTEM$QUERY_REFERENCE('SELECT id FROM my_table', FALSE);
```

For additional examples:

- Stored procedure example, see [Background: The problem with passing objects and queries to stored procedures](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-example).
- Native App Framework application example, see
  [Associating the Reference to the Application](https://other-docs.snowflake.com/en/native-apps/consumer-granting-privs#associating-the-reference-to-the-application).
- Class instance example, see [Training an Anomaly Detection Model with Labeled Data](/user-guide/ml-functions/anomaly-detection#label-analysis-anomaly-detection-single-series-labeled).

#### Unset a persistent reference for an application

An application or a class that requires a persistent reference will also provide a method to unset the reference. Method names can vary
by implementation.

Alternatively, you can unset references by using an [ALTER APPLICATION … UNSET REFERENCES](/sql-reference/sql/alter-application)
statement.

1. You can use the [SHOW REFERENCES](/sql-reference/sql/show-references) command to view all references, including references that have been
   set for an application.

   For example, to view references for application `my_app`:

   Copy code

   ```
   SHOW REFERENCES IN APPLICATION my_app;
   ```
2. You can unset any references that have been set for the application by using the ALTER APPLICATION command.

   For example, to unset the reference named `table_to_read` in application `my_app`:

   Copy code

   ```
   ALTER APPLICATION my_app UNSET REFERENCES('table_to_read');
   ```

   For example, to unset all references in application `my_app`:

   Copy code

   ```
   ALTER APPLICATION my_app UNSET REFERENCES;
   ```

## Considerations when using references

- If an object that is associated with a reference is renamed (or reparented), the reference is no longer valid.

  If a new object is created with the same name, and if the roles encoded in the reference association have the relevant
  privileges on the new object, the reference remains valid. Otherwise it fails with a permissions error.
- If an object is swapped, and the roles encoded in the reference association have the relevant privileges on the new object
  that now has the swapped name, the reference remains valid. Otherwise it fails with a permissions error.
- Object drop and undrop:

  - If an object that is associated with a reference is dropped, the reference association becomes invalid.
  - If the object is undropped, the reference association becomes valid again.
- Cloning

  You can clone a class instance, or its parent database or schema, that uses references to objects in your account.

  - If the reference object is referenced with a fully qualified name, the instance clone refers to the original object.
  - If the referenced object is referenced with a partially qualified or unqualified name, the instance clone might refer to
    the clone object, the original object, or to no real object depending on the cloning boundary.
- Replication is supported for an application or a database containing a class instance that uses a reference to objects
  in the consumer account.

  References function correctly in the target account as long as the following objects are replicated:

  - Application or class instance.
  - Referenced object.
  - Role that created the reference.

  These objects can be replicated in different replication or failover groups. Once all objects are replicated, the reference
  is usable.

For providers of Snowflake Native App Framework applications, see also [Considerations when using references](/developer-guide/native-apps/requesting-refs#label-native-apps-considerations-for-references).

## Monitoring usage of references

You can view references requested by an application by using the [SHOW REFERENCES](/sql-reference/sql/show-references) command. If you have set
any references for an application, the output will include information about the object, database, schema, and the identifier for each
reference.

For example, to view references in application `my_app`:

Copy code

```
SHOW REFERENCES IN APPLICATION my_app;
```
