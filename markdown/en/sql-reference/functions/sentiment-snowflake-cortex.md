Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# SENTIMENT (SNOWFLAKE.CORTEX)

Returns an overall sentiment score for the given English-language input text.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.SENTIMENT(<text>)
```

## Arguments

`text`
:   A string containing the text for which a sentiment score should be calculated.

## Returns

A floating-point number from -1 to 1 (inclusive) indicating the model’s level of certainty of any detected sentiment. A
score close to 0 indicates that the function could not determine a clear sentiment in the text; this result can be
considered neutral. A score close to 1 indicates positive sentiment, while a score close to -1 indicates negative
sentiment. The chart below provides guidance on how to interpret the sentiment scores:

| Sentiment | Sentiment Score |
| --- | --- |
| Positive | 0.5 to 1 |
| Neutral | -0.5 to 0.5 |
| Negative | -0.5 to -1 |

Expand

Show lessSee more

The result *does not* indicate the intensity of sentiment, but the polarity (positive, neutral, or negative) and certainty.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Examples

The following example uses SENTIMENT to get the sentiment classification of a food service review, which we can infer
as modestly positive, given the score of 0.54.

Copy code

```
SELECT SNOWFLAKE.CORTEX.SENTIMENT('A tourist\'s delight, in low urban light,
  Recommended gem, a pizza night sight. Swift arrival, a pleasure so right,
  Yet, pockets felt lighter, a slight pricey bite. 💰🍕🚀');
```

Response:

```
0.5424458
```

In the following example, a table named `reviews` contains a column named `review_content` containing the text of reviews
submitted by users. The query returns a sentiment score for each review.

Copy code

```
SELECT SNOWFLAKE.CORTEX.SENTIMENT(review_content), review_content FROM reviews LIMIT 10;
```

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
