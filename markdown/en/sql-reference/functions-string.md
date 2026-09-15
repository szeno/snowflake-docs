# String & binary functions

This family of functions performs operations on a string input value, or binary input value (for certain functions), and returns a string or numeric value.

The functions are grouped by type of operation performed.

| Function Name | Binary Input Supported | Collation Supported | Notes |
| --- | --- | --- | --- |
| **General Manipulation** |  |  |  |
| [ASCII](/sql-reference/functions/ascii) |  |  |  |
| [BIT\_LENGTH](/sql-reference/functions/bit_length) | ✔ |  |  |
| [CHR , CHAR](/sql-reference/functions/chr) |  |  |  |
| [CONCAT , ||](/sql-reference/functions/concat) | ✔ | ✔ |  |
| [CONCAT\_WS](/sql-reference/functions/concat_ws) | ✔ | ✔ |  |
| [INSERT](/sql-reference/functions/insert) | ✔ |  |  |
| [LENGTH, LEN](/sql-reference/functions/length) | ✔ |  |  |
| [LPAD](/sql-reference/functions/lpad) | ✔ |  |  |
| [LTRIM](/sql-reference/functions/ltrim) |  |  |  |
| [OCTET\_LENGTH](/sql-reference/functions/octet_length) | ✔ |  |  |
| [PARSE\_IP](/sql-reference/functions/parse_ip) |  |  |  |
| [PARSE\_URL](/sql-reference/functions/parse_url) |  |  |  |
| [REPEAT](/sql-reference/functions/repeat) |  |  |  |
| [REVERSE](/sql-reference/functions/reverse) | ✔ |  |  |
| [RPAD](/sql-reference/functions/rpad) | ✔ |  |  |
| [RTRIM](/sql-reference/functions/rtrim) |  |  |  |
| [RTRIMMED\_LENGTH](/sql-reference/functions/rtrimmed_length) |  |  |  |
| [SOUNDEX](/sql-reference/functions/soundex) |  |  |  |
| [SOUNDEX\_P123](/sql-reference/functions/soundex_p123) |  |  |  |
| [SPACE](/sql-reference/functions/space) |  |  |  |
| [SPLIT](/sql-reference/functions/split) |  | ✔ | Provides partial support for collation. For details, see the documentation of the function. |
| [SPLIT\_PART](/sql-reference/functions/split_part) |  |  |  |
| [SPLIT\_TO\_TABLE](/sql-reference/functions/split_to_table) |  |  |  |
| [STRTOK](/sql-reference/functions/strtok) |  |  |  |
| [STRTOK\_TO\_ARRAY](/sql-reference/functions/strtok_to_array) |  |  |  |
| [STRTOK\_SPLIT\_TO\_TABLE](/sql-reference/functions/strtok_split_to_table) |  |  |  |
| [TRANSLATE](/sql-reference/functions/translate) |  |  |  |
| [TRIM](/sql-reference/functions/trim) |  |  |  |
| [UNICODE](/sql-reference/functions/unicode) |  |  |  |
| [UUID\_STRING](/sql-reference/functions/uuid_string) |  |  |  |
| **Full-Text Search** |  |  |  |
| [SEARCH](/sql-reference/functions/search) |  |  |  |
| [SEARCH\_IP](/sql-reference/functions/search_ip) |  |  |  |
| **Case Conversion** |  |  |  |
| [INITCAP](/sql-reference/functions/initcap) |  |  |  |
| [LOWER](/sql-reference/functions/lower) |  |  |  |
| [UPPER](/sql-reference/functions/upper) |  |  |  |
| **Regular Expression Matching** |  |  |  |
| [[ NOT ] REGEXP](/sql-reference/functions/regexp) |  |  | Alias for RLIKE. |
| [REGEXP\_COUNT](/sql-reference/functions/regexp_count) |  |  |  |
| [REGEXP\_EXTRACT\_ALL](/sql-reference/functions/regexp_substr_all) |  |  | Alias for REGEXP\_SUBSTR\_ALL. |
| [REGEXP\_INSTR](/sql-reference/functions/regexp_instr) |  |  |  |
| [REGEXP\_LIKE](/sql-reference/functions/regexp_like) |  |  | Alias for RLIKE. |
| [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) |  |  |  |
| [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr) |  |  |  |
| [REGEXP\_SUBSTR\_ALL](/sql-reference/functions/regexp_substr_all) |  |  |  |
| [[ NOT ] RLIKE](/sql-reference/functions/rlike) |  |  |  |
| **Other Matching/Comparison** |  |  |  |
| [CHARINDEX](/sql-reference/functions/charindex) | ✔ | ✔ | Alias for POSITION. Provides partial support for collation. For details, see the documentation of the POSITION function. |
| [CONTAINS](/sql-reference/functions/contains) | ✔ | ✔ | Provides partial support for collation. For details, see the documentation of the function. |
| [EDITDISTANCE](/sql-reference/functions/editdistance) |  |  |  |
| [ENDSWITH](/sql-reference/functions/endswith) | ✔ | ✔ | Provides partial support for collation. For details, see the documentation of the function. |
| [[ NOT ] ILIKE](/sql-reference/functions/ilike) |  |  | Case-insensitive alternative for LIKE. |
| [ILIKE ANY](/sql-reference/functions/ilike_any) |  |  | Case-insensitive alternative for LIKE ANY. |
| [JAROWINKLER\_SIMILARITY](/sql-reference/functions/jarowinkler_similarity) |  |  |  |
| [LEFT](/sql-reference/functions/left) | ✔ | ✔ |  |
| [[ NOT ] LIKE](/sql-reference/functions/like) |  |  |  |
| [LIKE ALL](/sql-reference/functions/like_all) |  |  |  |
| [LIKE ANY](/sql-reference/functions/like_any) |  |  |  |
| [POSITION](/sql-reference/functions/position) | ✔ | ✔ | Provides partial support for collation. For details, see the documentation of the function. |
| [REPLACE](/sql-reference/functions/replace) |  |  |  |
| [RIGHT](/sql-reference/functions/right) | ✔ | ✔ |  |
| [STARTSWITH](/sql-reference/functions/startswith) | ✔ | ✔ | Provides partial support for collation. For details, see the documentation of the function. |
| [SUBSTR , SUBSTRING](/sql-reference/functions/substr) | ✔ | ✔ |  |
| **Compression/Decompression** |  |  |  |
| [COMPRESS](/sql-reference/functions/compress) | ✔ |  |  |
| [DECOMPRESS\_BINARY](/sql-reference/functions/decompress_binary) | ✔ |  |  |
| [DECOMPRESS\_STRING](/sql-reference/functions/decompress_string) | ✔ |  |  |
| **Encoding/Decoding** |  |  |  |
| [BASE64\_DECODE\_BINARY](/sql-reference/functions/base64_decode_binary) |  |  |  |
| [BASE64\_DECODE\_STRING](/sql-reference/functions/base64_decode_string) |  |  |  |
| [BASE64\_ENCODE](/sql-reference/functions/base64_encode) | ✔ |  |  |
| [HEX\_DECODE\_BINARY](/sql-reference/functions/hex_decode_binary) |  |  |  |
| [HEX\_DECODE\_STRING](/sql-reference/functions/hex_decode_string) |  |  |  |
| [HEX\_ENCODE](/sql-reference/functions/hex_encode) | ✔ |  |  |
| [TRY\_BASE64\_DECODE\_BINARY](/sql-reference/functions/try_base64_decode_binary) |  |  | Error-handling version of BASE64\_DECODE\_BINARY. |
| [TRY\_BASE64\_DECODE\_STRING](/sql-reference/functions/try_base64_decode_string) |  |  | Error-handling version of BASE64\_DECODE\_STRING. |
| [TRY\_HEX\_DECODE\_BINARY](/sql-reference/functions/try_hex_decode_binary) |  |  | Error-handling version of HEX\_DECODE\_BINARY. |
| [TRY\_HEX\_DECODE\_STRING](/sql-reference/functions/try_hex_decode_string) |  |  | Error-handling version of HEX\_DECODE\_STRING. |
| **Cryptographic/Checksum** |  |  |  |
| [MD5 , MD5\_HEX](/sql-reference/functions/md5) |  |  | Intended primarily for checksum operations. Not recommended for cryptography. |
| [MD5\_BINARY](/sql-reference/functions/md5_binary) |  |  | Intended primarily for checksum operations. Not recommended for cryptography. |
| [MD5\_NUMBER\_LOWER64](/sql-reference/functions/md5_number_lower64) |  |  | Intended primarily for checksum operations. Not recommended for cryptography. |
| [MD5\_NUMBER\_UPPER64](/sql-reference/functions/md5_number_upper64) |  |  | Intended primarily for checksum operations. Not recommended for cryptography. |
| [SHA1 , SHA1\_HEX](/sql-reference/functions/sha1) |  |  |  |
| [SHA1\_BINARY](/sql-reference/functions/sha1_binary) |  |  |  |
| [SHA2 , SHA2\_HEX](/sql-reference/functions/sha2) |  |  |  |
| [SHA2\_BINARY](/sql-reference/functions/sha2_binary) |  |  |  |
| **Hash (Non-cryptographic)** |  |  |  |
| [HASH](/sql-reference/functions/hash) | ✔ |  | Allows data types other than string and binary. Not intended for cryptography. |
| [HASH\_AGG](/sql-reference/functions/hash_agg) | ✔ |  | Allows data types other than string and binary. Not intended for cryptography. |
| **Collation** |  |  |  |
| [COLLATE](/sql-reference/functions/collate) |  |  |  |
| [COLLATION](/sql-reference/functions/collation) |  |  |  |
| **AI Functions** |  |  |  |
| [AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/agent_run-snowflake-cortex) |  |  |  |
| [AI\_AGG](/sql-reference/functions/ai_agg) |  |  |  |
| [AI\_CLASSIFY](/sql-reference/functions/ai_classify) |  |  |  |
| [AI\_COMPLETE](/sql-reference/functions/ai_complete) |  |  |  |
| [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens) |  |  |  |
| [AI\_EMBED](/sql-reference/functions/ai_embed) |  |  |  |
| [AI\_FILTER](/sql-reference/functions/ai_filter) |  |  |  |
| [AI\_MULTI\_EMBED](/sql-reference/functions/ai_multi_embed) |  |  |  |
| [AI\_REDACT](/sql-reference/functions/ai_redact) |  |  |  |
| [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) |  |  |  |
| [AI\_SIMILARITY](/sql-reference/functions/ai_similarity) |  |  |  |
| [AI\_SUMMARIZE](/sql-reference/functions/ai_summarize) |  |  |  |
| [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg) |  |  |  |
| [AI\_TRANSLATE](/sql-reference/functions/ai_translate) |  |  |  |
| [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](/sql-reference/functions/classify_text-snowflake-cortex) |  |  |  |
| [COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/complete-snowflake-cortex) |  |  |  |
| [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex) |  |  |  |
| [THREAD\_MESSAGES (SNOWFLAKE.CORTEX)](/sql-reference/functions/thread_messages-snowflake-cortex) |  |  |  |
| [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](/sql-reference/functions/embed_text-snowflake-cortex) |  |  |  |
| [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](/sql-reference/functions/embed_text_1024-snowflake-cortex) |  |  |  |
| [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/entity_sentiment-snowflake-cortex) |  |  |  |
| [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](/sql-reference/functions/extract_answer-snowflake-cortex) |  |  |  |
| [FINETUNE (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-snowflake-cortex) |  |  |  |
| [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/parse_document-snowflake-cortex) |  |  |  |
| [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](/sql-reference/functions/split_text_markdown_header-snowflake-cortex) |  |  |  |
| [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](/sql-reference/functions/split_text_recursive_character-snowflake-cortex) |  |  |  |
| [SENTIMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/sentiment-snowflake-cortex) |  |  |  |
| [TRANSLATE (SNOWFLAKE.CORTEX)](/sql-reference/functions/translate-snowflake-cortex) |  |  |  |
| [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](/sql-reference/functions/count_tokens-snowflake-cortex) |  |  |  |
| [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/try_complete-snowflake-cortex) |  |  |  |
| [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](/sql-reference/functions/search_preview-snowflake-cortex) |  |  |  |

Expand

Show lessSee more
