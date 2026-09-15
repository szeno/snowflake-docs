# Manage sequences

The Snowflake REST [Sequence API](/developer-guide/snowflake-rest-api/reference/sequence.html) provides the following endpoints to manage Snowflake secrets:

**Snowflake REST Sequence API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/sequences` | Lists sequences. |
| `POST /api/v2/databases/database/schemas/` `schema/sequences` | Creates a sequence. |
| `GET /api/v2/databases/database/schemas/` `schema/sequences/name` | Fetches a sequence. |
| `DELETE /api/v2/databases/database/schemas/` `schema/sequences/name` | Deletes a sequence. |
| `POST /api/v2/databases/database/schemas/` `schema/sequences/name:clone` | Creates a new sequence by cloning from the specified resource. |
| `POST /api/v2/databases/database/schemas/` `schema/sequences/name:rename` | Renames a sequence with a new identifier. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Sequence API reference](/developer-guide/snowflake-rest-api/reference/sequence.html).
