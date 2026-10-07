# Patterns — what went wrong, what every slide needs, generalised

Two catalogues, one entry format, read on demand (not loaded every session):

| file | holds | when to open |
|---|---|---|
| `issues.md` | **I-entries**: a symptom you see (a note, a picture, a timing) → its cause → the general fix | a `[layout]`/`[beats]`/PROBLEM line, or a still that looks wrong |
| `tasks.md` | **T-entries**: a kind of slide (a proportion, a 2×2 table, a sweep, a chain…) → the recipe | before writing a scene: find the closest task, start from its code |

The skill `slide-layout` (§4) is the index; `grow-skills` says when to add.

## The ladder (status of an entry)

```
note        seen once: what happened, on which slide, the fix there         (1 slide)
pseudocode  seen twice: the general fix, in steps that name the helpers     (2 slides)
code        "almost there" code: copy, change the numbers, it runs          (2+ slides)
helper      a tested function in aimanim/ does it; the entry just points    (3+ slides, or 2 if long)
```
Move an entry UP when it happens again; never write a helper for a note.
An entry whose helper exists keeps its symptom and cause (that is how it
is found) and drops its code.

## Entry template (copy into issues.md or tasks.md)

```markdown
### I12 — <the symptom, in the words you would search for>
- **status**: note | pseudocode | code | helper `<module.function>`
- **seen**: <scene> (<date>), <scene> (<date>)
- **symptom**: <what is printed or seen>
- **cause**: <why, measured if possible>
- **fix** (pseudocode):
      <3–8 lines, naming kit./layout./beats. functions>
- **code** (almost there):
      <≤ 12 lines, real names, the numbers as UPPER_CASE>
- **check**: <the command that shows it is fixed>
```
IDs never change (I01…, T01…); a merged entry says "→ I07".

## Searching
`grep -n "^### " docs/patterns/*.md` lists every entry. With the symptom's
words: `grep -n -i "touch" docs/patterns/issues.md`.
