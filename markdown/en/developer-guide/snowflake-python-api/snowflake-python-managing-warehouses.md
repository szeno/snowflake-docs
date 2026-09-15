# Managing Snowflake virtual warehouses with Python

You can use Python to manage Snowflake virtual warehouses, which are clusters of compute resources in Snowflake. For an overview of
warehouses, see [Virtual warehouses](/user-guide/warehouses).

The Snowflake Python APIs represents warehouses with two separate types:

- `Warehouse`: Exposes a warehouse’s properties such as its name, size, type, and auto-resume and auto-suspend settings.
- `WarehouseResource`: Exposes methods you can use to fetch a corresponding `Warehouse` object, suspend and resume the
  warehouse, and drop the warehouse.

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

## Creating a warehouse

To create a warehouse, first create a `Warehouse` object, and then create a `WarehouseCollection` object from the API `Root`
object. Using `WarehouseCollection.create`, add the new warehouse to Snowflake.

Code in the following example creates a `Warehouse` object that represents a warehouse named `my_wh`:

Copy code

```
from snowflake.core.warehouse import Warehouse

my_wh = Warehouse(
  name="my_wh",
  warehouse_size="SMALL",
  auto_suspend=600,
)
warehouses = root.warehouses
warehouses.create(my_wh)
```

The code creates a `WarehouseCollection` variable `warehouses` and uses `WarehouseCollection.create` to create a new warehouse in Snowflake.

## Getting warehouse details

You can get information about a warehouse by calling the `WarehouseResource.fetch` method, which returns a `Warehouse` object.

Code in the following example gets information about a warehouse named `my_wh`:

Copy code

```
my_wh = root.warehouses["my_wh"].fetch()
print(my_wh.to_dict())
```

## Creating or altering a warehouse

You can set properties of a `Warehouse` object and pass it to the `WarehouseResource.create_or_alter` method to create a
warehouse if it doesn’t exist, or alter it according to the warehouse definition if it does exist. The behavior of `create_or_alter`
is intended to be idempotent, which means that the resulting warehouse object will be the same regardless of whether the warehouse exists
before you call the method.

Note

The `create_or_alter` method uses default values for any [Warehouse](https://docs.snowflake.com/en/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.Warehouse)
properties that you don’t explicitly define. For example, if you don’t set `auto_suspend`, its value defaults to `None` even if
the warehouse previously existed with a different value.

Code in the following example updates the size and auto-suspend setting of the `my_wh` warehouse, and then alters the warehouse on
Snowflake.

Copy code

```
from snowflake.core.warehouse import Warehouse

my_wh = root.warehouses["my_wh"].fetch()
my_wh.warehouse_size = "LARGE"
my_wh.auto_suspend = 1800

my_wh_res = root.warehouses["my_wh"]
my_wh_res.create_or_alter(my_wh)
```

In this case, it changes the `my_wh` warehouse’s size to `LARGE` and its
auto-suspend setting to `1800` if you previously created it with different properties.

## Listing warehouses

You can list warehouses using the `WarehouseCollection.iter` method, which returns a `PagedIter` iterator of
`Warehouse` objects.

Code in the following example lists warehouses whose name includes the text *my* and prints the name of each:

Copy code

```
from snowflake.core.warehouse import WarehouseCollection

warehouses: WarehouseCollection = root.warehouses
wh_iter = warehouses.iter(like="my%")  # returns a PagedIter[Warehouse]
for wh_obj in wh_iter:
  print(wh_obj.name)
```

## Performing warehouse operations

You can perform common warehouse operations—such as suspending and resuming warehouses and aborting all queries on warehouses—with a
`WarehouseResource` object.

Code in the following example suspends and resumes the `my_wh` warehouse, aborts all running or queued queries on the warehouse, and
then drops the warehouse:

Copy code

```
my_wh_res = root.warehouses["my_wh"]

my_wh_res.suspend()
my_wh_res.resume()
my_wh_res.abort_all_queries()
my_wh_res.drop()
```
