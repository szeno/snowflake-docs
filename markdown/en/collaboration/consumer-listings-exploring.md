# Explore listings

Explore and try out paid and limited trial listings on the Snowflake Marketplace before you purchase or request them.
If there are listings or providers you need that are currently unavailable, you can request new data or providers
on the Snowflake Marketplace.

You must be a Snowflake listing consumer to access or purchase a listing. See [Use listings as a consumer](/collaboration/consumer-becoming).

## Browse listings on the Snowflake Marketplace

You can browse listings on the Snowflake Marketplace whether you have a Snowflake account or not.

- You can see listings on the web by browsing to the [Snowflake Marketplace](/collaboration/collaboration-marketplace-about).
- You can see listings in Snowsight by doing the following steps:
  1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
  2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.

After you find a listing relevant to your use cases, explore it further.

- Get a free listing. See [Access and install listings as a consumer](/collaboration/consumer-listings-access).
- Review the data dictionary. See [Preview the contents of a listing with data dictionaries](#label-consumer-data-dictionary).
- Trial a paid or limited trial listing. See [Trial a listing](#label-trial-paid-listing).

## View listing information

You can use the following SQL commands to view listing information:

- Run [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing) to view detailed information of listings available to you.
- Run [SHOW AVAILABLE LISTINGS](/sql-reference/sql/show-available-listings) to display all the listings available to you.

## Preview the contents of a listing with data dictionaries

Data dictionaries allow you to preview the contents of a listing on the Snowflake Marketplace before installing it in your
account. A data dictionary displays the tables, views, and functions within a listing.

There are two ways you can view the contents of a listing as a consumer:

- Featured objects: allow you to view the most important objects within the listing. Featured objects are selected by the
  listing provider.
- All objects: allow you to view all of the objects within a listing.

To view the contents of a listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search for the listing, then select it.
4. Review the items that appear under **Data Dictionary**.
   - To view the contents of a featured object, select the object’s name.
   - To view all of the objects within a listing, select **View all objects**. When viewing all objects you can browse
     through the contents of a listing or search for specific items.
   - To view the data dictionary associated with an object, select its **Data Preview** tab.

     If Data Preview is enabled for the selected listing, then up to 10 rows of data are displayed.

## Trial a listing

You can trial a limited trial or paid listing to explore the data available in the listing.

After you explore the data, you can [purchase the listing](/collaboration/consumer-listings-access#label-access-paid-listings) or
[request the full data product](/collaboration/consumer-listings-access#label-request-limited-trial-listing).

Note

You must use the ACCOUNTADMIN role or a custom role with the CREATE DATABASE and IMPORT SHARE privileges to trial a listing.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**, and then search for the listing that you want to trial.

   The pricing status of each listing is indicated on the listing.

   To view only listings available to trial:

   1. Select the **Data products** tab.
   2. In the **Pricing** filter, select **Free to Try**.
3. Select a paid or limited trial listing. The listing description page opens and you can read about the listing.
4. Select **Get**. You can read the description of the trial available for the listing.
5. Enter your preferred name for the database created from the data product in the listing.
6. Select **Get Data**.
7. If you want to query the data in the listing immediately, select **Open** to open a [Snowsight worksheet](/user-guide/ui-snowsight-worksheets)
   containing example SQL queries for the listing’s dataset. Otherwise, select **Done**.

### About trialing listings

When you trial a listing, you might have any of the following types of access:

- Indefinite access to a limited set of data.
- Indefinite access to limited functionality of the Snowflake Native App.
- Time-limited access to all data or a limited set of data.
- Time-limited access to all functionality or limited functionality of the Snowflake Native App.

If you are trialing a paid listing, you are not charged for the listing when your trial ends. You are only charged if you choose to purchase
the paid listing.

Using the data product in a listing that you’re trialing works similarly to using a database that you have full access to:

- An account administrator, the role that created the database (if different than the account admin), or any role with the global
  MANAGE GRANTS privilege can grant other roles access to the database and database objects (e.g. tables, views).
- Querying data while you trial a listing incurs compute charges in your Snowflake account, but you do not incur any charges for the listing.
- If the listing provides access to a limited set of data or functionality and you attempt to perform actions that are
  accessible only to consumers with full access to the listing, you see no results.

When your time-limited trial ends, or when you have finished exploring the limited trial data product, decide what to do with the listing:

- If you decide to purchase the data product of a paid listing, see [Accessing paid listings](/collaboration/consumer-listings-access#label-access-paid-listings).
- If you want to request unlimited access to the full data product of a limited trial listing, see [Request a limited trial listing](/collaboration/consumer-listings-access#label-request-limited-trial-listing).
- If you don’t want to purchase the data product, an account administrator can drop the database created or Snowflake Native App installed for your trial.
- If you want to continue trialing the data product but the time period of a time-limited trial has expired, other accounts in your
  organization can start a new trial of the listing.
