# Nov 21, 2025: AI\_COMPLETE function (*General availability*)

The AI\_COMPLETE function is now generally available. AI\_COMPLETE generates responses (completions) from prompts, using
your choice of large language model (LLM). AI\_COMPLETE is the most general Cortex AI Function; it is not specialized for
a particular use case, such as summarization or classification. Instead, it can generate a wide variety of responses
based on the provided content and instructions given in the prompt. Responses can be plain text or semi-structured data.

Prompts can contain text and one or more images, which are processed according to the plain English instructions you
provide. For example:

- Explain the concept of a large language model to a five year old.
- Assess the reading level of a given piece of text and simplify it to a target level.
- Critique the writing style of the provided text as bullet points.
- Estimate the star rating for a product based on the provided customer review.
- Compare two advertising creatives and describe the differences between them, in terms of content, style, and mood.
- Determine which of the countries in a graph of inflation rates has the highest rate.
- Identify the kithen appliances in an image and provide a brief description of each.
- Extract all the stock symbols and corresponding prices mentioned in an article as a JSON object.

The AI\_COMPLETE function is the updated version of the SNOWFLAKE.CORTEX.COMPLETE function. Use AI\_COMPLETE to take
advantage of the latest capabilities and models.

For more information about using the AI\_COMPLETE function, see [AI\_COMPLETE](/sql-reference/functions/ai_complete).
