# Sentiment extraction

Note

AI\_SENTIMENT is the updated version of [ENTITY\_SENTIMENT](/sql-reference/functions/entity_sentiment-snowflake-cortex).
For the latest functionality, use AI\_SENTIMENT.

The AI\_SENTIMENT function provides state-of-the-art quality sentiment classification across diverse markets and
languages. With AI\_SENTIMENT, you can get both overall and granular, aspect based sentiment analysis for use cases like
the following:

- Social media monitoring
- Detailed product analysis
- Comprehensive brand perception studies
- Advanced market intelligence
- Employee engagement analysis
- Customer experience journey mapping
- Content performance analysis
- Customer support optimization

## Sentiment extraction quality

AI\_SENTIMENT uses a custom Snowflake large language model that delivers industry-leading overall sentiment and
aspect-based sentiment accuracy. The following table provides information on how AI\_SENTIMENT performs on Overall
Sentiment and Aspect Based Sentiment (ABSA-mix) benchmarks compared to popular models. The languages evaluated in the
multilingual benchmark are English, Spanish, French, German, Hindi, Italian, and Portuguese.

Note

Some of the models benchmarked are not available in Snowflake Cortex.

| Model | Aspect based sentiment accuracy (`ABSA-mix`) | Aspect based sentiment accuracy (`ABSA-multilingual`) | Overall sentiment accuracy | Overall sentiment accuracy (multilingual) |
| --- | --- | --- | --- | --- |
| Cortex AI `AI_SENTIMENT` | 0.92 | 0.81 | 0.83 | 0.83 |
| `claude-4-sonnet` | 0.84 | 0.79 | 0.75 | 0.82 |
| `mistral-large2` | 0.83 | 0.80 | 0.77 | 0.78 |
| `openai-gpt-4.1` | 0.83 | 0.73 | 0.80 | 0.78 |
| `llama4-scout` | 0.82 | 0.79 | 0.71 | 0.76 |
| `llama3.3-70b` | 0.82 | 0.79 | 0.71 | 0.76 |
| AWS `DetectSentiment` | - | - | 0.62 | 0.64 |

Expand

Show lessSee more

## Calling the AI\_SENTIMENT function

By default, Cortex AI\_SENTIMENT returns overall sentiment scores for the overall content. However, AI\_SENTIMENT can also
capture a spectrum of customer opinions beyond overall positive, negative, and neutral buckets. For this optional
aspect-based sentiment analysis, specify the content (such as a customer comment or a review) and the aspects (also
called entities or categories) for which you want to analyze sentiment. AI\_SENTIMENT returns sentiment for each entity
as well as an overall sentiment. To obtain only the overall sentiment, specify the content without aspects.

### English examples

The following example uses AI\_SENTIMENT to get the sentiment classification of a product review.

Copy code

```
SELECT AI_SENTIMENT('I went to the store, bought the leggings and exact same as shorts...
  they are expensive but i heard such great things. After wearing them twice i noticed a string popping out already.
  And aince i believed that they were this amazing luxury brand i didnt keep the receipt 😭 ');
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

The following example uses AI\_SENTIMENT to get the sentiment classification for specific aspects of a restaurant review.

Copy code

```
SELECT AI_SENTIMENT('A tourist\'s delight, in low urban light,
  Recommended gem, a pizza night sight. Swift arrival, a pleasure so right,
  Yet, pockets felt lighter, a slight pricey bite. 💰🍕🚀',
  ['Cost', 'Quality' ,'Wait Time']);
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

If some aspects that you specify do not apply to the text you provide, AI\_SENTIMENT returns “unknown” for those aspects,
as shown for Professionalism and Brand in the following example.

Copy code

```
SELECT AI_SENTIMENT('A tourist\'s delight, in low urban light,
  Recommended gem, a pizza night sight. Swift arrival, a pleasure so right,
  Yet, pockets felt lighter, a slight pricey bite. 💰🍕🚀',
  ['Cost', 'Professionalism' ,'Brand']);
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

### Multilingual examples

As shown in the following two similar examples, AI\_SENTIMENT can analyze sentiment in multiple languages, so you don’t
need to translate the text and risk losing an essential part of its meaning. You do not need to specify the language of
the text. Aspects can be specified in the language of the text, as shown in the following example, or in English, as
shown in the second example.

Note

AI\_SENTIMENT supports English, French, German, Hindi, Italian, Spanish, and Portuguese.

Example with both text and labels in Spanish:

Copy code

```
SELECT AI_SENTIMENT ('Pedí dos pares del mismo modelo en diferentes colores.
    Uno tenía defectos en la costura y el cuero se veía de menor calidad.
    Por 350€ el par, esto es inaceptable. El servicio al cliente tardó una
    semana en responder y la solución no fue satisfactoria. Es una pena porque
    cuando están bien hechos, son zapatos hermosos. Pero la inconsistencia en la
    calidad es preocupante.', ['Calidad', 'Calidad de Servicio,' 'Precio', 'Tiempo de Espera']);
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

Example with text in German and labels in English:

Copy code

```
SELECT AI_SENTIMENT ('Die Schuhe selbst sind wirklich schön und gut verarbeitet.
    Das Leder ist weich und die Passform stimmt. Allerdings gab es erhebliche
    Verzögerungen bei der Lieferung - statt der versprochenen 5 Tage hat es 3
    Wochen gedauert. Der Kundenservice war freundlich, aber nicht sehr hilfreich.
    Für 320€ erwarte ich besseren Service. Die Schuhe sind in Ordnung, aber das
    Gesamterlebnis war mittelmäßig', ['Quality', 'Price', 'Service', 'WaitTime']);
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

## Model restrictions

All large language models (LLMs) available in Snowflake Cortex AI have limitations on the total number of input and
output tokens, which is referred to as the model’s *context window*. Inputs exceeding the context window limit
result in an error. Output which would exceed the context window limit is truncated.

The context window for AI\_SENTIMENT is set such that the model can sustain a high level of accuracy. AI\_SENTIMENT was
trained and optimized for text inputs of 2,048 tokens (roughly 1,600 words). You can specify a maximum of ten aspects,
each no longer than thirty characters.

| Function | Context window (tokens) | Maximum number of entity labels |
| --- | --- | --- |
| AI\_SENTIMENT | 2,048 | 10 |

Expand

Show lessSee more
