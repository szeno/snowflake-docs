# Nov 04, 2025: Cortex Agents (*General availability*)

With this release, we are pleased to announce the general availability of Cortex Agents, which was previously available as a preview feature. Cortex Agents orchestrate across both structured and unstructured data sources to deliver insights.

Cortex Agents plan tasks, use tools to execute these tasks, and generate responses. Agents use Cortex Analyst (structured) and Cortex Search (unstructured) as tools, along with LLMs, to analyze data.

The workflow involves four key components:

- **Planning:** Agents parse requests to orchestrate a plan and arrive at solutions. They can explore options, split tasks into subtasks, and route across tools to ensure governed access and compliance with enterprise policies.
- **Tool use:** Agents retrieve data efficiently using Cortex Search for unstructured sources and Cortex Analyst for structured data.
- **Reflection:** After each tool use, agents evaluate results to determine next steps - asking for clarification, iterating, or generating a final response.
- **Monitor and iterate:** Track metrics, analyze performance, and refine behavior for continuous improvements.

For more information, see [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).
