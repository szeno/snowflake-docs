# User-defined functions with Snowpark Connect for Spark

Snowpark Connect for Spark lets you create and use user-defined functions (UDFs) and user-defined table functions (UDTFs) using
standard Spark APIs in Python, Java, and Scala. Your functions are executed on Snowflake’s compute engine.

This topic covers Python UDFs and UDTFs, Java UDFs, and Scala UDFs.

## Python UDFs and UDTFs

You can define scalar UDFs, user-defined table functions (UDTFs), and vectorized UDTFs in Python.
You can also register Java UDFs from a Python session and manage Python package dependencies.

### Scalar UDFs

There are two ways to use a Python UDF, depending on whether you want to call it from the DataFrame
API or from Spark SQL.

**DataFrame API usage**

Define a UDF with the `@udf` decorator from `pyspark.sql.connect.functions` and use it directly
in DataFrame column expressions:

Copy code

```
from pyspark.sql.connect.functions import udf
from pyspark.sql.types import IntegerType

@udf(returnType=IntegerType())
def add_one(x: int) -> int:
    return x + 1

df = spark.createDataFrame([(1,), (2,), (3,)], ["value"])
df.select(add_one(df["value"]).alias("result")).show()
```

**SQL usage**

To call a Python function from Spark SQL, register it with `spark.udf.register()` and give it a
SQL-callable name:

Copy code

```
from pyspark.sql.types import IntegerType

spark.udf.register("add_one_sql", lambda x: x + 1, IntegerType())
spark.sql("SELECT add_one_sql(value) FROM my_table").show()
```

Both approaches create the same underlying Snowflake function. The difference is how you invoke it:
`add_one(df["value"])` in DataFrame expressions versus `add_one_sql(value)` in SQL strings.

### User-defined table functions

Define a table function with the `@udtf` decorator, implement `eval` to yield one or more output rows per
input, then register the class with `spark.udtf.register()`. You can invoke the UDTF from Spark SQL.

Copy code

```
from pyspark.sql.functions import udtf

@udtf(returnType="val: int")
class Powers:
    def eval(self, x: int):
        for v in [x**0, x**1, x**2]:
            yield (int(v),)

spark.udtf.register(name="powers", f=Powers)
spark.sql("SELECT * FROM powers(10)").show()
```

#### UDTF lifecycle: `__init__`, eval, and terminate

A UDTF class supports three lifecycle methods:

- `__init__`: Called once per partition before any rows. Use it to initialize accumulators or load resources.
- `eval`: Called once per input row. Yields zero or more output rows.
- `terminate`: Called after all rows in the partition. Yields final summary rows.

Copy code

```
@udtf(returnType="metric: string, value: double")
class StatsCollector:
    def __init__(self):
        self.values = []

    def eval(self, x: float):
        self.values.append(x)
        yield ("input", float(x))

    def terminate(self):
        import statistics
        if self.values:
            yield ("mean", statistics.mean(self.values))
            yield ("stdev", statistics.pstdev(self.values))
            yield ("count", float(len(self.values)))

spark.udtf.register("compute_stats", StatsCollector)
spark.sql("SELECT compute_stats(1)").show()
```

For Spark-compatible coercion and null handling on UDTFs, you can set `snowpark.connect.udtf.compatibility_mode` to `true`.
See [Snowpark Connect for Spark properties](/developer-guide/snowpark-connect/snowpark-connect-parameters).

### Vectorized UDTFs and Arrow transforms

By default, Python UDTFs serialize and deserialize data row by row. For workloads that process large amounts of data,
you can leverage Apache Arrow-based or Pandas-based vectorized functions to improve throughput. Under the hood,
Snowpark Connect for Spark implements these as Snowflake
[vectorized UDTFs](/developer-guide/udf/python/udf-python-tabular-vectorized).

#### Using mapInArrow for vectorized transforms

You can use `mapInArrow` to apply a function that processes entire Arrow record batches rather than individual
rows. This approach is well suited for numerical transforms, feature engineering, and other columnar operations:

Copy code

```
import pyarrow as pa

def double_values(iterator):
    for batch in iterator:
        result = pa.RecordBatch.from_pydict(
            {"id": [x * 2 for x in batch.column("id").to_pylist()]}
        )
        yield result

df = spark.range(10).toDF("id")
df.mapInArrow(double_values, "id long").show()
```

#### Using applyInPandas for grouped transforms

For grouped operations, `applyInPandas` applies a pandas function to each group of a grouped DataFrame:

Copy code

```
import pandas as pd

def normalize_group(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf["value"] = (pdf["value"] - pdf["value"].mean()) / pdf["value"].std()
    return pdf

df = spark.createDataFrame([
    ("a", 1.0), ("a", 2.0), ("a", 3.0),
    ("b", 10.0), ("b", 20.0), ("b", 30.0),
], ["group_id", "value"])

df.groupby("group_id").applyInPandas(
    normalize_group, schema="group_id string, value double"
).show()
```

### Packages and artifact repositories

Use `snowpark.connect.udf.packages` to list extra Python packages (from Snowflake’s package channel or your configured [artifact repository](#label-snowpark-connect-udfs-artifact-repo)) that your UDF or UDTF needs.
The value is a bracketed, comma-separated list, for example `[numpy,scipy]`.

Copy code

```
from pyspark.sql.types import DoubleType

spark.conf.set("snowpark.connect.udf.packages", "[numpy]")

@udf(returnType=DoubleType())
def compute(x: float) -> float:
    import numpy as np

    return float(np.sqrt(x))
```

This configuration only resolves packages from Snowflake’s curated Anaconda channel. If a package isn’t
available there, you’ll see `ModuleNotFoundError` at UDF execution time even though the package is installed
in your local environment. To check whether a package is available, run:

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE PACKAGE_NAME LIKE '%<package_name>%';
```

For packages not on Anaconda, use an [artifact repository](#label-snowpark-connect-udfs-artifact-repo) or
upload the package manually with `spark.addArtifacts("<package>.zip", pyfile=True)`. When you upload
manually, you must also list the package’s own dependencies in `snowpark.connect.udf.packages`.

For details on packages and `PACKAGES`, see [Python](/sql-reference/sql/create-function#label-create-function-python-packages).

#### Using custom packages with addArtifacts

When a package isn’t available in the Anaconda channel or your artifact repository, you can upload it directly from
your local machine using `spark.addArtifacts`. This is useful for private packages or packages from PyPI that
aren’t curated by Snowflake.

The following example uploads the `pykalman` package from a local `.whl` file:

Copy code

```
# 1. Download the .whl file from PyPI (outside your script).
# 2. Rename .whl to .zip (Snowpark Connect doesn't accept .whl files directly).
# 3. Upload the package and declare its Anaconda-available dependencies.

spark.addArtifacts("/path/to/pykalman-0.11.1.zip", pyfile=True)
spark.conf.set("snowpark.connect.udf.packages", "[numpy,scipy,skbase,packaging]")

@udf(returnType=DoubleType())
def kalman_predict(measurement: float) -> float:
    from pykalman import KalmanFilter

    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
    return float(kf.em([[measurement]]).filter([[measurement]])[0][0][0])
```

Note

When you upload a package with `addArtifacts`, you must also list its transitive dependencies
in `snowpark.connect.udf.packages` if those dependencies are available on Anaconda. The uploaded
package itself doesn’t carry its dependency metadata into Snowflake.

Verify that the ZIP archive has the package directory at its root (for example, `pykalman/` directly
inside the archive, not nested under another directory).

#### Using locally created libraries

If you have a custom Python module in your project, you can upload it with `addArtifacts` so UDFs can
import it:

Copy code

```
# Upload a local Python file as a pyfile dependency
spark.addArtifacts("/path/to/my_project/transforms.py", pyfile=True)

@udf(returnType=StringType())
def apply_transform(value: str) -> str:
    from transforms import normalize

    return normalize(value)
```

For multi-file packages, zip the directory and upload the archive:

Copy code

```
# my_package/
#   __init__.py
#   helpers.py

spark.addArtifacts("/path/to/my_package.zip", pyfile=True)

@udf(returnType=IntegerType())
def compute(x: int) -> int:
    from my_package.helpers import double

    return double(x)
```

#### Using an artifact repository

By default, Snowflake resolves Python packages from the curated Anaconda channel.
To use packages that are not available there (for example from PyPI via a Snowflake [artifact repository](/developer-guide/udf/python/udf-python-packages)), set `snowpark.connect.artifact_repository` to the repository name, then set `snowpark.connect.udf.packages` as usual.

The following end-to-end example sets up an artifact repository, configures Snowpark Connect for Spark to use it, and creates a UDF
that depends on a package available only through PyPI:

Copy code

```
-- Create an artifact repository that mirrors PyPI (run once in Snowflake)
CREATE GIT REPOSITORY IF NOT EXISTS my_pypi_repo
  ORIGIN = 'https://pypi.org/simple/'
  API_INTEGRATION = pypi_access_integration;
```

Copy code

```
# Configure the session to use the artifact repository
spark.conf.set("snowpark.connect.artifact_repository", "my_pypi_repo")

# List the packages your UDF needs (resolved from PyPI through the repository)
spark.conf.set("snowpark.connect.udf.packages", "[pykalman,numpy,scipy]")

@udf(returnType=DoubleType())
def kalman_smooth(measurement: float) -> float:
    from pykalman import KalmanFilter

    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
    state_means, _ = kf.em([[measurement]]).filter([[measurement]])
    return float(state_means[0][0])

df = spark.createDataFrame([(1.0,), (2.1,), (3.05,)], ["measurement"])
df.select(kalman_smooth(df["measurement"]).alias("smoothed")).show()
```

Changing the artifact repository invalidates cached UDFs and UDTFs so they are recreated on next use.

For more information about creating and managing artifact repositories, see
[Using third-party packages](/developer-guide/udf/python/udf-python-packages).

### Architecture constraints for x86-only packages

Some Python packages ship binaries only for the x86 CPU architecture.
Set `snowpark.connect.udf.resource_constraint.architecture` to `x86` so Snowpark Connect for Spark creates UDFs, UDTFs, and related operations with an x86 resource constraint.

You must run the workload on a [warehouse](/user-guide/warehouses-snowpark-optimized) that has a compatible x86 resource constraint.
If the warehouse does not match, UDF execution fails.

The following example configures the x86 constraint and creates a UDF that depends on an x86-only package:

Copy code

```
spark.conf.set("snowpark.connect.udf.resource_constraint.architecture", "x86")
spark.conf.set("snowpark.connect.udf.packages", "[tensorflow]")

@udf(returnType=DoubleType())
def predict(features: str) -> float:
    import tensorflow as tf

    model = tf.keras.models.load_model("/tmp/model")
    return float(model.predict([[float(x) for x in features.split(",")]])[0][0])
```

See [Snowpark Connect for Spark properties](/developer-guide/snowpark-connect/snowpark-connect-parameters) for more configuration details.

### Register Java UDFs from Python

Snowpark Connect for Spark lets you register Java functions for use in SQL queries from a Python session. Your Java
class must implement one of the Apache Spark UDF interfaces (`UDF1`, `UDF2`, and so on from
`org.apache.spark.sql.api.java`). For interface details, see the
[Spark Java UDF documentation](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/api/java/package-summary.html).

Java UDFs run on Snowflake’s compute engine using Java 17.

#### Registering a Java UDF from a class name

Use `spark.udf.registerJavaFunction()` to register a Java class that implements a Spark UDF interface. The
class must be available through a JAR that you provide.

Copy code

```
spark.addArtifact("/path/to/my-udf.jar")

spark.udf.registerJavaFunction("myJavaFunc", "com.example.MyFunction")
spark.sql("SELECT myJavaFunc(value) FROM my_table").show()
```

You can optionally specify a return type when the function doesn’t declare one:

Copy code

```
from pyspark.sql.types import IntegerType

spark.udf.registerJavaFunction("myJavaFunc", "com.example.MyFunction", IntegerType())
```

#### Loading JAR dependencies

Java UDFs typically depend on one or more JAR files: the JAR containing your UDF class itself, plus any third-party
libraries it uses. If your UDF calls into an external library that isn’t bundled in the same JAR, you must add that
library separately.

You can supply JAR dependencies in two ways:

**Local JARs with addArtifact**

Call `spark.addArtifact()` to upload a local JAR file to the session. This is the simplest approach when you
have the JAR on your machine:

Copy code

```
spark.addArtifact("/path/to/my-udf.jar")

# If your UDF depends on additional libraries, add those JARs too
spark.addArtifact("/path/to/dependency.jar")
```

**Staged JARs with configuration**

If your JAR is already on a Snowflake stage, use the `snowpark.connect.udf.java.imports` configuration instead
of `addArtifact`. This avoids uploading the file from your local machine on every session:

Copy code

```
spark.conf.set(
    "snowpark.connect.udf.java.imports",
    "[@my_stage/my-udf.jar, @my_stage/dependency.jar]"
)

spark.udf.registerJavaFunction("myJavaFunc", "com.example.MyFunction")
```

When you change `snowpark.connect.udf.java.imports`, all cached Java UDFs are invalidated and recreated
on next use.

## Java/Scala UDFs

Snowpark Connect for Spark supports UDFs written in Java and Scala that connect through a locally running
Snowpark Connect for Spark server. This section covers UDF registration, dependency management, and version
configuration for both languages.

### Scala UDFs

Snowpark Connect for Spark supports Scala UDFs through the Spark Connect protocol. Scala UDF closures are
serialized and wrapped in a Java handler that runs on Snowflake. You define Scala UDFs in a Scala
application that connects to a locally running Snowpark Connect for Spark server.

#### Registering a Scala UDF

There are two ways to use a Scala UDF, depending on whether you want to call it from the DataFrame
API or from Spark SQL.

**DataFrame API usage**

Create a UDF with `udf()` and use it directly in DataFrame column expressions:

Copy code

```
import com.snowflake.snowpark_connect.SnowparkConnectSession
import org.apache.spark.sql.functions.{udf, col}

val spark = SnowparkConnectSession.builder().appName("My App").getOrCreate()

val addOne = udf((x: Int) => x + 1)

val df = spark.table("my_table")
df.select(col("value"), addOne(col("value")).alias("incremented")).show()
```

**SQL usage**

To call a UDF from Spark SQL, register it with `spark.udf.register()` to give it a SQL-callable
name:

Copy code

```
import com.snowflake.snowpark_connect.SnowparkConnectSession
import org.apache.spark.sql.functions.udf

val spark = SnowparkConnectSession.builder().appName("My App").getOrCreate()

val addOne = udf((x: Int) => x + 1)
spark.udf.register("add_one", addOne)

spark.sql("SELECT add_one(value) FROM my_table").show()
```

Both approaches create the same underlying Snowflake function. The difference is how you invoke it:
`addOne(col("value"))` in DataFrame expressions versus `add_one(value)` in SQL strings.

### Java UDFs

Snowpark Connect for Spark supports Java UDFs through the Spark Connect protocol. Your Java class must implement
one of the Apache Spark UDF interfaces (`UDF1`, `UDF2`, and so on from
`org.apache.spark.sql.api.java`). Java UDFs run on Snowflake’s compute engine using Java 17.

#### Registering a Java UDF

There are two ways to use a Java UDF, depending on whether you want to call it from the DataFrame
API or from Spark SQL.

**DataFrame API usage**

Create a UDF with `udf()` and use it directly in DataFrame column expressions:

Copy code

```
import com.snowflake.snowpark_connect.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import static org.apache.spark.sql.functions.*;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.expressions.UserDefinedFunction;
import org.apache.spark.sql.types.DataTypes;

SparkSession spark = SnowparkConnectSession.builder().appName("My App").getOrCreate();

UserDefinedFunction addOne = udf(
    (UDF1<Integer, Integer>) x -> x + 1, DataTypes.IntegerType
);

Dataset<Row> df = spark.table("my_table");
df.select(col("value"), addOne.apply(col("value")).alias("incremented")).show();
```

**SQL usage**

To call a UDF from Spark SQL, register it with `spark.udf().register()` to give it a
SQL-callable name:

Copy code

```
import com.snowflake.snowpark_connect.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.types.DataTypes;

SparkSession spark = SnowparkConnectSession.builder().appName("My App").getOrCreate();

spark.udf().register("add_one", (UDF1<Integer, Integer>) x -> x + 1, DataTypes.IntegerType);

spark.sql("SELECT add_one(value) FROM my_table").show();
```

Both approaches create the same underlying Snowflake function. The difference is how you invoke it:
`addOne.apply(col("value"))` in DataFrame expressions versus `add_one(value)` in SQL strings.

#### Class discovery and artifact upload

Java and Scala UDFs run on Snowflake’s compute engine, not on your local machine. Snowpark Connect for Spark needs
to discover and upload your compiled classes to Snowflake so they can be executed server-side.
Choose one of the following approaches:

**addArtifact (recommended)**

For production workloads, package your application into an assembly JAR and upload it:

JavaScala

Copy code

```
spark.addArtifact("/path/to/my-app.jar");
```

Copy code

```
spark.addArtifact("/path/to/my-app-assembly.jar")
```

**registerClassFinder**

For interactive development, register a `REPLClassDirMonitor` that watches your compiled classes
directory and uploads changes automatically:

JavaScala

Copy code

```
import org.apache.spark.sql.connect.client.REPLClassDirMonitor;

var classFinder = new REPLClassDirMonitor(
    new File("target/test-classes").getAbsolutePath()
);
spark.registerClassFinder(classFinder);
```

Copy code

```
import org.apache.spark.sql.connect.client.REPLClassDirMonitor

val classFinder = new REPLClassDirMonitor("/absolute/path/to/target/scala-2.12/classes")
spark.registerClassFinder(classFinder)
```

#### Using structured types as UDF input and output

UDFs can accept and return structured types. In Scala, use case classes. In Java, use POJOs
(JavaBeans) that implement `Serializable` with a no-arg constructor, getters, and setters.

Snowpark Connect for Spark automatically infers the schema from the class structure. Nested types are also
supported.

JavaScala

Define POJOs (JavaBeans with a no-arg constructor, getters, and setters) and use them as UDF
return types:

Copy code

```
public static class Address implements Serializable {
    private String city;
    private String country;

    public Address() {}
    public Address(String city, String country) {
        this.city = city;
        this.country = country;
    }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
}

public static class PersonWithAddress implements Serializable {
    private String name;
    private int age;
    private Address address;

    public PersonWithAddress() {}
    public PersonWithAddress(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public Address getAddress() { return address; }
    public void setAddress(Address address) { this.address = address; }
}
```

Register and use the UDF:

Copy code

```
spark.udf().register(
    "make_person",
    (UDF1<String, PersonWithAddress>) name ->
        new PersonWithAddress(name, name.length(), new Address("NYC", "US")),
    Encoders.bean(PersonWithAddress.class).schema()
);

spark.sql("SELECT make_person('Alice')").show();
```

Define case classes and use them as UDF return types:

Copy code

```
case class Address(city: String, country: String)
case class PersonWithAddress(name: String, age: Long, address: Address)

val makePerson = udf((name: String) =>
  PersonWithAddress(name, name.length, Address("NYC", "US"))
)
spark.udf.register("make_person", makePerson)

spark.sql("SELECT make_person('Alice')").show()
```

### Dependency handling

#### External library dependencies

If your Java or Scala UDF depends on libraries that are already on a Snowflake stage, use
`snowpark.connect.udf.java.imports` to make them available at UDF runtime:

JavaScala

Copy code

```
spark.conf().set(
    "snowpark.connect.udf.java.imports",
    "[@my_stage/external-library.jar, @my_stage/other-dependency.jar]"
);
```

Copy code

```
spark.conf.set(
  "snowpark.connect.udf.java.imports",
  "[@my_stage/external-library.jar, @my_stage/other-dependency.jar]"
)
```

This pattern is useful when you want to avoid uploading large dependencies on every session. The
JAR must already exist on the stage (uploaded with PUT or another method).

#### Configuration reference

The following table lists all configuration properties that affect Java and Scala UDFs:

| Property | Default | Description |
| --- | --- | --- |
| `snowpark.connect.udf.java.imports` | (none) | Comma-separated list of staged JAR paths for Java and Scala UDF execution. Changing this setting invalidates all cached Java UDFs. Use stage paths in a bracketed list, for example `[@stage/lib.jar]`. |
| `snowpark.connect.scala.version` | `2.12` | Scala version used by the Snowpark runtime. Supported values: `2.12`, `2.13`. |

Expand

Show lessSee more

### Scala version

The default Scala version is 2.12. Workloads built with Scala 2.13 must specify the Scala version.

Copy code

```
spark.conf.set("snowpark.connect.scala.version", "2.13")
```

## Working with staged files

You can attach staged files and archives to the UDF execution environment so that your function code can reference
them at runtime. Snowpark Connect for Spark provides language-specific configuration properties for this purpose:

- **Python**: Use `snowpark.connect.udf.python.imports` to list staged files used in Python UDFs.
- **Java and Scala**: Use `snowpark.connect.udf.java.imports` to list staged files used in Java/Scala UDFs.

Provide stage paths in a bracketed list. Files must already exist on a stage your session can read.

Copy code

```
from pyspark.sql.types import StringType

spark.conf.set("snowpark.connect.udf.python.imports", "[@stage/library.py, @other_lib.zip]")

@udf(returnType=StringType())
def import_example(input: str) -> str:
    from library import first_function

    return first_function(input)
```

Snowflake unpacks dependencies into the UDF working directory without preserving original directory paths.
If a module relies on a specific path layout, zip the package and add the zip as an import, or use
`spark.addArtifacts` with `pyfile=True` for Python dependencies.
When uploading a ZIP, verify that the package directory sits at the root of the archive
(`<archive>/package_name/`, not `<archive>/some_other_dir/package_name/`). An incorrect layout causes
`ModuleNotFoundError` even though the upload succeeds.

Important

The `snowpark.connect.udf.python.imports` and `snowpark.connect.udf.java.imports` settings are
independent. Changing one doesn’t affect the other. The deprecated `snowpark.connect.udf.imports` is
Python-only and doesn’t make JARs available to Java or Scala UDFs.

### Reading data files inside a UDF

You can stage data files and list them in `snowpark.connect.udf.python.imports` or `snowpark.connect.udf.java.imports`
the same way as libraries.
Open them for read-only use inside the UDF.
Avoid writing to these files: changes do not persist after the function finishes.

PythonJavaScala

Copy code

```
from pyspark.sql.types import StringType

spark.conf.set("snowpark.connect.udf.python.imports", "[@stage/data.csv]")

@udf(returnType=StringType())
def read_staged_data(file_name: str) -> str:
    with open(file_name) as f:
        return f.read()
```

For general patterns for importing code from stages, see [Creating a Python UDF with code uploaded from a stage](/developer-guide/udf/python/udf-python-creating#label-udf-python-stage).

Copy code

```
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.types.DataTypes;
import java.nio.file.Files;
import java.nio.file.Paths;

spark.conf().set("snowpark.connect.udf.java.imports", "[@stage/data.csv]");

spark.udf().register("read_staged_data",
    (UDF1<String, String>) fileName -> {
        return new String(Files.readAllBytes(Paths.get(fileName)));
    },
    DataTypes.StringType);

spark.sql("SELECT read_staged_data('data.csv')").show();
```

Copy code

```
import org.apache.spark.sql.functions.udf
import scala.io.Source

spark.conf.set("snowpark.connect.udf.java.imports", "[@stage/data.csv]")

val readStagedData = udf((fileName: String) => {
  val source = Source.fromFile(fileName)
  try source.mkString finally source.close()
})

spark.table("my_table")
  .select(readStagedData(lit("data.csv")).alias("contents"))
  .show()
```

## Best practices

Understanding how Snowpark Connect for Spark manages UDF lifecycle helps you optimize query performance and avoid
unnecessary overhead.

### UDF caching and recreation

Snowpark Connect for Spark caches compiled UDFs in the server-side session. When you call the same UDF in successive queries, the
cached version is reused, which avoids the overhead of registering it again on Snowflake.

Cached UDFs are invalidated and recreated when any of the following changes occur:

- `snowpark.connect.udf.python.imports` or `snowpark.connect.udf.java.imports` is updated.
- `snowpark.connect.artifact_repository` is changed.
- New files are uploaded with `spark.addArtifacts()` (unless the uploaded file is a cache-only artifact).

UDF recreation involves re-registering the function on Snowflake with a new CREATE FUNCTION call. For large UDFs or
those with many dependencies, this can add several seconds of overhead. To minimize recreation:

- Set all configuration properties (`snowpark.connect.udf.packages`,
  `snowpark.connect.udf.python.imports`, `snowpark.connect.artifact_repository`) once before
  defining your UDFs, rather than changing them between queries.
- Use `spark.addArtifacts` for dependencies that change infrequently, and `snowpark.connect.udf.packages`
  for dependencies that remain stable.

### Performance tips

#### Prefer SQL and DataFrame operations over Python UDFs

Every UDF that Snowpark Connect for Spark registers on Snowflake involves a CREATE FUNCTION call and runs in a Python sandbox on
the warehouse. If SQL or DataFrame operations can express the same logic, they execute natively on the Snowflake
engine without that overhead.

#### Minimize data going into UDFs

Push filters and projections before applying UDFs in your DataFrame pipeline. The fewer rows and columns the UDF
processes, the less data Snowflake serializes to the Python sandbox.

Copy code

```
# Avoid: UDF processes all rows, then filter
df.select("id", my_udf("col1", "col2", "col3", "col4", "col5").alias("result")) \
  .filter(col("id") < 100)

# Better: filter first, select only needed columns
df.filter(col("id") < 100) \
  .select("id", my_udf("col1").alias("result"))
```

#### Manage packages carefully

When configuring `snowpark.connect.udf.packages`, keep the following in mind:

- Minimize package count: each additional package increases cold-start environment resolution time on the warehouse.
- Pin versions (for example, `spark.conf.set("snowpark.connect.udf.packages", "[pandas==2.0.3]")`) to avoid
  re-solving on every UDF creation.
- Use pre-installed packages: numpy, pandas, and other popular packages are pre-cached on Snowflake and start faster.
- Don’t declare packages you don’t import: the package resolver runs over all declared packages even if your UDF
  code doesn’t use them.

## Known limitations

UDFs running through Snowpark Connect for Spark behave slightly differently from standard Apache Spark UDFs in the following ways.
Understanding these differences helps avoid unexpected errors when migrating existing Spark applications.

### Lambda and closure limitations

User-defined functions (UDFs) are not supported within lambda expressions.
This includes both custom UDFs and certain built-in functions whose underlying implementation relies on Snowflake UDFs.
Attempting to use a UDF inside a lambda expression will result in an error.

Copy code

```
df = spark.createDataFrame([({"a": "U3Bhcms="},)], ("data",))
df.select(map_filter("data", lambda _, v: unbase64(v) > 3)).show() # does not work, since `unbase64` is implemented with UDF
```

## Related topics

- [Snowpark Connect for Spark properties](/developer-guide/snowpark-connect/snowpark-connect-parameters) for UDF and UDTF configuration properties
- [Using third-party packages](/developer-guide/udf/python/udf-python-packages) for artifact repositories and Python packages in Snowflake
