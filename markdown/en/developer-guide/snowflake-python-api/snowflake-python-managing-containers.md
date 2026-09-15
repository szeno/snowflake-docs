# Managing Snowpark Container Services (including service functions) with Python

Feature — Generally Available

Not supported in government regions.

You can use Python to manage Snowpark Container Services, a fully managed container service through which you can deploy, manage,
and scale containerized applications. For an overview of Snowpark Container Services,
see [About Snowpark Container Services](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-what-is).

With the Snowflake Python APIs, you can manage compute pools, image repositories, and services.

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

## Managing compute pools

You can manage compute pools, which are collections of virtual machine (VM) nodes on which Snowflake runs your Snowpark Container Services
jobs and services.

The Snowflake Python APIs represents compute pools with two separate types:

- `ComputePool`: Exposes a compute pool’s properties, such as its warehouse, maximum and minimum nodes, and auto resume and auto
  suspend settings.
- `ComputePoolResource`: Exposes methods for performing actions on compute pools, such as fetching a corresponding
  `ComputePool` object and suspending, resuming, and stopping pools.

For more information about compute pools, see [Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool).

### Creating a compute pool

You can create a compute pool by calling the `ComputePoolCollection.create` method, passing a `ComputePool` object
that represents the compute pool you want to create.

To create a compute pool, first create a `ComputePool` object that specifies pool properties such as the following:

- Compute pool name
- Maximum and minimum number of nodes that the pool will contain
- Name of the instance family that identifies the type of machine to provision for nodes in the pool
- Whether the pool should automatically resume when a service or job is submitted to it

Code in the following example creates a `ComputePool` object that represents a pool named `my_compute_pool`:

Copy code

```
from snowflake.core.compute_pool import ComputePool

compute_pool = ComputePool(name="my_compute_pool", min_nodes=1, max_nodes=2, instance_family="CPU_X64_XS", auto_resume=False)
root.compute_pools.create(compute_pool)
```

The code then creates the compute pool by passing the `ComputePool` object to the `ComputePoolCollection.create` method.

### Getting compute pool details

You can get information about a compute pool by calling the `ComputePoolResource.fetch` method, which returns a `ComputePool`
object.

Code in the following example gets information about a pool named `my_compute_pool`:

Copy code

```
compute_pool = root.compute_pools["my_compute_pool"].fetch()
print(compute_pool.to_dict())
```

### Creating or altering a compute pool

You can set properties of a `ComputePool` object and pass it to the `ComputePoolResource.create_or_alter` method to create a
compute pool if it doesn’t exist, or alter it according to the compute pool definition if it does exist. The behavior of
`create_or_alter` is intended to be idempotent, which means that the resulting compute pool object will be the same regardless of
whether the compute pool exists before you call the method.

Note

The `create_or_alter` method uses default values for any [ComputePool](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.compute_pool.ComputePool)
properties that you don’t explicitly define. For example, if you don’t set `auto_resume`, its value defaults to `None` even if
the compute pool previously existed with a different value.

Code in the following example updates the maximum allowed nodes of the `my_compute_pool` compute pool, and then alters the compute pool
on Snowflake:

Copy code

```
compute_pool = root.compute_pools["my_compute_pool"].fetch()
compute_pool.max_nodes = 3
compute_pool_res = root.compute_pools["my_compute_pool"].create_or_alter(compute_pool)
```

### Listing compute pools

You can list compute pools using the `iter` method, which returns a `PagedIter` iterator.

Code in the following example lists compute pools whose name begins with `my`:

Copy code

```
compute_pools = root.compute_pools.iter(like="my%")
for compute_pool in compute_pools:
  print(compute_pool.name)
```

### Performing compute pool operations

You can perform common compute pool operations—such as suspending, resuming, and stopping pools—with a `ComputePoolResource`
object, which you can get by using the `ComputePool.fetch` method.

Code in the following example suspends, resumes, and stops the `my_compute_pool` compute pool:

Copy code

```
compute_pool_res = root.compute_pools["my_compute_pool"]
compute_pool_res.suspend()
compute_pool_res.resume()
compute_pool_res.stop_all_services()
```

## Managing image repositories

You can manage image repositories, which store images for applications you run on container services.

An image repository is a schema-level object. When you create or reference a repository, you do so in the context of its schema.

The Snowflake Python APIs represents image repositories with two separate types:

- `ImageRepository`: Exposes an image repository’s properties, such as its database and schema names, repository URL, and owner.
- `ImageRepositoryResource`: Exposes methods you can use to fetch a corresponding `ImageRepository` object and to drop
  the image repository resource.

For more information about image repositories, see [Snowpark Container Services: Working with an image registry and repository](/developer-guide/snowpark-container-services/working-with-registry-repository).

### Creating an image repository

To create an image repository, first create an `ImageRepository` object that specifies the repository name.

Code in the following example creates an `ImageRepository` object that represents a repository named `my_repo`:

Copy code

```
from snowflake.core.image_repository import ImageRepository

my_repo = ImageRepository("my_repo")
root.databases["my_db"].schemas["my_schema"].image_repositories.create(my_repo)
```

The code then creates the image repository by passing the `ImageRepository` object to the `ImageRepositoryCollection.create`
method, creating the image repository in the `my_db` database and `my_schema` schema.

### Getting image repository details

You can get information about an image repository by calling the `ImageRepositoryResource.fetch` method, which returns an
`ImageRepository` object.

Code in the following example gets an `ImageRepository` object representing the `my_repo` image repository and then prints the
name of the repository’s owner:

Copy code

```
my_repo_res = root.databases["my_db"].schemas["my_schema"].image_repositories["my_repo"]
my_repo = my_repo_res.fetch()
print(my_repo.owner)
```

### Listing image repositories

You can list the image repositories in a specified schema using the `iter` method, which returns a `PagedIter` iterator
of `ImageRepository` objects.

Code in the following example lists repository names in the `my_db` database and `my_schema` schema:

Copy code

```
repo_list = root.databases["my_db"].schemas["my_schema"].image_repositories.iter()
for repo_obj in repo_list:
  print(repo_obj.name)
```

### Dropping an image repository

You can drop an image repository using the `ImageRepositoryResource.drop` method.

Code in the following example drops the `my_repo` repository:

Copy code

```
my_repo_res = root.databases["my_db"].schemas["my_schema"].image_repositories["my_repo"]
my_repo_res.drop()
```

## Managing services and service functions

You can manage services, which run application containers until you stop them. Snowflake restarts a service automatically if the service
container stops. In this way, the service effectively runs uninterrupted.

A service is a schema-level object. When you create or reference a service, you do so in the context of its schema.

The Snowflake Python APIs represents services with two separate types:

- `Service`: Exposes a service’s properties such as its specification, minimum and maximum instances, and database and schema name.
- `ServiceResource`: Exposes methods you can use to fetch a corresponding `Service` object, suspend and resume
  the service, and get its status.

For more information about services, see [Snowpark Container Services: Working with services](/developer-guide/snowpark-container-services/working-with-services).

### Creating a service

To create a service, you run the `services.create` method, passing a `Service` object representing the service you want to
create.

You create a service from a service specification `.yaml` file that has been uploaded to a stage. For more information about creating a
service specification, see [Service specification reference](/developer-guide/snowpark-container-services/specification-reference).

#### Uploading the specification

If you’re creating a service from a specification that hasn’t yet been uploaded to a stage, you can upload the specification using a
Snowpark [FileOperation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.FileOperation)
object.

Code in the following example uses the `FileOperation.put` method to upload a specification as a file:

Copy code

```
session.file.put("/local_location/my_service_spec.yaml", "@my_stage")
```

Code in the following example uses the `FileOperation.put_stream` method to upload a specification as a string:

Copy code

```
service_spec_string = """
// Specification as a string.
"""
session.file.put_stream(StringIO(sepc_in_string), "@my_stage/my_service_spec.yaml")
```

#### Creating the service

To create a service from a staged specification, first create a `Service` object that specifies service properties such as the
following:

- Service name
- Maximum and minimum number of service instances that Snowflake can create
- Compute pool to which the service should be added
- Stage location and name of the specification

Code in the following example creates a `Service` object representing a service named `my_service` from a specification in
`@my_stage/my_service_spec.yaml`:

Copy code

```
from snowflake.core.service import Service, ServiceSpec

my_service = Service(name="my_service", min_instances=1, max_instances=2, compute_pool="my_compute_pool", spec=ServiceSpec("@my_stage/my_service_spec.yaml"))
root.databases["my_db"].schemas["my_schema"].services.create(my_service)
```

The code then creates the service by passing the `Service` object to the `ServiceCollection.create` method, creating the service
in the `my_db` database and `my_schema` schema.

You can also create a service from a specification that you provide as inline text, as shown in the following example.
The `ServiceSpec` function takes a single string argument `spec`. If the string starts with `@`, the function interprets and
validates it as a stage file path. Otherwise the string is passed through as inline text.

Copy code

```
from textwrap import dedent
from snowflake.core.service import Service, ServiceSpec

spec_text = dedent(f"""\
    spec:
      containers:
      - name: hello-world
        image: repo/hello-world:latest
      endpoints:
      - name: hello-world-endpoint
        port: 8080
        public: true
    """)

my_service = Service(name="my_service", min_instances=1, max_instances=2, compute_pool="my_compute_pool", spec=ServiceSpec(spec_text))
root.databases["my_db"].schemas["my_schema"].services.create(my_service)
```

#### Creating a service function

After the service is up and running, you can create a service function that communicates with the service endpoint. A service function is a
user-defined function (UDF) that you create and associate with a service in Snowpark Container Services. For more information, see
[Service functions: Using a service from an SQL query](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function).

Code in the following example creates a UDF named `my-udf` that specifies the `hello-world` service and `hello-world-endpoint`
endpoint that you previously defined:

Copy code

```
from snowflake.core import CreateMode
from snowflake.core.function import FunctionArgument, ServiceFunction

root.databases["my_db"].schemas["my_schema"].functions.create(
  ServiceFunction(
    name="my-udf",
    arguments=[
        FunctionArgument(name="input", datatype="TEXT")
    ],
    returns="TEXT",
    service="hello-world",
    endpoint="'hello-world-endpoint'",
    path="/hello-world-path",
    max_batch_rows=5,
  ),
  mode = CreateMode.or_replace
)
```

#### Invoking a service function

After the service function is created, you can then invoke the function to test it.

Code in the following example invokes the `my-udf` service function that you previously created:

Copy code

```
result = root.databases["my_db"].schemas["my_schema"].functions["my-udf(TEXT)"].execute_function(["test"])
print(result)
```

### Getting service details

You can get information about a Snowflake service by calling the `ServiceResource.fetch` method, which returns a `Service`
object.

Code in the following example gets information about a service named `my_service`:

Copy code

```
my_service = root.databases["my_db"].schemas["my_schema"].services["my_service"].fetch()
```

### Listing services

You can list the services in a specified schema using the `iter` method, which returns a `PagedIter` iterator of
`Service` objects.

Code in the following example lists services whose name begins with `my`:

Copy code

```
services = root.databases["my_db"].schemas["my_schema"].services.iter(like="my%")
for service_obj in services:
  print(service_obj.name)
```

### Performing service operations

You can perform common service operations—such as suspending, resuming, and getting the service’s containers—with a `ServiceResource`
object.

Code in the following example suspends and resumes the `my_service` service and also gets the status of the containers corresponding
to the service:

Copy code

```
my_service_res = root.databases["my_db"].schemas["my_schema"].services["my_service"]

my_service_res.suspend()
my_service_res.resume()
container_statuses = [container.status for container in my_service_res.get_containers()]
```
