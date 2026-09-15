Categories:
:   [String & binary functions](/sql-reference/functions-string) (Case Conversion)

# LOWER

Returns the input string with all characters converted to lowercase.

## Syntax

Copy code

```
LOWER( <expr> )
```

## Arguments

`expr`
:   The string expression.

## Returns

This function returns a value of type VARCHAR.

## Examples

Convert strings in several different languages and character sets to lowercase:

Copy code

```
SELECT v, LOWER(v) FROM lu;
```

```
+----------------------------------+----------------------------------+
|                v                 |             lower(v)             |
+----------------------------------+----------------------------------+
|                                  |                                  |
| The Quick Gray Fox               | the quick gray fox               |
| LAUGHING ALL THE WAY             | laughing all the way             |
| OVER the River 2 Times           | over the river 2 times           |
| UuVvWwXxYyZz                     | uuvvwwxxyyzz                     |
| ÁáÄäÉéÍíÓóÔôÚúÝý                 | ááääééííóóôôúúýý                 |
| ÄäÖößÜü                          | ääöößüü                          |
| ÉéÀàÈèÙùÂâÊêÎîÔôÛûËëÏïÜüŸÿÇçŒœÆæ | ééààèèùùââêêîîôôûûëëïïüüÿÿççœœææ |
| ĄąĆćĘęŁłŃńÓóŚśŹźŻż               | ąąććęęłłńńóóśśźźżż               |
| ČčĎďĹĺĽľŇňŔŕŠšŤťŽž               | ččďďĺĺľľňňŕŕššťťžž               |
| АаБбВвГгДдЕеЁёЖжЗзИиЙй           | ааббввггддееёёжжззиийй           |
| КкЛлМмНнОоПпРрСсТтУуФф           | ккллммннооппррссттууфф           |
| ХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя           | ххццччшшщщъъыыььээююяя           |
| [NULL]                           | [NULL]                           |
+----------------------------------+----------------------------------+
```

LOWER supports [collation](/sql-reference/collation) specifications. This LOWER example
specifies collation with the `tr` (Turkish) locale:

Copy code

```
SELECT LOWER('I' COLLATE 'tr');
```

```
+-------------------------+
| LOWER('I' COLLATE 'TR') |
|-------------------------|
| ı                       |
+-------------------------+
```
