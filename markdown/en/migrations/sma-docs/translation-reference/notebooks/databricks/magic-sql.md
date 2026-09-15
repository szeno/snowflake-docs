# SQL magic cell transformation

This document describes how the Snowpark Migration Accelerator (SMA) handles the transformation of SQL magic cells during notebook migration.

## Magic SQL cell transformation

When the SMA processes a notebook and detects a magic cell that begins with `%sql`, it automatically transforms the cell into a standard Jupyter notebook (`.ipynb`) cell with the appropriate SQL metadata configuration.

### How it works

In Databricks notebooks, SQL code is commonly written using magic commands:

Copy code

```
%sql
SELECT * FROM my_table
WHERE status = 'active'
```

During migration, the SMA recognizes this pattern and converts it into a native notebook cell with the cell metadata set to `"sql"`. This ensures that the following occurs:

- The SQL code is properly recognized and executed as SQL in the target environment.
- Syntax highlighting is correctly applied for SQL.
- The notebook maintains its intended execution behavior.

### Before migration (Databricks)

A cell with the `%sql` magic command in the notebook JSON structure:

Copy code

```
{
  "cell_type": "code",
  "source": [
    "%sql\n",
    "SELECT COUNT(*) FROM customers"
  ],
  "metadata": {},
  "outputs": []
}
```

### After migration (Snowflake)

The same content is converted to a notebook cell with the language metadata set to `sql`, as shown in the following example. Note that the `%sql` magic command is removed from the source, and the cell metadata now includes `"language": "sql"` to indicate the cell should be executed as SQL.

Copy code

```
{
  "cell_type": "code",
  "source": [
    "SELECT COUNT(*) FROM customers"
  ],
  "metadata": {
    "language": "sql"
  },
  "outputs": []
}
```

### Benefits

- **Native SQL support**: The migrated notebook uses native SQL cell types instead of magic commands.
- **Better tooling integration**: SQL cells are recognized by IDEs and notebook environments for enhanced features like auto-completion and validation.
- **Cleaner code**: Removal of magic command prefixes results in cleaner, more portable SQL code.
