# CREATE PROVISIONED THROUGHPUT

Creates a new [Provisioned Throughput resource](/user-guide/snowflake-cortex/provisioned-throughput) or replaces an existing one.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] PROVISIONED THROUGHPUT <name>
    CLOUD_PROVIDER = '<cloud_provider>'
    MODEL = '<model_name>'
    PTUS = <num_ptus>
    TERM_START = '<start_date>'
    TERM_END = '<end_date>';
```

## Required parameters

`name`
:   String that specifies the identifier (i.e., name) for the provisioned throughput resource; must be unique for the schema in which the resource is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CLOUD_PROVIDER = 'cloud_provider'`
:   Specifies the cloud provider where the provisioned throughput will be allocated. Supported values are *aws* and *azure*.

`MODEL = 'model_name'`
:   Specifies the model for which the provisioned throughput is being reserved. Supported models include:

    - Mistral Large 2
    - Llama 3.1-405B
    - Llama 3.1-70B
    - Llama 3.1-8B
    - Snowflake-Llama3.3-70B
    - Snowflake-Llama3.3-405B

`PTUS = num_ptus`
:   Specifies the number of provisioned throughput units (PTUs) to allocate. The value must meet the minimum and incremental PTU requirements for the specified model.

`TERM_START = 'start_date'`
:   Specifies the start date of the provisioned throughput term in the format *YYYY-MM-DD*.

`TERM_END = 'end_date'`
:   Specifies the end date of the provisioned throughput term in the format *YYYY-MM-DD*.

## Access Control Requirements

| Privilege | Object |
| --- | --- |
| CREATE PROVISIONED THROUGHPUT | Account level. |
| USAGE | Schema in which you plan to create the provisioned throughput. |

Expand

Show lessSee more

Attention

To create a Provisioned Throughput resource, your role must have the CREATE PROVISIONED THROUGHPUT privilege at the account level.

## Usage Notes

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- Provisioned Throughput is subject to minimum and incremental PTU requirements. Ensure that your PTU request meets these requirements for the specified model.
- The term for provisioned throughput starts and ends at 8:00 a.m. PT on the specified dates.
- Provisioned Throughput does not renew automatically. To reserve throughput for another term, create a new provisioned throughput resource.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Example

Create a provisioned throughput resource named `my_pt` for the *Llama 3.1-8B* model on AWS, allocating 64 PTUs for a term from April 15, 2025, to May 15, 2025:

Copy code

```
CREATE PROVISIONED THROUGHPUT my_pt
    CLOUD_PROVIDER = 'aws'
    MODEL = 'llama3.1-8B'
    PTUS = 64
    TERM_START = '2025-04-15'
    TERM_END = '2025-05-15';
```

Replace an existing provisioned throughput resource named `my_pt` with updated PTUs and term dates:

Copy code

```
CREATE OR REPLACE PROVISIONED THROUGHPUT my_pt
    CLOUD_PROVIDER = 'aws'
    MODEL = 'llama3.1-8B'
    PTUS = 128
    TERM_START = '2025-06-01'
    TERM_END = '2025-07-01';
```
