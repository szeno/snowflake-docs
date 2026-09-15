# CREATE LISTING

Create a free listing to share directly with specific consumers, with an inline YAML manifest, or from a file located in a stage location.

See also:
:   [ALTER LISTING](/sql-reference/sql/alter-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [SHOW LISTINGS](/sql-reference/sql/show-listings), [SHOW VERSIONS IN LISTING](/sql-reference/sql/show-versions-in-listing), [DROP LISTING](/sql-reference/sql/drop-listing), [Listing manifest reference](/progaccess/listing-manifest-reference)

## Syntax

Copy code

```
CREATE EXTERNAL LISTING [ IF NOT EXISTS ] <name>
  [ { SHARE <share_name>  |  APPLICATION PACKAGE <package_name> } ]
  AS '<yaml_manifest_string>'
  [ PUBLISH = { TRUE | FALSE } ]
  [ REVIEW = { TRUE | FALSE } ]
  [ COMMENT = '<string>' ]

CREATE EXTERNAL LISTING [ IF NOT EXISTS ] <name>
  [ { SHARE <share_name>  |  APPLICATION PACKAGE <package_name> } ]
  FROM '<yaml_manifest_stage_location>'
  [ PUBLISH = { TRUE | FALSE } ]
  [ REVIEW = { TRUE | FALSE } ]
```

## Parameters

`name`
:   Specifies the listing identifier (name). It must conform to the following:

    - Must be unique within an organization, regardless of which Snowflake Region the account is located in.
    - Must start with an alphabetic character and cannot contain spaces or special characters except for
      underscores (`_`).

`SHARE share_name`
:   Specifies the identifier for the share to attach to the listing.

`APPLICATION PACKAGE package_name`
:   Specifies the application package attached to the listing.

    See also [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages).

`AS 'yaml_manifest_string'`
:   Specifies the YAML manifest for the listing. For manifest parameters, see [Listing manifest reference](/progaccess/listing-manifest-reference).

    Manifests are normally provided as dollar quoted strings.
    For more information, see [Dollar-quoted string constants](/sql-reference/data-types-text#label-dollar-quoted-string-constants).

`FROM 'yaml_manifest_stage_location'`
:   Specifies the path for the internal stage or Git repository clone manifest.yml file.

`PUBLISH = { TRUE | FALSE }`
:   Specifies how the listing should be published.

    If TRUE, listing is published immediately on listing to Marketplace Ops for review.

    Default: TRUE.

`REVIEW = { TRUE | FALSE }`
:   Specifies whether the listing should or should not submitted to Marketplace Ops review.

    Default: TRUE.

Different combinations of values for the PUBLISH and REVIEW properties result in the following behaviors:

| PUBLISH | REVIEW | Behavior |
| --- | --- | --- |
| TRUE | TRUE | Request review then immediately publish after approval. |
| TRUE | FALSE | Results in an error. You cannot publish a listing on the Snowflake Marketplace without review. |
| FALSE | TRUE | Request a review without publishing automatically after review. |
| FALSE | FALSE | Save your listing as a draft without requesting review or publishing. |

Expand

Show lessSee more

`COMMENT = 'string_literal'`
:   A comment for the listing.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE LISTING | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| Delegated privileges to configure cross-cloud auto-fulfillment. | If the ALTER command is modifying the manifest content for auto-fulfillment. | See [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Listings created using CREATE LISTING … are automatically published. For information about unpublish and publish operations, see [ALTER LISTING](/sql-reference/sql/alter-listing).

## Examples

Creates a listing named ‘MYLISTING’ with a specific YAML format manifest, and submits it for review and subsequent publication.

For additional examples and use-cases associated with managing listings using SQL, see [Manage listings with SQL as a provider - examples](/progaccess/listing-progaccess-examples).

Note

This example uses the default values for PUBLISH and REVIEW.

Copy code

```
CREATE EXTERNAL LISTING MYLISTING
SHARE MySHARE AS
$$
title: "MyListing"
subtitle: "Subtitle for MyListing"
description: "Description for MyListing"
listing_terms:
   type: "STANDARD"
targets:
    accounts: ["Org1.Account1"]
usage_examples:
    - title: "this is a test sql"
      description: "Simple example"
      query: "select *"
$$
;
```

Creates a draft listing named ‘MYLISTING’ with a specific YAML format manifest:

Copy code

```
CREATE EXTERNAL LISTING MYLISTING
SHARE MySHARE AS
$$
title: "MyListing"
subtitle: "Subtitle for MyListing"
description: "Description for MyListing"
listing_terms:
  type: "OFFLINE"
targets:
   regions: ["PUBLIC.AWS_US_EAST_1", "PUBLIC.AZURE_WESTUS2"]
usage_examples:
   - title: "this is a test sql"
     description: "Simple example"
     query: "select *"
$$ PUBLISH=FALSE REVIEW=FALSE;
```

Creates a draft listing named ‘MYLISTING’ from a specific stage location. In the following example, the `manifest.yml` file is located in the `listingmanifests` folder in the stage named `listingstage`.

Copy code

```
CREATE EXTERNAL LISTING MYLISTING
SHARE MySHARE FROM '@dbforstage.public.listingstage/listingmanifests';
```
