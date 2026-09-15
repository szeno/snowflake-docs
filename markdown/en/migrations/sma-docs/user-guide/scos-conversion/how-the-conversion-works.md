description:
:   What is converted? How?

# Snowpark Migration Accelerator: How the Conversion Works

The Snowpark Migration Accelerator (SMA) not only generates a comprehensive assessment of your code but can also convert specific elements from your source code into compatible formats for your target codebase. This conversion process follows the same steps as the initial assessment, with just one additional step.

## Conversion in the SMA

In both assessment and conversion modes, the Snowpark Migration Accelerator (SMA):

- Searches through all files within a specified directory
- Detects which files contain code
- Analyzes the code files according to their programming language
- Creates a structured representation of the code (Abstract Syntax Tree or AST)
- Creates and fills a Symbol Table with program information
- Identifies and classifies any errors found
- Creates detailed reports of the results

All of these processes are repeated when you run SMA in conversion mode, even if you previously ran it in assessment mode. However, conversion mode includes one additional final step.

- Format the generated code from the Abstract Syntax Tree (AST) to improve readability

The Abstract Syntax Tree (AST) is a model that represents how your source code works. When the same functionality exists in both the source and target languages, SMA can generate equivalent code in the target language. This code generation only happens during the actual conversion process.

## Types of Conversion in the SMA

The Snowpark Migration Accelerator (SMA) currently supports the following code conversions:

- Converts Python or Scala code from Spark API calls to equivalent Snowpark Connect calls

Note

The SMA does not perform any SQL conversion. For SQL files or SQL-only assessments, the tool provides assessment only, without any automated conversion.

Let’s examine an example written in both Scala and Python programming languages.

## Examples of Conversion of References to the Spark API to the Snowpark Connect

### Example of Spark Scala to Snowpark

When using Scala as your source language, the Snowpark Migration Accelerator (SMA) automatically converts Spark API references in your Scala code to their equivalent Snowpark Connect references. Below is an example that demonstrates how a basic Spark application is converted. The example application performs several common data operations:

- Reading data
- Filtering records
- Joining datasets
- Calculating averages
- Displaying results

Apache Spark Code Written in Scala

Copy code

```
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession

object SimpleApp {
  // This function calculates the average salary for jobs in a specific department
  def avgJobSalary(session: SparkSession, dept: String) {
    // Load employee data from CSV file
    val employees = session.read.csv("path/data/employees.csv")
    // Load job data from CSV file
    val jobs = session.read.csv("path/data/jobs.csv")

val jobsAvgSalary = employees
    .filter(column("Department") === dept)    // Filter employees by department
    .join(jobs)                              // Join with jobs table
    .groupBy("JobName")                      // Group results by job name
    .avg("Salary")                          // Calculate average salary for each job

// Calculate and display a list of all salaries in the department
jobsAvgSalary.select(collect_list("Salary")).show()

```scala
// Calculate and display the average salary
jobsAvgSalary.show()
}
```

The Code After Conversion to Snowflake:

Copy code

```
import com.snowflake.snowpark._
import com.snowflake.snowpark.functions._
import com.snowflake.snowpark.Session

object SimpleApp {
  // This function calculates the average salary for jobs in a specific department
  def avgJobSalary(session: Session, dept: String) {
    // Load employee data from CSV file
    val employees = session.read.csv("path/data/employees.csv")
    // Load job data from CSV file
    val jobs = session.read.csv("path/data/jobs.csv")

val jobsAvgSalary = employees
    .filter(column("Department") === dept)    // Filter employees by department
    .join(jobs)                              // Join with jobs table
    .groupBy("JobName")                      // Group results by job name
    .avg("Salary")                           // Calculate average salary per job

```scala
// Calculate and display all salaries in the department
jobsAvgSalary.select(array_agg("Salary")).show()

// Display the average salary
jobsAvgSalary.show()
}
}
```

In this example, the code structure remains largely unchanged. However, the code has been updated to use Snowpark Connect references instead of Spark API references.

### Example of PySpark to Snowpark Connect

When you choose Python as your source language, SMA automatically converts PySpark API calls in your Python code to their equivalent Snowpark Connect calls. Below is an example script that demonstrates various PySpark functions:

Copy code

```
from datetime import date, datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Row

Create a Spark session by building and initializing a new SparkSession object, or retrieve an existing one if already available.

df = spark_session.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])

# cube()
df.cube("name", df.age).count().orderBy("name", "age").show()

# take()
df_new1.take(2)

# describe()
df.describe(['age']).show()

# explain()
df.explain()
df.explain("simple") # Physical plan
df.explain(True)

# intersect()
df1 = spark_session.createDataFrame([("a", 1), ("a", 1), ("b", 3), ("c", 4)], ["C1", "C2"])
df2 = spark_session.createDataFrame([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])

# where()
df_new1.where(F.col('Id2')>30).show()
```

The Code After Conversion to Snowflake:

Copy code

```
from snowflake import snowpark_connect
from datetime import date, datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Row
conf = SparkConf()
conf.setAppName("test")

# Create a Spark session by building and initializing a new SparkSession object, or retrieve an existing one if already available.
#EWI: SPRKCNTPY3501 => The AppName method of pyspark.sql.session.SparkSession.Builder has been replaced with the SetName function to provide equivalent functionality in Snowpark Connect
#EWI: SPRKCNTPY1001 => The creation of the SparkSession has been replaced with the creation of an equivalent Snowpark Connect Session.
spark_session = snowpark_connect.server.init_spark_session(conf = conf)

df = spark_session.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])

# cube()
df.cube("name", df.age).count().orderBy("name", "age").show()

# take()
df_new1 = spark_session.createDataFrame([(1, "Alice"), (2, "Bob"), (3, "Charlie")], ["Id", "Name"])
df_new1.take(2)

# describe()
df.describe(['age']).show()

# explain()
df.explain()
df.explain("simple") # Physical plan
df.explain(True)

# intersect()
df1 = spark_session.createDataFrame([("a", 1), ("a", 1), ("b", 3), ("c", 4)], ["C1", "C2"])
df2 = spark_session.createDataFrame([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])

# where()
df_new1.where(F.col('Id2')>30).show()
```

In this example, the code structure remains largely unchanged. However, the code has been updated to use Snowpark Connect calls instead of Spark API calls.

During the conversion process with the Snowpark Migration Accelerator (SMA), you can expect the following:
