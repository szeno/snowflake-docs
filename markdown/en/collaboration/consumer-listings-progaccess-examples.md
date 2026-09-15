# Manage listings with SQL as a consumer - examples

The following are examples of the common tasks that consumers can complete programmatically with SQL commands:

- [Show available listings](#show-available-listings)
- [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing)
- [Request a listing and automatically poll for availability](#request-a-listing-and-automatically-poll-for-availability)
- [Create a database from a listing](#create-a-database-from-a-listing)
- [End-to-end example](#end-to-end-example)

## Show available listings

Shows the listings available to the consumer running the command. For more information about the SHOW AVAILABLE LISTINGS command, see [SHOW AVAILABLE LISTINGS](#show-available-listings).

| Description | Notes |
| --- | --- |
| Show the available listings. | Use `IS_SHARED_WITH_ME = TRUE` to show only the listings shared privately with the consumer running the command. Use `IS_IMPORTED = TRUE` to show only imported listings. |

Expand

Show lessSee more

Copy code

```
SHOW AVAILABLE LISTINGS
```

## Describe available listings

After running SHOW AVAILABLE LISTINGS to identify the available listings and the global listing names, a consumer can run DESCRIBE AVAILABLE LISTING to return descriptions of the columns in the listings that are available to them. For more information about the DESCRIBE AVAILABLE LISTING command, see [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing).

| Description | Notes |
| --- | --- |
| Describe the listing columns. | Use `listing_global_name` to identify the specific global listing to describe. When the `is_ready_for_import` column is `TRUE`, the data is already present in the region and can be imported by the consumer immediately. |

Expand

Show lessSee more

Copy code

```
DESCRIBE AVAILABLE LISTING < listing_global_name >
```

## Request a listing and automatically poll for availability

After running SHOW AVAILABLE LISTINGS to identify the available listings, a consumer can use the `SYSTEM$REQUEST_LISTING_AND_WAIT` stored procedure to request a listing and automatically poll for availability. A consumer can also use this stored procedure when the `is_ready_for_import` column is `FALSE`. For more information about the `SYSTEM$REQUEST_LISTING_AND_WAIT` stored procedure, see [SYSTEM$REQUEST\_LISTING\_AND\_WAIT](/sql-reference/stored-procedures/system_request_listing_and_wait).

| Description | Notes |
| --- | --- |
| Request a specific listing and poll for availability. | `<timeout_mins>` specifies the listing fulfillment waiting period in minutes. The default is 240 minutes or 4 hours.  When a requested listing becomes available or is already available, the message `Success: Listing <listing_global_name> is ready to be imported` is returned.  If the timeout period is exceeded, the message `Error: Timed out waiting for the listing to be available after <timeout_mins> min(s)` is returned.  To request a listing without waiting for listing fulfillment, enter 0 (zero) for the `<timeout_mins>` value. When the value is 0, the message `Success: Listing <listing_global_name> requested successfully, but not waiting to confirm fulfillment` is returned. |

Expand

Show lessSee more

Copy code

```
CALL SYSTEM$REQUEST_LISTING_AND_WAIT( ' <listing_global_name> ' [ , <timeout_mins>. ] );
```

## Create a database from a listing

After requesting a listing, a consumer can use the CREATE DATABASE … FROM LISTING … command to create a database from a listing. For more information about the CREATE DATABASE … FROM LISTING … command, see [CREATE DATABASE … FROM LISTING …](/sql-reference/sql/create-database).

| Description | Notes |
| --- | --- |
| Create a database from a listing. | `<name>` specifies the database identifier. It must be unique for your account. The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier string is enclosed in double quotes. For example `"My object"`. Identifiers enclosed in double quotes are also case-sensitive. |

Expand

Show lessSee more

Copy code

```
CREATE DATABASE <name> FROM LISTING '<listing_global_name>';
```

## End-to-end example

The following example shows how to use the SQL commands described above to manage listings as a consumer. The example assumes that the consumer has already been granted access to a listing for COVID-19 data named *GZ1MXZFTF1* and that the listing is available in the consumer’s region. The example also assumes that the consumer has been granted the *sysadmin* role, which is required to create a database from a listing.

Copy code

```
-- Switch to sysadmin role
USE ROLE sysadmin;

-- Show available listings with a filter for shared listings
-- Note that you can optionally filter for private shared listings using IS_SHARED_WITH_ME = TRUE
-- The example assumes that the response returns a listing with a listing_global_name of GZ1MXZFTF1
SHOW AVAILABLE LISTINGS;

-- Get the global name and title of listings and filter on the title
SELECT "global_name", "title"
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE "is_imported" = false
    AND "title" LIKE '%COVID-19%';

-- Request the listing returned in `SHOW AVAILABLE LISTINGS` and wait for completion
CALL SYSTEM$REQUEST_LISTING_AND_WAIT('GZ1MXZFTF1');

-- Accept legal terms for the listing. Email verification is required to create the database from listing GZ1MXZFTF1
CALL SYSTEM$ACCEPT_LEGAL_TERMS('DATA_EXCHANGE_LISTING', 'GZ1MXZFTF1');

-- Create database from the listing
CREATE DATABASE test_california_covid_import
  FROM LISTING 'GZ1MXZFTF1';

-- Use the new database
USE DATABASE test_california_covid_import;

-- Query the 'COVID.CASES' table and limit the results to 100 rows
SELECT * FROM COVID.CASES LIMIT 100;
```
