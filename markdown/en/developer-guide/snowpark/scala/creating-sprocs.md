# Creating stored procedures for DataFrames in Scala

Using the Snowpark API, you can create stored procedures for your custom lambdas and functions. You can call these
stored procedures to process the data in your DataFrame.

You can create:

- [Temporary stored procedures](#label-snowpark-scala-stored-proc-create-temp) that exist only within the current session.
- [Permanent stored procedures](#label-snowpark-scala-stored-proc-create-permanent) that you can use in other sessions, including
  from a Snowflake worksheet.

## Creating a temporary stored procedure

You can create a temporary procedure that will last for the current session only. The temporary procedure can be:

- An anonymous procedure that you can call by reference, such as by passing a [com.snowflake.snowpark.StoredProcedure](../reference/scala/com/snowflake/snowpark/StoredProcedure.html) variable
  representing it to code that calls the procedure.
- A named procedure with a name you assign. You can call the procedure by name from other code within the session.

To create a temporary procedure, you register it with one of the `registerTemporary` methods of [com.snowflake.snowpark.SProcRegistration](../reference/scala/com/snowflake/snowpark/SProcRegistration.html).
The method is overloaded multiple times to support different numbers of procedure arguments.

When calling `registerTemporary`, you can pass as arguments the following:

- The procedure’s name (when it is a named procedure).
- The procedure itself as a lambda expression.

### Creating an anonymous temporary procedure

To create an anonymous temporary procedure, you register it as a temporary procedure without specifying a name. Snowflake will create a
hidden name for its own use.

Code in the following example calls the `SProcRegistration.registerTemporary` method to create an anonymous procedure from a lambda
function. The function itself will take a `Session` object and an integer as arguments. The `Session` argument represents an implicit
parameter that callers needn’t pass as an argument.

Copy code

```
val session = Session.builder.configFile("my_config.properties").create

val sp = session.sproc.registerTemporary(
  (session: Session, num: Int) => num + 1
)
```

Code in the following example calls the anonymous procedure using the `storedProcedure` method of the
[com.snowflake.snowpark.Session](../reference/scala/com/snowflake/snowpark/Session.html) class, passing the `sp` variable and `1` as its arguments. Note that the `Session` object
is an implicit argument that you needn’t pass when you call the procedure.

Copy code

```
session.storedProcedure(sp, 1).show()
```

### Creating a named temporary procedure

To create a named temporary procedure, you register it as a temporary procedure, passing its name as one of the arguments.

Code in the following example calls the `registerTemporary` method to create a named temporary procedure called
`add_two` from a lambda expression, passing the procedure’s name as an argument. The method registers an `Int` as
the single parameter type.

The procedure itself will take a `Session` object and an integer as arguments. The `Session` argument represents an implicit
parameter that callers needn’t pass as an argument.

Copy code

```
val session = Session.builder.configFile("my_config.properties").create

val procName: String = "add_two"
val tempSP: StoredProcedure =
  session.sproc.registerTemporary(
    procName,
    (session: Session, num: Int) => num + 2)
```

Code in the following example calls the `add_two` procedure using a `storedProcedure` method of the
[com.snowflake.snowpark.Session](../reference/scala/com/snowflake/snowpark/Session.html) class, passing the procedure name and `1` as its arguments. Note that the `Session` object is
an implicit argument that you needn’t pass when you call the procedure.

Copy code

```
session.storedProcedure(procName, 1).show()
```

## Creating a permanent stored procedure

You can create a permanent stored procedure that you can call from any session, including
[from within a Snowflake worksheet](/developer-guide/stored-procedure/stored-procedures-calling).

To create a permanent procedure, you register it with a `registerPermanent` method of the [com.snowflake.snowpark.SProcRegistration](../reference/scala/com/snowflake/snowpark/SProcRegistration.html)
class. The method is overloaded multiple times to support a variety of procedure requirements.

When calling `registerPermanent`, you pass as arguments the following:

- The procedure’s name.
- The procedure itself as a lambda expression.
- An existing stage to which Snowflake should copy files resulting from compiling the procedure.

  Snowflake will copy all related data, including dependencies and lambda functions. This must be a permanent stage (not session temporary)
  because this stored procedure can be invoked outside of the current session. If the procedure is later dropped, you must manually
  remove related files from the stage.
- A boolean value indicating whether this procedure should execute with caller’s rights.

  For more about caller’s rights and owner’s rights, refer to [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

Code in the following example calls the `registerPermanent` method to create a permanent procedure called
`add_hundred` from a lambda expression.

The method specifies a stage called `sproc_libs` for the procedure and its dependencies. It also specifies that the procedure should
be executed with caller’s rights.

The procedure itself will take a `Session` object and an integer as arguments. The `Session` argument represents an implicit
parameter that callers needn’t pass as an argument.

Copy code

```
val session = Session.builder.configFile("my_config.properties").create

val procName: String = "add_hundred"
val stageName: String = "sproc_libs"

val sp: StoredProcedure =
  session.sproc.registerPermanent(
    procName,
    (session: Session, num: Int) => num + 100,
    stageName,
    true
  )
```

Code in the following example calls the `add_hundred` procedure using a `storedProcedure` method of the
[com.snowflake.snowpark.Session](../reference/scala/com/snowflake/snowpark/Session.html) class. The call passes the procedure name and `1` as its arguments. Note that the `Session`
object used in the handler as an argument is an implicit argument that you needn’t pass when you call the procedure.

Copy code

```
session.storedProcedure(procName, 1).show()
```
