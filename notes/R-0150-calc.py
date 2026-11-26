"""R-0150: reproduce the figures LH060 record 0.1 states or relies on.
Inputs are the figures as printed in the documents (reread 26 November 2026, sha256 equal to
studies/LH060/fetchlog.csv); no body is kept. Run: python3 -I notes/R-0150-calc.py"""
from math import exp, lgamma, log

def chi2_sf(x, k):
    # upper tail of chi-squared with k degrees of freedom (series for the regularised gamma)
    a, z = k / 2.0, x / 2.0
    s, term, n = 0.0, 1.0 / a, 0
    while term > 1e-15 * s or n == 0:
        s += term; n += 1; term *= z / (a + n)
    return 1.0 - exp(-z + a * log(z) - lgamma(a)) * s

# C07 (Haque and others, arXiv 2611.09703v1): shares printed in the paper
print("C07 hosts with a PQC key exchange: 688814/1523998 = %.1f%%" % (100 * 688814 / 1523998))
print("C07 entities with one on >=1 IP: 10788/27012 = %.1f%%" % (100 * 10788 / 27012))
print("C07 entities without: 16224/27012 = %.1f%%; 10788+16224 = %d" % (100 * 16224 / 27012, 10788 + 16224))

# C08 (Deng and Inthiran, arXiv 2605.18901), Table 4 row shares times row N -> counts
rows = {"Small (<50)": (10, (0.300, 0.500, 0.200)), "Medium (50-250)": (24, (0.333, 0.417, 0.250)),
        "Large (250-500)": (12, (0.333, 0.250, 0.417)), "Very large (>500)": (13, (0.538, 0.231, 0.231))}
counts = {}
for k, (n, sh) in rows.items():
    c = [round(n * s) for s in sh]
    assert sum(c) == n, (k, c)
    counts[k] = c
    print("C08 %-18s perimeter/zero trust/hybrid = %s (n=%d)" % (k, c, n))
tab = list(counts.values())
N = sum(map(sum, tab)); col = [sum(r[j] for r in tab) for j in range(3)]
chi = sum((r[j] - sum(r) * col[j] / N) ** 2 / (sum(r) * col[j] / N) for r in tab for j in range(3))
df = (len(tab) - 1) * (3 - 1)
exp_min = min(sum(r) * col[j] / N for r in tab for j in range(3))
cells_lt5 = sum(1 for r in tab for j in range(3) if sum(r) * col[j] / N < 5)
print("C08 four size groups, N=%d (the 5 N/A excluded): chi2=%.2f df=%d p=%.2f" % (N, chi, df, chi2_sf(chi, df)))
print("C08 smallest expected count %.2f; cells with expected < 5: %d of 12" % (exp_min, cells_lt5))
