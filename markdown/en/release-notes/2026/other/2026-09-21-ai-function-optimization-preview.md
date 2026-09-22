# September 21, 2026: Cortex AI Function Optimization for more efficient AI implementations (*Public Preview*)

Snowflake Cortex AI Function Optimization is now available in public preview, enabling customers to
automatically search across prompts and models for improved implementations of custom AI Functions. Using
the [AI\_FUNCTION\_OPTIMIZATION](/sql-reference/functions/ai_function_optimization) experiment type,
customers can evaluate multiple model candidates against a consistent dataset and metric, and compare
their quality and estimated cost.

Key use cases include:

- **Improve AI function quality automatically:** Generate and evaluate alternative prompt and model
  configurations without manually rewriting each implementation.
- **Compare models across capability and cost tiers:** Evaluate smaller, lower-cost models alongside
  larger, more capable models using the same data and scoring criteria.
- **Identify the most cost-efficient model:** Determine whether a lower-cost model meets the workload’s
  quality requirements or whether a more capable model provides a material improvement.
- **Create an optimized AI function:** Materialize the selected candidate as a reusable, governed AI
  function with a stable SQL interface.

After optimization, you can use the selected prompt and model directly in an
[AI\_COMPLETE](/sql-reference/functions/ai_complete) call, or create a reusable custom AI function
([CREATE AI FUNCTION](/sql-reference/sql/create-ai-function)) from the result. The original function is
not modified.

For more information, see
[Optimize an AI function](/user-guide/snowflake-cortex/ai-function-studio#label-cortex-ai-function-studio-optimize).
