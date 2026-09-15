# Managing tags with Python

You can use Python to manage tags in Snowflake. A tag is a schema-level object that can be assigned to another Snowflake object. You
associate a tag with an arbitrary string value when assigning the tag, and Snowflake stores the tag and its string value as a key-value
pair. After defining and assigning tags, you can query them to monitor usage on objects and facilitate data governance operations, such as
auditing and reporting.

For more information about tags, see [Introduction to object tagging](/user-guide/object-tagging/introduction).

The Snowflake Python APIs represents tags with the following types:

- `Tag`: Represents a tag object model with properties such as its name, the database and schema it’s stored in, and when it was
  created.
- `TagValue`: Represents the value of a tag.
- `TagResource`: Represents a reference to a tag object that you can use to fetch information about the tag object and perform
  operations on the tag object, such as renaming the tag and dropping the tag.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Create tags and manage them for a table

The following code example creates tags named `environment_tag` and `custom_tag`, assigns them to a table named `my_tagged_table`, and
fetches the tag assignments for the table. Then it unsets the `environment_tag` tag from the table and fetches the tag assignments again.

Copy code

```
from snowflake.core.tag import Tag, TagValue

table = root.databases["my_database"].schemas["my_schema"].tables["my_tagged_table"]
tags = root.databases["tag_database"].schemas["tag_schema"].tags

# Create tags
environment_tag = Tag(
    name="environment_tag",
    allowed_values=["prod", "dev", "staging"],
    comment="Tag to classify environment",
)
custom_tag = Tag(
    name="custom_tag",
)
environment_tag_resource = tags.create(environment_tag, mode="ifNotExists")
custom_tag_resource = tags.create(custom_tag, mode="ifNotExists")

# Set tags on a table
table.set_tags({environment_tag_resource: TagValue(value="prod"), custom_tag_resource: TagValue(value="custom value")})

# Fetch tag assignments for the table
fetched_tags = table.get_tags()
print(f"Tags on table: {fetched_tags}")
# Tags on table: {<TagResource: 'TAG_DATABASE.TAG_SCHEMA.CUSTOM_TAG'>: TagValue(value='custom value', level='TABLE'), <TagResource: 'TAG_DATABASE.TAG_SCHEMA.ENVIRONMENT_TAG'>: TagValue(value='prod', level='TABLE')}

# Unset one of the tags from the table
table.unset_tags({environment_tag_resource})

# Fetch tag assignments again
fetched_tags_after_unset = table.get_tags()
print(f"Tags after unset: {fetched_tags_after_unset}")
# Tags after unset: {<TagResource: 'TAG_DATABASE.TAG_SCHEMA.CUSTOM_TAG'>: TagValue(value='custom value', level='TABLE')}
```

## Manage tags for a schema and table with inheritance

The following code example assigns an existing tag named `environment_tag` to a schema named `my_schema` and fetches the tag assignments
for a table named `another_tagged_table` in the schema. Then it fetches the tag assignments for the table with inheritance
(`with_lineage=True`).

Copy code

```
from snowflake.core.tag import TagValue

schema = root.databases["my_database"].schemas["my_schema"]
table = schema.tables["another_tagged_table"]
environment_tag = root.databases["tag_database"].schemas["tag_schema"].tags["environment_tag"]

# Set tag on a schema
schema.set_tags({environment_tag: TagValue(value="prod")})

# Fetch tag assignments for the table
fetched_tags = table.get_tags()
print(f"Tags on table: {fetched_tags}")
# Tags on table: {}

# Fetch tag assignments for the table with inheritance
fetched_tags_with_lineage = table.get_tags(with_lineage=True)
print(f"Tags including inheritance: {fetched_tags_with_lineage}")
# Tags including inheritance: {<TagResource: 'TAG_DATABASE.TAG_SCHEMA.ENVIRONMENT_TAG'>: TagValue(value='prod', level='SCHEMA')}
```
