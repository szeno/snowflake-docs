# DESCRIBE LISTING

Describes the columns in a [listing](/collaboration/collaboration-listings-about).

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [ALTER LISTING](/sql-reference/sql/alter-listing), [SHOW LISTINGS](/sql-reference/sql/show-listings), [SHOW VERSIONS IN LISTING](/sql-reference/sql/show-versions-in-listing), [DROP LISTING](/sql-reference/sql/drop-listing)

## Syntax

Copy code

```
{ DESC | DESCRIBE } LISTING <name>  [ REVISION = { DRAFT | PUBLISHED } ]
```

## Parameters

`name`
:   The identifier, specified when the listing was created, for the listing to describe.
    If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    See [SHOW LISTINGS](/sql-reference/sql/show-listings) for listing details, including listing **name**.

`REVISION = { DRAFT | PUBLISHED }`
:   Specifies which revision to display.

    For example, If you have a draft of a published listing, you can specify either the draft or published version to display.

    Valid values:
    :   - `DRAFT`: Describe the draft version of the listing.
        - `PUBLISHED`: Describe the published version of the listing.

        Default:
        :   `PUBLISHED`

## Usage notes

- You can describe a listing only if you use a role that has the USAGE, MODIFY, or OWNERSHIP privilege on the listing.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

The command output provides listing properties and metadata in the following columns:

|  |  |
| --- | --- |
| Column | Description |
| `global_name` | Global name of the listing |
| `name` | Name specified when the listing was created. |
| `owner` | The listing owner. |
| `owner_role_type` | The listing owner role type. |
| `created_on` | Date and time the listing was created. |
| `updated_on` | Date and time the listing was last updated. |
| `published_on` | Date and time the listing was last published. |
| `title` | Title specified in the listing manifest |
| `subtitle` | Sub title specified in the listing manifest |
| `description` | The listing description. |
| `listing_terms` | The listing terms. |
| `state` | State of the listing, one of:   - DRAFT - PUBLISHED - UNPUBLISHED |
| `share` | The share identifier for this listing. |
| `application_package` | The application package associated with the listing. |
| `business_needs` | The business needs the listing satisfies. |
| `usage_examples` | An example showing a query of the listing. |
| `data_attributes` | The listing’s attributes, including the refresh rate, geographic coverage, and time range. |
| `categories` | The listing categories. |
| `resources` | Listing resources, such as a documentation link. |
| `profile` | The provider’s profile name. |
| `customized_contact_info` | Provider contact information. |
| `data_dictionary` | Listing metadata. |
| `data_preview` | Preview of the listing data. |
| `comment` | Associated comment, if present. |
| `revisions` | Revision state, for public listings only. |
| `target_accounts` | Comma separated list of target accounts. |
| `regions` | The listing regions. |
| `refresh_schedule` | The listing refresh frequency in minutes. |
| `refresh_type` | The listing refresh type. |
| `review_state` | The listing review state. |
| `rejection_reason` | The reason the listing was rejected. |
| `unpublished_by_admin_reasons` | The reason the listing owner didn’t publish the listing. |
| `is_monetized` | Is monetized flag. |
| `is_application` | Is application flag. If `true`, an application package is attached to the listing. |
| `is_targeted` | Is targeted flag. |
| `is_limited_trial` | Is limited trial flag. |
| `is_by_request` | Is by request flag. |
| `limited_trial_plan` | The plan associated with a limited trial listing. |
| `retired_on` | Date and time the listing was retired. Null if not retired. |
| `scheduled_drop_time` | Date and time the listing is scheduled to be dropped (no longer available to existing consumers). Null if not scheduled. |
| `manifest_yaml` | The entire published manifest when `REVISION` is `PUBLISHED`, and the entire published manifest with draft changes when `REVISION` is `DRAFT`. |
| `distribution` | Distribution details, if present, such as `EXTERNAL`. |
| `is_mountless_queryable` | `true` If the listing can be queried without being mounted; `false` otherwise. |
| `organization_profile_name` | The associated organization profile name. |
| `uniform_listing_locator` | The uniform listing locator (ULL). For more information about ULLs, see [Configure organizational listings](/user-guide/collaboration/listings/organizational/org-listing-configure). |
| `trial_details` | Details associated with trial listings. |
| `approver_contact` | Approver contact information. |
| `support_contact` | Support contact information. |
| `live_version_uri` | Full uniform resource indictor (URI) of the live version of the listing, against which stage operations can be performed. NULL if no live version exists for the listing. |
| `last_committed_version_uri` | Full URI of the last committed version of the listing. |
| `last_committed_version_name` | System-generated name for the last committed version of the listing. |
| `last_committed_version_alias` | User-specified alias for the last committed version of the listing. |
| `published_version_uri` | Full URI of the current published version of the listing. |
| `published_version_name` | System-generated name of the published version of the listing. |
| `published_version_alias` | User-specified alias for the last published version of the listing. |
| `compliance_badges` | Compliance badges associated with this listing, if any. |
| `is_share` | Is share flag. If `true`, the listing was created based on a share. |
| `monetization_version` | Monetization model that the listing uses. |
| `request_approval_type` | Listing access request type. The access request type defines how discovery targets of a listing submit access requests to the listing approver. Any one of:  - `NULL` - `REQUEST_AND_APPROVE_IN_SNOWFLAKE` indicates access requests are submitted and approved within the Snowflake environment. - `REQUEST_AND_APPROVE_OUTSIDE_SNOWFLAKE` indicates the provider manages access request submissions and approvals independently. The value for external listings is always `NULL`. |
| `monetization_display_order` | The order in which pricing plans and offers are displayed to consumers. |
| `legacy_uniform_listing_locator` | Specifies the legacy Uniform Listing Locator (ULL). If an existing organizational listing profile is updated to use a custom organization profile, this column includes the ULL associated with the previous default profile that continues to be valid.  If no profile updates have been made, this column is NULL.  For more information on ULLs, see [Set the Uniform Listing Locator or listing name](/user-guide/collaboration/listings/organizational/org-listing-configure#label-olisting-im-ull). |
| `share_restrictions` | A flag that indicate whether share restrictions exist on external private listings. |

Expand

Show lessSee more

## Examples

To describe the columns in a listing named `MYLISTING`, run the following command:

Copy code

```
DESC LISTING MYLISTING;
```
