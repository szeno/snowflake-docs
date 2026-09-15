# Reference organizational listings in queries

Note

Organizational listings can be queried without mounting.

To reference an organizational listing’s datasets in a SQL query, use the Uniform Listing Locator (ULL).
The ULL serves as a unique identifier that points to a listing in the Internal Marketplace, making it
easy to query its datasets directly.

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

Example queries:

Copy code

```
SELECT * FROM "<orgdatacloud$internal$organizational_listing_name>".<schema_name>.<object_within_listing>;
SELECT * FROM <orgdatacloud$internal$organizational_listing_name>.<schema_name>.<object_within_listing>;
```

The following query example uses the ULL as a replacement for the database name. Replace `<object_within_listing>` with the name of a table or view that’s part of the listing:

Copy code

```
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
