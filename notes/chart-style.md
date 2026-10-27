# One style for Lighthouse figures

27 October 2026. Figure authoring guidance for issue #38. Existing released figures keep their editions; adopt this style when drawing a new figure or reviewing a new edition. The demonstration is LH033's working, unreviewed figure, using its retained 27 October read. Its counts and comparisons are unchanged.

## Colour and type

Use `scripts/chart_style.py`, which needs only Python's standard library. `css()` returns an embedded SVG style block, `svg_open(width, height, title, description)` supplies an accessible root and escapes the two text fields, and `series_stroke(index)` pairs each categorical colour with a different dash pattern. A study script can add the repository's `scripts` directory to `sys.path`, as LH033 does. Use semantic CSS variables rather than literal colours in the drawing.

| Token | Light | Dark | Purpose |
| --- | --- | --- | --- |
| bg | #fbfaf7 | #15191b | Site paper and dark background |
| ink | #1f1f1f | #e6e2d9 | Labels and values |
| muted | #5d5850 | #aaa498 | Axes, sources and notes |
| grid | #e3ddd1 | #2f3538 | Optional, decorative guides |
| teal | #1f6576 | #8ec4d4 | First category |
| amber | #93600c | #e0a650 | Second category |
| purple | #78549b | #c6a7df | Third category |
| blue | #2866ab | #8bb9ed | Fourth category |
| neutral | #74716a | #aaa498 | A named comparison or remainder |

The helper uses the site's incoming interface stack: Source Sans 3, Source Sans Pro, system fonts. No chart fetches a font from a third party. A standalone SVG falls back to the fonts installed on its reader's system. Use tabular, lining figures; labels normally 12 to 14 SVG units, title 17, on a 720-unit viewBox. Check actual legibility at the width used, and make the full-size figure available on tap. Do not shrink a dense figure until the smallest labels become the only way to understand it; give its main observation in its caption and alternative text too.

Use colour consistently within a figure, not as a judgement that one category is good and another bad. Distinguish lines with dashes and labelled endpoints, and regions with outlines or hatching where needed. Categories must remain identifiable without hue. Teal and blue, and purple and blue, converge under some simulated deficiencies; this is why the helper pairs colours with line patterns. Four colours do not promise four independently distinguishable hues for every reader. Use fewer series, direct labels or small multiples when lines crowd.

## Axes, labels and evidence

Draw only useful gridlines, quietly; their colour is not a data mark. Essential axes, threshold lines and range boundaries use `muted` or an opaque categorical stroke at least 1.5 units wide; measured lines normally 2.5. A pale band needs a contrasting boundary. Zero is shown for bars; a truncated line-chart axis is explicit. State the unit and the observation window beside the axes. Unknown and unobserved values are gaps, never zeros.

Put a series name beside its line or bar instead of in a detached key. Use leader lines where names have to move apart, as in LH033's closely spaced branch endpoints. Use patterns and position as well as colour. Do not rely on tooltips: every observation needed to read the chart is present without hover.

A one-line caption gives the observation, its population and period, with the qualification that changes how it reads. Alternative text gives the chart type, axes, central numbers, relevant limits and source; it does not merely say "chart showing". An SVG carries a title and description. A Markdown image still needs its own meaningful alt text because an embedded image's inner description is not consistently exposed. Counts, rounding and claims follow the reviewed record; styling must not change them. Working material is labelled unreviewed.

The SVG contains its own `prefers-color-scheme` block, so the same file follows light or dark mode when embedded as an image or opened on its own. Page CSS lets figures extend to 960px on screens at least 1000px wide while preserving phone gutters and the text measure.

## Checks retained with this change

Run `python3 scripts/check_chart_style.py`. It checks opaque text and all marks against each theme's background: the lowest ordinary contrast is 4.67:1 in light and 7.14:1 in dark. Those exceed the 4.5:1 text and 3:1 meaningful-graphic thresholds described by W3C. The decorative grid is intentionally quieter and must carry no information on its own. These are token checks, not a claim that every possible figure passes accessibility requirements.

The same script simulates the categorical palette in linear sRGB at the protanopia, deuteranopia and tritanopia endpoints of Machado's matrices. It clips transformed values before encoding and checks marks against the transformed background at 3:1. The JSON output records the simulated colours. These simulations reveal collisions, not proof of an accessible chart; direct labels and non-colour cues remain mandatory. It does not test every severity or individual viewer. The LH033 figure is also checked rendered in both themes. All six measured path geometries and every point coordinate match the earlier SVG; only presentation and labels changed. Chromium 153 through Playwright rendered both screenshots; the preinstalled path advertised in CLAUDE.md was absent, so a retained local Chromium package supplied the binary. A browser bounds check found no text outside the viewBox.

Sources read 27 October 2026:

- [W3C: text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), opened and read for the thresholds and the distinction between essential graphics and decoration.
- [Colour's Machado matrix implementation](https://github.com/colour-science/colour/blob/develop/colour/blindness/datasets/machado2010.py), opened through GitHub to verify all three endpoint matrices used by the script. The authors' own supplement and paper host timed out here; the paper's abstract was read in search results, not treated as a read of the full paper.

Replay: `python3 studies/LH033/scripts/draw_figure.py 2026-10-27T0637Z` redraws the demonstration from the retained tables. Screenshots are kept in `site/test/screenshots/chart-style-38/`. No released figure or article was edited. Model spend is unavailable in this harness.
