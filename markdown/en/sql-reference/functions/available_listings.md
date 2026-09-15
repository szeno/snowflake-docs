Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# AVAILABLE\_LISTINGS

Returns all listings that are available for the consumer to discover and access.

## Syntax

Copy code

```
AVAILABLE_LISTINGS(
      [ IS_IMPORTED => { TRUE | FALSE | NULL } ]
      [ , IS_ORGANIZATION => { TRUE | FALSE | NULL } ]
      [ , IS_SHARED_WITH_ME => { TRUE | FALSE | NULL } ] )
```

## Arguments

You can optionally specify the following arguments to filter listings in this view.

Note

Only one of the arguments can be `TRUE` at a time.

`IS_IMPORTED => { TRUE | FALSE | NULL }`
:   Set to `TRUE` to return only imported listings; set to `FALSE` or `NULL` to return all listings.

    Default: `NULL`.

`IS_ORGANIZATION => { TRUE | FALSE | NULL }`
:   Set to `TRUE` to return only organization listings; set to `FALSE` or `NULL` to return all listings.

    Default: `NULL`.

`IS_SHARED_WITH_ME => { TRUE | FALSE | NULL }`
:   Set to `TRUE` to return only listings that have been shared privately with the current account; set to `FALSE` or `NULL` to return all listings.

    Default: `NULL`.

## Output

The function returns the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| GLOBAL\_NAME | VARCHAR | The global name of the listing. |
| CREATED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was created. |
| TITLE | VARCHAR | The title of the listing. |
| SUBTITLE | VARCHAR | The subtitle of the listing. |
| DESCRIPTION | VARCHAR | The description of the listing. |
| IS\_MONETIZED | BOOLEAN | Indicates whether the listing is monetized. |
| IS\_BY\_REQUEST | BOOLEAN | Indicates whether the listing is by request (personalized listing). |
| IS\_LIMITED\_TRIAL | BOOLEAN | Indicates whether the listing is limited trial. |
| IS\_READY\_FOR\_IMPORT | BOOLEAN | Indicates whether the listing is ready for import. |
| IS\_IMPORTED | BOOLEAN | Indicates whether the listing has been imported. |
| IS\_APPLICATION | BOOLEAN | Indicates whether the listing is associated with an application. |
| IS\_PRIVATE | BOOLEAN | Indicates whether the listing is private. |
| CATEGORIES | VARCHAR | Categories associated with the listing. |
| DATA\_ATTRIBUTES | VARCHAR | Data attributes associated with the listing. |
| TERMS | VARCHAR | Terms of service for the listing. |
| RESOURCES | VARCHAR | Resources associated with the listing. |
| DISTRIBUTION | VARCHAR | The distribution of the listing. Possible values are `EXTERNAL` and `ORGANIZATION`. |
| UNIFORM\_LISTING\_LOCATOR | VARCHAR | The uniform listing locator (ULL) of the listing. |
| ORGANIZATION\_PROFILE\_NAME | VARCHAR | The organization profile attached to the listing, if any. |
| IS\_DISCOVERY\_ONLY | BOOLEAN | Indicates whether the listing is discovery only. |
| SUPPORT\_CONTACT | VARCHAR | The support contact information associated with the listing. |
| REQUEST\_APPROVAL\_TYPE | VARCHAR | The request approval type of the listing. Incidates whether the consumer listing requests will be approved within or outside of Snowflake. |
| IS\_CORTEX\_KNOWLEDGE\_EXTENSION | BOOLEAN | Indicates whether this listing has Cortex Search services attached. |
| PROVIDER\_COMPANY\_NAME | VARCHAR | The company name of the listing provider. |
| RESHARING | VARCHAR | Resharing configuration of the listing. |

Expand

Show lessSee more

## Examples

Retrieve all available listings in the current account:

Copy code

```
SELECT * FROM TABLE(<any_database>.INFORMATION_SCHEMA.AVAILABLE_LISTINGS());
```

Retrieve all available listings that have been imported by the current account:

Copy code

```
SELECT * FROM TABLE(<any_database>.INFORMATION_SCHEMA.AVAILABLE_LISTINGS(IS_IMPORTED => TRUE));
```

Retrieve all available organization listings in the current account:

Copy code

```
SELECT * FROM TABLE(<any_database>.INFORMATION_SCHEMA.AVAILABLE_LISTINGS(IS_ORGANIZATION => TRUE));
```

Retrieve all available listings that have been shared privately with the current account:

Copy code

```
SELECT * FROM TABLE(<any_database>.INFORMATION_SCHEMA.AVAILABLE_LISTINGS(IS_SHARED_WITH_ME => TRUE));
```
