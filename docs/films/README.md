# The films made so far — what each slide shows

One contact sheet per film (its stills in order, 270 px wide each), made
from the full-size stills in `scenes/<scene>/out/`. Script and numbers:
`films/<film>.script.txt`, `scenes/<scene>/spec.md`. Remake a sheet after a
slide changes:
`ffmpeg -i <still 1> ... -i <still n> -filter_complex "hstack=inputs=n,scale=n*270:-1" docs/films/<film>.png`

## zeroing — Zeroing a Rifle Sight (5 slides, 2026-10-05/06) — `zeroing.png`
| # | scene | the one idea |
|---|---|---|
| 01 | zero-group | correct the group's centre, not single holes (4.5 cm left, 5 cm low at 100 m) |
| 02 | zero-clicks | cm ÷ cm-per-click: Triumph 3 up 3 right, SLx 7 up 6 right |
| 03 | zero-mil | MOA turrets, mil reticle: 1 mil ≈ 14 quarter-MOA clicks |
| 04 | zero-reticle | the Aurora MIL, parts named; a 1.78 m man: stadia 2/4/6 = 180/370/550 m |
| 05 | zero-range | 50 cm wide: chevron 300 m, bars 2/3/4 = 400/500/600 m |

## mil-measure — Measuring with a MIL Reticle (8 slides, 2026-10-06) — `mil-measure.png`
| # | scene | the one idea |
|---|---|---|
| 01 | mil-unit | 1 mil = 10 cm at 100 m |
| 02 | mil-man | 1.78 m man at 6/4/3/2 mil on the ladder = 297/445/593/890 m |
| 03 | mil-plate | 50 cm plate filling 2 mil = 250 m |
| 04 | mil-angle | a mil is an angle: 10/20/30 cm at 100/200/300 m |
| 05 | mil-speed | a 2 m car at 200 m, 10 mil/s = 2 m/s = 7.2 km/h |
| 06 | mil-drop | drop = ½gt² below the bore line: 1.2 m at 0.5 s, 4.9 m at 1 s |
| 07 | mil-wind | drift = wind × lag; 30 cm at 300 m = 1 mil |
| 08 | mil-finale | size, distance, angle, movement, trajectory: a measuring instrument |

Not yet made, and asked about or natural next: holds on the MIL grid (drop
and wind together), leads with a measured time of flight, MOA vs mil.
