"""R-0118 reader review: two checks on LH039 record 1.1 figures (values typed from
record-1.0-tabulation.txt and LH039.md Findings 1 and 4; no network; stdlib only).
1. Least-squares line through each branch's first-fix share (fixed release alone,
   W3Techs as given, reads of days 12 to 21, before the second release), and the day
   at which the line crosses zero. A line through about day 0 is what a sampler that
   revisits each site about once a month would show even if every updating site
   updated on day 0; it does not by itself show sites updated gradually.
2. Branch-matched positions against PHP (LH033 figures as LH039 quotes them).
"""
days = list(range(12, 22))
first_fix = {  # share of branch, the fixed release alone, as W3Techs gives it
 "7.1.4": [19.6, 21.4, 23.7, 25.1, 26.7, 28.9, 30.6, 32.0, 34.4, 36.3],
 "7.0.8": [7.3, 8.4, 10.5, 11.4, 12.7, 14.0, 15.4, 16.8, 18.4, 19.7],
 "6.9.11": [None]*10,
}
def fit(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    b = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/sum((x-mx)**2 for x in xs)
    a = my - b*mx
    r = [y-(a+b*x) for x, y in zip(xs, ys)]
    return a, b, max(abs(e) for e in r)
for k in ("7.1.4", "7.0.8"):
    a, b, m = fit(days, first_fix[k])
    print(f"{k}: slope {b:.2f} points/day, intercept {a:.2f}, zero at day {-a/b:.1f}, max residual {m:.2f}")
print("7.1.4 W3Techs history 1 Nov (day 4): 6.6; line predicts", round(fit(days, first_fix['7.1.4'])[0]+4*fit(days, first_fix['7.1.4'])[1], 1))
print()
# Superseded releases on the history pages, 1 Nov -> 21 Nov (share of branch)
for k, v in {"7.0.7 (superseded by 7.0.8)": (20.0, 28.4), "6.9.10 (superseded by 6.9.11)": (23.8, 28.4), "7.1.3 (superseded by 7.1.4)": (54.7, 39.3)}.items():
    print(f"{k}: {v[0]} -> {v[1]}")
print()
php = {"day12": {"8.2": 10.7, "8.3": 12.1, "8.4": 16.0, "8.5": 23.8},
       "day19": {"8.2": 20.0, "8.3": 21.4, "8.4": 27.2, "8.5": 38.9},
       "day26": {"8.2": 32.5, "8.3": 36.6, "8.4": 41.8, "8.5": 55.4}}
wp = {"day12": {"7.1": 19.60, "7.0": 7.31, "6.9": 8.31},
      "day19": {"7.1": 32.00, "7.0": 16.78, "6.9": 16.92},
      "day24": {"7.1": 43.26, "7.0": 24.90, "6.9": 25.87}}
for wd, pd in (("day12", "day12"), ("day19", "day19"), ("day24", "day26")):
    for br, v in wp[wd].items():
        below = [p for p, s in php[pd].items() if v < s]
        print(f"WP {br} {wd} {v}: below PHP {below or 'none'} at PHP {pd}; newest-to-newest (7.1 v 8.5): " + (f"{v - php[pd]['8.5']:+.1f}" if br == "7.1" else ""))
