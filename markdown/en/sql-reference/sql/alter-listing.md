# ALTER LISTING

Modifies the properties of a [listings](/collaboration/collaboration-listings-about) with an inline YAML manifest, or from a file located in a stage location.

Note

We recommend running [DESCRIBE LISTING](/sql-reference/sql/desc-listing) to view the current properties of a listing before running `ALTER LISTING`.

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [SHOW LISTINGS](/sql-reference/sql/show-listings), [SHOW VERSIONS IN LISTING](/sql-reference/sql/show-versions-in-listing), [DROP LISTING](/sql-reference/sql/drop-listing)

## Syntax

Copy code

```
ALTER LISTING [ IF EXISTS ] <name> [ { PUBLISH | UNPUBLISH | REVIEW } ]

ALTER LISTING [ IF EXISTS ] <name> AS '<yaml_manifest_string>'
  [ PUBLISH = { TRUE | FALSE } ]
  [ REVIEW = { TRUE | FALSE } ]
  [ COMMENT = '<string>' ]

ALTER LISTING <name> ADD VERSION [ [ IF NOT EXISTS ] <version_name> ]
  FROM <yaml_manifest_stage_location>
  [ COMMENT = '<string>' ]

ALTER LISTING [ IF EXISTS ] <name> { ADD | REMOVE } TARGETS <manifest>

ALTER LISTING [ IF EXISTS ] <name> RENAME TO <new_name>;

ALTER LISTING [ IF EXISTS ] <name> SET COMMENT = '<string>'
```

## Parameters

`name`
:   Specifies the identifier (name) for the listing being altered.

`{ PUBLISH | UNPUBLISH | REVIEW }`
:   The action to perform on the listing:

    - `PUBLISH` Makes a previously undiscoverable listing discoverable.

      Specifying PUBLISH on a previously published listing has no effect.
    - `UNPUBLISH` Makes a previously discoverable listing undiscoverable for new consumers.
      Existing consumers can continue to access the data associated with an unpublished listing.

      Specifying UNPUBLISH on a previously unpublished listing has no effect.

    See also [Unpublish a listing](/collaboration/provider-listings-modifying#label-unpublish-listing).

    - `REVIEW` Submits the listing for review.

`yaml_manifest_string`
:   The YAML manifest for the listing. For manifest parameters, see [Listing manifest reference](/progaccess/listing-manifest-reference).

    Manifests are normally provided as dollar quoted strings.
    For more information, see [Dollar-quoted string constants](/sql-reference/data-types-text#label-dollar-quoted-string-constants).

`ADD VERSION version_name`
:   Specifies the unique version identifier for the version being added.
    If the identifier contains spaces, special characters, or mixed-case characters, the entire identifier must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case sensitive. For information about identifier syntax,
    see [Identifier Requirements](/sql-reference/identifiers-syntax).

`FROM 'yaml_manifest_stage_location'`
:   Specifies the path for the internal or Snowflake [Git repository clone](/developer-guide/git/git-overview) manifest.yml file. If the changes require Marketplace Ops review, use the REVIEW and PUBLISH operations.

`{ ADD | REMOVE } TARGETS manifest`
:   Add targets to or remove targets from a listing using the manifest containing *only* the targets you want to add or remove. This partial manifest reuses the familiar structures *targets*, *external\_targets*, and *organization\_targets*, which are already defined in the listing manifest specification.

    > The table below lists unsupported listing-manifest / incoming-manifest combinations:

    Note

    V2 listings are still in preview. Upon feature enablement, all subsequent listings, whether public or private, will be created as v2 listings.

    | External listing targets version | Incoming manifest | Result | Workaround |
    | --- | --- | --- | --- |
    | V1 targets | V2 external targets | Returns an error. | Provide a version 1 incoming manifest. |
    | V2 targets | V1 targets | Returns an error. | Provide a version 2 incoming manifest. |
    | Any external listing | Organization-level target that specifies an organization without accounts. | Returns an error. | Organization-level targets aren’t supported at this time. |

    Expand

    Show lessSee more

    For organizational listings, the table below lists unsupported use cases for adding and removing targets:

    | External listing | Incoming manifest | Add or remove | Result | Action |
    | --- | --- | --- | --- | --- |
    | Any organization listing | Manifest has the `organization_user_group` field set. | Both | Returns an error. | Remove the `organization_user_group` field and try again. |
    | Account or account and role | Manifest has the `all_internal_accounts` field set to `TRUE`. | Remove | Returns an error. | Remove specific accounts and try again. |
    | The listing has the `all_internal_accounts` field set to `TRUE`. | The incoming manifest includes an account or an account and role. | Remove | Returns an errors. | Replace `all_internal_accounts` with specific accounts and try again. |
    | Account has no roles specified | Incoming manifest has an account with roles. | Remove | Returns an error. | Remove the account first and then add specific roles. |

    Expand

    Show lessSee more

`RENAME TO new_name`
:   Changes the name of the listing to `new_name`. Listing names must be unique. The new identifier cannot be used if the identifier is already in use for a different listing.

`SET ...`

> Specifies one (or more) properties to set for the listing (separated by blank spaces, commas, or new lines).
>
> `COMMENT = 'string_literal'`
> :   Adds a comment or overwrites the existing comment for an existing listing.

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

## Usage notes

- Listings can be renamed only in DRAFT state.
- When setting the live version of the YAML format manifest for a listing, you must use *COMMIT* to apply the changes, or *ABORT* to discard the changes.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MODIFY | On the listing being modified. |  |

Expand

Show lessSee more

If you’re using the ALTER command to modify the manifest content for auto-fulfillment,
you must use a role with the delegated privileges necessary to configure cross-cloud auto-fulfillment.
See [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges).

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Alters the listing `mylisting` to use an updated manifest file:

> Copy code
>
> ```
> ALTER LISTING mylisting
> AS
> $$
> title: "MyListing"
> subtitle: "Subtitle for MyListing"
> description: "Description or MyListing"
> listing_terms:
>   type: "STANDARD"
> targets:
>   accounts: ["Org1.Account1"]
> usage_examples:
>   - title: "this is a test sql"
>     description: "Simple example"
>     query: "select *"
> $$;
> ```

Submits the `mylisting` listing for review:

> Copy code
>
> ```
> ALTER LISTING mylisting REVIEW;
> ```

Alters the `mylisting` listing by publishing it:

> Copy code
>
> ```
> ALTER LISTING mylisting PUBLISH;
> ```

Alters the `mylisting` listing by unpublishing it:

> Copy code
>
> ```
> ALTER LISTING mylisting UNPUBLISH;
> ```

Alters the `mylisting` listing by setting a new comment:

> Copy code
>
> ```
> ALTER LISTING mylisting SET COMMENT = 'My listing is ready!';
> ```

Adds a new version from the specified YAML manifest file stage location:

> Copy code
>
> ```
> ALTER LISTING mylisting ADD VERSION V3 FROM @dbforstage.public.listingstage/listingmanifests;
> ```

Alters a listing so that targets will take the incoming manifest and merge it with the existing listing targets:

> Copy code
>
> ```
> ALTER LISTING mylisting ADD TARGETS $$manifest$$;
> ```

Adds targets to an external V1 listing:

> Copy code
>
> ```
> ALTER LISTING mylisting ADD TARGETS
> $$
> targets:
>   accounts: ["Org1.Account1", "Org2.Account2"]
> $$;
> ```

Adds targets to an external V2 listing:

> Copy code
>
> ```
> ALTER LISTING mylisting ADD TARGETS
> $$
> external_targets:
>   access:
>     - organization: OrgName2
>       accounts: [acc1, acc2]
> $$;
> ```

When adding targets, this takes the incoming manifest and merges it with the existing `organization_targets`.

> Copy code
>
> ```
> ALTER LISTING mylisting ADD TARGETS
> $$
> organization_targets:
>   access:
>     - account: account2
>       roles: [role1, role2]
> $$;
> ```

Removes a target:

> Copy code
>
> ```
> ALTER LISTING mylisting REMOVE TARGETS $$manifest$$;
> ```

Removes targets from an external V1 listing:

> Copy code
>
> ```
> ALTER LISTING mylisting REMOVE TARGETS
> $$
> targets:
>   accounts: ["Org1.Account1", "Org2.Account2"]
> $$;
> ```

Removes targets from an external V2 listing:

> Copy code
>
> ```
> ALTER LISTING mylisting REMOVE TARGETS
> $$
> external_targets:
>   access:
>     - organization: OrgName2
>       accounts: [acc1, acc2]
> $$;
> ```

Removes targets from an organizational listing:

> Copy code
>
> ```
> ALTER LISTING mylisting REMOVE TARGETS
> $$
> organization_targets:
>   access:
>     - account: account1
> $$;
> ```
