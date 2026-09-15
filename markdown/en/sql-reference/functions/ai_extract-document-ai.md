Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_EXTRACT (Document AI legacy models)

Decommissioned Feature

Document AI and the `model_build_name!PREDICT` method are decommissioned. For more information, see [Document AI decommission](/release-notes/bcr-bundles/un-bundled/bcr-2156).

Extracts information from a file using a legacy Document AI model.

## Syntax

Copy code

```
AI_EXTRACT ( model => <model> ,
            file => <file> )
```

## Arguments

`model => model`
:   Specifies the Document AI Arctic-TILT model for extraction stored in the Snowflake Model Registry; for example, `my_db.my_schema.my_model`.

`file => file`
:   A [FILE](/sql-reference/data-types-unstructured#label-data-types-file) for extraction.

## Returns

### Entity extraction

```
{
  "error": null,
  "response": {
    "invoice_items": [
      "NEW CRUSHED VELVET DIVAN BED",
      "Vintage Radiator",
      "Solid Wooden Worktop",
      "Sienna Crushed Velvet Curtains"
    ],
    "invoice_number": "123/20",
    "tax_amount": "77.57",
    "total_amount": "465.43 GBP",
    "vendor_name": "UK Exports & Imports Ltd"
  }
}
```

### Table extraction

```
{
  "error": null,
  "response": {
    "table1": {
      "gross": ["10", "31", "10"],
      "item": ["apples", "banana", "pear"],
      "net": ["9", "30", "10"],
      "tax": ["1", "1", ""]
    },
    "table2": {
      "name": ["John", "Ana", "Lisa"],
      "surname": ["Smith", "Nixon", "Gonzales"]
    }
  }
}
```

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
For information about granting this privilege, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

Additionally, you must have the OWNERSHIP privilege on the model.

## Usage notes

- The model must be in the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).
- The Document AI model should not have more than 100 entities.
- If not set explicitly, the latest available model version is used by default (the version set when the model was published or
  trained in the Document AI UI). To set the default version of a model, use the [ALTER MODEL](/sql-reference/sql/alter-model) command
  as shown in the following example:

  Copy code

  ```
  ALTER MODEL my_model SET DEFAULT_VERSION = new_version;
  ```
- Confidence scores are not supported.
- AI\_EXTRACT uses token-based billing. For more information on the AI\_EXTRACT cost for Document AI legacy models, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

  - Entity extraction cost is labeled as `arctic-tilt-entity`.
  - Table extraction cost is labeled as `arctic-tilt-table`.

## Regional availability

The following regions are available:

- AWS Canada (Central)
- AWS EU (Frankfurt)
- AWS EU (Ireland)
- AWS US East (N. Virginia)
- AWS US East (Ohio)
- AWS US West (Oregon)
- Azure Australia East (New South Wales)
- Azure East US 2 (Virginia)
- Azure Southeast Asia (Singapore)
- Azure West Europe (Netherlands)
- Azure West US 2 (Washington)

If your region is not listed, use [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference).

## Examples

The following example extracts the features defined in the Document AI model:

Copy code

```
SELECT AI_EXTRACT(
  model => 'my_db.my_schema.my_model',
  file => TO_FILE('@files_db.files_schema.files', 'agreement.pdf')
);
```

The following example extracts information from all files in a directory on a stage:

Copy code

```
SELECT AI_EXTRACT(
  model => 'my_db.my_schema.my_model',
  file => TO_FILE('@db.schema.files', relative_path)
) FROM DIRECTORY (@db.schema.files);
```

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
