# Processing Databricks files

This document describes how the Snowpark Migration Accelerator (SMA) processes Databricks files based on their file extensions during the inventory and migration phases.

## File processing by extension

The SMA recognizes and processes various Databricks file formats. Each file type is handled according to its structure and origin.

### SQL files

| Extension | Format | Description |
| --- | --- | --- |
| .sql | JSON cells | Inventoried by the SMA. Typically extracted from a `.dbc` file. |
| .sql | First-line-comment | Databricks notebook exported to SQL format. Inventoried by the SMA. |

Expand

Show lessSee more

#### Example: SQL with JSON cells format

Copy code

```
{
  "version": "NotebookV1",
  "commands": [
    {
      "command": "CREATE TABLE customers (\n  id INT,\n  name STRING\n)",
      "commandType": "sql"
    },
    {
      "command": "SELECT * FROM customers",
      "commandType": "sql"
    }
  ]
}
```

#### Example: SQL with first-line-comment format

Copy code

```
-- Databricks notebook source
CREATE TABLE customers (
  id INT,
  name STRING
)

-- COMMAND ----------

SELECT * FROM customers
```

### Python files

| Extension | Format | Description |
| --- | --- | --- |
| .python | JSON cells | Inventoried by the SMA. Typically extracted from a `.dbc` file. |
| .py | First-line-comment | Databricks notebook exported to Python format. Inventoried by the SMA. |

Expand

Show lessSee more

#### Example: Python with JSON cells format

Copy code

```
{
  "version": "NotebookV1",
  "commands": [
    {
      "command": "df = spark.read.table(\"customers\")",
      "commandType": "python"
    },
    {
      "command": "df.filter(df.status == \"active\").show()",
      "commandType": "python"
    }
  ]
}
```

#### Example: Python with first-line-comment format (.py)

Copy code

```
# Databricks notebook source
df = spark.read.table("customers")

# COMMAND ----------

df.filter(df.status == "active").show()
```

### Scala files

| Extension | Format | Description |
| --- | --- | --- |
| .scala | JSON cells | Inventoried by the SMA. Typically extracted from a `.dbc` file. |
| .scala | First-line-comment | Databricks notebook exported to Scala format. Inventoried by the SMA. |

Expand

Show lessSee more

#### Example: Scala with JSON cells format

Copy code

```
{
  "version": "NotebookV1",
  "commands": [
    {
      "command": "val df = spark.read.table(\"customers\")",
      "commandType": "scala"
    },
    {
      "command": "df.filter($\"status\" === \"active\").show()",
      "commandType": "scala"
    }
  ]
}
```

#### Example: Scala with first-line-comment format

Copy code

```
// Databricks notebook source
val df = spark.read.table("customers")

// COMMAND ----------

df.filter($"status" === "active").show()
```

### Databricks archive files

| Extension | Description |
| --- | --- |
| .dbc | Databricks compressed archive file. The SMA extracts and analyzes its contents. |

Expand

Show lessSee more

#### Example: DBC file structure

A `.dbc` file is a ZIP archive containing notebook files. When extracted, the structure looks like the following:

```
my_project.dbc (extracted)
|-- notebook1.python
|-- notebook2.sql
|-- folder/
|   |-- notebook3.python
|   |-- notebook4.scala
|-- utils/
    |-- helpers.python
```

## How it works

- **DBC Files**: When the SMA encounters a `.dbc` file, it automatically extracts the compressed contents and processes each file individually based on its extension.
- **JSON Cells Format**: Files with JSON cell structure are native Databricks notebook formats, typically found inside `.dbc` archives. These contain cell definitions with metadata, source code, and outputs.
- **First-Line-Comment Format**: Files exported from Databricks using the export functionality contain a special comment in the first line that identifies them as Databricks notebooks. The SMA recognizes this pattern and processes them accordingly.

## Inventory process

During the inventory phase, the SMA:

1. Scans all provided files and directories.
2. Identifies file types based on extension and internal structure.
3. Catalogs each notebook with its language, cell count, and dependencies.
4. Prepares the files for the translation phase.
