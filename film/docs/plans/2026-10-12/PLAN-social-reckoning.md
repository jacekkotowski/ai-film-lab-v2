# The Social Reckoning: likes, a quiz, points (plan, 2026-10-12)

Source: Jacek's pasted plan (speech, photo list, links, bibliography, R code
fragments), 2026-10-12. Made with skill `evidence-short`. Nothing built yet.

## Deviations from the pasted plan (his decision)

1. **No word of the speech changed.** 270 words (wc; paragraphs 45 / 58 / 56
   / 60 / 51): ~144 s at Map and Calculator 01's 1.875 w/s, 113-135 s at his
   Excel finals' 2.0-2.4 w/s. Under 2.5 min, nothing to cut.
2. **Two paragraphs split over two pictures**, at a sentence boundary:
   [02] Kogan's 3 sentences on the code, "Cambridge Analytica, a political
   consultancy..." on Nix's photo; [03] "In 2021 Frances Haugen..." on her
   photo, the rest on the code.
3. **Photos changed:** Kosiński HAS free photos (the plan found none); Haugen
   and Nix from Web Summit's portrait crops, CC BY 2.0 (the plan's Haugen was
   CC BY-SA 2.0). Kosiński's photo is an option only: slide 01 shows code.
4. **The plan's R replaced** by lines of 18 characters or less (the most that
   fit at 56, measured) using base `svd`/`glm` instead of irlba/pROC; run on
   toy data (below), not the real model.

## Slides: 6 (intro on camera)

| NN | his sentences | shows | numbers: source |
|---|---|---|---|
| intro | "When people hear..." (3) | camera | film: Variety 2025 (reporting) |
| 01 | "In 2013 Michał Kosiński..." (3) | code: likes → 100 columns → glm; result "85 in 100" | PNAS 110(15) 5802, 2013 (primary): 58,466 volunteers, AUC 0.85 Dem/Rep |
| 02 | "In 2014 Aleksandr Kogan..." (3) | code: lm on the quiz, predict the friends | The Conversation 2018 (reporting): ~270,000 users |
| 02a | "Cambridge Analytica, a political consultancy..." (1) | photo Nix | |
| 03a | "In 2021 Frances Haugen..." (1) | photo Haugen | |
| 03 | "From 2018 the news feed..." (3) | code: score = 1·like + 5·emoji + 30·comment, arrange | CNN Facebook Papers 2021 (reporting) |
| 04 | outro "The angry emoji..." (3) | code: `w["angry"] <- 5` struck, `<- 0`; "50 % → 80 %" | Washington Post 2021 (reporting) |

## Photos (Wikimedia Commons, read 2026-10-12 through its API)

| slide | file page | px | licence | credit |
|---|---|---|---|---|
| 02a Nix | https://commons.wikimedia.org/wiki/File:Web_Summit_2017_-_Centre_Stage_Day_3_SAM_7378_(38286774551)_(cropped).jpg | 1316 x 1872 | CC BY 2.0 | Web Summit (Sam Barnes / Sportsfile) |
| 03a Haugen | https://commons.wikimedia.org/wiki/File:2021_-_Opening_night_EN1_1635_(51648502375)_(cropped).jpg | 1375 x 1892 | CC BY 2.0 | Web Summit |
| (01 option) Kosiński | https://commons.wikimedia.org/wiki/File:Michał_Kosiński_2019.jpg | 4658 x 6501 | CC BY-SA 3.0 PL | Adrian Grycuk; caption: "Profesor Michał Kosiński (Stanford University)", Warsaw lecture, 20 Dec 2019 |

Both crops are wider than 1080 and portrait: they fill the frame without
upscaling. Credits go in the YouTube description. The person in Nix's and
Haugen's crops is known from the Commons category only, not from a caption I
read; look at them before use. Not downloaded (needs his yes).

## The code, as it will appear (each line ≤ 18 characters)

```r
# 01                     # 02                  # 03
X <- likes |>            fit <- lm(            posts |>
  svd(nu = 100)            open ~ .,             mutate(score =
fit <- glm(                quiz)                  1 * like +
  dem ~ X$u,             predict(fit,             5 * emoji +
  binomial)                friends)              30 * comment) |>
                                                 arrange(-score)
# 04
w["angry"] <- 5
w["angry"] <- 0
```

Toy run (scratchpad social_code.R, Rscript 4.6.1, dplyr): 600 people x 300
pages, all four parts run; longest slide line 18 characters; slide 01's toy
AUC 0.77 (random data: the 0.85 on screen is the paper's).

## Next (his go)

slides.script.txt with [intro] [01] [02] [02a] [03a] [03] [04] [outro] in his
words; the four scenes (new-scene, slide-layout); the two photos downloaded
into media/ as 02a_nix.jpg, 03a_haugen.jpg; `look film`; publish (ask).
