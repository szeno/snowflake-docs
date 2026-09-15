# CREATE ORGANIZATION LISTING

Create an organization listing to share data products securely within your organization.

## Syntax

Copy code

```
CREATE ORGANIZATION LISTING [ IF NOT EXISTS ] <name>
  [ { SHARE <share_name>  |  APPLICATION PACKAGE <package_name> } ]
  AS '<yaml_manifest_string>'
  [ PUBLISH = { TRUE | FALSE } ]

CREATE ORGANIZATION LISTING [ IF NOT EXISTS ] <name>
  [ { SHARE <share_name>  |  APPLICATION PACKAGE <package_name> } ]
  FROM '<yaml_manifest_stage_location>'
  [ PUBLISH = { TRUE | FALSE } ]
```

## Parameters

`name`
:   Specifies the identifier (name) for the listing. It must conform to the following:

    - Must be unique within an account, regardless of which Snowflake Region the account is located in. The Uniform Listing Locator (ULL) must be unique within an organization.
    - Cannot contain embedded dollar signs.
    - Must conform to Snowflake identifier requirements. See [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM 'yaml_manifest_stage_location'`
:   Specifies the path for the internal stage or Git repository clone manifest.yml file.

`SHARE share_name`
:   Specifies the identifier for the share to attach to the listing.

`APPLICATION PACKAGE package_name`
:   Specifies the application package attached to the listing.

    See also [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages).

`AS 'yaml_manifest_string'`
:   The YAML manifest for the organization profile. For manifest field details and examples,
    see [Organization listing manifest reference](/user-guide/collaboration/listings/organizational/org-listing-manifest-reference).

    Manifests are normally provided as dollar-quoted strings. For more information, see
    [Dollar-quoted string constants](/sql-reference/data-types-text#label-dollar-quoted-string-constants).

`PUBLISH = { TRUE | FALSE }`
:   Specifies how to publish the listing.

    If TRUE, the listing is published to the Internal Marketplace immediately.

    Default: TRUE.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ORGANIZATION LISTING or CREATE LISTING | Account | To create and alter organization listings. |

Expand

Show lessSee more

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ORGANIZATION LISTING | ACCOUNT | To attach the specified share or the specified Snowflake Native App Framework to a listing. When specifying a Snowflake Native App Framework, OWNERSHIP or ATTACH LISTING are also required. |
| IMPORT ORGANIZATION LISTING | ACCOUNT | To mount a listing or to execute a query that uses a Uniform Listing Locator (ULL) to reference an organizational listing. |

Expand

Show lessSee more

## Usage notes

- Listings created using CREATE ORGANIZATION LISTING … are automatically published.

## Examples

This example creates a listing named MYORGLISTING using the settings specified in the manifest YAML. It targets one role in one account in one region and includes support and approver contacts.

Note

`support_contact` is required.
`approver_contact` is required if a `discovery` target is provided.

Copy code

```
USE ROLE <organization_listing_role>;

CREATE ORGANIZATION LISTING MYORGLISTING
SHARE <share_name> AS
$$
title: "My title"
description: "One region, all accounts"
organization_profile: "INTERNAL"
organization_targets:
  discovery:
    - account: "<account_name>"
      roles:
        - "<role>"
  access:
    - account: "<account_name>"
      roles:
        - "<role>"
support_contact: "support@somedomain.com"
approver_contact: "approver@somedomain.com"
locations:
   access_regions:
   - name: "PUBLIC.<snowflake_region>"
$$
```

Creates a draft listing named ‘MYLISTING’ from a specific stage location. In the following example, the `manifest.yml` file is located in the `listingmanifests` folder in the stage named `listingstage`.

Copy code

```
CREATE ORGANIZATION LISTING MYLISTING
SHARE MySHARE FROM @dbforstage.public.listingstage/listingmanifests;
```
