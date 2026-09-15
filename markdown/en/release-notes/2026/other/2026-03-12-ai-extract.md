# Mar 12, 2026: AI\_EXTRACT scale factor parameter (*General availability*)

The AI\_EXTRACT function now supports the optional `scale_factor` parameter to improve extraction quality when
you receive unexpected or unclear responses in the following scenarios:

- Documents with page sizes larger than A4
- Documents containing small text, detailed visual elements, or dense layouts
- Extracted text contains typos or character-level OCR errors

For more information, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).
