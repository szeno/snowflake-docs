# May 19, 2025: Cortex COMPLETE Structured Output schema references

Snowflake announces support for schema references in Cortex COMPLETE Structured Outputs, making it easier
for developers to create and maintain complex schemas. The new `$ref` mechanism allows developers to define
common components once and reference them throughout their schema. This enhancement also unlocks compatibility with
third-party libraries like Pydantic that rely on schema references, enabling developers to use existing Pydantic
schemas with COMPLETE Structured Outputs.

Key benefits include:

- **Use existing schemas:** Streamlined development workflow for Python developers already using Pydantic in their application code.
- **Maintenance simplicity:** Change definitions in one place and all references automatically inherit updates.
- **Error reduction:** Standardized referenced components eliminate discrepancies across implementations.
- **Scalability:** Referenced components allow you to extend functionality without duplicating validation logic
- **Schema clarity:** References create a clear, organized hierarchy that better represents real-world relationships.

To get started, see [COMPLETE Structured Outputs](/user-guide/snowflake-cortex/complete-structured-outputs).
