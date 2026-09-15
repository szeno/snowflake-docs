Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_METRIC\_FUNCTION\_EXPECTATIONS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view lists the [expectations](/user-guide/data-quality-expectations) in an account. It lists the expectations that
were added to an association between a data metric function (DMF) and an object.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| METRIC\_DATABASE\_NAME | VARCHAR | Database that contains the data metric function. |
| METRIC\_SCHEMA\_NAME | VARCHAR | Schema that contains the data metric function. |
| METRIC\_NAME | VARCHAR | Name of the data metric function. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the metric arguments. |
| DATA\_TYPE | VARCHAR | Return data type of the data metric function. |
| REF\_DATABASE\_NAME | VARCHAR | Database that contains the object that is associated with the data metric function. |
| REF\_SCHEMA\_NAME | VARCHAR | Schema that contains the object that is associated with the data metric function. |
| REF\_ENTITY\_NAME | VARCHAR | Name of the table or view that is associated with the data metric function. |
| REF\_ENTITY\_DOMAIN | VARCHAR | Type of the object (table, view) that the data metric function is associated with. |
| REF\_ARGUMENTS | ARRAY | Reference arguments used to evaluate the rule. |
| REF\_ID | VARCHAR | System-generated identifier for the association of the data metric function to the table or view. |
| EXPECTATION\_ID | VARCHAR | System-generated identifier. |
| EXPECTATION\_NAME | VARCHAR | Name that was given to the expectation when it was added to the association between the DMF and the object. |
| EXPECTATION\_EXPRESSION | VARCHAR | Boolean expression of the expectation. See [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression). |

Expand

Show lessSee more

## Usage notes

Latency for the view might be up to 30 minutes.
