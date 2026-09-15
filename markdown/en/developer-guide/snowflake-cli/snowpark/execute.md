# Execute a Snowpark procedure or function

To execute a Snowpark procedure or function, use the `snow snowpark execute OBJECT_TYPE EXECUTION_IDENTIFIER` command, where:

- `OBJECT_TYPE` is one of `function` or `procedure`.
- `EXECUTION_IDENTIFIER` is function or procedure signature, with all arguments provided.

The following example calls a Snowpark function called `hello_function`:

Copy code

```
snow snowpark execute function "hello_function('Olaf')"
```

```
+--------------------------------------+
| key                    | value       |
|------------------------+-------------|
| HELLO_FUNCTION('Olaf') | Hello Olaf! |
+--------------------------------------+
```
