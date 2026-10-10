# Knowledge Base — what the five workbooks teach

Summary of the five "Data science in Excel" issue workbooks (`source/Issue1…Issue5*.xlsm`). Formulas are quoted as written in the files (comma separators). Items flagged **⚠ not in 2013** appear in the files but would not work in Excel 2013.

## Issue 1 — SUMPRODUCT: weighted sums, weighted averages, multi-criteria sums

**Core idea:** SUMPRODUCT multiplies arrays element by element and adds the results. Multiplying by 1/0 acts as a filter; multiplying by a weight gives a weighted result.

| Technique | Formula pattern | Why it works |
|---|---|---|
| Warm-up: conditional sum | `=SUMIF(condition_range, condition, data_range)` | One condition, one column. |
| Sum a share of each value | `=SUMPRODUCT(data_range, percent_range)` | Each value × its percentage, then summed. Complement column `=1-D23` gives the "No" share. |
| Weighted average | `=SUMPRODUCT(cost, cases)/SUM(cases)` | Sum of (value × weight) ÷ sum of weights. |
| Weighted average that respects filters | helper `=SUBTOTAL(2, Table2[[#This Row],[Cases]])` then `=SUMPRODUCT(cost, cases, is_visible)/SUMPRODUCT(cases, is_visible)` | SUBTOTAL ignores filtered rows: helper is 1 visible, 0 hidden. |
| Weighted average by group | `=SUMPRODUCT(Table3[Cost], Table3[Cases], --(Table3[Group]=G53)) / SUMPRODUCT(Table3[Cases], --(Table3[Group]=G53))` | `--` converts TRUE/FALSE to 1/0. |
| Multi-criteria sum on a 2-D block | `=SUMPRODUCT((names=E99)*(months>=E101)*(months<=G101)*(data_block))` | Each condition is a 1/0 array; multiplying is AND; row × column condition broadcasts over the block. |
| Adding a criterion | `…*(regions=G132)*…` | Multiply in another condition. |
| Named ranges for readability | `data_2012`, `customer_2012`, `months`, `products`, `regions_2012` | Formula reads like a sentence. |
| Text-safe alternative (array) | `{=SUM(IF((crit1)*(crit2)*…=1, data_range, ""))}` — Ctrl+Shift+Enter | SUMPRODUCT returns #VALUE! on text; SUM(IF()) skips it. |
| Finding dirty data | `=SUMPRODUCT(--(ISTEXT(D77:L77)))` | Counts text cells in a numeric range. |

**Lookups previewed:**
- Year total for a person: `=SUM(INDEX(data, MATCH(name, names, 0), 0))` — column 0 returns the whole row.
- Quarter total: `=SUM(OFFSET(first_cell, MATCH(name, names, 0)-1, MATCH(q*3-2, months, 0)-1, 1, 3))`.
- Single month: `=INDEX(block, MATCH(name, names, 0), MATCH(month, header, 0))`.

**Advantages / disadvantages:** SUMPRODUCT often replaces a PivotTable and needs no refresh; it requires clean numeric columns.

**Advanced sheet — heat map + drill-down:**
- 2-D binned count: `=SUMPRODUCT((Value>lower_y)*(Value<=upper_y)*(Discount>lower_x)*(Discount<=upper_x))` with a colour-scale conditional format.
- All matching rows (pre-FILTER, array formula): `{=IFERROR(SMALL(IF((conditions), ROW(Table1[Agreement])), ROW(1:1))-3, "")}` then `=IFERROR(INDEX(Table1[], P12, col), "")`.
- VBA `Worksheet_SelectionChange`: clicking a heat-map cell writes its bin limits into parameter cells, driving the drill-down list.

## Issue 2 — Tables, structured references, absolute references, VBA on tables

**Creating a table:** Ctrl+A on a contiguous block, **Ctrl+T**, then Table Tools › Design › Table Name — rename immediately.

**Naming rule:** object type first (`tbl_`), then general → specific: `tbl_Sales_mthly_NorthTeam`.

**Why tables:** autocomplete (`tbl` lists tables, `[` lists columns); columns referenced by name; tables grow and extend formulas, formats and validation.

**INDEX/MATCH against a table:**
- `=MATCH(A82, tbl_Sales_mthly_NorthTeam[name\months], 0)` → row position.
- `=INDEX(tbl_Sales_mthly_NorthTeam[], row, COLUMN(tbl_Sales_mthly_NorthTeam[3]))` — works because the table starts in column A; otherwise subtract the table's first column.
- Fully dynamic: `=INDEX(tbl[], MATCH(name, tbl[name\months], 0), MATCH("3", tbl[#Headers], 0))`.

**Absolute references in table notation:**
- `=SUM(tbl_block_ref[ValueA])` shifts to ValueB, ValueC when fill-dragged sideways.
- `=SUM(tbl_block_ref[[ValueA]:[ValueA]])` stays locked.
- `=SUM(INDIRECT("tbl_block_ref[ValueA]"))` — also locked (text reference).

**VBA on tables (ListObject):**
- Recorded `Range("F7:F21,H6,E7:L7").Select` breaks when the table moves; `Range("Table1[Col1]").Select` does not.
- `ListObjects("Table1")` exposes `.Range`, `.HeaderRowRange`, `.DataBodyRange`, `.ListColumns(n or "name")`, `.ListRows(n)`, `.TotalsRowRange`.
- Combine with `Union`, `Intersect`, `.Resize(, 3)`; find a row with `.ListColumns("Column1").Range.Find(...)`.
- `Dim lo As ListObject: Set lo = ActiveSheet.ListObjects("Table1")` or `With … End With`.
- Total row: `=SUBTOTAL(109, Table1[Col7])` (109 = SUM ignoring hidden rows).

**Follow-up notes:** Microsoft's "Using structured references with Excel tables"; F4 also locks structured references; add the Developer ribbon to record macros.

## Issue 3 — INDEX and MATCH

- `=MATCH(value, range, 0)` → position of an exact match.
- Existence check: `=ISNUMBER(MATCH(A35, tbl[name\months], 0))`.
- New items not in old list: `=IF(ISNUMBER(MATCH(C57, $B$57:$B$62, 0)), "", C57)`.
- Header lookup: `=MATCH(A47, tbl[#Headers], 0)`.
- `=INDEX(range, row, column)`: `=INDEX(B6:F10, 4, 2)`.
- Join tables: MATCH in a helper column, INDEX to pull data; or nest both.
- Better than VLOOKUP: lookup column need not be first; column chosen by MATCH, so inserted columns don't break it.
- Trap: a number stored as text (`'1`) does not match the number 1.
- Two-column match (Ctrl+Shift+Enter): `{=MATCH(B58&C58, tblPettyCash[Name]&tblPettyCash[Subject], 0)}`.

## Issue 4 — OFFSET and dynamic ranges

- `=OFFSET(reference, rows, cols, height, width)`.
- `=SUM(OFFSET(B11, 2, , 10))`; `=SUM(OFFSET(G11, 1, 1, 2, 2))`.
- Moving average: `=AVERAGE(OFFSET(C31, lag, , period))`.
- Many matches: `=MATCH(target, OFFSET($C$6, prev_row, , 1000), 0) + prev_row`.
- Range to last filled row: `=OFFSET(tbl_codes[Products], 0, , COUNTA(tbl_codes[Products]))`.
- Inspect part of a formula: select it in the formula bar, **F9**, then Esc.
- Named dynamic range: Ctrl+F3 › New, `rng_major_codes` = the OFFSET formula; used as a self-expanding validation list.
- Dependent dropdown: `=MATCH(choice, tbl_codes[#Headers], 0)-1`, then `rng_minor_codes = OFFSET(tbl_codes[Products], 0, col, COUNTA(OFFSET(tbl_codes[Products], 0, col, )))`.
- ⚠ not in 2013: `CONCAT`, `TEXTJOIN` (used in the file only for display).
- OFFSET is volatile — fine for small models.

## Issue 5 — INDIRECT

- `=INDIRECT(ref_text, a1)`; FALSE = R1C1.
- `=INDIRECT("A"&"6")`; `=SUM(INDIRECT("A"&C9&":"&"A"&E9))`.
- `=SUM(INDIRECT("R17C"&C14&":"&"R17C"&E14, FALSE))`.
- Named range from a dropdown: `=SUM(INDIRECT(H21))` (H21 = `rng_alpha` / `rng_beta`).
- Sheet from a dropdown: `=SUM(INDIRECT("'"&D14&"'!B4:M8"))`.
- Two-level dependent dropdown: ranges `Fruit`, `Vegetables`; second list `=INDIRECT($B6)`.
- Named input: `input_text` refers to `tblShortCodes7[codes]`.
- First code `=LEFT(x, FIND(";", x)-1)`; last code `=RIGHT(x, LEN(x)-SEARCH("#", SUBSTITUTE(x, ";", "#", LEN(x)-LEN(SUBSTITUTE(x, ";", "")))))`.
- Transpose: `=INDIRECT(ADDRESS(COLUMN(A1), ROW(A1)))`.
- Trap: volatile; breaks if the referenced sheet/name is renamed.

## Cross-cutting habits

- Name everything (`tbl_`, `rng_`), general → specific; prefer tables over grid addresses.
- `FORMULATEXT()` next to a result shows the formula.
- `--` converts booleans; `SUBTOTAL` respects filters; validate with ISTEXT counts before aggregating.
- Polish Excel uses `;` as separator; the files mix both.

## Gaps (from standard Excel 2013, not the workbooks — verify before recording)

PivotTables and PivotCharts, Slicers and Timelines, Data Model / Power Pivot relationships, SUMIFS/COUNTIFS, KPI conditional formatting, charts (combo, sparklines), dashboard layout and protection, GETPIVOTDATA, Freeze Panes.
