# Databricks to Snowflake notebook transformation

This document describes the transformation process from Databricks notebooks to Snowflake notebooks (vNext).

The transformation tool converts Databricks notebooks (`.py` format with `# COMMAND ----------` markers) to Snowflake notebooks (`.ipynb` format), adapting Databricks-specific APIs to functional equivalents in Snowflake.

---

## Input and output files

### Input

| File | Description |
| --- | --- |
| `input/dbx_with_dbutis_run.py` | Databricks notebook with `dbutils` commands |

Expand

Show lessSee more

### Output

| File | Description |
| --- | --- |
| `output/Output/dbx_with_dbutis_run.ipynb` | Transformed notebook for Snowflake |

Expand

Show lessSee more

---

## Transformation example

### Input file: `dbx_with_dbutis_run.py`

Copy code

```
# Databricks notebook source
dbutils.notebook.help("run")

# COMMAND ----------

dbutils.notebook.run("./my_second_notebook", timeout_seconds=1000)

# COMMAND ----------

print(myVar)

# COMMAND ----------

# MAGIC %r
# MAGIC names <- c("Product A", "Product B", "Product C", "Product D")
# MAGIC sales <- c(120, 450, 300, 780)
# MAGIC df <- data.frame(names, sales)
# MAGIC df$total_with_tax <- df$sales * 1.15
# MAGIC print(df)
# MAGIC barplot(df$sales, names.arg=df$names, col="steelblue", main="Sales Overview")
```

### Output file: `dbx_with_dbutis_run.ipynb`

The transformed notebook contains the following cells:

#### Cell 0 - Connection configuration

Copy code

```
-- To configure the connection in vNext notebook, uncomment the following code and update the values accordingly.
--     use role <ROLE>;
--     use database <DATABASE>;
--     USE SCHEMA <SCHEMA>;
--     USE WAREHOUSE <WAREHOUSE>;
```

#### Cell 1 - Utility imports

Copy code

```
import sfutils
from snowflake.snowpark.session import Session

spark = Session.getActiveSession() or Session.builder.configs(connection_parameter).getOrCreate()
```

#### Cell 2 - dbutils help (unchanged)

Copy code

```
dbutils.notebook.help("run")
```

#### Cell 3 - Notebook execution (transformed)

Copy code

```
sfutils.notebook.run("./my_second_notebook", timeout_seconds = 1000)
```

#### Cell 4 - Python code (unchanged)

Copy code

```
print(myVar)
```

#### Cell 5 - R code (with warning)

SPRKDBX1003 R cells code are not supported in Snowsight. You must rewrite the R code in Python.

For more information, see EWI codes in this topic.

Copy code

```
names <- c("Product A", "Product B", "Product C", "Product D")
sales <- c(120, 450, 300, 780)
df <- data.frame(names, sales)
df$total_with_tax <- df$sales * 1.15
print(df)
barplot(df$sales, names.arg=df$names, col="steelblue", main="Sales Overview")
```

## Applied transformations

### 1. Addition of initialization cells

Cells are automatically added at the beginning of the notebook for:

- Snowflake connection configuration (commented for customization)
- Import of `sfutils` and Snowpark session creation

### 2. Conversion of `dbutils.notebook.run()`

| Databricks | Snowflake |
| --- | --- |
| `dbutils.notebook.run("./my_second_notebook", timeout_seconds=1000)` | `sfutils.notebook.run("./my_second_notebook", timeout_seconds = 1000)` |

Expand

Show lessSee more

### 3. Handling of unsupported language cells

Cells with `# MAGIC %r` (R) or `# MAGIC %scala` (Scala) are marked with an EWI (Early Warning Issue) comment:

Copy code

```
#EWI: SPRKDBX1003 => R cells code are not supported in Snowsight. It is necessary to rewrite the R code in Python.
```

For more information, see EWI codes in this topic.

## EWI codes (early warning issues)

During transformation, warnings may be generated for code that requires manual review:

| Code | Description |
| --- | --- |
| `SPRKDBX1003` | R cell code is not supported in Snowsight. Requires rewriting in Python |

Expand

Show lessSee more

## Important considerations

1. **Snowflake Session**: The transformed notebook automatically initializes a Snowpark session.
2. **R/Scala Cells**: Require manual migration to Python.
3. **Notebook Execution**: `dbutils.notebook.run()` is converted to `sfutils.notebook.run()`.

## Recommended workflow

1. Databricks Notebook (.py with COMMAND)
2. Transformation Tool
3. Snowflake Notebook (.ipynb)

## Complete migration example

### Before (Databricks)

Copy code

```
# Databricks notebook source

# Get widget value
env = dbutils.widgets.get("env")
print(f"Running in environment: {env}")

# COMMAND ----------

# Execute child notebook
result = dbutils.notebook.run("./process_data", timeout_seconds=3600, arguments={"env": env})

# COMMAND ----------

# Read file
content = dbutils.fs.head("/mnt/data/config.json")
print(content)
```

### After (Snowflake)

Copy code

```
# Cell 0 - Configuration
import sfutils
from snowflake.snowpark.session import Session

spark = Session.getActiveSession() or Session.builder.configs(connection_parameter).getOrCreate()
```

Copy code

```
# Cell 1 - Get widget
env = sfutils.widgets.get("env")
print(f"Running in environment: {env}")
```

Copy code

```
# Cell 2 - Execute notebook
result = sfutils.notebook.run("./process_data", timeout_seconds=3600, arguments={"env": env})
```

Copy code

```
# Cell 3 - Read file
content = sfutils.fs.head("/mnt/data/config.json")
print(content)
```
