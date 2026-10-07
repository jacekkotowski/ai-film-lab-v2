# scr-rarity — slide 4 of screening

**Problem (Jacek's words):** Blood tests catch 99.7 % of Down syndrome and
were sold as highly accurate for rarer defects, yet the NYT calculated
about 85 % of their positives are wrong. The fairest score is the positive
likelihood ratio, because rarity does not change it. Hers is 18.

**One idea:** the same test on a rarer condition: the true positives
shrink, the false ones stay, so most positives are wrong; LR+ stays put.

**Data** (an ILLUSTRATION of the mechanism, not the NYT's data)
- blood test (Gil 2017): sensitivity 99.7 %, false positives 0.04 %
- per 100,000 at 1 in 490 (Down syndrome at 12 weeks): 204 affected →
  TP 203, FP 99,796 × 0.0004 = 40 → 84 % of positives real
- the prevalence where these rates give 85 % wrong:
  p = 0.15 × 0.0004 / (0.997 × 0.85 + 0.15 × 0.0004) = 1 in 14,125 → "1 in 14,000"
- per 100,000 at 1 in 14,000: 7 affected → TP 7, FP 40 → 7 / 47 = 15 % real, **85 % wrong**
- the red dot's AREA is the prevalence: radius 1.0 → √(490/14,000) = 0.19
- the FP pile does not grow (40 both times); the real pile shrinks 203 → 7.
  (His animation list said the grey pile grows; it grows as a SHARE.)
- LR+ (combined test) = 0.90 / 0.05 = 18; blood test 0.997 / 0.0004 = 2,492
  → "≈ 2,500", on screen only, not narrated

**Steps**
0. title "99.7% caught"
1. line 0, "Blood" — red dot + "1 in 490"; "positives in 100,000": 203 red, 40 grey
2. line 0, "rarer" — dot shrinks, "1 in 14,000"; 196 red go, the rest packs to 7 + 40
3. line 0, "85" — "85% wrong"
4. line 1, "fairest" — "LR+ = 0.90 / 0.05"
5. line 2, "Hers" — "= 18"; "newer blood test / LR+ ≈ 2,500" (not narrated)

**Narration:** films/screening.script.txt [04], his words.

**Sources:** Gil MM et al. 2017 (UOG meta-analysis); Kliff & Bhatia, NYT
1 Jan 2022 (85 %, 80–93 % by condition, microdeletion screens); Deeks &
Altman 2004 BMJ 329:168. The 1 in 14,000 is derived (above). Caveat: for
tests read subjectively, sensitivity and specificity can shift with prevalence.

**Status:** written 2026-10-06. Full-size still, no layout notes.
