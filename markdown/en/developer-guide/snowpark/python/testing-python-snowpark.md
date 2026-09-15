# Writing Tests for Snowpark Python

This topic explains how to test your Snowpark code while connected to Snowflake.
You can use standard testing utilities, like PyTest, to test your Snowpark Python UDFs, DataFrame transformations, and stored procedures.

Thorough testing can help to prevent unintended breaking changes. Unit tests verify that a section of code works as expected.
Integration tests help ensure that components work together correctly for an end-to-end use case.

The examples in this document use PyTest, one of the most popular testing frameworks for Python.
For additional guidance and best practices, see the [PyTest documentation](https://docs.pytest.org/en/7.4.x/).

Alternatively, you can use the Snowpark Python local testing framework to create and operate on Snowpark Python DataFrames locally without
connecting to a Snowflake account. For more information, see [Local testing framework](/developer-guide/snowpark/python/testing-locally).

## Setting up your Tests

Install PyTest in your project, by running `pip install pytest` or `conda install pytest`.
You can also add it to your `requirements.txt` or conda environment file.

Create a `test` directory next to your source code directory and add your unit and integration tests to it.
To see an example, refer to the [Snowpark Python project template](https://github.com/Snowflake-Labs/snowpark-python-template/).

## Creating a PyTest Fixture for the Snowpark Session

PyTest fixtures are functions that are executed before a test (or module of tests) to provide data or connections to tests.
In this scenario, create a PyTest fixture that returns a Snowpark `Session` object.

1. Create a `test` directory if you do not already have one.
2. Create a `conftest.py` under `test` with the following contents, where `connection_parameters` is a dictionary with your Snowflake
   account credentials. For more information about the dictionary format, see [Creating a Session](/developer-guide/snowpark/python/creating-session#label-snowpark-python-creating-session).
3. Create the `Session` fixture as a module-scoped fixture instead of as a file-scoped fixture to prevent multiple sessions from being created
   and causing issues due to conflicting session objects.

Copy code

```
from snowflake.snowpark.session import Session

@pytest.fixture(scope='module')
def session(request) -> Session:
    connection_parameters = {}
    return Session.builder.configs(...).create()
```

## Unit Tests for UDFs

You can test your Python UDF logic by testing the UDF handler as a generic Python method.

1. Create a file under your `test` directory for the UDF unit tests. For example, name the file `test_functions.py`.
2. Import the Python methods to test.
3. For each test scenario, create a Python method named `test_<scenario_to_test>`.

For example, here is a Python UDF handler:

Copy code

```
def fahrenheit_to_celsius(temp_f: float) -> float:
    """
    Converts fahrenheit to celsius
    """
    return (float(temp_f) - 32) * (5/9)
```

You can import this method into the test file (`test/test_functions.py`) and test it as a generic Python method.

Copy code

```
import fahrenheit_to_celsius

def test_fahrenheit_to_celsius():
    expected = 0.0
    actual = fahrenheit_to_celsius(32)
    assert expected == actual
```

## Unit Tests for DataFrame Transformations

Adding unit tests for your DataFrame transformations helps to protect against unexpected bugs and regressions.
To make your DataFrame logic easily testable, encapsulate the transformations into a Python method that takes as
input the DataFrames to be transformed and returns the transformed DataFrames.

In the example below, `my_df_transformer` contains the transformation logic. It can be imported into other
modules in the Python project and tested easily.

Copy code

```
from snowflake.snowpark.dataframe import DataFrame, col

def my_df_transformer(df: DataFrame) -> DataFrame:
    return df \
        .with_column('c', df['a']+df['b']) \
        .filter(col('c') > 3)
```

To test this transformation, follow these steps:

1. Create a file for the DataFrame tests, `test_transformers.py`, under the `test` directory (`test/test_transformers.py`).
2. Create a test method for the transformer to be tested: `test_my_df_transformer(session)`. The `session` parameter here refers to the session fixture created in the earlier section.
3. Using the session fixture, create the input and expected output DataFrames within the test method.
4. Pass the input DataFrame to the transformer and compare the expected DataFrame to the actual DataFrame returned by the transformer.

Copy code

```
# test/test_transformers.py

from my_df_transformer import my_df_transformer

def test_my_df_transformer(session):
    input_df = session.create_dataframe([[1,2],[3,4]], ['a', 'b'])
    expected_df = session.create_dataframe([[3,4,7]], ['a','b','c'])
    actual_df = my_df_transformer(input_df)
    assert expected_df.collect() == actual_df.collect()
```

## Integration Tests for Stored Procedures

To test your stored procedure handlers, use the session fixture to call the stored procedure handler.
If your stored procedure reads from tables, such as in an ETL pipeline, you can create those tables prior to calling the stored procedure handler,
as shown in the example below. This pattern ensures that your input data is tracked in source control and does not unexpectedly change between test executions.

Copy code

```
from project import my_sproc_handler  # import stored proc handler

def test_my_sproc_handler(session: Session):

    # Create input table
    input_tbl = session.create_dataframe(
        data=[...],
        schema=[...],
    )

    input_tbl.write.mode('overwrite').save_as_table(['DB', 'SCHEMA', 'INPUT_TBL'], mode='overwrite')

    # Create expected output dataframe
    expected_df = session.create_dataframe(
        data=[...],
        schema=[...],
    ).collect()

    # Call the stored procedure
    my_sproc_handler()

    # Get actual table
    actual_tbl = session.table(['DB', 'SCHEMA', 'OUTPUT_TBL']).collect()

    # Clean up tables
    session.table(['DB', 'SCHEMA', 'OUTPUT_TBL']).delete()
    session.table(['DB', 'SCHEMA', 'INPUT_TBL']).delete()

    # Compare the actual and expected tables
    assert expected_df == actual_tbl
```
