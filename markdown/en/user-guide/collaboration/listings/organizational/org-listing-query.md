# Reference organizational listings in queries

Note

Organizational listings can be queried without mounting.

To reference an organizational listing’s datasets in a SQL query, use the Uniform Listing Locator (ULL).
The ULL serves as a unique identifier that points to a listing in the Internal Marketplace, making it
easy to query its datasets directly.
If the listing is published in a different region, see [Query a listing from another region](/user-guide/collaboration/listings/organizational/org-listing-create#label-olisting-ull-cross-region).

## ULL format

A ULL has this format:

Copy code

```
ORGDATACLOUD$<organization_profile_name>$<listing_name>
```

- `ORGDATACLOUD`: Fixed prefix for all organizational listings.
- `<organization_profile_name>`: The organization profile that published the listing (for example, `INTERNAL`).
- `<listing_name>`: The listing name.

Separate the parts of a ULL with dollar signs (`$`). A ULL takes the place of a database name in a query.
To reference an object in the listing, add the schema and object names with periods, for example
`ORGDATACLOUD$INTERNAL$MY_LISTING.my_schema.my_table`.

Copy the exact ULL from Snowsight (**Copy ULL**) instead of building it by hand.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Browse or search for a data product.
4. Select a listing and select **Copy ULL**.
5. In the navigation menu, select **Projects** » **Notebooks** or another project tool.
6. Write a SQL query, using the ULL in place of the database name.

To query an organizational listing, use the following syntax:

Copy code

```
SELECT * FROM <ull>.<schema>.<view>
```

Example queries. Each query uses the ULL as a replacement for the database name. Replace `<object_within_listing>` with the name of a table or view that’s part of the listing:

Copy code

```
SELECT * FROM "<orgdatacloud$internal$organizational_listing_name>".<schema_name>.<object_within_listing>;
SELECT * FROM <orgdatacloud$internal$organizational_listing_name>.<schema_name>.<object_within_listing>;
```

If you prefer a more convenient name, consider creating a view:

Copy code

```
CREATE OR REPLACE VIEW <view_name>
AS
SELECT *
FROM <orgdatacloud$internal$organizational_listing_name>.<schema_name>.<object_within_listing>;
```
