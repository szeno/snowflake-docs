description:
:   What are we taking away from this?

# Snowpark Migration Accelerator: Conclusions

By utilizing the SMA, we were able to accelerate the migration of both a data pipeline and a reporting notebook. The more of each that you have, the more value a tool like the SMA can provide.

And let’s go back to the assessment -> conversion -> validation flow that we have consistently come back to. In this migration, we:

- Setup out project in the SMA
- Ran SMA’s assessment and conversion engine on the code files
- Reviewed the output reporting from the SMA to better understand what we have
- Review what could not be converted by the SMA in VS Code
- Resolve issues and errors
- Resolve session references
- Resolve input/output references
- Run the code locally

  - And run the code in Snowflake
- Ran the newly migrated scripts and validated their success

Snowflake has spent a great deal of time improving its ingestion and data engineering capabilities, just as it has spent time improving migration tools like SnowConvert, the SnowConvert Migration Assistant, and the Snowpark Migration Accelerator. Each of these will continue to improve. Please feel free to reach out if you have any suggestions for migration tooling. These teams are always looking for additional feedback to improve the tools.
