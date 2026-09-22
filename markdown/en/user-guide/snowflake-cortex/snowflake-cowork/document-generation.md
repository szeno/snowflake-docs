# Document generation in Snowflake CoWork

[Preview Feature](/release-notes/preview-features)  — Open

Available to all accounts.

Snowflake CoWork can turn your analysis into a PDF, PowerPoint, or HTML file. After you explore a question
in chat, ask Snowflake CoWork to generate the file so you can review the insights without repeating the
analysis.

Reach for document generation when you want to package findings, for example:

- An executive deck that summarizes trends, risks, and recommended actions
- A PDF brief that captures key metrics and supporting detail for a working group
- An HTML report that presents the same findings in a formatted page you can view in chat

Document generation is built into Snowflake CoWork: ask for a PDF, PowerPoint, or HTML file in chat, and
the agent produces it. When generation finishes, you can view the file inline in Snowflake CoWork. To
customize how generation works, for example always using a company PowerPoint template or a fixed deck
structure, create a [user skill](/user-guide/snowflake-cortex/snowflake-cowork/user-skills) or attach an
[agent skill](/user-guide/snowflake-cortex/cortex-agents-skills). Your user and agent skills take precedence
over the built-in behavior.

## Prerequisites

Document generation requires the Cortex Agent
[code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) (code sandbox). The agent
you use in Snowflake CoWork must have code execution enabled so the skill can assemble the file during
orchestration.

Ask your administrator to enable the [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) on the agent if document generation isn’t available
or fails to run.

## Supported formats

Snowflake CoWork can generate the following file formats:

| Format | File type | Typical use |
| --- | --- | --- |
| PDF | `.pdf` | Share a written brief, summary, or report |
| PowerPoint | `.pptx` | Share a presentation deck with slides and talking points |
| HTML | `.html` | View a formatted report inline in Snowflake CoWork |

Expand

Show lessSee more

## Generate a document, presentation, or HTML file

Ask Snowflake CoWork in chat for the format you want, and describe the audience and content. For example:

> “Create a PowerPoint deck that summarizes Q4 pipeline risk by region for the leadership review.”

> “Generate a PDF brief with the top churn drivers and the supporting metrics from this analysis.”

> “Create an HTML report that visualizes Q4 pipeline risk by region, with the supporting metrics from this analysis.”

Snowflake CoWork uses the conversation context and your agent’s data tools to draft the file. When
generation finishes, you can view the file inline in Snowflake CoWork.

## Use your own template

For PowerPoint generation, you can upload a `.pptx` template so the generated deck matches your organization’s
style and branding. Attach the template in the chat, then ask Snowflake CoWork to generate the presentation
using that template.

You can also upload a PDF as a reference when generating a PDF. The generated PDF isn’t guaranteed to follow
the uploaded file’s layout or formatting strictly.

For supported upload file types and size limits, see
[Zero-setup file upload](/user-guide/snowflake-cortex/snowflake-cowork#label-snowflake-cowork-zero-setup-file-upload).
