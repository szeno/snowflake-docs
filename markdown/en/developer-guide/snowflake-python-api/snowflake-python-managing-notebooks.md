# Managing Snowflake Notebooks with Python

You can use Python to manage Snowflake Notebooks, which is a development interface in Snowsight that offers an interactive, cell-based
programming environment for Python and SQL. For more information, see [About Legacy Snowflake Notebooks](/user-guide/ui-snowsight/notebooks).

The Snowflake Python APIs represents notebooks with two separate types:

- `Notebook`: Exposes a notebook’s properties such as its name, version, query warehouse, and `.ipynb` file.
- `NotebookResource`: Exposes methods you can use to fetch a corresponding `Notebook` object, manage versions of the notebook,
  and execute the notebook.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Creating a notebook

To create a notebook, first create a `Notebook` object, and then create a `NotebookCollection` object from the API `Root`
object. Using `NotebookCollection.create`, add the new notebook to Snowflake.

Code in the following example creates a `Notebook` object that represents a notebook named `my_nb` in the `my_db` database
and the `my_schema` schema:

Copy code

```
from snowflake.core.notebook import Notebook

my_nb = Notebook(name="my_nb")

notebooks = root.databases["my_db"].schemas["my_schema"].notebooks
notebooks.create(my_nb)
```

The code creates a `NotebookCollection` variable `notebooks` and uses `NotebookCollection.create` to create a new
notebook in Snowflake.

You can also create a notebook from a stage with an existing `.ipynb` file. Code in the following example creates a notebook from the
`@my_stage` stage with the `notebook_file.ipynb` file:

Copy code

```
from snowflake.core.notebook import Notebook

my_nb = Notebook(name="my_nb",
  query_warehouse="my_wh",
  from_location="@my_stage",
  main_file="notebook_file.ipynb")

notebooks = root.databases["my_db"].schemas["my_schema"].notebooks
notebooks.create(my_nb)
```

## Getting notebook details

You can get information about a notebook by calling the `NotebookResource.fetch` method, which returns a `Notebook` object.

Code in the following example gets information about a notebook named `my_nb` in the `my_db` database and the `my_schema` schema:

Copy code

```
my_nb = root.databases["my_db"].schemas["my_schema"].notebooks["my_nb"].fetch()
print(my_nb.to_dict())
```

## Listing notebooks

You can list notebooks using the `NotebookCollection.iter` method, which returns a `PagedIter` iterator of
`Notebook` objects.

Code in the following example lists notebooks whose name starts with `my` in the `my_db` database and the `my_schema` schema, and
then prints the name of each:

Copy code

```
from snowflake.core.notebook import NotebookCollection

notebooks: NotebookCollection = root.databases["my_db"].schemas["my_schema"].notebooks
nb_iter = notebooks.iter(like="my%")  # returns a PagedIter[Notebook]
for nb_obj in nb_iter:
  print(nb_obj.name)
```

## Performing notebook operations

You can perform common notebook operations—such as managing versions and executing notebooks—with a `NotebookResource` object.

To demonstrate some operations you can do with a notebook resource, code in the following example does the following:

1. Gets the `my_nb` notebook resource object.
2. Adds a lives version to the notebook object. This is equivalent to [ALTER NOTEBOOK … ADD LIVE VERSION](/sql-reference/sql/alter-notebook).
3. Commits the live version of the notebook to a Git repository, if a Git connection is set up. Otherwise, sets the live version to `null`.

   For more information, see [ALTER NOTEBOOK](/sql-reference/sql/alter-notebook).
4. Executes the notebook.

   Note

   To execute a notebook, you must add a live version to it first.
5. Drops the notebook.

Copy code

```
my_nb_res = root.databases["my_db"].schemas["my_schema"].notebooks["my_nb"]

my_nb_res.add_live_version(from_last=True)
my_nb_res.commit()
my_nb_res.execute()
my_nb_res.drop()
```
