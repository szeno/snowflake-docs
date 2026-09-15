Categories:
:   [String & binary functions](/sql-reference/functions-string) (Case Conversion)

# UPPER

Returns the input string with all characters converted to uppercase.

## Syntax

Copy code

```
UPPER( <expr> )
```

## Arguments

`expr`
:   The string expression.

## Returns

This function returns a value of type VARCHAR.

## Examples

Copy code

```
SELECT v, UPPER(v) FROM lu;
```

```
+----------------------------------+----------------------------------+
|                v                 |             upper(v)             |
+----------------------------------+----------------------------------+
|                                  |                                  |
| 1č2Щ3ß4Ę!-?abc@                  | 1Č2Щ3SS4Ę!-?ABC@                 |
| AaBbCcDdEeFfGgHhIiJj             | AABBCCDDEEFFGGHHIIJJ             |
| KkLlMmNnOoPpQqRrSsTt             | KKLLMMNNOOPPQQRRSSTT             |
| UuVvWwXxYyZz                     | UUVVWWXXYYZZ                     |
| ÁáÄäÉéÍíÓóÔôÚúÝý                 | ÁÁÄÄÉÉÍÍÓÓÔÔÚÚÝÝ                 |
| ÄäÖößÜü                          | ÄÄÖÖSSÜÜ                         |
| ÉéÀàÈèÙùÂâÊêÎîÔôÛûËëÏïÜüŸÿÇçŒœÆæ | ÉÉÀÀÈÈÙÙÂÂÊÊÎÎÔÔÛÛËËÏÏÜÜŸŸÇÇŒŒÆÆ |
| ĄąĆćĘęŁłŃńÓóŚśŹźŻż               | ĄĄĆĆĘĘŁŁŃŃÓÓŚŚŹŹŻŻ               |
| ČčĎďĹĺĽľŇňŔŕŠšŤťŽž               | ČČĎĎĹĹĽĽŇŇŔŔŠŠŤŤŽŽ               |
| АаБбВвГгДдЕеЁёЖжЗзИиЙй           | ААББВВГГДДЕЕЁЁЖЖЗЗИИЙЙ           |
| КкЛлМмНнОоПпРрСсТтУуФф           | ККЛЛММННООППРРССТТУУФФ           |
| ХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя           | ХХЦЦЧЧШШЩЩЪЪЫЫЬЬЭЭЮЮЯЯ           |
| [NULL]                           | [NULL]                           |
+----------------------------------+----------------------------------+
```

UPPER supports [collation](/sql-reference/collation) specifications. This UPPER example
specifies collation with the `tr` (Turkish) locale:

Copy code

```
SELECT UPPER('i' COLLATE 'tr');
```

```
+-------------------------+
| UPPER('I' COLLATE 'TR') |
|-------------------------|
| İ                       |
+-------------------------+
```
