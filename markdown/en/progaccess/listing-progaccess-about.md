# About managing listings using SQL

Providers can use listings to share data products with accounts in any Snowflake region. To learn more about listings,
see [About sharing with listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about).

Providers can use SQL commands to create and manage listings and offer them to specific consumers. To share a listing using SQL, providers complete the following tasks:

- (Optional) Create a Provider Profile to offer listings. See [Use listings as a provider](/collaboration/provider-becoming).
- [Define a listing manifest](#label-listings-programmatic-manifest).
- [Create a listing using SQL](#label-listings-programmatic-create).
- [Publish a listing using SQL](#label-listings-programmatic-publish).

Note

Providers can’t offer paid, personalized listings, or listings on private data exchanges.

## Prerequisites for working with listings using SQL

- [Review and accept the Snowflake Provider and Consumer Terms](/collaboration/provider-becoming#label-accept-provider-tos-marketplace)

  You don’t need to accept the Snowflake Provider and Consumer Terms if you’re creating free private listings and
  you’ve accepted the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/).
- Prepare the data for your listing. See [Prepare data for a listing](/collaboration/provider-listings-preparing).
- Review the [Provider Policies](https://www.snowflake.com/provider-policies/).
- Configure account privileges.

## Listing and application owner roles

When you create a listing, you create it from the account that has the data or application package in it. The role that attaches a data
product to a listing and publishes the listing must be the same role that created, and therefore owns, the application package or share.
You cannot transfer the OWNERSHIP privilege for a share.

If you use a different role to create and manage the listing, grant the MODIFY privilege on the listing to the role
that owns the application package or share. For example:

Share or application package owner role:
:   OWNERSHIP privilege on the share or application package.
    MODIFY privilege on the listing.

Listing owner role:
:   OWNERSHIP privilege on the listing.

    Global CREATE LISTING privilege.

Within the provider account, you can use one of the following to create and manage listings:

ACCOUNTADMIN:
:   If you use the ACCOUNTADMIN role to create and manage listings, the ORGADMIN role must first
    [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges).

Custom role:
:   If you use a custom role, the ORGADMIN role must first [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges)
    to the ACCOUNTADMIN role, which can then be used to grant the relevant privileges to the custom role.

For more information about granting sharing privileges, see [Granting Privileges to Other Roles:](/user-guide/data-exchange-marketplace-privileges).

## Define a listing manifest

To create a listing you must first create a listing manifest. Manifests are written in YAML
(<https://yaml.org/spec/>), and include a prefix and required and optional fields.

For example, to create a simple titled listing with listing terms, define a manifest similar to:

Copy code

```
title: A title for the listing.
subtitle: An optional subtitle.
description: A general description.
profile: Provider profile reference.
listing_terms: ...
targets: ...
```

Each manifest then includes additional sections, such as:

Copy code

```
auto_fulfillment: ...
```

And a number of optional fields, such as `data_dictionary`, `business_needs`, and more.

A simple manifest would include:

Copy code

```
title: "MyFirstListing"
subtitle: "Example listing"
description: "This is my first listing!"
listing_terms:
  type: "OFFLINE"
targets:
   accounts: ["Org1.Account1"]
```

For more information, see [Listing manifest reference](/progaccess/listing-manifest-reference).

For additional examples and use cases associated with managing listings using SQL see [Manage listings with SQL as a provider - examples](/progaccess/listing-progaccess-examples).

## Create a listing using SQL

To create a listing, you use the [CREATE LISTING](/sql-reference/sql/create-listing) command, specifying a name and the listing details inline in a YAML manifest that describes the listing.
Listings created using CREATE LISTING … are automatically published.

After a listing is created, you can alter it using [ALTER LISTING](/sql-reference/sql/alter-listing), which includes unpublish and publish
support. Additionally, listings can be [described](/sql-reference/sql/desc-listing), [shown](/sql-reference/sql/show-listings),
[published and unpublished](/sql-reference/sql/alter-listing), and [dropped](/sql-reference/sql/drop-listing).

Note

Creating a listing using SQL is conceptually similar to [Share data or apps with specific consumers using a private listing](https://other-docs.snowflake.com//collaboration/provider-listings-creating-publishing#label-listings-create). You should be familiar and comfortable
with creating, viewing, and publishing listings using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) and **Provider Studio** before creating listings using SQL.
For more information, see [Share data or apps with specific consumers using a private listing](https://other-docs.snowflake.com//collaboration/provider-listings-creating-publishing#label-listings-create).

Before you create your listing, ensure you have completed all [prerequisites](#label-listings-programmatic-prereqs).

For example, if you want to create a DRAFT listing `my1stlisting` from share `myshare` with title “My first SQL listing”, execute the following command:

Copy code

```
CREATE EXTERNAL LISTING my1stlisting
SHARE myshare AS
$$
 title: "My first SQL listing"
 description: "This is my first listing"
 listing_terms:
   type: "OFFLINE"
 targets:
   accounts: ["Org1.Account1"]
$$ PUBLISH=FALSE REVIEW=FALSE;
```

Note

Listings are identified using the listing’s *NAME*. A listing *NAME* is the identifier used when initially creating the listing.
In the example above, the listing name is MY1STLISTING. While title, subtitle and other listing characteristics can be altered,
*NAME* cannot be altered by specifying a new name in yaml. Use [ALTER LISTING … RENAME TO](/sql-reference/sql/alter-listing) to rename a listing.
Commands such as [ALTER LISTING](/sql-reference/sql/alter-listing), [SHOW LISTINGS](/sql-reference/sql/show-listings), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), and [DROP LISTING](/sql-reference/sql/drop-listing)
all use *NAME* to identify a listing.
Listing *NAME* is not shown in Snowsight, which identifies listings by title.

For additional examples and use-cases associated with managing listings using SQL see [Manage listings with SQL as a provider - examples](/progaccess/listing-progaccess-examples).

## Publish a listing using SQL

You can publish and un-publish listings using [ALTER LISTING … PUBLISH](/sql-reference/sql/alter-listing) and ALTER LISTING … UNPUBLISH.

For more information about publishing listings using Snowsight, see [Publish a listing](https://other-docs.snowflake.com//collaboration/provider-listings-creating-publishing#label-listings-create-publish).

Note that listings can be automatically published when created using [CREATE LISTING](/sql-reference/sql/create-listing).

For example, to publish the previously unpublished listing, execute the following command:

Copy code

```
ALTER LISTING MY1STLISTING PUBLISH;
```

Additionally, before a listing can be dropped, it must be un-published. To
un-publish a previously published listing, execute a command similar to:

Copy code

```
ALTER LISTING MY1STLISTING UNPUBLISH;
```

For additional examples and use-cases associated with managing listings using SQL see [Manage listings with SQL as a provider - examples](/progaccess/listing-progaccess-examples).

## Expand the definition of a listing using SQL

The previous example did not include targets or usage examples. You can use the [ALTER LISTING](/sql-reference/sql/alter-listing) to alter a listing’s characteristics.
In this example, we update an existing listing to add targets and example SQL. Note that the original YAML manifest is extended to include
new content.

To alter a listing to include additional fields execute a command similar to:

Copy code

```
ALTER LISTING MY1STLISTING AS
$$
   title: "My First SQL Listing"
   description: "This is my first listing"
   listing_terms:
     type: "OFFLINE"
   targets:
     accounts: ["Org1.Account1"]
   usage_examples:
     - title: "this is a test sql"
       description: "Simple example"
       query: "select *"
$$;
```

For additional examples and use-cases associated with managing listings using SQL see [Manage listings with SQL as a provider - examples](/progaccess/listing-progaccess-examples).

## Examine listings using SQL

Much like tables and other SQL elements, listings can be described and shown. [DESCRIBE LISTING](/sql-reference/sql/desc-listing) takes a single listing name
as a parameter and provides details about that listing. [SHOW LISTINGS](/sql-reference/sql/show-listings) can provide information about a group of listings, using a
`LIKE` filter, or all listings created by a given account if no filter is provided.

To show the details of the MY1STLISTING listing, execute a command similar to:

Copy code

```
SHOW LISTINGS LIKE 'MY1STLISTING';
```

To show all listings that your role has access to, execute a command similar to:

Copy code

```
SHOW LISTINGS;
```

To [describe](/sql-reference/sql/desc-listing) the listing MY1STLISTING, execute a command similar to:

Copy code

```
DESC LISTING MY1STLISTING;
```

## Drop listings using SQL

To remove a listing, you must first un-publish the listing. You should be familiar with removing listings using Snowsight
before dropping listings using SQL. For more information about removing listings using Snowsight,
see [Removing listings as a provider](https://other-docs.snowflake.com/en/collaboration/provider-listings-removing).

To un-publish a listing, execute a command similar to:

Copy code

```
ALTER LISTING MY1STLISTING UNPUBLISH;
```

To drop a listing, execute a command similar to:

Copy code

```
DROP LISTING IF EXISTS MY1STLISTING
```
