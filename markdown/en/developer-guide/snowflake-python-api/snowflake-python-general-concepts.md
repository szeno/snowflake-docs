# Snowflake Python APIs: General concepts

The programming model of the Snowflake Python APIs is *resource-based*, which means that the APIs consist of a set of objects that represent their
respective object counterparts in Snowflake. Some basic examples of Snowflake resource object types include the following:

- Databases
- Schemas
- Tables
- Views
- Alerts
- Pipes
- Stages
- Users
- Warehouses

For each supported resource, the Python API provides three distinct classes that you can use to create and manage objects:

- [Collection class](#label-snowflake-python-collection-class)
- [Model class](#label-snowflake-python-model-class)
- [Resource class](#label-snowflake-python-resource-class)

## Entry point: The `Root` object

The `Root` object is the entry point for the Python API. To create an instance of `Root` that is configured with the Snowflake
context in which it will run, you use a Python Connector `Connection` object or a Snowpark `Session` object.

For example, the following code instantiates a `Root` object with a `Connection` object named `my_connection`:

Copy code

```
from snowflake.core import Root

root = Root(my_connection)
```

You can also instantiate a `Root` object with a `Session` object. In a notebook environment or stored procedure, you retrieve
the session by using `get_active_session()`, as follows:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark.context import get_active_session

session = get_active_session()
root = Root(session)
```

### Account, database, and schema scopes

With a `Root` object, you can access the collections of *account-scoped* objects, such as warehouses (`root.warehouses`),
databases (`root.databases`), and external volumes (`root.external_volumes`).

You can access *database-scoped* objects under a `DatabaseResource`, which in turn you can retrieve through the
`DatabaseCollection` object under `Root`. Currently, `SchemaCollection` is the only object type available under the
database scope.

You can access *schema-scoped* objects, such as tables, views, streams, and stages, through the `SchemaResource` object.

For example, the following code accesses a `StageCollection` first, and then a `StageResource`:

Copy code

```
root = Root(my_connection)
stages = root.databases["my_db"].schemas["my_schema"].stages
my_stage = stages["my_stage"] # Access the "my_stage" StageResource
```

### `snowflake.core` class diagram

The following diagram shows some basic classes in the `snowflake.core` package and how they relate to each other, starting with the
`Root` object:

![Diagram showing some basic classes in the snowflake.core package and how they relate to each other](/static/images/snowflake-python-api/snowflake-python-api-class-diagram.svg)

## Collection class

The `Collection` classes correspond to classes that are named `<SnowflakeObjectType>Collection`.

A `Collection` class represents the set of a particular object type visible within the given context. For schema-scoped objects
(like tables, views, functions, and streams), the collection consists of all objects of that type within the given schema that are visible
to the current role or user.

`SchemaCollection` objects are scoped to a database. Account-scoped objects like `DatabaseCollection` and `WarehouseCollection` are accessible
directly from the `Root` instance.

In general, collections enable you to do the following operations:

- Create an object in the schema, database, or account (depending the scope and context, as described previously).
- Iterate through the set of objects visible in that scope.

For example, the following code creates a new warehouse using a `WarehouseCollection` object:

Copy code

```
# my_wh is created from scratch
my_wh = Warehouse(name="my_wh", warehouse_size="X-Small")
root.warehouses.create(my_wh)
```

### Retrieving a `Resource` object from a collection

Additionally, collections provide an entry point to retrieve specific `Resource` objects in the underlying Snowflake database to
which the API is connected. You use the square bracket index operator (`[ ]`) on a collection to “point” to, or get a reference to, a
Snowflake object within that collection.

For example, the following code retrieves a reference to an existing warehouse named `my_wh` in your Snowflake account:

Copy code

```
# my_wh_ref is retrieved from an existing warehouse
# This returns a WarehouseResource object, which is a reference to a warehouse named "my_wh" in your Snowflake account
my_wh_ref = root.warehouses["my_wh"]
```

## Model class

The model classes simply have the same names as their equivalent resources in Snowflake, such as `Warehouse` for warehouses and
`Table` for tables.

A model class represents a Snowflake object along with its associated properties, such as its name, the database and schema to which it
belongs (if applicable), and attributes specific to that object type. For example, a Warehouse model indicates the `warehouse_size`,
`type`, and `auto_resume` properties for that particular warehouse object.

Model objects contain a *property bag* (a collection of properties and their values) that describes the object. You can use
these properties to either describe an existing object in Snowflake, or to provide the specification of that resource to alter an existing
object with.

### Fetching a model object from a `Resource`

To return the property bag of an object as it currently exists in your Snowflake database, you run a `fetch()` operation on the
`Resource` object.

For example, the following code demonstrates some operations you can perform using a model object:

Copy code

```
# my_wh is fetched from an existing warehouse
my_wh = root.warehouses["my_wh"].fetch()
print(my_wh.name, my_wh.auto_resume)
```

Copy code

```
# my_wh is fetched from an existing warehouse
my_wh = root.warehouses["my_wh"].fetch()
my_wh.warehouse_size = "X-Small"
root.warehouses["my_wh"].create_or_alter(my_wh)
```

Note

This fetch operation fails if the `my_wh` object does not exist in Snowflake.

## Resource class

The `Resource` classes correspond to classes that are named `<SnowflakeObjectType>Resource`.

You can consider a `Resource` object as a pointer or reference to an underlying Snowflake object. Whereas the model class is a simple
property bag representing the properties or specification of an object, the `Resource` class is a reference to the actual object in
your Snowflake database.

To get a `Resource` object, you typically refer to it by name from its corresponding `Collection` and use the square bracket
index operator (`[ ]`). The following code example retrieves an existing warehouse named `my_wh` from the warehouse collection:

Copy code

```
# my_wh_ref is retrieved from an existing warehouse
# This returns a WarehouseResource object, which is a reference to a warehouse named "my_wh" in your Snowflake account
my_wh_ref = root.warehouses["my_wh"]

# Fetch returns the properties of the object (returns a "Model" Warehouse object that represents that warehouse's properties)
wh_properties = my_wh_ref.fetch()
```

To convert a `Resource` object to its corresponding model, perform a `fetch()` on the resource, which retrieves the properties
of the corresponding object in Snowflake. Note that this fetch operation fails if the object does not actually exist in Snowflake.

### Performing type-specific operations on a `Resource` object

The `Resource` class also implements the object type’s specialized API operations. For example, you use a `WarehouseResource`
object to resume a warehouse, or a `StageResource` object to list the files on a stage.

The following code examples show how to perform these type-specific operations using their respective `Resource` objects:

Copy code

```
# my_wh_ref is retrieved from an existing warehouse
my_wh_ref = root.warehouses["my_wh"]

# Resume a warehouse using a WarehouseResource object
my_wh_ref.resume()
```

Copy code

```
# my_stage is retrieved from an existing stage
stage_ref = root.databases["my_db"].schemas["my_schema"].stages["my_stage"]

# Print file names and their sizes on a stage using a StageResource object
for file in stage_ref.list_files():
  print(file.name, file.size)
```

### Using the `create_or_alter` API

`Resource` objects also expose the `create_or_alter` API method if it’s supported by the resource. This method enables you to,
as the name suggests, create or alter Snowflake objects.

Note

The Python API uses this create-or-alter (COA) mechanism for modifying objects in Snowflake. The purpose of this mechanism is to ensure
that the result of a COA operation is the same regardless of whether that particular object already exists in your Snowflake database.

In other words, if the object does not exist, the COA operation creates one with the provided specification; if it does
already exist, the operation alters the existing object to match the requested specification. This logic enables you to create or
alter resources by using a single piece of code in an idempotent and atomic manner.

## Consistent design pattern to manage resources

The Snowflake Python APIs have a consistent design pattern that you use to manage resources in Snowflake. Consider an example scenario where you need
to alter an existing warehouse object in your account. The following steps outline how you typically work with the API’s design pattern by
using all three class types, as described previously.

### 1. Get a `WarehouseCollection` from `Root`

Warehouses are account-scoped objects that you can directly access from `Root`:

Copy code

```
my_warehouses = root.warehouses # my_warehouses is a WarehouseCollection
```

### 2. Get a `WarehouseResource` object from `WarehouseCollection`

To retrieve a `Resource` object, you typically start with its collection. `Collection` objects provide an entry point for you to
retrieve specific resources in the underlying Snowflake database by using the square bracket index operator (`[ ]`):

Copy code

```
my_wh_ref = my_warehouses.warehouses["my_wh"] # my_wh_ref is a WarehouseResource
```

### 3. Fetch the `Warehouse` model from `WarehouseResource`

Using the `WarehouseResource` object, you fetch the corresponding `Warehouse` model and its properties from Snowflake:

Copy code

```
my_wh = my_wh_ref.fetch() # my_wh is a Warehouse model object
```

### 4. Modify a property in the `Warehouse` model

Modify a property, such as the `warehouse_size`, in your warehouse model:

Copy code

```
my_wh.warehouse_size = "X-Small"
```

### 5. Alter the existing warehouse object in Snowflake

Finally, using your modified warehouse model specification, you alter the existing warehouse object in Snowflake (or create the warehouse
object if it doesn’t exist):

Copy code

```
my_wh_ref.create_or_alter(my_wh) # Use the WarehouseResource to perform create_or_alter
```

Using this `my_wh_ref` reference, you can also perform other operations on the object in Snowflake, such as dropping it, if necessary.

### Full code example

The following code example shows the create-or-alter warehouse operation in full from start to end:

Copy code

```
# my_wh is fetched from an existing warehouse
my_warehouses = root.warehouses # my_warehouses is a WarehouseCollection
my_wh_ref = my_warehouses.warehouses["my_wh"] # my_wh_ref is a WarehouseResource
my_wh = my_wh_ref.fetch() # my_wh is a Warehouse model object
my_wh.warehouse_size = "X-Small"

my_wh_ref.create_or_alter(my_wh) # Use the WarehouseResource perform create_or_alter
```
