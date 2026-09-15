Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_TRANSLATE

Translates the given input text from one supported language to another.

## Syntax

Copy code

```
AI_TRANSLATE(
    <text>, <source_language>, <target_language> [, <return_error_details> ] )
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

**Optional:**

`return_error_details`
:   A BOOLEAN flag that indicates whether to return error details in case of error. When set to TRUE, the function returns
    an OBJECT that contains the value and the error message, one of which is NULL depending on whether the function
    succeeded or failed. See [Error behavior](#error-behavior) for details.

## Returns

A string containing a translation of the original text into the target language.

## Error behavior

By default, if AI\_TRANSLATE can’t process the input, the function returns NULL. If the query processes multiple rows,
rows with errors return NULL and don’t prevent the query from completing.

The return value on error depends on the `return_error_details`
argument. The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value` and `error` fields | `value`: A VARCHAR value that contains the translated text, or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. |
>
> Expand
>
> Show lessSee more

For more information about error handling for AI functions, see [Snowflake Cortex AI Function: Multirow error handling improvements](/release-notes/bcr-bundles/2026_02/bcr-2184).

## Usage notes

The following languages are supported by the AI\_TRANSLATE function. Use the corresponding language code for the source and
target language.

The AI\_TRANSLATE model also supports a mix of different languages in the text being translated (for example,
“Spanglish”). In this case, specify an empty string (`''`) as the source language to auto-detect the languages
used in the source text.

AI\_TRANSLATE accepts up to 100,000 input tokens. Across supported languages, translations average an approximately
1:1 input-to-output token ratio, so a translation request can process up to 200,000 total tokens across the source
text (input tokens) and generated translation (output tokens).

| Language | Code |
| --- | --- |
| Arabic | `'ar'` |
| Chinese | `'zh'` |
| Croatian | `'hr'` |
| Czech | `'cs'` |
| Dutch | `'nl'` |
| English | `'en'` |
| Finnish | `'fi'` |
| French | `'fr'` |
| German | `'de'` |
| Greek | `'el'` |
| Hebrew | `'he'` |
| Hindi | `'hi'` |
| Italian | `'it'` |
| Japanese | `'ja'` |
| Korean | `'ko'` |
| Norwegian | `'no'` |
| Polish | `'pl'` |
| Portuguese | `'pt'` |
| Romanian | `'ro'` |
| Russian | `'ru'` |
| Spanish | `'es'` |
| Swedish | `'sv'` |
| Turkish | `'tr'` |

Expand

Show lessSee more

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Examples

The following example translates each row of a table from English to German (in this example, `review_content` is
a column from the `reviews` table):

Copy code

```
SELECT AI_TRANSLATE(review_content, 'en', 'de') FROM reviews LIMIT 10;
```

The following example translates a fictitious product review from English to Spanish:

Copy code

```
SELECT AI_TRANSLATE(
  'Hit the slopes with Snowflake\'s latest innovation - "Skii Headphones" designed to keep your ears warm and your soul ablaze. Engineered specifically for snow weather, these rugged headphones combine crystal-clear sound with thermally-insulated ear cups to keep the chill out and the beats in. Whether you\'re carving through powder or cruising down groomers, Skii Headphones will fuel your mountain adventures with vibrant sound and unrelenting passion. Stay warm, stay fired up, and shred the mountain with Snowflake Skii Headphones',
'en','es');
```

The result of this query is:

```
Sube a las pistas con la última innovación de Snowflake: "Skii Headphones", diseñados para mantener tus oídos calientes y tu alma encendida. Diseñados específicamente para el clima de nieve, estos audífonos resistentes combinan un sonido cristalino con copas de oído aisladas térmicamente para mantener el frío fuera y los ritmos dentro. Ya sea que estés esculpiendo en polvo o deslizándote por pistas preparadas, los Skii Headphones alimentarán tus aventuras en la montaña con un sonido vibrante y una pasión incesante. Mantente caliente, mantente encendido y arrasa la montaña con los Skii Headphones de Snowflake.
```

The following example translates a call transcript from German to English:

Copy code

```
SELECT AI_TRANSLATE(
  ('Kunde: Hallo
    Agent: Hallo, ich hoffe, es geht Ihnen gut. Um Ihnen am besten helfen zu können, teilen Sie bitte Ihren Vor- und Nachnamen und den Namen der Firma, von der aus Sie anrufen.
    Kunde: Ja, hier ist Thomas Müller von SkiPisteExpress.
    Agent: Danke Thomas, womit kann ich Ihnen heute helfen?
    Kunde: Also wir haben die XtremeX Helme in Größe M bestellt, die wir speziell für die kommende Wintersaison benötigen. Jedoch sind alle Schnallen der Helme defekt, und keiner schließt richtig.
    Agent: Ich verstehe, dass das ein Problem für Ihr Geschäft sein kann. Lassen Sie mich überprüfen, was mit Ihrer Bestellung passiert ist. Um zu bestätigen: Ihre Bestellung endet mit der Nummer 56682?
    Kunde: Ja, das ist meine Bestellung.
    Agent: Ich sehe das Problem. Entschuldigen Sie die Unannehmlichkeiten. Ich werde sofort eine neue Lieferung mit reparierten Schnallen für Sie vorbereiten, die in drei Tagen bei Ihnen eintreffen sollte. Ist das in Ordnung für Sie?
    Kunde: Drei Tage sind ziemlich lang, ich hatte gehofft, diese Helme früher zu erhalten. Gibt es irgendeine Möglichkeit, die Lieferung zu beschleunigen?
    Agent: Ich verstehe Ihre Dringlichkeit. Ich werde mein Bestes tun, um die Lieferung auf zwei Tage zu beschleunigen. Wie kommst du damit zurecht?
    Kunde: Das wäre großartig, ich wäre Ihnen sehr dankbar.
    Agent: Kein Problem, Thomas. Ich kümmere mich um die eilige Lieferung. Danke für Ihr Verständnis und Ihre Geduld.
    Kunde: Vielen Dank für Ihre Hilfe. Auf Wiedersehen!
    Agent: Bitte, gerne geschehen. Auf Wiedersehen und einen schönen Tag noch!'
,'de','en');
```

The result is:

```
Customer: Hello
Agent: Hello, I hope you are well. To best assist you, please share your first and last name and the name of the company you are calling from.
Customer: Yes, this is Thomas Müller from SkiPisteExpress.
Agent: Thank you, Thomas, what can I help you with today?
Customer: So, we ordered the XtremeX helmets in size M, which we specifically need for the upcoming winter season. However, all the buckles on the helmets are defective and none of them close properly.
Agent: I understand that this can be a problem for your business. Let me check what happened with your order. To confirm: your order ends with the number 56682?
Customer: Yes, that's my order.
Agent: I see the issue. I apologize for the inconvenience. I will prepare a new delivery with repaired buckles for you immediately, which should arrive in three days. Is that okay for you?
Customer: Three days is quite a long time; I was hoping to receive these helmets sooner. Is there any way to expedite the delivery?
Agent: I understand your urgency. I will do my best to expedite the delivery to two days. How does that sound?
Customer: That would be great, I would be very grateful.
Agent: No problem, Thomas. I will take care of the urgent delivery. Thank you for your understanding and patience.
Customer: Thank you very much for your help. Goodbye!
Agent: You're welcome. Goodbye and have a nice day!
```

Finally, the following example illustrates translating text from two different languages (in this case English and Spanish, or “Spanglish”) to English.
Note that the specification of the source language is the empty string, which tells AI\_TRANSLATE to automatically detect the language.

Copy code

```
SELECT AI_TRANSLATE('Voy a likear tus fotos en Insta.', '', 'en')
```

This query results in:

```
I'm going to like your photos on Insta.
```

Note

AI\_TRANSLATE is the updated version of [TRANSLATE](/sql-reference/functions/translate-snowflake-cortex).
For the latest functionality, use AI\_TRANSLATE.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
