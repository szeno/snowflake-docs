# Python user-defined aggregate functions

User-defined aggregate functions (UDAFs) take one or more rows as input and produce a single row of output.
They operate on values across multiple rows to perform mathematical calculations such as sum, average, counting,
finding minimum or maximum values, standard deviation, and estimation, as well as some non-mathematical operations.

Python UDAFs provide a way for you to write your own aggregate functions that are similar to the Snowflake system-defined
SQL [aggregate functions](/sql-reference/functions-aggregation).

You can also create your own UDAFs using Snowpark APIs as described in [Creating User-Defined Aggregate Functions (UDAFs) for DataFrames in Python](/developer-guide/snowpark/python/creating-udafs).

## Limitations

- The `aggregate_state` has a maximum size of 64 MB in a serialized version, so try to control the size of the aggregate state.
- You can’t call a UDAF as a [window function](/sql-reference/functions-window) (in other words, with an OVER clause).
- IMMUTABLE is not supported on an aggregate function (when you use the AGGREGATE parameter). Therefore, all aggregate functions are
  VOLATILE by default.
- User-defined aggregate functions cannot be used in conjunction with the WITHIN GROUP clause. Queries will fail to execute.

## Interface for aggregate function handler

An aggregate function aggregates state in child nodes and then, eventually, those aggregate states are serialized and sent to the parent
node where they get merged and the final result is calculated.

To define an aggregate function, you must define a Python class (which is the function’s handler) that includes methods that Snowflake
invokes at run time. Those methods are described in the table below. See examples elsewhere in this topic.

| Method | Requirement | Description |
| --- | --- | --- |
| `__init__` | Required | Initializes the internal state of an aggregate. |
| `aggregate_state` | Required | Returns the current state of an aggregate.   - The method must have a [@property decorator](https://docs.python.org/3.12/library/functions.html#property). - An aggregate state object can be any Python data type serializable by the   [Python pickle library](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled). - For simple aggregate states, use a primitive Python data type. For more complex aggregate states, use   [Python data classes](https://docs.python.org/3/library/dataclasses.html). |
| `accumulate` | Required | Accumulates the state of the aggregate based on the new input row. |
| `merge` | Required | Combines two intermediate aggregated states. |
| `finish` | Required | Produces the final result based on the aggregated state. |

Expand

Show lessSee more

![Diagram showing input values being accumulated in child nodes and then being sent to a parent node and merged to produce a final result.](/static/images/aggregate-function-diagram.png)

## Example: Calculate a sum

Code in the following example defines a `python_sum` user-defined aggregate function (UDAF) to return the sum of the numeric values.

1. Create the UDAF.

   Copy code

   ```
   CREATE OR REPLACE AGGREGATE FUNCTION PYTHON_SUM(a INT)
     RETURNS INT
     LANGUAGE PYTHON
     RUNTIME_VERSION = 3.12
     HANDLER = 'PythonSum'
   AS $$
   class PythonSum:
     def __init__(self):
    # This aggregate state is a primitive Python data type.
    self._partial_sum = 0

     @property
     def aggregate_state(self):
    return self._partial_sum

     def accumulate(self, input_value):
    self._partial_sum += input_value

     def merge(self, other_partial_sum):
    self._partial_sum += other_partial_sum

     def finish(self):
    return self._partial_sum
   $$;
   ```
2. Create a table of test data.

   Copy code

   ```
   CREATE OR REPLACE TABLE sales(item STRING, price INT);

   INSERT INTO sales VALUES ('car', 10000), ('motorcycle', 5000), ('car', 7500), ('motorcycle', 3500), ('motorcycle', 1500), ('car', 20000);

   SELECT * FROM sales;
   ```
3. Call the `python_sum` UDAF.

   Copy code

   ```
   SELECT python_sum(price) FROM sales;
   ```
4. Compare results with the output of the Snowflake system-defined SQL function, [SUM](/sql-reference/functions/sum), and see that the result
   is the same.

   Copy code

   ```
   SELECT sum(col) FROM sales;
   ```
5. Group by sum values by the item type in the sales table.

   Copy code

   ```
   SELECT item, python_sum(price) FROM sales GROUP BY item;
   ```

## Example: Calculate an average

Code in the following example defines a `python_avg` user-defined aggregate function to return the average of the numeric values.

1. Create the function.

   Copy code

   ```
   CREATE OR REPLACE AGGREGATE FUNCTION python_avg(a INT)
     RETURNS FLOAT
     LANGUAGE PYTHON
     RUNTIME_VERSION = 3.12
     HANDLER = 'PythonAvg'
   AS $$
   from dataclasses import dataclass

   @dataclass
   class AvgAggState:
    count: int
    sum: int

   class PythonAvg:
    def __init__(self):
        # This aggregate state is an object data type.
        self._agg_state = AvgAggState(0, 0)

    @property
    def aggregate_state(self):
        return self._agg_state

    def accumulate(self, input_value):
        sum = self._agg_state.sum
        count = self._agg_state.count

        self._agg_state.sum = sum + input_value
        self._agg_state.count = count + 1

    def merge(self, other_agg_state):
        sum = self._agg_state.sum
        count = self._agg_state.count

        other_sum = other_agg_state.sum
        other_count = other_agg_state.count

        self._agg_state.sum = sum + other_sum
        self._agg_state.count = count + other_count

    def finish(self):
        sum = self._agg_state.sum
        count = self._agg_state.count
        return sum / count
   $$;
   ```
2. Create a table of test data.

   Copy code

   ```
   CREATE OR REPLACE TABLE sales(item STRING, price INT);
   INSERT INTO sales VALUES ('car', 10000), ('motorcycle', 5000), ('car', 7500), ('motorcycle', 3500), ('motorcycle', 1500), ('car', 20000);
   ```
3. Call the `python_avg` user-defined function.

   Copy code

   ```
   SELECT python_avg(price) FROM sales;
   ```
4. Compare results with the output of the Snowflake system-defined SQL function, [AVG](/sql-reference/functions/avg), and see that the
   result is the same.

   Copy code

   ```
   SELECT avg(price) FROM sales;
   ```
5. Group average values by the item type in the sales table.

   Copy code

   ```
   SELECT item, python_avg(price) FROM sales GROUP BY item;
   ```

## Example: Return only unique values

Code in the following example takes an array and returns an array containing only the unique values.

Copy code

```
CREATE OR REPLACE AGGREGATE FUNCTION pythonGetUniqueValues(input ARRAY)
  RETURNS ARRAY
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'PythonGetUniqueValues'
AS $$
class PythonGetUniqueValues:
    def __init__(self):
        self._agg_state = set()

    @property
    def aggregate_state(self):
        return self._agg_state

    def accumulate(self, input):
        self._agg_state.update(input)

    def merge(self, other_agg_state):
        self._agg_state.update(other_agg_state)

    def finish(self):
        return list(self._agg_state)
$$;
```

Copy code

```
CREATE OR REPLACE TABLE array_table(x array) AS
SELECT ARRAY_CONSTRUCT(0, 1, 2, 3, 4, 'foo', 'bar', 'snowflake') UNION ALL
SELECT ARRAY_CONSTRUCT(1, 3, 5, 7, 9, 'foo', 'barbar', 'snowpark') UNION ALL
SELECT ARRAY_CONSTRUCT(0, 2, 4, 6, 8, 'snow');

SELECT * FROM array_table;

SELECT pythonGetUniqueValues(x) FROM array_table;
```

## Example: Return a count of strings

Code in the following example returns counts of all instances of strings in an object.

Copy code

```
CREATE OR REPLACE AGGREGATE FUNCTION pythonMapCount(input STRING)
  RETURNS OBJECT
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'PythonMapCount'
AS $$
from collections import defaultdict

class PythonMapCount:
    def __init__(self):
        self._agg_state = defaultdict(int)

    @property
    def aggregate_state(self):
        return self._agg_state

    def accumulate(self, input):
        # Increment count of lowercase input
        self._agg_state[input.lower()] += 1

    def merge(self, other_agg_state):
        for item, count in other_agg_state.items():
            self._agg_state[item] += count

    def finish(self):
        return dict(self._agg_state)
$$;
```

Copy code

```
CREATE OR REPLACE TABLE string_table(x STRING);
INSERT INTO string_table SELECT 'foo' FROM TABLE(GENERATOR(ROWCOUNT => 1000));
INSERT INTO string_table SELECT 'bar' FROM TABLE(GENERATOR(ROWCOUNT => 2000));
INSERT INTO string_table SELECT 'snowflake' FROM TABLE(GENERATOR(ROWCOUNT => 50));
INSERT INTO string_table SELECT 'snowpark' FROM TABLE(GENERATOR(ROWCOUNT => 123));
INSERT INTO string_table SELECT 'SnOw' FROM TABLE(GENERATOR(ROWCOUNT => 1));
INSERT INTO string_table SELECT 'snow' FROM TABLE(GENERATOR(ROWCOUNT => 4));

SELECT pythonMapCount(x) FROM string_table;
```

## Example: Return top k largest values

Code in the following example returns a list of the top largest values for `k`. The code accumulates negated input values on a min
heap, then returns the top `k` largest values.

Copy code

```
CREATE OR REPLACE AGGREGATE FUNCTION pythonTopK(input INT, k INT)
  RETURNS ARRAY
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'PythonTopK'
AS $$
import heapq
from dataclasses import dataclass
import itertools
from typing import List

@dataclass
class AggState:
    minheap: List[int]
    k: int

class PythonTopK:
    def __init__(self):
        self._agg_state = AggState([], 0)

    @property
    def aggregate_state(self):
        return self._agg_state

    @staticmethod
    def get_top_k_items(minheap, k):
      # Return k smallest elements if there are more than k elements on the min heap.
      if (len(minheap) > k):
        return [heapq.heappop(minheap) for i in range(k)]
      return minheap

    def accumulate(self, input, k):
        self._agg_state.k = k

        # Store the input as negative value, as heapq is a min heap.
        heapq.heappush(self._agg_state.minheap, -input)

        # Store only top k items on the min heap.
        self._agg_state.minheap = self.get_top_k_items(self._agg_state.minheap, k)

    def merge(self, other_agg_state):
        k = self._agg_state.k if self._agg_state.k > 0 else other_agg_state.k

        # Merge two min heaps by popping off elements from one and pushing them onto another.
        while(len(other_agg_state.minheap) > 0):
            heapq.heappush(self._agg_state.minheap, heapq.heappop(other_agg_state.minheap))

        # Store only k elements on the min heap.
        self._agg_state.minheap = self.get_top_k_items(self._agg_state.minheap, k)

    def finish(self):
        return [-x for x in self._agg_state.minheap]
$$;
```

Copy code

```
CREATE OR REPLACE TABLE numbers_table(num_column INT);
INSERT INTO numbers_table SELECT 5 FROM TABLE(GENERATOR(ROWCOUNT => 10));
INSERT INTO numbers_table SELECT 1 FROM TABLE(GENERATOR(ROWCOUNT => 10));
INSERT INTO numbers_table SELECT 9 FROM TABLE(GENERATOR(ROWCOUNT => 10));
INSERT INTO numbers_table SELECT 7 FROM TABLE(GENERATOR(ROWCOUNT => 10));
INSERT INTO numbers_table SELECT 10 FROM TABLE(GENERATOR(ROWCOUNT => 10));
INSERT INTO numbers_table SELECT 3 FROM TABLE(GENERATOR(ROWCOUNT => 10));

-- Return top 15 largest values from numbers_table.
SELECT pythonTopK(num_column, 15) FROM numbers_table;
```
