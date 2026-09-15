Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# TRANSLATE (SNOWFLAKE.CORTEX)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_TRANSLATE](/sql-reference/functions/ai_translate), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Translates the given input text from one supported language to another.

Attention

This function does not transform a string given a search string and a replacement string. See the [TRANSLATE](/sql-reference/functions/translate) function if that
functionality is what you’re looking for.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.TRANSLATE(
    <text>, <source_language>, <target_language>)
```

## Arguments

`text`
:   A string containing the text to be translated.

`source_language`
:   A string specifying the language code for the language the text is currently in. See [Usage notes](#usage-notes) for a list of
    supported language codes. If the source language code is an empty string, `''`, the source language is
    automatically detected.

`target_language`
:   A string specifying the language code into which the text should be translated. See [Usage notes](#usage-notes) for a list of
    supported language codes.

## Returns

A string containing a translation of the original text into the target language.

## Usage notes

The following languages are supported by the TRANSLATE function. Use the corresponding language code for the source and
target language.

The TRANSLATE model also supports a mix of two different languages in the text being translated (for example,
“Spanglish”). In this case, specify an empty string (`''`) as the source language to auto-detect the languages
used in the source text.

| Language | Code |
| --- | --- |
| Chinese | `'zh'` |
| Dutch | `'nl'` |
| English | `'en'` |
| French: | `'fr'` |
| German | `'de'` |
| Hindi | `'hi'` |
| Italian | `'it'` |
| Japanese | `'ja'` |
| Korean | `'ko'` |
| Polish | `'pl'` |
| Portuguese | `'pt'` |
| Russian | `'ru'` |
| Spanish | `'es'` |
| Swedish | `'sv'` |

Expand

Show lessSee more

The TRANSLATE function produces its best results when either the source or target language is English (for example,
English to Spanish or German to English). Results for other language pairs, such as German to Spanish, might be less
accurate.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
