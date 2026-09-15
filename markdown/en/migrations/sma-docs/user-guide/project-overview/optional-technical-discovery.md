description:
:   Configuration, setup, and everything else you need to know

# Snowpark Migration Accelerator: Optional Technical Discovery

## What is Technical Discovery?

*Technical discovery* is an optional questionnaire within the Snowpark Migration Accelerator (SMA). With it, you can gather high-level information about your workload, which is a type of information that code analysis alone cannot detect.

## Why is it important?

While code analysis can identify transformations and logic, it lacks operational context. To provide accurate migration recommendations and a relevant suggested architecture, the tool needs to understand details like:

- Your technology stack (cloud platform, regions, tool versions).
- Your data ecosystem (external sources, governance tools, ETL processes, etc.).

By providing this information, you can allow the AI assistant to offer a much more complete and accurate assessment.

## How is this information used?

The answers you provide are linked directly to your assessment results and are used to:

- Categorize your workload.
- Inform the AI assistant.

## Is it mandatory?

No. This feature is optional. If you choose to skip the questionnaire, the assessment and recommendation features will still function, based solely on the data collected from the code analysis.
