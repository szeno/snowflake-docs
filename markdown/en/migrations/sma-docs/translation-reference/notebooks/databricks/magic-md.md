# Markdown magic cell transformation

This document describes how the Snowpark Migration Accelerator (SMA) handles the transformation of Markdown magic cells during notebook migration.

## Magic Markdown cell transformation

When the SMA processes a notebook and detects a magic cell that begins with `%md`, it automatically transforms the cell into a standard Jupyter notebook (`.ipynb`) markdown cell.

### How it works

In Databricks notebooks, Markdown content is commonly written using magic commands:

Copy code

```
%md
# My Documentation
This is a **markdown** cell with formatted text.
```

During migration, the SMA recognizes this pattern and converts it into a native notebook cell with the cell metadata set to `"markdown"`. This ensures that:

- The content is properly recognized as documentation/markdown in the target environment.
- Markdown rendering is correctly applied.
- The notebook maintains its intended documentation structure.

### Before migration (Databricks)

A cell with the `%md` magic command in the notebook JSON structure:

Copy code

```
{
  "cell_type": "code",
  "source": [
    "%md\n",
    "# Customer Analysis\n",
    "This notebook performs **customer segmentation** analysis."
  ],
  "metadata": {},
  "outputs": []
}
```

### After migration (Snowflake)

The same content is converted to a notebook cell with the language metadata set to `markdown`:

Copy code

```
{
  "cell_type": "code",
  "source": [
    "# Customer Analysis\n",
    "This notebook performs **customer segmentation** analysis."
  ],
  "metadata": {
    "language": "markdown"
  },
  "outputs": []
}
```

Note that the `%md` magic command is removed from the source, and the cell metadata now includes `"language": "markdown"` to indicate the cell contains documentation content.

### Benefits

- **Native markdown support**: The migrated notebook uses native markdown cell types instead of magic commands.
- **Better rendering**: Markdown cells are properly rendered in notebook environments without requiring code execution.
- **Cleaner structure**: Removal of magic command prefixes results in cleaner, more portable documentation cells.
