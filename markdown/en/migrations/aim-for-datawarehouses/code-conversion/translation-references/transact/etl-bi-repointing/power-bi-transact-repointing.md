# Transact - Power BI Repointing

Applies to

- SQL Server
- Azure Synapse Analytics

## Description

The Power BI repointing is a feature that provides an easy way to redefine the connections from the M language in the Power Query Editor. This means that the connection parameters will be redefined to point to the Snowflake migration database context. For SQL Server and Azure Synapse, the method in M Language that defined the connection is `Sql.Database(...)`. In Snowflake, there is a connector that depends on some other parameters and the main connection is defined by `Snowflake.Database(...)` method.

## Source Pattern Samples

This section will explain the cases currently addressed.

### Simple Entity Repointing Case

Even a simple connection to a table from Power BI requires many transformations to be used with the implicit Power BI connector from Snowflake. In this case, new information variables such as database and schema are added, and the source table is called with the implicit type (it can also be a view).

Also, a mapping is generated between the columns to match the text case with the database migration context or, if possible, with the Power BI report internal information.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

Copy code

```
:force:
let
    Source = Sql.Database("your_connection", "LibraryDatabase"),
    dbo_Authors = Source{[Schema="dbo",Item="Authors"]}[Data]
in
    dbo_Authors
```

**Snowflake SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="DBO", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="BOOKS", Kind="Table"]}[Data],
    dbo_Books = Table.RenameColumns(SourceSfTbl, {{ "BOOKID", "BookID"}, { "TITLE", "Title"}, { "AUTHORID", "AuthorID"}, { "PUBLICATIONYEAR", "PublicationYear"}})
in
    dbo_Books
```

### Simple Entity With Multiple Lines Repointing Case

In this case “Filtered Rows” is an additional step into the logic of the query. In the repointing version, the additional logic is preserved as it is.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

Copy code

```
:force:
let
  Source = Sql.Database("your_connection", "mytestdb"),
  dbo_Employee = Source{[Schema="dbo",
  Item="Employee"]}[Data],
  #"Filtered Rows" = Table.SelectRows(dbo_Employee, each Text.StartsWith([name], "John"))
in
  #"Filtered Rows"
```

**Snowflake SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
  Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
  SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
  SourceSfSchema = SourceSfDb{[Name="DBO", Kind="Schema"]}[Data],
  SourceSfTbl = SourceSfSchema{[Name="EMPLOYEE", Kind="Table"]}[Data],
  dbo_Employee = SourceSfTbl,
  #"Filtered Rows" = Table.SelectRows(dbo_Employee, each Text.StartsWith([name], "John"))
in
  #"Filtered Rows"
```

### Embedded SQL Query Repointing Case

For the SQL queries embedded inside the connections, these queries will be extracted, migrated, and re-inserted. Warning messages in the migrated queries may require extra attention. In this case, the warning message does not stop the query from being run in the Snowflake database.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

Copy code

```
:force:
let
    Source = Sql.Database("your_connection", "LibraryDatabase", [Query="SELECT DISTINCT#(lf)    B.Title#(lf)FROM#(lf)    DBO.Books AS B#(lf)JOIN#(lf)    DBO.Authors AS A ON B.AuthorID = A.AuthorID#(lf)JOIN#(lf)    DBO.BookGenres AS BG ON B.BookID = BG.BookID#(lf)JOIN#(lf)    DBO.Genres AS G ON BG.GenreID = G.GenreID#(lf)WHERE#(lf)    A.Nationality = 'American' AND G.Origin = 'USA'#(lf)ORDER BY#(lf)    B.Title;", CreateNavigationProperties=false])
in
    Source
```

**Snowflake SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS ""DBO.Books"", ""DBO.Authors"", ""DBO.BookGenres"", ""DBO.Genres"" **
SELECT DISTINCT
    B.Title
FROM
    DBO.Books AS B
    JOIN
        DBO.Authors AS A
        ON B.AuthorID = A.AuthorID
    JOIN
        DBO.BookGenres AS BG
        ON B.BookID = BG.BookID
    JOIN
        DBO.Genres AS G
        ON BG.GenreID = G.GenreID
WHERE
    A.Nationality = 'American' AND G.Origin = 'USA'
ORDER BY B.Title", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "TITLE", "Title"}})
in
    Source
```

### Embedded SQL Query With Multiple Lines Repointing Case

This case showcases the connection with SQL queries and multiple lines of logic after the connection logic.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

Copy code

```
:force:
let
  Source = Sql.Database("your_connection", "mytestdb", [Query="SELECT DISTINCT#(lf)    P.ProductName,#(lf)    P.Category,#(lf)    P.StockQuantity#(lf)FROM#(lf)    Products AS P#(lf)WHERE#(lf)    P.StockQuantity > 0#(lf)ORDER BY#(lf)    P.Category ASC;"]),
  #"Filtered Rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "Cards"))
in
 #"Filtered Rows"
```

**Snowflake SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
  Source = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT ""Products"" **
SELECT DISTINCT
    P.ProductName,
    P.Category,
    P.StockQuantity
FROM
    Products AS P
WHERE
    P.StockQuantity > 0
ORDER BY P.Category ASC", null, [EnableFolding=true]),
  #"Filtered Rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "Cards"))
in
  #"Filtered Rows"
```

### Embedded SQL Query With Column Renaming Repointing Case

At the moment, column renaming for SQL queries cases are only applied if the internal information of the provided Power BI report contains this information.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

Copy code

```
:force:
let
    Source = Sql.Database("your_connection", "SalesSampleDB", [Query="SELECT DISTINCT#(lf)    P.ProductName,#(lf)    P.Category,#(lf)    P.StockQuantity#(lf)FROM#(lf)    Products AS P#(lf)WHERE#(lf)    P.StockQuantity > 0#(lf)ORDER BY#(lf)    P.Category ASC;"])
in
    Source
```

**Snowflake SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT ""Products"" **
SELECT DISTINCT
    P.ProductName,
    P.Category,
    P.StockQuantity
FROM
    Products AS P
WHERE
    P.StockQuantity > 0
ORDER BY P.Category ASC", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "PRODUCTNAME", "ProductName"}, { "CATEGORY", "Category"}, { "STOCKQUANTITY", "StockQuantity"}})
in
    Source
```

### Function For Entity Case Repointing Case

Currently, the functions are only supported for entities import case, and Transact only.

**Transact-SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
  Source = Sql.Database("your_connection", "mytestdb"),
  dbo_MultiParam = Source{[Schema="dbo",Item="MultiParam"]}[Data],
  #"Invoked Functiondbo_MultiParam1" = dbo_MultiParam(1,"HELLO")
in
  #"Invoked Functiondbo_MultiParam1"
```

**Snowflake SQL Connection in the Power Query Editor**

Copy code

```
:force:
let
  Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
  SourceSfDb = Source{[Name="mytestdb, Kind="Database"]}[Data],
  SourceSfFunc = (x, y) => Value.NativeQuery(SourceSfDb, "SELECT DBO.MultiParam(" & Text.From(x) & "," &  (if y = null then null else ("'" & y & "'"))  & ")"),
  dbo_MultiParam = SourceSfFunc,
  #"Invoked Functiondbo_MultiParam1" = dbo_MultiParam(1,"HELLO")
in
  #"Invoked Functiondbo_MultiParam1"
```
