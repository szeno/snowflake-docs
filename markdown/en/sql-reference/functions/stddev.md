Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window function syntax and usage](/sql-reference/functions-window-syntax) (General)

# STDDEV, STDDEV\_SAMP

Returns the sample standard deviation (square root of sample variance) of non-NULL values. STDDEV and STDDEV\_SAMP are aliases
for the same function.

See also [STDDEV\_POP](/sql-reference/functions/stddev_pop), which returns the population standard deviation (square root of variance).

## Syntax

**Aggregate function**

Copy code

```
{ STDDEV | STDDEV_SAMP } ( [ DISTINCT ] <expr1> )
```

**Window function**

Copy code

```
{ STDDEV | STDDEV_SAMP } ( [ DISTINCT ] <expr1> ) OVER (
                                                       [ PARTITION BY <expr2> ]
                                                       [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                                       )
```

For details about `window_frame` syntax, see [Usage notes for window frames](/sql-reference/functions-window-syntax#label-window-frames).

## Arguments

`expr1`
:   An expression that evaluates to a numeric value. This is the expression on which the standard deviation is calculated.

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the optional expression to order by within each partition.

## Returns

The data type of the returned value is DOUBLE.

If all records inside a group are NULL, this function returns NULL.

## Usage notes

- For single-record inputs, STDDEV and STDDEV\_SAMP both return NULL. This is different from the Oracle behavior, where STDDEV\_SAMP returns NULL for a single record and STDDEV returns 0.
- When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast cannot be performed, an error is returned.
- When this function is called as a window function and the OVER clause contains an ORDER BY clause:

  - The DISTINCT keyword is prohibited and results in a SQL compilation error.
  - A window frame must be specified. If you do not specify a window frame, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

  For more details about window frames, including syntax and examples, see [Usage notes for window frames](/sql-reference/functions-window-syntax#label-window-frames).

## Aggregate function examples

The following example calculates the standard deviation for a small sample of integers:

Copy code

```
CREATE TABLE t1 (c1 INTEGER);
INSERT INTO t1 (c1) VALUES
  (6),
  (10),
  (14);
SELECT STDDEV(c1) FROM t1;
```

```
+----------+
| STDDEV() |
|----------|
|        4 |
+----------+
```

Note that the function STDDEV\_SAMP returns the same result:

Copy code

```
SELECT STDDEV_SAMP(c1) FROM t1;
```

```
+-----------------+
| STDDEV_SAMP(C1) |
|-----------------|
|               4 |
+-----------------+
```

The following example uses a small table named `menu_items`, which lists items for sale from a food
truck. If you would like to create and load this table, see [Create and load the menu\_items table](#label-create-and-load-menu-items-table).

To find the sample standard deviation for both the cost of goods sold (COGS) and the sale price for the
`Dessert` rows, run this query:

Copy code

```
SELECT menu_category, STDDEV(menu_cogs_usd) AS stddev_cogs, STDDEV(menu_price_usd) AS stddev_price
  FROM menu_items
  WHERE menu_category = 'Dessert'
  GROUP BY 1;
```

```
+---------------+-------------+--------------+
| MENU_CATEGORY | STDDEV_COGS | STDDEV_PRICE |
|---------------+-------------+--------------|
| Dessert       |  1.00519484 |  1.471960144 |
+---------------+-------------+--------------+
```

## Window function example

The following example also uses the `menu_items` table (see [Create and load the menu\_items table](#label-create-and-load-menu-items-table))
but calls the STDDEV function as a window function.

The window function partitions rows by the `menu_category` column. Therefore, the standard deviation is
calculated once for each category, and that value is repeated in the result for each row in the group.
In this example, the rows must be grouped by both the menu category and the cost of goods sold.

Copy code

```
SELECT menu_category, menu_cogs_usd,
  STDDEV(menu_cogs_usd) OVER(PARTITION BY menu_category) AS stddev_cogs
  FROM menu_items
  GROUP BY 1, 2
  ORDER BY menu_category;
```

The following output is a partial result set for this query (the first 15 rows):

```
+---------------+---------------+--------------+
| MENU_CATEGORY | MENU_COGS_USD |  STDDEV_COGS |
|---------------+---------------+--------------|
| Beverage      |          0.50 | 0.1258305738 |
| Beverage      |          0.65 | 0.1258305738 |
| Beverage      |          0.75 | 0.1258305738 |
| Dessert       |          1.25 | 1.054751155  |
| Dessert       |          3.00 | 1.054751155  |
| Dessert       |          1.00 | 1.054751155  |
| Dessert       |          2.50 | 1.054751155  |
| Dessert       |          0.50 | 1.054751155  |
| Main          |          4.50 | 3.444051572  |
| Main          |          2.40 | 3.444051572  |
| Main          |          1.50 | 3.444051572  |
| Main          |         11.00 | 3.444051572  |
| Main          |          8.00 | 3.444051572  |
| Main          |          NULL | 3.444051572  |
| Main          |         12.00 | 3.444051572  |
...
```

## Create and load the menu\_items table

To create and insert rows into the `menu_items` table that is used in some function examples,
run the following SQL commands. (This table contains 60 rows. It is based on, but not identical to,
the `menu` table in the
[Tasty Bytes sample database](https://quickstarts.snowflake.com/guide/tasty_bytes_introduction/index.html#0).)

Copy code

```
CREATE OR REPLACE TABLE menu_items(
  menu_id INT NOT NULL,
  menu_category VARCHAR(20),
  menu_item_name VARCHAR(50),
  menu_cogs_usd NUMBER(7,2),
  menu_price_usd NUMBER(7,2));
```

Copy code

```
INSERT INTO menu_items VALUES(1,'Beverage','Bottled Soda',0.500,3.00);
INSERT INTO menu_items VALUES(2,'Beverage','Bottled Water',0.500,2.00);
INSERT INTO menu_items VALUES(3,'Main','Breakfast Crepe',5.00,12.00);
INSERT INTO menu_items VALUES(4,'Main','Buffalo Mac & Cheese',6.00,10.00);
INSERT INTO menu_items VALUES(5,'Main','Chicago Dog',4.00,9.00);
INSERT INTO menu_items VALUES(6,'Main','Chicken Burrito',3.2500,12.500);
INSERT INTO menu_items VALUES(7,'Main','Chicken Pot Pie Crepe',6.00,15.00);
INSERT INTO menu_items VALUES(8,'Main','Combination Curry',9.00,15.00);
INSERT INTO menu_items VALUES(9,'Main','Combo Fried Rice',5.00,11.00);
INSERT INTO menu_items VALUES(10,'Main','Combo Lo Mein',6.00,13.00);
INSERT INTO menu_items VALUES(11,'Main','Coney Dog',5.00,10.00);
INSERT INTO menu_items VALUES(12,'Main','Creamy Chicken Ramen',8.00,17.2500);
INSERT INTO menu_items VALUES(13,'Snack','Crepe Suzette',4.00,9.00);
INSERT INTO menu_items VALUES(14,'Main','Fish Burrito',3.7500,12.500);
INSERT INTO menu_items VALUES(15,'Snack','Fried Pickles',1.2500,6.00);
INSERT INTO menu_items VALUES(16,'Snack','Greek Salad',4.00,11.00);
INSERT INTO menu_items VALUES(17,'Main','Gyro Plate',8.00,12.00);
INSERT INTO menu_items VALUES(18,'Main','Hot Ham & Cheese',7.00,11.00);
INSERT INTO menu_items VALUES(19,'Dessert','Ice Cream Sandwich',1.00,4.00);
INSERT INTO menu_items VALUES(20,'Beverage','Iced Tea',0.7500,3.00);
INSERT INTO menu_items VALUES(21,'Main','Italian',6.00,11.00);
INSERT INTO menu_items VALUES(22,'Main','Lean Beef Tibs',6.00,13.00);
INSERT INTO menu_items VALUES(23,'Main','Lean Burrito Bowl',3.500,12.500);
INSERT INTO menu_items VALUES(24,'Main','Lean Chicken Tibs',5.00,11.00);
INSERT INTO menu_items VALUES(25,'Main','Lean Chicken Tikka Masala',10.00,17.00);
INSERT INTO menu_items VALUES(26,'Beverage','Lemonade',0.6500,3.500);
INSERT INTO menu_items VALUES(27,'Main','Lobster Mac & Cheese',10.00,15.00);
INSERT INTO menu_items VALUES(28,'Dessert','Mango Sticky Rice',1.2500,5.00);
INSERT INTO menu_items VALUES(29,'Main','Miss Piggie',2.600,6.00);
INSERT INTO menu_items VALUES(30,'Main','Mothers Favorite',4.500,12.00);
INSERT INTO menu_items VALUES(31,'Main','New York Dog',4.00,8.00);
INSERT INTO menu_items VALUES(32,'Main','Pastrami',8.00,11.00);
INSERT INTO menu_items VALUES(33,'Dessert','Popsicle',0.500,3.00);
INSERT INTO menu_items VALUES(34,'Main','Pulled Pork Sandwich',7.00,12.00);
INSERT INTO menu_items VALUES(35,'Main','Rack of Pork Ribs',11.2500,21.00);
INSERT INTO menu_items VALUES(36,'Snack','Seitan Buffalo Wings',4.00,7.00);
INSERT INTO menu_items VALUES(37,'Main','Spicy Miso Vegetable Ramen',7.00,17.2500);
INSERT INTO menu_items VALUES(38,'Snack','Spring Mix Salad',2.2500,6.00);
INSERT INTO menu_items VALUES(39,'Main','Standard Mac & Cheese',3.00,8.00);
INSERT INTO menu_items VALUES(40,'Dessert','Sugar Cone',2.500,6.00);
INSERT INTO menu_items VALUES(41,'Main','Tandoori Mixed Grill',11.00,18.00);
INSERT INTO menu_items VALUES(42,'Main','The Classic',4.00,12.00);
INSERT INTO menu_items VALUES(43,'Main','The King Combo',12.00,20.00);
INSERT INTO menu_items VALUES(44,'Main','The Kitchen Sink',6.00,14.00);
INSERT INTO menu_items VALUES(45,'Main','The Original',1.500,5.00);
INSERT INTO menu_items VALUES(46,'Main','The Ranch',2.400,6.00);
INSERT INTO menu_items VALUES(47,'Main','The Salad of All Salads',6.00,12.00);
INSERT INTO menu_items VALUES(48,'Main','Three Meat Plate',10.00,17.00);
INSERT INTO menu_items VALUES(49,'Main','Three Taco Combo Plate',7.00,11.00);
INSERT INTO menu_items VALUES(50,'Main','Tonkotsu Ramen',7.00,17.2500);
INSERT INTO menu_items VALUES(51,'Main','Two Meat Plate',9.00,14.00);
INSERT INTO menu_items VALUES(52,'Dessert','Two Scoop Bowl',3.00,7.00);
INSERT INTO menu_items VALUES(53,'Main','Two Taco Combo Plate',6.00,9.00);
INSERT INTO menu_items VALUES(54,'Main','Veggie Burger',5.00,9.00);
INSERT INTO menu_items VALUES(55,'Main','Veggie Combo',4.00,9.00);
INSERT INTO menu_items VALUES(56,'Main','Veggie Taco Bowl',6.00,10.00);
INSERT INTO menu_items VALUES(57,'Dessert','Waffle Cone',2.500,6.00);
INSERT INTO menu_items VALUES(58,'Main','Wonton Soup',2.00,6.00);
INSERT INTO menu_items VALUES(59,'Main','Mini Pizza',null,null);
INSERT INTO menu_items VALUES(60,'Main','Large Pizza',null,null);
```
