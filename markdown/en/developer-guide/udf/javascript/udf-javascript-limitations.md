# JavaScript UDF limitations

To ensure stability within the Snowflake environment, Snowflake places the following limitations on JavaScript UDFs. These
limitations are not invoked at the time of UDF creation, but rather at runtime when the UDF is called.
This topic covers general JavaScript UDF (user-defined function) requirements and usage details, as well as limitations that are
specific to JavaScript UDFs.

## Maximum size of JavaScript source code

Snowflake limits the maximum size of the JavaScript source code in the body of a JavaScript UDF. Snowflake recommends limiting
the size to 100 KB. (The code is stored in a compressed form, and the exact limit depends on the compressibility of the code.)

## Consuming too much memory will cause UDF to fail

JavaScript UDFs will fail if they consume too much memory. The specific limit is subject to change. Using too much memory will
result in an error being returned.

## Taking too long to complete will cause a UDF to be killed and an error returned

JavaScript UDFs that take too long to complete will be killed and an error returned to the user. In addition, JavaScript UDFs that
enter endless loops will result in errors.

## Excess stack depth will result in an error

Excessive stack depth due to recursion will result in an error.

## Global state

Snowflake usually preserves the JavaScript global state between iterations of a UDF. However, you should not rely on previous
modifications to the global state being available between function calls. Additionally, you should not assume that all rows will
execute within the same JavaScript environment.

In practice, the global state is relevant with:

- Complex/expensive initialization logic. By default, the provided UDF code is evaluated for every row processed. If that code
  contains complex logic, this might be inefficient.
- Functions that contain code that is not idempotent. A typical pattern would be:

  Copy code

  ```
  Date.prototype._originalToString = Date.prototype.toString;
  Date.prototype.toString = function() {
    /* ... SOME CUSTOM CODE ... */
    this._originalToString()
    }
  ```

  The first time that this code is executed, it changes the state of `toString` and `_originalToString`. Those changes
  are preserved in the global state, and the second time that this code is executed, the values are changed again in a way that
  creates recursion. The second time that `toString` is called, the code recurses infinitely (until it runs out of stack space).

For these situations, a recommended pattern is to guarantee that relevant code is evaluated only once, using JavaScript’s global
variable semantics. For example:

> Copy code
>
> ```
> var setup = function() {
> /* SETUP LOGIC */
> };
>
> if (typeof(setup_done) === "undefined") {
>   setup();
>   setup_done = true;  // setting global variable to true
> }
> ```

Note that this mechanism is only safe for caching the effects of code evaluation. It is not guaranteed that after an initialization
the global context will be preserved for all rows, and no business logic should depend on it.

## JavaScript libraries

JavaScript UDFs support access to the standard JavaScript library. Note that this excludes many objects and methods typically
provided by browsers. There is no mechanism to import, include, or call additional libraries. All required code should be embedded
within the UDF.

Additionally, the built-in JavaScript `eval()` function is disabled.

## Returned variant size and depth

Returned variant objects are subject to size and nesting-depth limitations:

Size:
:   Currently limited to several megabytes, but subject to change.

Depth:
:   Currently limited to a nesting depth of 1000, but subject to change.

If any object is too large or too deep, an error is returned when the UDF is called.

## Argument and return type constraints are sometimes ignored

Certain type characteristics declared for an argument or return value will be ignored when the UDF is called. In these cases, the
received value may be used as received whether or not it conforms to constraints specified in the declaration.

The following are ignored for UDFs whose logic is written in JavaScript:

- Length for arguments of type VARCHAR

### Example

Code in the following example declares that the `arg1` argument and the return value must be a VARCHAR no more than one character
long. However, calling this function with an `arg1` whose value is longer than one character will succeed as if the constraint were
not specified.

Copy code

```
CREATE OR REPLACE FUNCTION tf (arg1 VARCHAR(1))
RETURNS VARCHAR(1)
LANGUAGE JAVASCRIPT AS 'return A.substr(3, 3);';
```
