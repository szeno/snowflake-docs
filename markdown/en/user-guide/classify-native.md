# Native semantic categories of sensitive data classification

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A semantic category is a label that describes the meaning or type of information in a data column, beyond the fundamental data type.
You can use semantic categories to add business context and improve data governance. Snowflake provides the following semantic categories
that identify common types of sensitive attributes, such as names and addresses. These native semantic categories can be sectioned into the
following privacy categories:

- [Identifiers](#label-classify-identifier-categories)
- [Quasi-identifiers](#label-classify-quasi-identifier-categories)
- [Sensitive information](#label-classify-sensitive-information)

Important

Under various laws and regulations, multiple semantic categories can be considered “Sensitive Personal Data”, “Special Categories of
Data”, or similar terms. These semantic categories might require additional protections or controls.

To classify attributes that are not supported natively, refer to [Create custom categories for sensitive data](/user-guide/classify-custom).

## About semantic subcategories

If Snowflake identifies that the type of sensitive data is specific to a country, it records a *semantic subcategory* in the classification details. For example, a social security number (SSN) is an identifier in the United States (US), and its semantic subcategory is `NATIONAL_IDENTIFIER`.

You can find the semantic subcategory in the `Details` field of the JSON object returned by the classification
process. For more information about viewing this response object, refer to [Use SQL to view classification results](/user-guide/classify-results#label-classify-view-results-sql).

If the type of sensitive data is not specific to a country and is globally applicable, it does not have a semantic subcategory. This type of
sensitive data is categorized as a global identifier.

## Identifiers

Identifier semantic categories represent personally identifiable information (PII) or sensitive data elements that can be used to
identify individuals or entities.

### Global identifiers

Global identifier categories are semantic categories that are not specific to a country and are globally applicable.

| Semantic category | Notes |
| --- | --- |
| BANK\_ACCOUNT | For countries outside of Canada, New Zealand, and the United States, the semantic subcategory is International Bank Account Number (IBAN). |
| EMAIL |  |
| IMEI | An International Mobile Equipment Identity (IMEI) is a unique number that identifies a phone’s model and serial number. |
| IP\_ADDRESS |  |
| NAME |  |
| PAYMENT\_CARD |  |
| URL | A Uniform Resource Locator (URL) is the unique address of a resource (such as a document or website) on the Internet. |
| VIN | The Vehicle Identification Number. |

Expand

Show lessSee more

### Country-specific identifiers

| Semantic category | Country | Semantic subcategory | Notes |
| --- | --- | --- | --- |
| BANK\_ACCOUNT | Canada (CA) | CA\_BANK\_ACCOUNT |  |
|  | New Zealand (NZ) | NZ\_BANK\_ACCOUNT |  |
|  | United States (US) | US\_BANK\_ACCOUNT |  |
| DRIVERS\_LICENSE | Austria (AT) | AT\_DRIVERS\_LICENSE |  |
|  | Australia (AU) | AU\_DRIVERS\_LICENSE |  |
|  | Belgium (BE) | BE\_DRIVERS\_LICENSE |  |
|  | Bulgaria (BG) | BG\_DRIVERS\_LICENSE |  |
|  | Canada (CA) | CA\_DRIVERS\_LICENSE |  |
|  | Croatia (HR) | HR\_DRIVERS\_LICENSE |  |
|  | Cyprus (CY) | CY\_DRIVERS\_LICENSE |  |
|  | Czechia (CZ) | CZ\_DRIVERS\_LICENSE |  |
|  | Denmark (DK) | DK\_DRIVERS\_LICENSE |  |
|  | Estonia (EE) | EE\_DRIVERS\_LICENSE |  |
|  | Finland (FI) | FI\_DRIVERS\_LICENSE |  |
|  | France (FR) | FR\_DRIVERS\_LICENSE |  |
|  | Germany (DE) | DE\_DRIVERS\_LICENSE |  |
|  | Greece (GR) | GR\_DRIVERS\_LICENSE |  |
|  | Hungary (HU) | HU\_DRIVERS\_LICENSE |  |
|  | India (IN) | IN\_DRIVERS\_LICENSE |  |
|  | Ireland (IE) | IE\_DRIVERS\_LICENSE |  |
|  | Italy (IT) | IT\_DRIVERS\_LICENSE |  |
|  | Latvia (LV) | LV\_DRIVERS\_LICENSE |  |
|  | Lithuania (LT) | LT\_DRIVERS\_LICENSE |  |
|  | Luxembourg (LU) | LU\_DRIVERS\_LICENSE |  |
|  | Malta (MT) | MT\_DRIVERS\_LICENSE |  |
|  | Netherlands (NL) | NL\_DRIVERS\_LICENSE |  |
|  | New Zealand (NZ) | NZ\_DRIVERS\_LICENSE |  |
|  | Poland (PL) | PL\_DRIVERS\_LICENSE |  |
|  | Portugal (PT) | PT\_DRIVERS\_LICENSE |  |
|  | Romania (RO) | RO\_DRIVERS\_LICENSE |  |
|  | Slovakia (SK) | SK\_DRIVERS\_LICENSE |  |
|  | Slovenia (SI) | SI\_DRIVERS\_LICENSE |  |
|  | Spain (ES) | ES\_DRIVERS\_LICENSE |  |
|  | Sweden (SE) | SE\_DRIVERS\_LICENSE |  |
|  | United States (US) | US\_DRIVERS\_LICENSE |  |
| MEDICARE\_NUMBER | Australia (AU) | AU\_MEDICARE\_NUMBER |  |
|  | New Zealand (NZ) | NZ\_NHI\_NUMBER |  |
| NATIONAL\_IDENTIFIER | Austria (AT) | AT\_IDENTITY\_CARD AT\_SSN |  |
|  | Belgium (BE) | BE\_NATIONAL\_NUMBER |  |
|  | Bulgaria (BG) | BG\_UNIFORM\_CIVIL\_NUMBER |  |
|  | Canada (CA) | CA\_SOCIAL\_INSURANCE\_NUMBER |  |
|  | Croatia (HR) | HR\_PERSONAL\_IDENTIFICATION\_NUMBER |  |
|  | Cyprus (CY) | CY\_IDENTITY\_CARD |  |
|  | Czechia (CZ) | CZ\_PERSONAL\_IDENTITY\_NUMBER |  |
|  | Denmark (DK) | DK\_PERSONAL\_IDENTIFICATION\_NUMBER |  |
|  | Estonia (EE) | EE\_PERSONAL\_IDENTIFICATION\_CODE |  |
|  | Finland (FI) | FI\_NATIONAL\_IDENTITY\_CARD |  |
|  | France (FR) | FR\_CNI FR\_SSN | The FR\_SSN is also known as the INSEE number. |
|  | Germany (DE) | DE\_IDENTITY\_CARD |  |
|  | Greece (GR) | GR\_NATIONAL\_IDENTITY\_CARD GR\_SSN | The GR\_SSN is also known as the AMKA number. |
|  | Hungary (HU) | HU\_PERSONAL\_IDENTIFICATION\_NUMBER HU\_SSN | The HU\_SSN is also known as the TAJ number. |
|  | India (IN) | IN\_PAN IN\_AADHAAR IN\_VOTER\_ID |  |
|  | Ireland (IE) | IE\_PERSONAL\_PUBLIC\_SERVICE\_NUMBER |  |
|  | Latvia (LV) | LV\_PERSONAL\_CODE |  |
|  | Lithuania (LT) | LT\_PERSONAL\_CODE |  |
|  | Luxembourg (LU) | LU\_NATIONAL\_IDENTIFICATION\_NUMBER\_NATURAL\_PERSONS LU\_NATIONAL\_IDENTIFICATION\_NUMBER\_NON\_NATURAL\_PERSONS |  |
|  | Malta (MT) | MT\_IDENTITY\_CARD |  |
|  | Netherlands (NL) | NL\_CITIZEN\_SERVICE\_NUMBER |  |
|  | New Zealand (NZ) | NZ\_STUDENT\_NUMBER |  |
|  | Poland (PL) | PL\_NATIONAL\_ID |  |
|  | Portugal (PT) | PT\_CITIZEN\_CARD\_NUMBER |  |
|  | Romania (RO) | RO\_PERSONAL\_NUMERIC\_CODE |  |
|  | Singapore (SG) | SG\_NATIONAL\_REGISTRATION\_IDENTITY\_CARD |  |
|  | Slovakia (SK) | SK\_PERSONAL\_NUMBER |  |
|  | Slovenia (SI) | SI\_UNIQUE\_MASTER\_CITIZEN\_NUMBER |  |
|  | Spain (ES) | ES\_DNI ES\_SSN |  |
|  | Sweden (SE) | SE\_NATIONAL\_ID |  |
|  | United Kingdom (UK) | UK\_NATIONAL\_INSURANCE\_NUMBER |  |
|  | United States (US) | US\_SSN |  |
| ORGANIZATION\_IDENTIFIER | Australia (AU) | AU\_BUSINESS\_NUMBER AU\_COMPANY\_NUMBER |  |
|  | New Zealand (NZ) | NZ\_BUSINESS\_NUMBER |  |
|  | Singapore (SG) | SG\_UNIQUE\_ENTITY\_NUMBER |  |
| PASSPORT | Australia (AU) | AU\_PASSPORT |  |
|  | Austria (AT) | AT\_PASSPORT |  |
|  | Belgium (BE) | BE\_PASSPORT |  |
|  | Bulgaria (BG) | BG\_PASSPORT |  |
|  | Canada (CA) | CA\_PASSPORT |  |
|  | Croatia (HR) | HR\_PASSPORT |  |
|  | Cyprus (CY) | CY\_PASSPORT |  |
|  | Czechia (CZ) | CZ\_PASSPORT |  |
|  | Denmark (DK) | DK\_PASSPORT |  |
|  | Estonia (EE) | EE\_PASSPORT |  |
|  | Finland (FI) | FI\_PASSPORT |  |
|  | France (FR) | FR\_PASSPORT |  |
|  | Germany (DE) | DE\_PASSPORT |  |
|  | Greece (GR) | GR\_PASSPORT |  |
|  | Hungary (HU) | HU\_PASSPORT |  |
|  | Ireland (IE) | IE\_PASSPORT |  |
|  | Italy (IT) | IT\_PASSPORT |  |
|  | Latvia (LV) | LV\_PASSPORT |  |
|  | Lithuania (LT) | LT\_PASSPORT |  |
|  | Luxembourg (LU) | LU\_PASSPORT |  |
|  | Malta (MT) | MT\_PASSPORT |  |
|  | Netherlands (NL) | NL\_PASSPORT |  |
|  | New Zealand (NZ) | NZ\_PASSPORT |  |
|  | Poland (PL) | PL\_PASSPORT |  |
|  | Portugal (PT) | PT\_PASSPORT |  |
|  | Romania (RO) | RO\_PASSPORT |  |
|  | Singapore (SG) | SG\_PASSPORT |  |
|  | Slovakia (SK) | SK\_PASSPORT |  |
|  | Slovenia (SI) | SI\_PASSPORT |  |
|  | Spain (ES) | ES\_PASSPORT |  |
|  | Sweden (SE) | SE\_PASSPORT |  |
|  | United States (US) | US\_PASSPORT |  |
| PHONE\_NUMBER | Australia (AU) | AU\_PHONE\_NUMBER |  |
|  | Canada (CA) | CA\_PHONE\_NUMBER |  |
|  | Japan (JP) | JP\_PHONE\_NUMBER |  |
|  | United Kingdom (UK) | UK\_PHONE\_NUMBER |  |
|  | United States (US) | US\_PHONE\_NUMBER |  |
| STREET\_ADDRESS | Canada (CA) | CA\_STREET\_ADDRESS |  |
|  | New Zealand (NZ) | NZ\_STREET\_ADDRESS |  |
|  | United States (US) | US\_STREET\_ADDRESS |  |
| TAX\_IDENTIFIER | Australia (AU) | AU\_TAX\_NUMBER |  |
|  | Austria (AT) | AT\_TAX\_ID\_NUMBER |  |
|  | Cyprus (CY) | CY\_TAX\_ID\_NUMBER |  |
|  | France (FR) | FR\_TAX\_ID\_NUMBER |  |
|  | Germany (DE) | DE\_TAX\_ID\_NUMBER |  |
|  | Greece (GR) | GR\_TAX\_ID\_NUMBER |  |
|  | Hungary (HU) | HU\_TAX\_ID\_NUMBER |  |
|  | India (IN) | IN\_GST\_NUMBER |  |
|  | Italy (IT) | IT\_FISCAL\_CODE |  |
|  | Malta (MT) | MT\_TAX\_ID\_NUMBER |  |
|  | Netherlands (NL) | NL\_TAX\_ID\_NUMBER |  |
|  | New Zealand (NZ) | NZ\_INLAND\_REVENUE\_NUMBER |  |
|  | Poland (PL) | PL\_TAX\_ID\_NUMBER |  |
|  | Portugal (PT) | PT\_TAX\_ID\_NUMBER |  |
|  | Slovenia (SI) | SI\_TAX\_ID\_NUMBER |  |
|  | Spain (ES) | ES\_TAX\_ID\_NUMBER |  |
|  | Sweden (SE) | SE\_TAX\_ID\_NUMBER |  |
|  | United States (US) | US\_TAX\_IDENTIFIER | The semantic subcategory US\_TAX\_IDENTIFIER is an identifier because it is the ITIN of an individual. The EMPLOYER\_IDENTIFICATION\_NUMBER subcategory of the TAX\_IDENTIFIER category is a quasi-identifier because it is the EIN of a company. |

Expand

Show lessSee more

## Quasi-identifiers

Quasi-identifiers are attributes that do not uniquely identify an individual on their own, but when combined with other data, could
be used to re-identify someone. Examples of quasi-identifiers include demographic information, geographic data, and administrative regions.

### Global quasi-identifiers

Global quasi-identifiers are quasi-identifier semantic categories that are not specific to a country and are globally applicable.

| Semantic category |
| --- |
| AGE |
| COUNTRY |
| DATE\_OF\_BIRTH |
| ETHNICITY |
| GENDER |
| LATITUDE |
| LAT\_LONG |
| LONGITUDE |
| MARITAL\_STATUS |
| MEDICAL\_SPECIALTY |
| OCCUPATION |
| YEAR\_OF\_BIRTH |

Expand

Show lessSee more

### Country-specific quasi-identifiers

| Semantic category | Country | Semantic subcategory | Notes |
| --- | --- | --- | --- |
| ADMINISTRATIVE\_AREA\_1 | Canada (CA) | CA\_PROVINCE\_OR\_TERRITORY |  |
|  | New Zealand (NZ) | NZ\_REGION |  |
|  | United States (US) | US\_STATE\_OR\_TERRITORY |  |
| ADMINISTRATIVE\_AREA\_2 | United States (US) | US\_COUNTY |  |
| CITY | Canada (CA) | CA\_CITY |  |
|  | New Zealand (NZ) | NZ\_CITY |  |
|  | United States (US) | US\_CITY |  |
| POSTAL\_CODE | Australia (AU) | AU\_POSTAL\_CODE |  |
|  | Canada (CA) | CA\_POSTAL\_CODE |  |
|  | Japan (JP) | JP\_POSTAL\_CODE |  |
|  | New Zealand (NZ) | NZ\_POSTAL\_CODE |  |
|  | Switzerland (CH) | CH\_POSTAL\_CODE |  |
|  | United Kingdom (UK) | UK\_POSTAL\_CODE | Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). |
|  | United States (US) | US\_POSTAL\_CODE |  |
| TAX\_IDENTIFIER | United States (US) | EMPLOYER\_IDENTIFICATION\_NUMBER | The semantic subcategory EMPLOYER\_IDENTIFICATION\_NUMBER is a quasi-identifier, not an identifier, because it is the EIN of a company. The US\_TAX\_IDENTIFIER subcategory of the TAX\_IDENTIFIER category represents the ITIN of an individual, and is an identifier. |

Expand

Show lessSee more

## Sensitive information

Sensitive information includes data elements that contain confidential or private details. While such data does not directly identify an
individual, they require protection due to their sensitive nature.

### Global sensitive information

| Semantic category | Semantic subcategory | Notes |
| --- | --- | --- |
| MEDICAL\_DATA | ICD\_10\_CODE | International Classification of Diseases, 10th Revision, codes. |
|  | LAB\_TEST\_TERM | This includes terms related to laboratory analysis of blood samples (for example, CBC, lipid panel) and general terms for non-blood laboratory analyses (for example, urine analysis, biopsy). |
|  | MEDICAL\_CONDITION | This includes specific medical conditions, illnesses, or disorders, and loss or abnormality of psychological, physiological, or anatomical structure or function (for example, impairments). |
|  | MEDICAL\_PROCEDURE | Interventions involving physical alteration of tissues or organs (for example, appendectomy). |
|  | MEDICINE\_NAME | This includes classifications of drugs based on function or composition (for example, antibiotics, antihistamines), proprietary trademarked names of drugs (for example, Advil, Amoxil), and non-proprietary chemical names of drugs (for example, ibuprofen, amoxicillin). |
| SALARY | n/a | n/a |

Expand

Show lessSee more
