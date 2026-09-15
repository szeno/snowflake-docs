# DESCRIBE AVAILABLE LISTING

Describes the columns in the listings that are available to the user who runs the command. For more information on available listings, see [Listing availability options](https://other-docs.snowflake.com/collaboration/collaboration-listings-about#label-listing-availability).

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [CREATE APPLICATION](/sql-reference/sql/create-application), [ALTER LISTING](/sql-reference/sql/alter-listing),
    [SHOW LISTINGS](/sql-reference/sql/show-listings), [DROP LISTING](/sql-reference/sql/drop-listing)

## Syntax

Copy code

```
{ DESC | DESCRIBE } AVAILABLE LISTING <listing_global_name>
```

## Parameters

`listing_global_name`
:   The global listing name to describe.

## Output

The command output provides listing properties and metadata in the following columns:

|  |  |
| --- | --- |
| Column | Description |
| `global_name` | Global name of the listing |
| `updated_on` | Date and time the listing was last updated. |
| `first_published_on` | Date and time the listing was first published. |
| `last_published_on` | Date and time the listing was last published. |
| `created_on` | Date and time the listing was created. |
| `title` | Title specified in the listing manifest |
| `subtitle` | Sub title specified in the listing manifest |
| `description` | Listing description. |
| `state` | State of the listing, one of:   - DRAFT - PUBLISHED - UNPUBLISHED |
| `profile` | Provider profile name as specified in the listing manifest. |
| `regions` | The listing regions. |
| `is_monetized` | `true` if the listing is monetized; `false` otherwise. |
| `is_targeted` | `true` if the listing is targeted; `false` otherwise. |
| `is_by_request` | `true` if the listing is by request; `false` otherwise. |
| `is_limited_trial` | `true` if the listing is a limited trial; `false` otherwise. |
| `is_ready_for_import` | `true` If the listing is available in the local region and does not require replication; `false` otherwise. |
| `is_imported` | `true` If the listing was previously imported into the caller’s account; `false` otherwise. |
| `is_application` | `true` If the listing is based on an application; `false` otherwise. |
| `application_data` | Associated application data, such as version or patch, where present. |
| `evaluation_plan` | Associated evaluation plan details, where present. Typically associated with trial listings. |
| `business_needs` | The business needs the listing satisfies. |
| `usage_examples` | Examples provided with the listing. |
| `categories` | The listing categories. |
| `data_attributes` | Data attributes of the listing. |
| `listing_terms` | The listing terms. |
| `resources` | The listing resources. |
| `data_dictionary_url` | Metadata about the data dictionary featured objects. |
| `data_preview_url` | URL of the data preview, if present. |
| `retired_on` | Date and time the listing was retired. Null if not retired. |
| `scheduled_drop_time` | Date and time the listing is scheduled to be dropped. Null if not scheduled. |
| `trial_details` | Details about the trial, if present. |
| `distribution` | Distribution details, if present. |
| `uniform_listing_locator` | The uniform listing locator. For more information about ULLs, see [Configure organizational listings](/user-guide/collaboration/listings/organizational/org-listing-configure). |
| `organization_profile_name` | The associated organization profile name. |
| `is_mountless_queryable` | `true` If the listing can be queried without being mounted; `false` otherwise. |
| `discover_only` | `true` If the listing is discoverable only; `false` otherwise. |
| `approver_contact` | The contact information for the approver, if present. |
| `support_contact` | The contact information for the support, if present. |
| `compliance_badges` | The compliance badges associated with the listing. |
| `request_approval_type` | Displays the organization listing access request type. The access request type defines how discovery targets of a listing submit access requests to the listing approver. Any one of:  - `NULL` - `REQUEST_AND_APPROVE_IN_SNOWFLAKE` indicates access requests are submitted and approved within the Snowflake environment. - `REQUEST_AND_APPROVE_OUTSIDE_SNOWFLAKE` indicates the provider manages access request submissions and approvals independently. The value for external listings is always `NULL`. |

Expand

Show lessSee more

## Examples

Describe the columns in the listing named `MYLISTING`:

Copy code

```
DESC AVAILABLE LISTING MYLISTING;
```

```
+---------------------+------------------------------+-------------------------------+------------------------------+-------------------------------+------------------------+----------+-------------+-----------+-----------+---------+--------------+-------------+---------------+------------------+---------------------+--------------+----------------+------------------+-----------------+---------------------+----------------+------------+-----------------+----------------------+-----------+---------------------+------------------+------------+---------------------+---------------+-------------------+-----------------------+
| global_name         | updated_on                   | first_published_on            | last_published_on            | created_on                    | title                  | subtitle | description | state     | profile   | regions | is_monetized | is_targeted | is_by_request | is_limited_trial | is_ready_for_import | is_imported  | is_application | application_data | evaluation_plan | business_needs      | usage_examples | categories | data_attributes | listing_terms        | resources | data_dictionary_url | data_preview_url | retired_on | scheduled_drop_time | trial_details | compliance_badges | request_approval_type |
+---------------------+------------------------------+-------------------------------+------------------------------+-------------------------------+------------------------+----------+-------------+-----------+-----------+---------+--------------+-------------+---------------+------------------+---------------------+--------------+----------------+------------------+-----------------+---------------------+----------------+------------+-----------------+----------------------+-----------+---------------------+------------------+------------+---------------------+---------------+-------------------+-----------------------+
| GZDZKY6O            |2023-11-15 13:13:54.840 -0800 | 2023-11-15 13:15:05.751 -0800 | 2023-11-15 13:15:05.751 -0800| 2023-11-15 13:12:48.988 -0800 | public-listing-test-v2 |          | test        | PUBLISHED | GZDZKY57  | ALL     | false        | false       | false.        | false            | false               | false        | true           | "{...}"          | NULL            |  [ {"type":'...' }] | NULL           | HEALTH     |   {...}         |  {"type":"STANDARD"} |  {...}    | NULL                | NULL             | NULL       | NULL                | NULL          | NULL              |  NULL                 |
+---------------------+------------------------------+-------------------------------+------------------------------+-------------------------------+------------------------+----------+-------------+-----------+-----------+---------+--------------+-------------+---------------+------------------+---------------------+--------------+----------------+------------------+-----------------+---------------------+----------------+------------+-----------------+----------------------+-----------+---------------------+------------------+------------+---------------------+---------------+-------------------+-----------------------+
```
