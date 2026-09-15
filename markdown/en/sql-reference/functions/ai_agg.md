Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)
    [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_AGG

Reduces a column of text data using a natural language instruction.

For example, `AI_AGG(reviews, 'Describe the most common complaints mentioned in the book reviews')` will return a summary of user feedback.

Unlike [COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/complete-snowflake-cortex) and [AI\_SUMMARIZE](/sql-reference/functions/ai_summarize), this function supports datasets larger than the maximum language model context window.

See also:
:   [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg)

## Syntax

Copy code

```
AI_AGG( <expr>, <instruction> )
```

## Arguments

**Required:**

`expr`
:   This is an expression that contains text on which an aggregation operation is to be performed, such as restaurant reviews or phone transcripts.

`instruction`
:   A string containing a natural language specification of the aggregation to perform, for example “Summarize the reviews” or “Identify all people mentioned and write a short biography for each of them”.

## Returns

Returns a string containing the result of the aggregation.

The function may indicate that the data you’ve provided doesn’t contain the answer if:

- You don’t provide a clear instruction specifying how to aggregate the data
- The data doesn’t have the information necessary to complete your instruction

## Usage notes

For optimal performance, follow these guidelines:

- Use plain English text for the instruction.
- Provide a declarative instruction instead of asking a question. For example, instead of a question like “Can you summarize this?”, use “Summarize the phone call transcripts”.
- Describe the text provided in the instruction. For example, instead of an instruction like “summarize”, use “Summarize the phone call transcripts”.
- Describe the intended use case. For example, instead of “find the best review”, use “Find the most positive and well-written restaurant review to highlight on the restaurant website”.
- Multiple columns can be used in the string expression using `CONCAT` or the `||` operator. See the example below.
- Consider breaking the instruction into multiple steps. For example, instead of “Summarize the new articles”, use “You will be provided with news articles from various publishers presenting events from different points of view. Please create a concise and elaborative summary of source texts without missing any crucial information.”.

## Examples

AI\_AGG can be used as a simple scalar function on string constants. In the following example, AI\_AGG is used to
summarize product ratings, which are provided as a single string.

Copy code

```
SELECT AI_AGG('[Excellent, Excellent, Great, Mediocre]',
              'Summarize the product ratings for a blog post targeting consumers');
```

```
Overall, the product has received overwhelmingly positive reviews, with the majority of users rating it as 'Excellent' or 'Great'. Only a small percentage of users had a mediocre experience with the product. This suggests that the product is well-liked by most consumers and is a great option for those looking for a reliable choice.
```

AI\_AGG can also be used on a column of data. In the following example, the product ratings from the above example are provided as a column in a table using a [Common Table Expression](/user-guide/queries-cte).

Copy code

```
WITH reviews AS (
            SELECT 'The restaurant was excellent.' AS review
  UNION ALL SELECT 'Excellent! I loved the pizza!'
  UNION ALL SELECT 'It was great, but the service was meh.'
  UNION ALL SELECT 'Mediocre food and mediocre service'
)
SELECT AI_AGG(review, 'Summarize the restaurant reviews for potential consumers')
  FROM reviews;
```

```
Reviews for this restaurant are mixed. Some customers had a very positive experience, describing the restaurant as "excellent" and loving the pizza. However, others had a more neutral or negative experience, citing mediocre food and service.
```

AI\_AGG can be used on multiple columns of data using `CONCAT` or the `||` operator.

Copy code

```
WITH reviews AS (
            SELECT 'The restaurant was excellent.' AS review, 'Pizza' AS menu_item
  UNION ALL SELECT 'Excellent! I loved the pizza!', 'Pizza'
  UNION ALL SELECT 'It was great, but the service was meh.', 'Burger'
  UNION ALL SELECT 'Mediocre food and mediocre service', 'Pancakes'
)
SELECT AI_AGG('Menu Item: ' || menu_item || '\nReview: ' || review,
              'Summarize the restaurant reviews for potential consumers')
  FROM reviews;
```

```
Based on the reviews, the restaurant seems to receive high praise for their pizza, with two reviews using the word "excellent" to describe their experience. However, the reviews for other menu items, such as burgers and pancakes, are more mixed, with some customers expressing disappointment with the service or finding the food to be just mediocre. Overall, potential consumers may want to consider ordering pizza if they decide to dine at this restaurant.
```

AI\_AGG can also be used in combination with GROUP BY. The following example summarizes product ratings for two products (identified by the column `product_id`) in a table of reviews.

Copy code

```
WITH reviews AS (
            SELECT 1 AS restaurant_id, 'The restaurant was excellent.' AS review
  UNION ALL SELECT 1, 'Excellent! I loved the pizza!'
  UNION ALL SELECT 1, 'It was great, but the service was meh.'
  UNION ALL SELECT 1, 'Mediocre food and mediocre service'
  UNION ALL SELECT 2, 'Terrible quality ingredients, I should have eaten at home.'
  UNION ALL SELECT 2, 'Bad restaurant, I would avoid this place.'
)
SELECT restaurant_id,
       AI_AGG(review, 'Summarize the restaurant reviews for potential consumers')
  FROM reviews
 GROUP BY 1;
```

```
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| RESTAURANT_ID | SUMMARIZED_REVIEW                                                                                                                                                                                                                                 |
|---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1             | Reviews for this restaurant are mixed. Some customers had a very positive experience, describing the restaurant as "excellent" and loving the pizza. However, others had a more neutral or negative experience, citing mediocre food and service. |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 2             | Two reviewers had extremely negative experiences at this restaurant, citing poor quality ingredients and advising others to avoid it.                                                                                                             |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

The instruction can be used for various aggregation tasks and to configure the style and tone of the response. The following example uses an instruction to find the most positive rating for each product and provide
French and Polish translations of the rating.

Copy code

```
WITH reviews AS (
            SELECT 1 AS product_id, 'Excellent' AS review
  UNION ALL SELECT 1, 'Excellent'
  UNION ALL SELECT 1, 'Great'
  UNION ALL SELECT 1, 'Mediocre'
  UNION ALL SELECT 2, 'Terrible'
  UNION ALL SELECT 2, 'Bad'
  UNION ALL SELECT 2, 'Average'
)
SELECT product_id,
       AI_AGG(review, 'Identify the most positive rating and translate it into French and Polish, one word only') AS summarized_review
  FROM reviews
 GROUP BY 1;
```

```
+------------+--------------------+
| PRODUCT_ID | SUMMARIZED_REVIEW  |
|------------+--------------------+
| 1          | French: Excellent  |
|            | Polish: Doskonały  |
+------------+--------------------+
| 2          | French: Moyen      |
|            | Polish: Przeciętny |
+------------+--------------------+
```

See also [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg).

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.
