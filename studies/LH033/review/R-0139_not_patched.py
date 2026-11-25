"""R-0139 (reader review of the week-one revision): from day 14 to day 30, how did the
count of services NOT counted patched change in each branch, beside the patched count?
Reads only data/record_v1.json (m1_counts), written by scripts/record_v1.py.
Run: python3 -I studies/LH033/review/R-0139_not_patched.py > studies/LH033/review/R-0139_not_patched.txt"""
import json, pathlib
d = json.load(open(pathlib.Path(__file__).resolve().parents[1] / "data" / "record_v1.json"))
c = d["m1_counts"]
print("branch | not patched d14 | d30 | change | change % of d14 | patched change | targets change")
for b in ["8.2", "8.3", "8.4", "8.5"]:
    a, z = c[b]["14"], c[b]["30"]
    np14, np30 = a["targets"] - a["patched"], z["targets"] - z["patched"]
    print(f"{b} | {np14:,} | {np30:,} | {np30-np14:+,} | {100*(np30-np14)/np14:+.1f}% | "
          f"{z['patched']-a['patched']:+,} | {z['targets']-a['targets']:+,}")

# All PHP services counted, approximately, from version-reporting services and the
# rounded share with no version (m2_unfixed_tail); approximate because the share is rounded to 0.1.
m2 = d["m2_unfixed_tail"]
print("\nday | version-reporting | no-version % of all | all services counted (approx.)")
for day in ["14", "28", "30"]:
    r = m2[day]
    print(f"{day} | {r['versioned']:,} | {r['unknown_pct_of_all']} | ~{r['versioned']/(1-r['unknown_pct_of_all']/100):,.0f}")
