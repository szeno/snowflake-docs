# External integration setup reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

The following database objects are created through the file `setup_external_integration.sql`.

## PUBLIC.SETUP\_EXTERNAL\_INTEGRATION\_WITH\_NAMES()

The procedure alters other procedures or functions, whose signatures are passed as procedure argument in an array, with
an `EXTERNAL ACCESS INTEGRATION` and a `SECRET` objects names that are stored in the connection configuration under the
following keys:

> - `external_access_configuration` for an `EXTERNAL ACCESS INTEGRATION` object identifier.
> - `secret` for a `SECRET` object identifier.

Secret is attached to altered procedure/function with the `credentials` key. By default, the procedure is not available for any
of application user roles.

### Procedure signature

> Copy code
>
> ```
> CREATE OR REPLACE PROCEDURE PUBLIC.SETUP_EXTERNAL_INTEGRATION_WITH_NAMES(methods ARRAY)
>     RETURNS VARIANT
>     LANGUAGE SQL
>     [...]
> ```

Where:

- `methods ARRAY` stand for an array of procedure/function signatures as varchar, e.g. `ARRAY_CONSTRUCT('PUBLIC.PROC_1(VARIANT)', 'PUBLIC.PROC_2()')`.

### Returned values

The procedure always returns a Variant with a standard connector response structure.

In case of a successful procedure execution:

> Copy code
>
> ```
> {
>   "response_code": "OK",
>   "message": "Successfully set up <number> method(s)."
> }
> ```
>
> Note
>
> The procedure execution finishes successfully even when procedure/function signatures passed as arguments do not
> represent existing objects or an application does not have an access to these objects. The altering process of this
> kind of procedure/function is skipped and the general process continues.

In case of a failure:

> Copy code
>
> ```
> {
>   "response_code": "<ERROR_CODE>",
>   "message": "<error message>",
>   "SQLCODE": "<code of a thrown exception>",
>   "SQLERRM": "<error message of a thrown exception>",
>   "SQLCODE": "<sql code of a thrown exception>"
> }
> ```
>
> Attention
>
> The procedure does not throw any error if an error occurs during the execution. Each error is wrapped into the
> connector response, and mapped to appropriate `response_code` which allows validating the procedure result and
> using it safely in the `setup.sql` during the application installation (otherwise any unhandled error could
> interrupt and terminate the application installation process).

### Possible errors

- `EAI_UNAVAILABLE` - an `EXTERNAL ACCESS INTEGRATION` object does not exist or an application does not have a `USAGE` privilege on it.
- `SECRET_UNAVAILABLE` - a `SECRET` object does not exist or an application does not have at least a `READ` privilege on it.
- `INTERNAL ERROR` - this response code is returned in case of unexpected errors occurrences.

### Example usage

> Copy code
>
> ```
> CALL PUBLIC.SETUP_EXTERNAL_INTEGRATION_WITH_NAMES(ARRAY_CONSTRUCT(
>     'PUBLIC.TEST_CONNECTION()',
>     'PUBLIC.FINALIZE_CONFIGURATION(VARIANT)',
>     'PUBLIC.TEMPLATE_WORKER(NUMBER, STRING)')
> );
> ```

## PUBLIC.SETUP\_EXTERNAL\_INTEGRATION\_WITH\_REFERENCES()

The procedure alters other procedures or functions, whose signatures are passed as procedure argument in an array, with
an `EXTERNAL ACCESS INTEGRATION` and a `SECRET` objects that are assigned to application references. When using this
procedure, it’s required to have references registered with the following names:

- `EAI_REFERENCE` - for a reference to an `EXTERNAL ACCESS INTEGRATION` object.
- `SECRET_REFERENCE` - for a reference to a `SECRET` object.

Secret is attached to altered procedure/function with the `credentials` key. By default, the procedure is not available for any
of application user roles.

### Procedure signature

> Copy code
>
> ```
> CREATE OR REPLACE PROCEDURE PUBLIC.SETUP_EXTERNAL_INTEGRATION_WITH_REFERENCES(methods ARRAY)
>     RETURNS VARIANT
>     LANGUAGE SQL
>     [...]
> ```

Where:

- `methods ARRAY` stand for an array of procedure/function signatures as varchar, e.g. `ARRAY_CONSTRUCT('PUBLIC.PROC_1(VARIANT)', 'PUBLIC.PROC_2()')`.

### Returned values

The procedure always returns a Variant with a standard connector response structure.

In case of a successful procedure execution:

> Copy code
>
> ```
> {
>   "response_code": "OK",
>   "message": "Successfully set up <number> method(s)."
> }
> ```
>
> Note
>
> The procedure execution finishes successfully even when procedure/function signatures passed as arguments do not
> represent existing objects or an application does not have an access to these objects. The altering process of this
> kind of procedure/function is skipped and the general process continues.

In case of a failure:

> Copy code
>
> ```
> {
>   "response_code": "<ERROR_CODE>",
>   "message": "<error message>",
>   "SQLCODE": "<code of a thrown exception>",
>   "SQLERRM": "<error message of a thrown exception>",
>   "SQLCODE": "<sql code of a thrown exception>"
> }
> ```
>
> Attention
>
> The procedure does not throw any error if an error occurs during the execution. Each error is wrapped into the
> connector response, and mapped to appropriate `response_code` which allows validating the procedure result and
> using it safely in the `setup.sql` during the application installation (otherwise any unhandled error could
> interrupt and terminate the application installation process).

### Possible errors

- `EAI_UNAVAILABLE` - an `EXTERNAL ACCESS INTEGRATION` object does not exist or an application does not have a `USAGE` privilege on it.
- `SECRET_UNAVAILABLE` - a `SECRET` object does not exist or an application does not have at least a `READ` privilege on it.
- `INTERNAL ERROR` - this response code is returned in case of unexpected errors occurrences.

### Example usage

> Copy code
>
> ```
> CALL PUBLIC.SETUP_EXTERNAL_INTEGRATION_WITH_REFERENCES(ARRAY_CONSTRUCT(
>     'PUBLIC.TEST_CONNECTION()',
>     'PUBLIC.FINALIZE_CONFIGURATION(VARIANT)',
>     'PUBLIC.TEMPLATE_WORKER(NUMBER, STRING)')
> );
> ```

## PUBLIC.SETUP\_EXTERNAL\_INTEGRATION()

This is a raw version of procedures described above which is also used by them. The procedure alters other procedures or
functions, whose signatures are passed as procedure argument in an array, with an `EXTERNAL ACCESS INTEGRATION` and
a `SECRET` object names that are also passed as procedure arguments. This procedure gives developer a freedom to decide
how to provide information about external access related objects to the procedure.

Secret is attached to altered procedure/function with the `credentials` key. By default, the procedure is not available for any
of application user roles.

Using this procedure is recommended only when there is no possibility of using procedures described above, that use references
with predefined names or object names stored under predefined keys in connection configuration.

### Procedure signature

> Copy code
>
> ```
> CREATE OR REPLACE PROCEDURE PUBLIC.SETUP_EXTERNAL_INTEGRATION(eai_idf VARCHAR, secret_idf VARCHAR, methods ARRAY)
>     RETURNS VARIANT
>     LANGUAGE SQL
>     [...]
> ```

Where:

- `eai_idf VARCHAR` - stands for an identifier of an `EXTERNAL_ACCESS_INTEGRATION` object. If you want to pass there a reference name, you need to wrap it as follows: `'reference(\'<reference_name>\')'`
- `secret_idf VARCHAR` - stands for an identifier of aa `SECRET` object. If you want to pass there a reference name, you need to wrap it as follows: `'reference(\'<reference_name>\')'`
- `methods ARRAY` stand for an array of procedure/function signatures as varchar, e.g. `ARRAY_CONSTRUCT('PUBLIC.PROC_1(VARIANT)', 'PUBLIC.PROC_2()')`.

### Returned values

The procedure always returns a Variant with a standard connector response structure.

In case of a successful procedure execution:

> Copy code
>
> ```
> {
>   "response_code": "OK",
>   "message": "Successfully set up <number> method(s)."
> }
> ```
>
> Note
>
> The procedure execution finishes successfully even when procedure/function signatures passed as arguments do not
> represent existing objects or an application does not have an access to these objects. The altering process of this
> kind of procedure/function is skipped and the general process continues.

In case of a failure:

> Copy code
>
> ```
> {
>   "response_code": "<ERROR_CODE>",
>   "message": "<error message>",
>   "SQLCODE": "<code of a thrown exception>",
>   "SQLERRM": "<error message of a thrown exception>",
>   "SQLCODE": "<sql code of a thrown exception>"
> }
> ```
>
> Attention
>
> The procedure does not throw any error if an error occurs during the execution. Each error is wrapped into the
> connector response, and mapped to appropriate `response_code` which allows validating the procedure result and
> using it safely in the `setup.sql` during the application installation (otherwise any unhandled error could
> interrupt and terminate the application installation process).

### Possible errors

- `EAI_UNAVAILABLE` - an `EXTERNAL ACCESS INTEGRATION` object does not exist or an application does not have a `USAGE` privilege on it.
- `SECRET_UNAVAILABLE` - a `SECRET` object does not exist or an application does not have at least a `READ` privilege on it.
- `INTERNAL ERROR` - this response code is returned in case of unexpected errors occurrences.

### Example usage

> Copy code
>
> ```
> CALL PUBLIC.SETUP_EXTERNAL_INTEGRATION(
>     'EXAMPLE_EAI_IDF',
>     'reference(\'CUSTOM_REFERENCE_NAME\')',
>     ARRAY_CONSTRUCT('PUBLIC.TEST_CONNECTION()',
>     'PUBLIC.FINALIZE_CONFIGURATION(VARIANT)',
>     'PUBLIC.TEMPLATE_WORKER(NUMBER, STRING)')
> );
> ```

When you want to use this procedure in the `setup.sql` script and names of a `SECRET` and an `EXTERNAL ACCESS INTEGRATION`
objects are stored in a different way from the one which is recommended by the Native SDK for Connectors, you need to
retrieve these values somehow. In this case, you can use the `EXECUTE IMMEDIATE` mechanism:

> Copy code
>
> ```
> EXECUTE IMMEDIATE $$
>     DECLARE
>         eai_idf VARCHAR;
>         secret_idf VARCHAR;
>     BEGIN
>         -- retrieve name of an EXTERNAL ACCESS INTEGRATION object
>         :eai_idf = <eai_object_name>;
>
>         -- retrieve name of a SECRET object
>         :secret_idf = <secret_object_name>;
>
>         CALL PUBLIC.SETUP_EXTERNAL_INTEGRATION(
>             :eai_idf,
>             :secret_idf,
>             ARRAY_CONSTRUCT('PUBLIC.TEST_CONNECTION()',
>             'PUBLIC.FINALIZE_CONFIGURATION(VARIANT)',
>             'PUBLIC.TEMPLATE_WORKER(NUMBER, STRING)')
>         );
>     END;
> $$
> ;
> ```
