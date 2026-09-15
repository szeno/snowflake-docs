# Writing external functions

External functions are user-defined functions that are stored and executed outside of Snowflake.

External functions make it easier to access external API services such as geocoders, machine learning models, and other custom code
running outside of Snowflake. This feature eliminates the need to export and reimport data when using third-party services, significantly
simplifying your data pipelines.

Note

When using external functions in China, use the [syntax and workflow described for AWS](/sql-reference/external-functions-creating-aws).

[Introduction to external functions](/sql-reference/external-functions-introduction)
:   Learn about external functions, which call executable code that is developed, maintained, stored, and executed outside Snowflake.

[Remote service input and output data formats](/sql-reference/external-functions-data-format)
:   Understand the data formats sent and received by Snowflake.

[Using request and response translators with data for a remote service](/sql-reference/external-functions-translators)
:   Change the format of data sent to and received from remote services.

[Designing high-performance external functions](/sql-reference/external-functions-implementation)
:   Design high-performance functions with these tips on asynchronous services, scalability, concurrency, and reliability.

[External functions best practices](/sql-reference/external-functions-best-practices)
:   Improve efficiency and prevent unexpected results with these best practices.

[Securing an external function](/sql-reference/external-functions-security)
:   Create secure external functions.

## Remote services

[Creating external functions on AWS](/sql-reference/external-functions-creating-aws)
:   Create an external function from functionality on AWS.

[Creating external functions on GCP](/sql-reference/external-functions-creating-gcp)
:   Create an external function from functionality on GCP.

[Creating external functions on Microsoft Azure](/sql-reference/external-functions-creating-azure)
:   Create an external function from functionality on Azure.
