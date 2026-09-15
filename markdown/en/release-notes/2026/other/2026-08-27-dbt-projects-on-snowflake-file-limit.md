# Aug 27, 2026: Increased file limit for deployed dbt project objects

A dbt project object on Snowflake can now include up to 100,000 files (up from 20,000).
This limit counts every file in the project directory and its subdirectories, including
the `models/` folder and generated folders such as `target/`, `dbt_packages/`, and `logs/`.

For more information, see [Limitations, requirements, and considerations for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-limitations).
