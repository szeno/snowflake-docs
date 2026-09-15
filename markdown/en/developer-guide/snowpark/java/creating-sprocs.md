# Creating stored procedures for DataFrames in Java

Using the Snowpark API, you can create stored procedures for your custom lambda expression in Java. You can call these stored procedures
to process the data in your `DataFrame`.

You can create:

- [Temporary stored procedures](#label-snowpark-java-stored-proc-create-temp) that exist only within the current session.
- [Permanent stored procedures](#label-snowpark-java-stored-proc-create-permanent) that you can use in other sessions, including
  from a Snowflake worksheet.

## Creating a temporary stored procedure

You can create a temporary procedure that will last for the current session only. The temporary procedure can be:

- An anonymous procedure that you can call by reference, such as by passing a variable of type [com.snowflake.snowpark\_java.StoredProcedure](../reference/java/com/snowflake/snowpark_java/StoredProcedure.html)
  representing it to code that calls the procedure.
- A named procedure with a name you assign. You can call the procedure by name from other code within the session.

To create a temporary procedure, you register it with one of the `registerTemporary` methods of
[com.snowflake.snowpark\_java.SProcRegistration](../reference/java/com/snowflake/snowpark_java/SProcRegistration.html). The method is overloaded multiple times to support different numbers of procedure
arguments. To get an `SProcRegistration` instance, call the [sproc](../reference/java/com/snowflake/snowpark_java/Session.html#sproc()) method of the [com.snowflake.snowpark\_java.Session](../reference/java/com/snowflake/snowpark_java/Session.html) class.

When calling `registerTemporary`, you can pass as arguments the following:

- The procedure’s name (when it is a named procedure).
- The procedure itself as a lambda expression.
- Parameter data types as a single or array of `com.snowflake.snowpark_java.types.DataType` class. Omit this argument when the
  procedure you’re creating has no parameters.

  These should correspond to the parameter types defined in the procedure.
- Return data type as a `com.snowflake.snowpark_java.types.DataType` class.

You can call the procedure with a `storedProcedure` method of the [com.snowflake.snowpark\_java.Session](../reference/java/com/snowflake/snowpark_java/Session.html) class.

### Creating an anonymous temporary procedure

To create an anonymous temporary procedure, you register it as a temporary procedure without specifying a name. Snowflake will create a
hidden name for its own use.

Code in the following example calls the `SProcRegistration.registerTemporary` method to create an anonymous procedure from a lambda
expression. The procedure takes a `Session` object and an integer as arguments. The method registers a `DataTypes.IntegerType`
as the single parameter type and a `DataTypes.IntegerType` as the return type.

The procedure itself will take a `Session` object and an integer as arguments. The `Session` argument represents an implicit
parameter that callers needn’t pass as an argument.

Copy code

```
Session session = Session.builder().configFile("my_config.properties").create();

StoredProcedure sp =
  session.sproc().registerTemporary(
    (Session spSession, Integer num) -> num + 1,
    DataTypes.IntegerType,
    DataTypes.IntegerType
  );
```

Code in the following example calls the anonymous procedure, passing the `sp` variable and `1` as its arguments.
Note that the `Session` object is an implicit argument that you needn’t pass when you call the procedure.

Copy code

```
session.storedProcedure(sp, 1).show();
```

### Creating a named temporary procedure

To create a named temporary procedure, you register it as a temporary procedure, passing its name as one of the arguments.

Code in the following example calls the `registerTemporary` method to create a named temporary procedure called
`increment` from a lambda expression, passing the procedure’s name as an argument. The method registers a `DataTypes.IntegerType` as
the single parameter type and a `DataTypes.IntegerType` as the return type.

The procedure itself will take a `Session` object and an integer as arguments. The `Session` argument represents an implicit
parameter that callers needn’t pass as an argument.

Copy code

```
Session session = Session.builder().configFile("my_config.properties").create();

String procName = "increment";

StoredProcedure tempSP =
  session.sproc().registerTemporary(
    procName,
    (Session session, Integer num) -> num + 1,
    DataTypes.IntegerType,
    DataTypes.IntegerType
  );
```

Code in the following example calls the `increment` procedure, passing the procedure name and `1` as its
arguments. Note that the `Session` object is an implicit argument that you needn’t pass when you call the procedure.

Copy code

```
session.storedProcedure(procName, 1).show();
```

## Creating a permanent stored procedure

You can create a permanent stored procedure that you can call from any session, including
[from within a Snowflake worksheet](/developer-guide/stored-procedure/stored-procedures-calling).

To create a permanent procedure, you register it with a `registerPermanent` method of the [com.snowflake.snowpark\_java.SProcRegistration](../reference/java/com/snowflake/snowpark_java/SProcRegistration.html)
class. The method is overloaded multiple times to support different numbers of procedure arguments.

When calling `registerPermanent`, you pass as arguments the following:

- The procedure’s name.
- The procedure itself as a lambda expression.
- Parameter data types as a single or array of `com.snowflake.snowpark_java.types.DataType` class. Omit this argument when the
  procedure you’re creating has no parameters.

  These should correspond to the parameter types defined in the procedure.
- The return data type as a `com.snowflake.snowpark_java.types.DataType` class.
- An existing stage to which Snowflake should copy files resulting from compiling the procedure.

  Snowflake will copy all related data, including dependencies and lambda functions. This must be a permanent stage (not session temporary)
  because this stored procedure can be invoked outside of the current session. If the procedure is later dropped, you must manually
  remove related files from the stage.
- A boolean value indicating whether this procedure should execute with caller’s rights.

  For more about caller’s rights and owner’s rights, refer to [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

Code in the following example calls the `registerPermanent` method to create a permanent procedure called
`add_hundred` from a lambda expression.

The method registers a `DataTypes.IntegerType` as the single parameter type and a `DataTypes.IntegerType` as the return type.
It specifies a stage called `sproc_libs` for the procedure and its dependencies. It also specifies that the procedure should be
executed with caller’s rights.

The procedure itself will take a `Session` object and an integer as arguments. The `Session` argument represents an implicit
parameter that callers needn’t pass as an argument.

Copy code

```
Session session = Session.builder().configFile("my_config.properties").create();

String procName = "add_hundred";
String stageName = "sproc_libs";

StoredProcedure sp =
    session.sproc().registerPermanent(
        procName,
        (Session session, Integer num) -> num + 100,
        DataTypes.IntegerType,
        DataTypes.IntegerType,
        stageName,
        true
    );
```

Code in the following example calls the `add_hundred` procedure using a `storedProcedure` method of the
[com.snowflake.snowpark\_java.Session](../reference/java/com/snowflake/snowpark_java/Session.html) class. The call passes the procedure name and `1` as its arguments. Note that the `Session`
object used in the handler as an argument is an implicit argument that you needn’t pass when you call the procedure.

Copy code

```
session.storedProcedure(procName, 1).show();
```
