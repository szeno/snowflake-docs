Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_SENTIMENT

AI\_SENTIMENT provides sentiment classification across diverse markets and languages. It uses a custom
Snowflake large language model to return overall sentiment for a piece of text and, optionally,
aspect-based (also called category-based or entity-based) sentiment for specific topics that you specify.

Common use cases include:

- Social media monitoring
- Detailed product analysis
- Comprehensive brand perception studies
- Advanced market intelligence
- Employee engagement analysis
- Customer experience journey mapping
- Content performance analysis
- Customer support optimization

## Syntax

Copy code

```
AI_SENTIMENT( <text> [ , <categories> ] [, <return_error_details> ] )
```

## Arguments

**Required:**

`text`
:   A string containing the text in which sentiment is detected.

**Optional:**

`categories`
:   An array containing up to ten categories (also called entities or aspects) for which sentiment should be extracted. Each category is a
    string. For example, if extracting sentiment from a restaurant review, you might specify
    `['cost', 'quality', 'service', 'wait time']` as the categories. Each category may be a maximum of 30 characters long.

    If you do not provide this argument, AI\_SENTIMENT returns only the overall sentiment.

`return_error_details`
:   A BOOLEAN flag that indicates whether to return error details in case of error. When set to TRUE, the function returns
    an OBJECT that contains the value and the error message, one of which is NULL depending on whether the function
    succeeded or failed. See [Error behavior](#error-behavior) for details.

## Returns

An OBJECT value containing a `categories` field. `categories` is an array of category records. Each category includes these fields:

- `name`: The name of the category. The category names match the categories specified in the `categories` argument.
- `sentiment`: The sentiment of the category. Each sentiment result is one of the following strings.
  - `unknown`: The category was not mentioned in the text.
  - `positive`: The category was mentioned positively in the text.
  - `negative`: The category was mentioned negatively in the text.
  - `neutral`: The category was mentioned in the text, but neither positively nor negatively.
  - `mixed`: The category was mentioned both positively and negatively in the text.

The `overall` category record is always included and contains the overall sentiment of the text.

Example:

```
{
  "categories": [
    {
      "name": "overall",
      "sentiment": "mixed"
    },
    {
      "name": "Brand",
      "sentiment": "unknown"
    },
    {
      "name": "Cost",
      "sentiment": "negative"
    },
    {
      "name": "Professionalism",
      "sentiment": "unknown"
    }
  ]
}
```

## Error behavior

By default, if AI\_SENTIMENT can’t process the input, the function returns NULL. If the query processes multiple rows,
rows with errors return NULL and don’t prevent the query from completing.

The return value on error depends on the `return_error_details`
argument. The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value` and `error` fields | `value`: An OBJECT containing the sentiment analysis result, or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. |
>
> Expand
>
> Show lessSee more

For more information about error handling for AI functions, see [Snowflake Cortex AI Function: Multirow error handling improvements](/release-notes/bcr-bundles/2026_02/bcr-2184).

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this role.

## Usage notes

- **Supported languages:** AI\_SENTIMENT can analyze sentiment in English, French, German, Hindi, Italian, Spanish, and
  Portuguese. Aspects can be specified in the language of the text or in English.
- **Context window:** AI\_SENTIMENT is optimized for text inputs of 2,048 tokens (roughly 1,600 words). Inputs that
  exceed the context window return an error; outputs that would exceed the context window are truncated.
- **Aspect limits:** You can specify a maximum of ten aspects, each no longer than 30 characters.

| Function | Context window (tokens) | Maximum number of entity labels |
| --- | --- | --- |
| AI\_SENTIMENT | 2,048 | 10 |

Expand

Show lessSee more

## Examples

### Get the overall sentiment of text

The following example uses AI\_SENTIMENT to get the overall sentiment of a product review.

Copy code

```
SELECT AI_SENTIMENT('I went to the store, bought the leggings and exact same as shorts...
  they are expensive but i heard such great things. After wearing them twice i noticed a string popping out already.
  And since i believed that they were this amazing luxury brand i didnt keep the receipt 😭 ');
```

Return value:

```
{
  "categories": [
    {
      "name": "overall",
      "sentiment": "mixed"
    }
  ]
}
```

### Get aspect-based sentiment

Specify one or more aspects to get aspect-based sentiment in addition to the overall sentiment. The following example
uses AI\_SENTIMENT to get the sentiment classification for specific aspects of a restaurant review.

Copy code

```
SELECT AI_SENTIMENT('A tourist\'s delight, in low urban light,
  Recommended gem, a pizza night sight. Swift arrival, a pleasure so right,
  Yet, pockets felt lighter, a slight pricey bite. 💰🍕🚀',
  ['Cost', 'Quality', 'Wait Time']);
```

Return value:

```
{
  "categories": [
    {
      "name": "overall",
      "sentiment": "mixed"
    },
    {
      "name": "Cost",
      "sentiment": "negative"
    },
    {
      "name": "Quality",
      "sentiment": "positive"
    },
    {
      "name": "Wait Time",
      "sentiment": "positive"
    }
  ]
}
```

If some aspects that you specify do not apply to the text you provide, AI\_SENTIMENT returns `unknown` for those aspects,
as shown for `Professionalism` and `Brand` in the following example.

Copy code

```
SELECT AI_SENTIMENT('A tourist\'s delight, in low urban light,
  Recommended gem, a pizza night sight. Swift arrival, a pleasure so right,
  Yet, pockets felt lighter, a slight pricey bite. 💰🍕🚀',
  ['Cost', 'Professionalism', 'Brand']);
```

Return value:

```
{
  "categories": [
    {
      "name": "overall",
      "sentiment": "mixed"
    },
    {
      "name": "Brand",
      "sentiment": "unknown"
    },
    {
      "name": "Cost",
      "sentiment": "negative"
    },
    {
      "name": "Professionalism",
      "sentiment": "unknown"
    }
  ]
}
```

### Analyze multiple reviews from a table

In this example, a table named `reviews` contains a column named `review_content` containing the text of movie reviews
submitted by users. The query returns the sentiment of several facets of up to ten reviews.

Copy code

```
SELECT
  AI_SENTIMENT(
    review_content,
    ['concept', 'performance', 'script', 'cinematography', 'soundtrack']
  ),
  review_content
  FROM reviews LIMIT 10;
```

### Multilingual sentiment analysis

AI\_SENTIMENT can analyze sentiment in multiple languages, so you don’t need to translate the text and risk losing an
essential part of its meaning. You do not need to specify the language of the text. Aspects can be specified in the
language of the text or in English.

The following example has both text and labels in Spanish:

Copy code

```
SELECT AI_SENTIMENT ('Pedí dos pares del mismo modelo en diferentes colores.
    Uno tenía defectos en la costura y el cuero se veía de menor calidad.
    Por 350€ el par, esto es inaceptable. El servicio al cliente tardó una
    semana en responder y la solución no fue satisfactoria. Es una pena porque
    cuando están bien hechos, son zapatos hermosos. Pero la inconsistencia en la
    calidad es preocupante.',
    ['Calidad', 'Calidad de Servicio', 'Precio', 'Tiempo de Espera']);
```

Return value:

```
{
  "categories": [
    {
      "name": "overall",
      "sentiment": "negative"
    },
    {
      "name": "Calidad",
      "sentiment": "negative"
    },
    {
      "name": "Calidad de Servicio",
      "sentiment": "negative"
    },
    {
      "name": "Precio",
      "sentiment": "negative"
    },
    {
      "name": "Tiempo de Espera",
      "sentiment": "negative"
    }
  ]
}
```

The following example has text in German and labels in English:

Copy code

```
SELECT AI_SENTIMENT ('Die Schuhe selbst sind wirklich schön und gut verarbeitet.
    Das Leder ist weich und die Passform stimmt. Allerdings gab es erhebliche
    Verzögerungen bei der Lieferung - statt der versprochenen 5 Tage hat es 3
    Wochen gedauert. Der Kundenservice war freundlich, aber nicht sehr hilfreich.
    Für 320€ erwarte ich besseren Service. Die Schuhe sind in Ordnung, aber das
    Gesamterlebnis war mittelmäßig',
    ['Quality', 'Price', 'Service', 'WaitTime']);
```

Return value:

```
{
  "categories": [
    {
      "name": "overall",
      "sentiment": "mixed"
    },
    {
      "name": "Price",
      "sentiment": "neutral"
    },
    {
      "name": "Quality",
      "sentiment": "positive"
    },
    {
      "name": "Service",
      "sentiment": "neutral"
    },
    {
      "name": "WaitTime",
      "sentiment": "negative"
    }
  ]
}
```

## Regional availability

AI\_SENTIMENT is available in the following regions:

| Function (Model) | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) | Azure East US 2 (Virginia) | Azure West Europe (Netherlands) | AWS (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI\_SENTIMENT | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

Note

AI\_SENTIMENT is the updated version of [ENTITY\_SENTIMENT](/sql-reference/functions/entity_sentiment-snowflake-cortex).
For the latest functionality, use AI\_SENTIMENT.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
