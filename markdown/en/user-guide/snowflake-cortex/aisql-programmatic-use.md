# Using Cortex AI Functions with Python and Snow CLI

You can call Cortex AI Functions from Python (via the Snowpark Python API or Snowflake ML) and from the Snowflake CLI.
Use one of these entry points when you want to integrate AI Functions into application code or scripts rather than
running them as SQL statements.

## Call Cortex AI Functions in Snowpark Python

You can use Snowflake Cortex AI Functions in the Snowpark Python API. These functions include the following. Note that the functions in Snowpark Python have names in Pythonic “snake\_case”
format, with words separated by underscores and all letters in lowercase.

- [ai\_agg](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ai_agg)
- [ai\_classify](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ai_classify)
- [ai\_complete](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ai_complete)
- [ai\_filter](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ai_filter)
- [ai\_similarity](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ai_similarity)
- [ai\_summarize\_agg](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ai_summarize_agg)

### `ai_agg` example

The `ai_agg` function aggregates a column of text using natural language instructions in a similar manner to how you would ask an analyst to summarize or extract findings from grouped or ungrouped data.

The following example summarizes customer reviews for each product using the `ai_agg` function. The function takes a column of text and a natural language instruction to summarize the reviews.

Copy code

```
from snowflake.snowpark.functions import ai_agg, col

df = session.create_dataframe([
    [1, "Excellent product!"],
    [1, "Great battery life."],
    [1, "A bit expensive but worth it."],
    [2, "Terrible customer service."],
    [2, "Won’t buy again."],
], schema=["product_id", "review"])

# Summarize reviews per product
summary_df = df.group_by("product_id").agg(
    ai_agg(col("review"), "Summarize the customer reviews in one sentence.")
)
summary_df.show()
```

Note

Use task descriptions that are detailed and centered on the use case. For example, “Summarize the customer feedback for an investor report”.

### Classify text with `ai_classify`

The `ai_classify` function takes a string or image and classifies it into the categories that you define.

The following example classifies travel reviews into categories such as “travel” and “cooking”. The function takes a column of text and a list of categories to classify the text into.

Copy code

```
from snowflake.snowpark.functions import ai_classify, col

df = session.create_dataframe([
    ["I dream of backpacking across South America."],
    ["I made the best pasta yesterday."],
], schema=["sentence"])

df = df.select(
    "sentence",
    ai_classify(col("sentence"), ["travel", "cooking"]).alias("classification")
)
df.show()
```

### Filter rows with `ai_filter`

The `ai_filter` function evaluates a natural language condition and returns `True` or `False`. You can use it to filter or tag rows.

Copy code

```
from snowflake.snowpark.functions import ai_filter, prompt, col

df = session.create_dataframe(["Canada", "Germany", "Japan"], schema=["country"])

filtered_df = df.select(
    "country",
    ai_filter(prompt("Is {0} in Asia?", col("country"))).alias("is_in_asia")
)
filtered_df.show()
```

Note

You can filter on both strings and files. For dynamic prompts, use the `prompt` function.
For more information, see
[Snowpark Python reference](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/index).

## Call Cortex AI Functions in Snowflake ML

[Snowflake ML](/developer-guide/snowflake-ml/overview) contains the older AI Functions, those with names that don’t
begin with “AI”. These functions are supported in version 1.1.2 and later of Snowflake ML. The names are rendered in Pythonic
“snake\_case” format, with words separated by underscores and all letters in lowercase.

If you run your Python script outside of Snowflake, you must create a Snowpark session to use these functions. See
[Connecting to Snowflake](/developer-guide/snowflake-ml/snowpark-ml#label-snowpark-ml-authenticating) for instructions.

### Process single values

The following Python example illustrates calling Snowflake Cortex AI functions on single values:

Copy code

```
from snowflake.cortex import complete, extract_answer, sentiment, summarize, translate

text = """
    The Snowflake company was co-founded by Thierry Cruanes, Marcin Zukowski,
    and Benoit Dageville in 2012 and is headquartered in Bozeman, Montana.
"""

print(complete("llama3.1-8b", "how do snowflakes get their unique patterns?"))
print(extract_answer(text, "When was snowflake founded?"))
print(sentiment("I really enjoyed this restaurant. Fantastic service!"))
print(summarize(text))
print(translate(text, "en", "fr"))
```

### Pass hyperparameter options

You can pass options that affect the model’s hyperparameters when using the `complete` function. The following
Python example illustrates modifying the maximum number of output tokens that the model can generate:

Copy code

```
from snowflake.cortex import complete, CompleteOptions

model_options1 = CompleteOptions(
    {'max_tokens':30}
)

print(complete("llama3.1-8b", "how do snowflakes get their unique patterns?", options=model_options1))
```

### Call functions on table columns

You can call an AI function on a table column, as shown below. This example requires a session object (stored in
`session`) and a table `articles` containing a text column `abstract_text`, and creates a new column
`abstract_summary` containing a summary of the abstract.

Copy code

```
from snowflake.cortex import summarize
from snowflake.snowpark.functions import col

article_df = session.table("articles")
article_df = article_df.withColumn(
    "abstract_summary",
    summarize(col("abstract_text"))
)
article_df.collect()
```

Note

The advanced chat-style (multi-message) form of COMPLETE is not currently supported in Snowflake ML Python.

## Using Snowflake Cortex AI functions with Snowflake CLI

Snowflake Cortex AI Functions are available in [Snowflake CLI](/developer-guide/snowflake-cli/index) version 2.4.0
and later. See [Introducing Snowflake CLI](/developer-guide/snowflake-cli/introduction/introduction) for more information about using Snowflake CLI.
The functions are the old-style functions, those with names that don’t begin with “AI”.

The following examples illustrate using the `snow cortex` commands on single values. The `-c` parameter specifies which connection to use.

Note

The advanced chat-style (multi-message) form of COMPLETE is not currently supported in Snowflake CLI.

Copy code

```
snow cortex complete "Is 5 more than 4? Please answer using one word without a period." -c "snowhouse"
```

Copy code

```
snow cortex extract-answer "what is snowflake?" "snowflake is a company" -c "snowhouse"
```

Copy code

```
snow cortex sentiment "Mary had a little Lamb" -c "snowhouse"
```

Copy code

```
snow cortex summarize "John has a car. John's car is blue. John's car is old and John is thinking about buying a new car. There are a lot of cars to choose from and John cannot sleep because it's an important decision for John."
```

Copy code

```
snow cortex translate herb --to pl
```

You can also use files that contain the text you want to use for the commands. For this example, assume that the file `about_cortex.txt` contains the following content:

```
Snowflake Cortex gives you instant access to industry-leading large language models (LLMs) trained by researchers at companies like Anthropic, Mistral, Reka, Meta, and Google.

Since these LLMs are fully hosted and managed by Snowflake, using them requires no setup. Your data stays within Snowflake, giving you the performance, scalability, and governance you expect.

Snowflake Cortex features are provided as SQL functions and are also available in Python. The available functions are summarized below.

COMPLETE: Given a prompt, returns a response that completes the prompt. This function accepts either a single prompt or a conversation with multiple prompts and responses.
EMBED_TEXT_768: Given a piece of text, returns a vector embedding that represents that text.
EXTRACT_ANSWER: Given a question and unstructured data, returns the answer to the question if it can be found in the data.
SENTIMENT: Returns a sentiment score, from -1 to 1, representing the detected positive or negative sentiment of the given text.
SUMMARIZE: Returns a summary of the given text.
TRANSLATE: Translates given text from any supported language to any other.
```

You can then execute the `snow cortex summarize` command by passing in the filename using the `--file` parameter, as shown:

Copy code

```
snow cortex summarize --file about_cortex.txt
```

```
Snowflake Cortex offers instant access to industry-leading language models with SQL functions for completing prompts (COMPLETE), text embedding (EMBED\_TEXT\_768), extracting answers (EXTRACT\_ANSWER), sentiment analysis (SENTIMENT), summarizing text (SUMMARIZE), and translating text (TRANSLATE).
```

For more information about these commands, see [snow cortex commands](/developer-guide/snowflake-cli/command-reference/cortex-commands/overview).
