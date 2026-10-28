# Connecting to Snowflake with SQLAlchemy

## Connection parameters

Snowflake SQLAlchemy uses the following syntax for the connection string used to connect to Snowflake and initiate a session:

Copy code

```
'snowflake://<user_login_name>:<password>@<account_identifier>'
```

Where:

- `<user_login_name>` is the login name for your Snowflake user.
- `<password>` is the password for your Snowflake user.
- `<account_identifier>` is the identifier for your Snowflake account.

Include the region in the `<account_identifier>` if applicable. Don’t include the `snowflakecomputing.com` domain. For more information, see [Account name in your organization](/user-guide/admin-account-identifier#label-account-name).

You can optionally specify the initial database and schema for the Snowflake session by including them at the end of the connection string, separated by `/`. You can also specify the initial warehouse and role for the session as a parameter string at the end of the connection string:

Copy code

```
'snowflake://<user_login_name>:<password>@<account_identifier>/<database_name>/<schema_name>?warehouse=<warehouse_name>&role=<role_name>'
```

### Escaping special characters in passwords

As noted in [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/core/engines.html#escaping-special-characters-such-as-signs-in-passwords), URLs containing special characters need to be URL encoded to be parsed correctly. This includes the `%` and `@` signs. Unescaped passwords containing special characters could lead to authentication failure.

The encoding for the password can be generated using `urllib.parse`:

Copy code

```
import urllib.parse
urllib.parse.quote("kx@% jj5/g")
'kx%40%25%20jj5/g'
```

Note

`urllib.parse.quote_plus` may also be used if there is no space in the string, as `urllib.parse.quote_plus` will replace space with `+`.

To create an engine with the proper encodings, either manually construct the URL string by formatting or use the `snowflake.sqlalchemy.URL` helper method:

Copy code

```
import urllib.parse
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

quoted_password = urllib.parse.quote("kx@% jj5/g")

# 1. Manually constructing a URL string
url = f'snowflake://testuser1:{quoted_password}@abc123/testdb/public?warehouse=testwh&role=myrole'
engine = create_engine(url)

# 2. Using the snowflake.sqlalchemy.URL helper method
engine = create_engine(URL(
    account='abc123',
    user='testuser1',
    password=quoted_password,
    database='testdb',
    schema='public',
    warehouse='testwh',
    role='myrole',
))
```

The `URL` helper validates the `account` and `region` values, which may contain only letters, digits, hyphens, dots, and underscores, and raises `sqlalchemy.exc.ArgumentError` otherwise. It also percent-encodes `user`, so characters such as `?`, `&`, `@`, and `#` can’t inject extra URL parameters. `URL` doesn’t accept private key parameters; pass those through `connect_args` (see [Key pair authentication support](/developer-guide/sqlalchemy/sqlalchemy-auth#label-sqlalchemy-key-pair)).

Note

After login, the initial database, schema, warehouse and role specified in the connection string can always be changed for the session.

The following example calls the `create_engine` method with the user name `testuser1`, password `0123456`, account name `abc123`, database `testdb`, schema `public`, warehouse `testwh`, and role `myrole`:

Copy code

```
from sqlalchemy import create_engine
engine = create_engine(
    'snowflake://testuser1:0123456@abc123/testdb/public?warehouse=testwh&role=myrole'
)
```

Other connector parameters, such as `timezone`, can be passed as a `URL` argument or through `connect_args`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://testuser1:0123456@abc123/testdb/public?warehouse=testwh&role=myrole',
    connect_args={
        'timezone': 'America/Los_Angeles',
    }
)
```

To fetch NumPy data types (`numpy.int64`, `numpy.float64`, and `numpy.datetime64`), add `'numpy': True` to `connect_args`. Binding NumPy values works without this setting.

### Special characters in database and schema names

The URL path holds `database` or `database/schema`. A `/` outside double quotes separates the two; inside a quoted identifier such as `"a/b"`, it’s part of the name.

- **`snowflake.sqlalchemy.URL` helper (recommended):** Pass names as you would write them in SQL, for example `database='"my db"', schema='"a/b"'`. The helper percent-encodes them, and the connector receives the original values on SQLAlchemy 2.0 and 2.1.
- **`sqlalchemy.engine.URL.create(...)`:** On SQLAlchemy 2.1, values are used as passed, so `database='my%20db'` stays `my%20db`. On SQLAlchemy 2.0, the dialect can’t tell a `URL.create()` value from a parsed URL string, so a name that contains `%` and no raw `"` is percent-decoded (`my%20db` becomes `my db`). `database='"a%20b"'` stays `"a%20b"` on both versions. To keep a literal `%` on SQLAlchemy 2.0, quote the name or write the `%` as `%25`.
- **Hand-written URL strings:** Percent-encode reserved characters in each name with `urllib.parse.quote(name, safe="")`, including the double quotes. SQLAlchemy 2.1 decodes the path itself. On SQLAlchemy 2.0, the dialect decodes each database or schema name that has no raw `"`; unquoted Snowflake identifiers can’t contain `%`, so such a `%` is always an encoding. A name that contains a raw `"` is treated as unencoded on SQLAlchemy 2.0; the other name in the path is still decoded.

Starting with Snowflake SQLAlchemy 2.1, the helper encodes a space as `%20` rather than `+`, because SQLAlchemy 2.1 doesn’t decode `+` in the path. For URLs built with the helper, the resulting connection values are unchanged; only the generated URL string differs. Hand-written URLs are read differently than in 2.0.0: a `+` in the path stays `+` (it used to become a space), and an encoded `%2F` outside quotes separates the database from the schema. For details, see [URL database and schema path decoding](/developer-guide/sqlalchemy/sqlalchemy-migrate#label-sqlalchemy-migrate-url-path-decoding).

### Using the create\_snowflake\_engine helper

To connect with a case-sensitive (mixed-case) schema name, use `create_snowflake_engine()` instead of building the URL by hand. It quotes the schema name for you. Other keyword arguments are passed to `create_engine()`:

Copy code

```
from snowflake.sqlalchemy import create_snowflake_engine

engine = create_snowflake_engine(
    'snowflake://user:password@account/database',
    schema='MixedCaseSchema',
    case_sensitive_schema=True,
)
```

The base URL must not already include a schema. For the async equivalent, see [Async support in Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-async#label-quick-start).

### Using a proxy server

The Snowflake Connector for Python supports tunneling connections through a proxy server. To use a proxy server with Snowflake SQLAlchemy, pass the proxy parameters through `connect_args`. You can also set `proxy_scheme` to `http` (the default) or `https`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user:password@account/database/schema',
    connect_args={
        'proxy_host': 'proxy.example.com',
        'proxy_port': 8080,
        'proxy_user': 'proxy_user',
        'proxy_password': 'proxy_password',
    }
)
```

When no explicit proxy parameters are set, the connector uses the `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables. To ignore them, set `'use_proxy_env': False` in `connect_args`.

### Using session parameters

Session parameters specify the default behavior for the session. Pass them through the `session_parameters` dictionary in `connect_args`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user:password@account/database/schema',
    connect_args={
        'session_parameters': {
            'STATEMENT_TIMEOUT_IN_SECONDS': 10,
            'QUERY_TAG': 'my_tag',
            'QUOTED_IDENTIFIERS_IGNORE_CASE': True,
        }
    }
)
```

Session parameters set this way apply to every query in the session. To change a parameter for specific queries, run `ALTER SESSION`:

Copy code

```
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("ALTER SESSION SET QUERY_TAG = 'batch_job_1'"))
    conn.execute(text("..."))  # Uses 'batch_job_1'

    conn.execute(text("ALTER SESSION UNSET QUERY_TAG"))
    conn.execute(text("..."))  # No tag
```

### Sensitive connection parameters

A set of connector parameters is blocked from the URL query string because they change the connection target, read or write local files, or relax a connector safety check. Passing any of them in the URL query string raises `sqlalchemy.exc.ArgumentError`. Pass them through `connect_args` in `create_engine()` instead:

- `host`
- `protocol`
- `token_file_path`
- `private_key_file`
- `ocsp_response_cache_filename`
- `connection_diag_log_path`
- `crl_cache_dir`
- `unsafe_file_write`
- `unsafe_skip_file_permissions_check`
- `unsafe_skip_config_file_permissions_check`
- `crl_unsafe_skip_file_permissions_check`

For example:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://user:password@account/',
    connect_args={
        'protocol': 'https',
        'token_file_path': '/path/to/token',
    }
)
```

### Dialect options

Pass these options as keyword arguments to `create_engine()`:

| Option | Default | Description |
| --- | --- | --- |
| `enable_decfloat` | `False` | Maps `DECFLOAT` columns to `snowflake.sqlalchemy.DECFLOAT` with full 38-digit precision. See [Snowflake SQLAlchemy data types](/developer-guide/sqlalchemy/sqlalchemy-data-types). |
| `enable_native_uuid` | `False` | Renders SQLAlchemy’s generic `Uuid` type as the native Snowflake `UUID` type instead of `CHAR(32)`. Turning this on changes the DDL for existing `Uuid` columns. See [Snowflake SQLAlchemy data types](/developer-guide/sqlalchemy/sqlalchemy-data-types). |
| `case_sensitive_identifiers` | `False` | Treats identifiers as case-sensitive. |
| `enable_structured_type_json` | `True` | Enables JSON serialization and deserialization for `VARIANT`, `OBJECT`, `ARRAY`, and `MAP` columns. Setting it to `False` is deprecated and emits a `DeprecationWarning`. |
| `strict_host_names` | `False` | Stops the dialect from inferring or appending domains to host names and forwards connection parameters to the connector unvalidated. See [Strict host-name mode](#label-sqlalchemy-strict-host-names). |

Expand

Show lessSee more

The `legacy_url_params` and `force_div_is_floordiv` options were removed. Passing either to `create_engine()` raises an error. The `/` operator always performs true division, and `//` always performs floor division.

### Strict host-name mode

For air-gapped or custom-domain deployments, set `strict_host_names=True` in `create_engine()` (or set the `SNOWFLAKE_SQLALCHEMY_STRICT_HOST_NAMES=true` environment variable). In this mode the dialect doesn’t infer or append any domain to host names. It forwards connection parameters, such as `host`, `port`, authentication, and `connection_name`, to the Snowflake Connector for Python unchanged and doesn’t validate them; the connector handles connection establishment, including missing parameters. When strict mode is off (the default), behavior is unchanged.

Supply all connection parameters through `connect_args`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://',
    strict_host_names=True,
    connect_args={
        'account': 'myaccount',
        'host': 'myaccount.snowflake.example.com',
        'port': 443,
        'user': 'myuser',
        'authenticator': 'SNOWFLAKE_JWT',
        'private_key_file': '/path/to/rsa_key.p8',
        'database': 'mydb',
        'schema': 'public',
        'warehouse': 'mywh',
    },
)
```

Or use a named profile from the connector’s `connections.toml`, which the connector reads and applies itself:

Copy code

```
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

engine = create_engine(
    URL(account=''),
    strict_host_names=True,
    connect_args={'connection_name': 'my_profile'},
)
```

`AzureContainer` accepts an explicit `endpoint` (for example, `endpoint='blob.storage.example.com'`). In strict mode, an `AzureContainer` without one fails at SQL compilation instead of defaulting to `.blob.core.windows.net`.

## Opening and closing a connection

To open a connection:

Copy code

```
connection = engine.connect()
```

To close the connection:

Copy code

```
connection.close()
```

To dispose of the engine:

Copy code

```
engine.dispose()
```

Prefer a context manager, which closes the connection for you:

Copy code

```
from sqlalchemy import text

with engine.connect() as connection:
    connection.execute(text('select 1'))
```

When using SQLAlchemy sessions, connections are managed automatically. Typically, you don’t need to call `close()` or `dispose()` directly.

Connections use the `READ COMMITTED` isolation level with the connector’s autocommit turned off, so changes aren’t saved until you commit. Use `connection.commit()`, `engine.begin()`, or an ORM `Session` transaction.

## Automatic reconnection on expired sessions

The dialect flags recoverable Snowflake session and token loss errors, such as “Authentication token has expired” or “Session no longer exists,” as disconnects. SQLAlchemy’s connection pool then discards the dead connection and opens a new one. To validate pooled connections before use, set `pool_pre_ping=True`:

Copy code

```
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

engine = create_engine(
    URL(account='myaccount', user='me', password='secret'),
    pool_pre_ping=True,
)
```

Permanent authentication failures, such as revoked credentials, aren’t treated as disconnects. They’re raised as errors, because reconnecting can’t fix them.
