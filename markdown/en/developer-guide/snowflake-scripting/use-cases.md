# Examples for common use cases of Snowflake Scripting

You can write anonymous blocks and stored procedures that use Snowflake Scripting language elements,
data types, and variables for solutions that address common use cases. This topic includes examples of
Snowflake Scripting code for some common use cases.

## Update table data with user input

The following example creates a stored procedure that updates table data with user input. It uses
a [FOR loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for) to iterate over the rows in a [RESULTSET](/developer-guide/snowflake-scripting/resultsets)
for the table. The FOR loop contains [conditional logic](/developer-guide/snowflake-scripting/branch). [Bind variables](/developer-guide/snowflake-scripting/variables#label-snowscript-variables-binding) based on user input determine the exact updates performed by the
stored procedure.

The example uses the following data:

Copy code

```
CREATE OR REPLACE TABLE bonuses (
  emp_id INT,
  performance_rating INT,
  salary NUMBER(12, 2),
  bonus NUMBER(12, 2)
);

INSERT INTO bonuses (emp_id, performance_rating, salary, bonus) VALUES
  (1001, 3, 100000, NULL),
  (1002, 1, 50000, NULL),
  (1003, 4, 75000, NULL),
  (1004, 4, 80000, NULL),
  (1005, 5, 120000, NULL),
  (1006, 2, 60000, NULL),
  (1007, 5, 40000, NULL),
  (1008, 3, 140000, NULL),
  (1009, 1, 95000, NULL);

SELECT * FROM bonuses;
```

```
+--------+--------------------+-----------+-------+
| EMP_ID | PERFORMANCE_RATING |    SALARY | BONUS |
|--------+--------------------+-----------+-------|
|   1001 |                  3 | 100000.00 |  NULL |
|   1002 |                  1 |  50000.00 |  NULL |
|   1003 |                  4 |  75000.00 |  NULL |
|   1004 |                  4 |  80000.00 |  NULL |
|   1005 |                  5 | 120000.00 |  NULL |
|   1006 |                  2 |  60000.00 |  NULL |
|   1007 |                  5 |  40000.00 |  NULL |
|   1008 |                  3 | 140000.00 |  NULL |
|   1009 |                  1 |  95000.00 |  NULL |
+--------+--------------------+-----------+-------+
```

The following stored procedure uses a FOR loop to iterate over the rows in a RESULTSET for the `bonuses` table.
It applies the bonus as the specified percentage of the salary of each employee with the specified performance
rating. The stored procedure uses conditional logic to apply the bonus only to the employees with the specified
performance rating. It also uses the inputs (`bonus_percentage` and `performance_value`) as bind variables.

Copy code

```
CREATE OR REPLACE PROCEDURE apply_bonus(bonus_percentage INT, performance_value INT)
  RETURNS TEXT
  LANGUAGE SQL
AS
DECLARE
  -- Use input to calculate the bonus percentage
  updated_bonus_percentage NUMBER(2,2) DEFAULT (:bonus_percentage/100);
  --  Declare a result set
  rs RESULTSET;
BEGIN
  -- Assign a query to the result set and execute the query
  rs := (SELECT * FROM bonuses);
  -- Use a FOR loop to iterate over the records in the result set
  FOR record IN rs DO
    -- Assign variable values using values in the current record
    LET emp_id_value INT := record.emp_id;
    LET performance_rating_value INT := record.performance_rating;
    LET salary_value NUMBER(12, 2) := record.salary;
    -- Determine whether the performance rating in the record matches the user input
    IF (performance_rating_value = :performance_value) THEN
      -- If the condition is met, update the bonuses table using the calculated bonus percentage
      UPDATE bonuses SET bonus = ( :salary_value * :updated_bonus_percentage )
        WHERE emp_id = :emp_id_value;
    END IF;
  END FOR;
  -- Return text when the stored procedure completes
  RETURN 'Update applied';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE apply_bonus(bonus_percentage INT, performance_value INT)
  RETURNS TEXT
  LANGUAGE SQL
AS
$$
DECLARE
  -- Use input to calculate the bonus percentage
  updated_bonus_percentage NUMBER(2,2) DEFAULT (:bonus_percentage/100);
  --  Declare a result set
  rs RESULTSET;
BEGIN
  -- Assign a query to the result set and execute the query
  rs := (SELECT * FROM bonuses);
  -- Use a FOR loop to iterate over the records in the result set
  FOR record IN rs DO
    -- Assign variable values using values in the current record
    LET emp_id_value INT := record.emp_id;
    LET performance_rating_value INT := record.performance_rating;
    LET salary_value NUMBER(12, 2) := record.salary;
    -- Determine whether the performance rating in the record matches the user input
    IF (performance_rating_value = :performance_value) THEN
      -- If the condition is met, update the bonuses table using the calculated bonus percentage
      UPDATE bonuses SET bonus = ( :salary_value * :updated_bonus_percentage )
        WHERE emp_id = :emp_id_value;
    END IF;
  END FOR;
  -- Return text when the stored procedure completes
  RETURN 'Update applied';
END;
$$
;
```

To run the stored procedure, specify the bonus percentage and the performance rating. For example, call
the stored procedure and apply a 3% bonus for employees with a performance rating of 5:

Copy code

```
CALL apply_bonus(3, 5);
```

Run a query to show the results:

Copy code

```
SELECT * FROM bonuses;
```

```
+--------+--------------------+-----------+---------+
| EMP_ID | PERFORMANCE_RATING |    SALARY |   BONUS |
|--------+--------------------+-----------+---------|
|   1001 |                  3 | 100000.00 |    NULL |
|   1002 |                  1 |  50000.00 |    NULL |
|   1003 |                  4 |  75000.00 |    NULL |
|   1004 |                  4 |  80000.00 |    NULL |
|   1005 |                  5 | 120000.00 | 3600.00 |
|   1006 |                  2 |  60000.00 |    NULL |
|   1007 |                  5 |  40000.00 | 1200.00 |
|   1008 |                  3 | 140000.00 |    NULL |
|   1009 |                  1 |  95000.00 |    NULL |
+--------+--------------------+-----------+---------+
```

## Filter and collect data

The following example creates a stored procedure that filters and collects the data in a table.
The procedure inserts rows using the collected data into another table to track historical trends.

The example uses the following data, which tracks the ownership and settings of virtual machines (VMs):

Copy code

```
CREATE OR REPLACE TABLE vm_ownership (
  emp_id INT,
  vm_id VARCHAR
);

INSERT INTO vm_ownership (emp_id, vm_id) VALUES
  (1001, 1),
  (1001, 5),
  (1002, 3),
  (1003, 4),
  (1003, 6),
  (1003, 2);

CREATE OR REPLACE TABLE vm_settings (
  vm_id INT,
  vm_setting VARCHAR,
  value NUMBER
);

INSERT INTO vm_settings (vm_id, vm_setting, value) VALUES
  (1, 's1', 5),
  (1, 's2', 500),
  (2, 's1', 10),
  (2, 's2', 600),
  (3, 's1', 3),
  (3, 's2', 400),
  (4, 's1', 8),
  (4, 's2', 700),
  (5, 's1', 1),
  (5, 's2', 300),
  (6, 's1', 7),
  (6, 's2', 800);

CREATE OR REPLACE TABLE vm_settings_history (
  vm_id INT,
  vm_setting VARCHAR,
  value NUMBER,
  owner INT,
  date DATE
);
```

Assume that a company wants to track the data in this table over time when the values of the settings exceed specific
thresholds. The following stored procedure collects and filters the data in the `vm_settings` table, then inserts rows into
the `vm_settings_history` table when the following conditions are met:

- A `vm_setting` with a value of `s1` is set lower than `5`.
- A `vm_setting` with a value of `s2` is set higher than `500`.

The rows inserted into the `vm_settings_history` table include all of the column values from the `vm_settings`
table, along with the `emp_id` of the employee who owns the VM and the current date.

Copy code

```
CREATE OR REPLACE PROCEDURE vm_user_settings()
  RETURNS VARCHAR
  LANGUAGE SQL
AS
DECLARE
  -- Declare a cursor and a variable
  c1 CURSOR FOR SELECT * FROM vm_settings;
  current_owner NUMBER;
BEGIN
  -- Open the cursor to execute the query and retrieve the rows into the cursor
  OPEN c1;
  -- Use a FOR loop to iterate over the records in the result set
  FOR record IN c1 DO
    -- Assign variable values using values in the current record
    LET current_vm_id NUMBER := record.vm_id;
    LET current_vm_setting VARCHAR := record.vm_setting;
    LET current_value NUMBER := record.value;
    -- Assign a value to the current_owner variable by querying the vm_ownership table
    SELECT emp_id INTO :current_owner
      FROM vm_ownership
      WHERE vm_id = :current_vm_id;
    -- If the record has a vm_setting equal to 's1', determine whether its value is less than 5
    IF (current_vm_setting = 's1' AND current_value < 5) THEN
      -- If the condition is met, insert a row into the vm_settings_history table
      INSERT INTO vm_settings_history VALUES (
        :current_vm_id,
        :current_vm_setting,
        :current_value,
        :current_owner,
        SYSDATE());
    -- If the record has a vm_setting equal to 's2', determine whether its value is greater than 500
    ELSEIF (current_vm_setting = 's2' AND current_value > 500) THEN
      -- If the condition is met, insert a row into the vm_settings_history table
      INSERT INTO vm_settings_history VALUES (
        :current_vm_id,
        :current_vm_setting,
        :current_value,
        :current_owner,
        SYSDATE());
    END IF;
  END FOR;
  -- Close the cursor
  CLOSE c1;
  -- Return text when the stored procedure completes
  RETURN 'Success';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE vm_user_settings()
  RETURNS VARCHAR
  LANGUAGE SQL
AS
$$
DECLARE
  -- Declare a cursor and a variable
  c1 CURSOR FOR SELECT * FROM vm_settings;
  current_owner NUMBER;
BEGIN
  -- Open the cursor to execute the query and retrieve the rows into the cursor
  OPEN c1;
  -- Use a FOR loop to iterate over the records in the result set
  FOR record IN c1 DO
    -- Assign variable values using values in the current record
    LET current_vm_id NUMBER := record.vm_id;
    LET current_vm_setting VARCHAR := record.vm_setting;
    LET current_value NUMBER := record.value;
    -- Assign a value to the current_owner variable by querying the vm_ownership table
    SELECT emp_id INTO :current_owner
      FROM vm_ownership
      WHERE vm_id = :current_vm_id;
    -- If the record has a vm_setting equal to 's1', determine whether its value is less than 5
    IF (current_vm_setting = 's1' AND current_value < 5) THEN
      -- If the condition is met, insert a row into the vm_settings_history table
      INSERT INTO vm_settings_history VALUES (
        :current_vm_id,
        :current_vm_setting,
        :current_value,
        :current_owner,
        SYSDATE());
    -- If the record has a vm_setting equal to 's2', determine whether its value is greater than 500
    ELSEIF (current_vm_setting = 's2' AND current_value > 500) THEN
      -- If the condition is met, insert a row into the vm_settings_history table
      INSERT INTO vm_settings_history VALUES (
        :current_vm_id,
        :current_vm_setting,
        :current_value,
        :current_owner,
        SYSDATE());
    END IF;
  END FOR;
  -- Close the cursor
  CLOSE c1;
  -- Return text when the stored procedure completes
  RETURN 'Success';
END;
$$;
```

Run the stored procedure:

Copy code

```
CALL vm_user_settings();
```

You can see the data that the procedure inserted into the `vm_settings_history` table by running
the following query:

Copy code

```
SELECT * FROM vm_settings_history ORDER BY vm_id;
```

```
+-------+------------+-------+-------+------------+
| VM_ID | VM_SETTING | VALUE | OWNER | DATE       |
|-------+------------+-------+-------+------------|
|     2 | s2         |   600 |  1003 | 2024-04-01 |
|     3 | s1         |     3 |  1002 | 2024-04-01 |
|     4 | s2         |   700 |  1003 | 2024-04-01 |
|     5 | s1         |     1 |  1001 | 2024-04-01 |
|     6 | s2         |   800 |  1003 | 2024-04-01 |
+-------+------------+-------+-------+------------+
```
