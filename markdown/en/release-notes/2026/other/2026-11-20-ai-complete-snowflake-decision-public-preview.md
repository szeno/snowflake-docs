# Nov 20, 2026: AI\_COMPLETE adds support for Snowflake Decision (*Preview*)

Snowflake Cortex [AI\_COMPLETE](/sql-reference/functions/ai_complete) now supports Snowflake Decision in public preview,
a purpose-built model designed for high-throughput classification, scoring, and decision-making across massive datasets.
Snowflake Decision enables organizations to evaluate unstructured data against predefined criteria and return structured
answers with probabilities and confidence values, making it easier to automate routing, prioritization, and processing
workflows directly in Snowflake.

Key capabilities include:

- **High-throughput, cost-effective processing:** Evaluate large volumes of data at just $0.042 per million tokens,
  with approximately 1.58 milliseconds of processing time per row.
- **Flexible classification and scoring:** Classify content into predefined categories, evaluate information against
  ordered scoring criteria, and assess the probability that a statement is true.
- **Multiple assessments in a single request:** Evaluate content against multiple independent criteria in one
  AI\_COMPLETE call, reducing the need for separate model requests.
- **Confidence-based decision-making:** Use returned probabilities and confidence values to guide automated workflows,
  route uncertain results for human review, or trigger fallback processing.
- **Scalable AI-powered workflows:** Apply classification and scoring across Snowflake tables using SQL to support use
  cases such as support ticket prioritization, document classification, customer feedback analysis, and agent routing.
- **Seamless integration with Cortex AI Functions:** Combine Snowflake Decision with functions such as AI\_TRANSCRIBE,
  AI\_PARSE\_DOCUMENT, AI\_EXTRACT, and AI\_AGG to build end-to-end AI-powered data processing workflows.

For more information, see [Cortex AI Functions: Snowflake Decision](/user-guide/snowflake-cortex/snowflake-decision).
