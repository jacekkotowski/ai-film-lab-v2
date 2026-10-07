# Sources — every outside fact, once, with how far it was checked

Each slide's spec says WHICH number came from WHERE; this file says how
much each source was actually checked, so nobody searches twice and no
"from memory" passes as "read". Add a source here the first time a spec
cites it; add a film to "used by" when another one does.

Status, strongest first:
- **read** — the document itself was opened and the number found in it
- **abstract** — only an abstract or a search snippet was seen
- **his notes** — from Jacek's bibliography, not opened this side
- **memory** — cited from memory, not opened (say so on the slide's spec)
- **calculated** — not a source: derived in a spec / aimanim module

| source | facts used | status (date) | used by |
|---|---|---|---|
| Vortex Triumph red dot manual M-00433-0 | ½ MOA per click, ~0.50 in at 100 yd | read (2026-10-05) | zeroing |
| Primary Arms SLx 5x MicroPrism product page + both manuals | ¼ MOA click; newer "5x MicroPrism Optic Manual": elevation CCW = up, windage CCW = right; the older manual says the opposite — never cite it | read (2026-10-05); directions also on Jacek's own caps (10-05, 10-06) | zeroing |
| ACSS Aurora MIL reticle manual (SLx 5x MicroPrism), primaryarmsoptics.com …/SLx-5x-MicroPrism-5.56-Aurora-MIL-Reticle-Manual-WEB.pdf | reticle geometry, ranging by width/height, holdovers, chevron 18 in at 300 yd, stadia for 5'10" | read (2026-10-05/06); picture measured at 13.6 px/mil | zeroing, mil-measure, `aimanim/aurora.py` |
| R. L. McCoy, *Modern Exterior Ballistics* (1999) | wind drift = wind × lag; flat-fire drop below the bore line | memory (2026-10-06) — OPEN.md | mil-measure (mil-drop, mil-wind) |
| B. Litz, *Applied Ballistics for Long Range Shooting* | the lag rule | memory (2026-10-06) | mil-measure (mil-wind) |
| Kagan et al., combined first-trimester screening, 75,821 pregnancies | 90 % of trisomy 21 detected at 5 % false positives | his notes; 90 %/5 % also in a search snippet (2026-10-06) | screening |
| Down syndrome prevalence: ~1 in 700 births, ~30 % of affected pregnancies lost after 12 weeks → ~1 in 490 at 12 weeks | 20 in 10,000 | his notes | screening |
| Gigerenzer G (2008), Cochrane Colloquium abstract; Gigerenzer et al. 2007, PSPI | 160 gynecologists, mammography; most frequent answer 90 % (47 %), true PPV ~10 % | abstract (2026-10-06: APS Observer, PSPI abstract, a solution page for the 47 %) | screening |
| Gil MM et al. 2017, UOG meta-analysis, cfDNA | trisomy 21: 99.7 % detected, 0.04 % false positives | abstract (PubMed 28397325 snippet: "> 99 %") | screening |
| Kliff S, Bhatia A, NYT 1 Jan 2022, "When They Warn of Rare Disorders, These Prenatal Tests Are Usually Wrong" | top five microdeletion screens: positives wrong ~85 % (80–93 %) | title + date read (search); numbers his notes | screening |
| Deeks JJ, Altman DG 2004, BMJ 329:168, "Diagnostic tests 4: likelihood ratios" | post-test odds = pre-test odds × LR; LR > 10 strong | his notes | screening, `binary-diagnostics` |
| Salomon LJ et al. 2019, UOG, PubMed 31124209 | amniocentesis procedure-related loss 0.30 % (95 % CI 0.11–0.49 %); CVS 0.20 % (CI crosses 0) | abstract (2026-10-06) | screening |
| Amniocentesis timing: offered weeks 15–20, results in ~10 days to 2 weeks | weeks 15 → 17 | his notes | screening |
| Manim Community v0.21.0 on this machine | sizes, render times, `-r` behaviour | measured (docs/tech/manim.md) | all |
| ai-film-lab film.yaml / captions | 1080×1920, 24 fps, caption zone | measured (2026-10-05/06) | all |

To check next (from the status column): Kagan's numbers and the NYT's
85 % from the documents themselves; McCoy/Litz chapters for the lag rule.
