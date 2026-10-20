# Snowflake SQLAlchemy

Snowflake SQLAlchemy runs on top of the Snowflake Connector for Python as a [dialect](https://docs.sqlalchemy.org/en/latest/dialects/) to bridge a Snowflake database and SQLAlchemy applications.

## Prerequisites

### Python and SQLAlchemy versions

Snowflake SQLAlchemy 2.x requires:

- Python 3.11 or later.
- SQLAlchemy 2.0.44 or later, but earlier than 2.1 (`>=2.0.44,<2.1`).

### Snowflake Connector for Python

The only other requirement for Snowflake SQLAlchemy is the Snowflake Connector for Python; however, the connector does not need to be installed separately because installing Snowflake SQLAlchemy automatically installs the connector.

### Data analytics and web application frameworks (optional)

Snowflake SQLAlchemy can be used with [Pandas](https://pandas.pydata.org/), [Jupyter](https://jupyter.org/) and [Pyramid](https://www.pylonsproject.org/), which provide higher levels of application frameworks for data analytics and web applications. However, building a working environment from scratch is not a trivial task, particularly for novice users. Installing the frameworks requires C compilers and tools, and choosing the right tools and versions is a hurdle that might deter users from using Python applications.

An easier way to build an environment is through [Anaconda](https://www.continuum.io/why-anaconda), which provides a complete, precompiled technology stack for all users, including non-Python experts such as data analysts and students. For Anaconda installation instructions, see the [Anaconda install documentation](https://docs.continuum.io/anaconda/install). The Snowflake SQLAlchemy package can then be installed on top of Anaconda using [pip](https://pypi.python.org/pypi/pip).

## Installing Snowflake SQLAlchemy

The Snowflake SQLAlchemy package can be installed from the public PyPI repository using `pip`:

Copy code

```
pip install --upgrade snowflake-sqlalchemy
```

`pip` automatically installs all required modules, including the Snowflake Connector for Python.

Snowflake SQLAlchemy 2.x requires Python 3.11 or later, SQLAlchemy `>=2.0.44,<2.1`, and `snowflake-connector-python>=5.0.0`. If you’re upgrading from 1.x, see [Migrating Snowflake SQLAlchemy from 1.x to 2.x](/developer-guide/sqlalchemy/sqlalchemy-migrate).

To use pandas with Snowflake SQLAlchemy, install the `pandas` extra:

Copy code

```
pip install "snowflake-sqlalchemy[pandas]"
```

## Verifying your installation

1. Create a file (for example, `validate.py`) that contains the following Python sample code, which connects to Snowflake and displays the Snowflake version:

Copy code

```
from sqlalchemy import create_engine, text

engine = create_engine(
    'snowflake://{user}:{password}@{account}/'.format(
        user='<your_user_login_name>',
        password='<your_password>',
        account='<account_identifier>',
    )
)
try:
    with engine.connect() as connection:
        results = connection.execute(text('select current_version()')).fetchone()
        print(results[0])
finally:
    engine.dispose()
```

2. Replace `<your_user_login_name>`, `<your_password>`, and `<account_identifier>` with the appropriate values for your Snowflake account and user.

   For more details, see [Connection Parameters](/developer-guide/sqlalchemy/sqlalchemy-connect#label-connection-parameters).
3. Execute the sample code. For example, if you created a file named `validate.py`:

Copy code

```
python validate.py
```

The Snowflake version (for example, `10.38.10`) should be displayed.

Note

SQLAlchemy 2.x doesn’t accept plain SQL strings in `connection.execute()`. Wrap raw SQL in `sqlalchemy.text()`, or use `connection.exec_driver_sql()`. Passing a bare string raises `sqlalchemy.exc.ObjectNotExecutableError`.

## Verifying package signatures

Python packages on PyPI can be digitally signed by their publishers using GPG. Verify the package signature of `snowflake-sqlalchemy` to ensure that the package you downloaded was published by Snowflake and has not been tampered with.

The package signatures and the public key can be found on the [Snowflake Python Packages repository](https://github.com/snowflakedb/snowflake-python-packages).

**Next Topics:**

- [Connecting to Snowflake with SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-connect)
- [Async support in Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-async)
- [Data type support in SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-data-types)
- [Schema reflection in SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-reflection)
- [DDL features in SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-ddl)
- [DML and bulk operations in SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-dml)
- [Using Alembic with Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-alembic)
- [Authentication and connection options](/developer-guide/sqlalchemy/sqlalchemy-auth)
- [Migrating Snowflake SQLAlchemy from 1.x to 2.x](/developer-guide/sqlalchemy/sqlalchemy-migrate)
- [Known limitations of Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-limitations)

## Support

For support, please visit [Snowflake Community Forum](https://community.snowflake.com/) or [contact Snowflake Support](/user-guide/contacting-support).
