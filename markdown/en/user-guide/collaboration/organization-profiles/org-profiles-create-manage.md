# Create and manage organization profiles

Organization profiles allow providers to organize their Internal Marketplace listings by department.
For example, individual organization profiles can be created for sales, marketing, and human resources.
This allows providers to identify and brand organizational listings that are specific
to their organization’s business unit, and associate all organizational listings
created within their business unit with the same organization profile.

Organization profiles provide consumers with a reliable method to confirm that
the organizational listings they use come from trusted sources within their organization.
Organization profiles also allow consumers to filter and locate organizational
listings that are specific to their business unit or use case.

Note

Organization profiles cannot be used outside an organization’s Internal Marketplace,
and they are unique within an organizational data cloud. Organization profiles
can be created and modified programmatically or via Snowsight and then assigned to
an organizational listing.

An organization account is required to create and manage organization profiles.
To learn more about organization accounts, see [Organization accounts](/user-guide/organization-accounts).

## Organization profile format

An organization profile forms part of the Uniform Listing Locator (ULL). The
format of an organization profile is `ORGDATACLOUD${org_profile_name}${organizational_listing_name}`.
The ULL identifies the organization profile and its associated organizational listing.
The ULL can be used in programmatic queries similar to this example:

Copy code

```
SELECT * FROM "ORGDATACLOUD$<ProfileName>$<ListingName>.<SchemaName>.<TableName>;
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ORGANIZATION PROFILE | Account | Organization profiles can only be created from the organization account in an organization. The GLOBALORGADMIN role has been granted the CREATE ORGANIZATION PROFILE privilege. |

Expand

Show lessSee more

## Create an organization profile

To create an organization profile, you can use Snowsight or SQL commands.

SnowsightSQL

Create a new organization profile.

> 1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
> 2. In the navigation menu, select **Data sharing** » **Internal sharing**.
> 3. In the right pane, select the **Profiles** tab.
> 4. Select **+ Create profile**.
> 5. On the **Basic information** page, specify the following:
>
>    - **Profile title**: The title for this profile.
>
>      Specifying a title generates a ULL reference name.
>    - **ULL reference name**: (Optional) Edit the ULL reference name.
>    - **Description**: Enter a description for the profile.
> 6. Select **Next**.
> 7. On the **Access** page, specify who in the organization can use the profile to publish internal listings.
>
>    - **Entire organization**: Anyone in the organization can use the profile.
>    - **Selected accounts and roles**: Only specific accounts and roles can use the profile.
>      1. Select one or more accounts.
>
>         By default, all roles in the selected accounts can use the profile.
>      2. (Optional) To grant access to specific roles in each account, select the **All roles** drop-down, then select **Selected roles**.
>
>         - Select one or more roles in the account that can use the profile.
> 8. Select **Next**.
> 9. On the **Contact information** page, specify email addresses for the owner of the profile and for the approver of profile access requests.
> 10. Select **Next**.
> 11. On the **Appearance** page, select an icon to use as the profile avatar and select the avatar background color.
> 12. Upon completion, select one of the following options:
>
> - **Publish**: Publish the profile and make it Live on the **Profiles** page.
> - **Save as draft**: Save the profile without publishing.
> - **Cancel**: Discard the profile without saving or publishing.
> - **Previous**: Return to a prior page to make changes.

To create an organization profile use the [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile)
and execute a statement similar to:

Copy code

```
USE ROLE GLOBALORGADMIN;

CREATE ORGANIZATION PROFILE MyOrgPROFILE
AS
$$
title: "My Org Profile"
description: "An appropriate desc"
contact: "contact@test.com"
approver_contact: "approver@test.com"
allowed_publishers:
  access:
    - all_internal_accounts: true
$$ publish=True;
```

For details of organization profile manifest fields, see [Organization profile manifest reference](/user-guide/collaboration/organization-profiles/org-profile-manifest-reference).

## Assign an organization profile to a organizational listing

To assign an organization profile to a new or existing organizational listing, you can use the Snowsight or SQL commands.

SnowsightSQL

Assign an organization profile to a new listing.

> 1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
> 2. In the navigation menu, select **Data sharing** » **Internal sharing**.
> 3. Select **Create Listing**.
> 4. Select a data product such as a table, view, or other data product to add to the listing.
>
>    1. Review the generated share identifier, then select **Generate listing**.
> 5. Enter a name for your listing.
> 6. Select the **Select Profile** drop-down.
> 7. Select an organization profile in the **Profile** list.
> 8. Complete the organizational listing setup. See [Create an organizational listing](/user-guide/collaboration/listings/organizational/org-listing-create).

Assign an organization profile to an existing draft listing.

Note

You can only assign an organization profile to a listing that is in draft status.
If the organizational listing has been published, an organization profile cannot be assigned or changed.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. On the **Listings** tab, select the listing that you want to edit.
4. Select the **Select profile** drop-down, and select a profile for the listing.

> You can update an existing listing to use a different organization profile using the
> [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile) command and executing a command similar to:
>
> Note the value of the `organization_profile` field in the manifest YAML
> which specifies the organization profile associated with the listing.

Copy code

```
USE ROLE GLOBALORGADMIN;

ALTER LISTING MyLISTING
AS $$
title: "my listings title"
description: "Listing updated for new org profile"
auto_fulfillment:
   refresh_type: "SUB_DATABASE"
   refresh_schedule: "10 MINUTE"
organization_profile: "MyOrgPROFILE"
organization_targets:
access:
   - all_internal_accounts: true
locations:
access_regions:
    - name: "ALL"
$$;
```

For details of organization profile manifest fields, see [Organization profile manifest reference](/user-guide/collaboration/organization-profiles/org-profile-manifest-reference).

## Modify an existing organizational listing profile

By default, the contact support email defined in the organization profile appears on the organizational listing landing page.
You can specify a custom support email address or URL when the original email address changes.

To assign an organization profile to a new or existing organizational listing, you can use the Snowsight or SQL commands.

SnowsightSQL

To modify listing support contact email address:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. In the right pane, select the **Listings** tab.
4. Select an organizational listing in the list.
5. In the **Details** section, select **Edit** next to the support contact email address.
6. Select **Use custom email or URL** in the **Profile** list.
7. Enter an email address or a URL.
8. Select **Save**.

To alter an existing organization profile use the [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile) and execute a statement similar to:

Unlike Snowsight, SQL commands can be used to alter many of the fields in an organization profile, including the contact email address.

Copy code

```
USE ROLE GLOBALORGADMIN;

ALTER ORGANIZATION PROFILE MyOrgPROFILE
AS
$$
title: "New Title"
description: "New desc"
contact: "contact@test.com"
approver_contact: "approver@test.com"
allowed_publishers:
  access:
   - all_internal_accounts: true
logo: "urn:emoji:smile"
$$
```

For details of organization profile manifest fields, see [Organization profile manifest reference](/user-guide/collaboration/organization-profiles/org-profile-manifest-reference).

## View organization profiles

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Browse the available profiles or use the search bar to find a specific organization listing and examine its profile.

Use [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles) to find organization profiles which are available to
you.

Copy code

```
SHOW AVAILABLE ORGANIZATION PROFILES;
```
