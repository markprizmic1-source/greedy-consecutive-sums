# Exact long equality runs in a greedy sequence avoiding four-term sums

**Mark Vladimir Prizmic · Research note · Version 0.1 · November 27, 2026**

[Paper (PDF)](paper.pdf) · [LaTeX source](paper.tex) · [Run checker](verify_runs.py) · [Greedy generator](verify_greedy.py) · [Retained results](verification.json)

## Theorem

Let $(a_n)$ be [OEIS A394676](https://oeis.org/A394676): start at 1 and choose each next larger integer greedily, excluding sums of four consecutive previously selected terms. Put

$$U_n=\left\lfloor\frac{5n-1}{4}\right\rfloor.$$

The **maximal intervals of equality $a_n=U_n$ with length at least four** are exactly

$$\left[\frac{7\cdot16^m-2}{5},\frac{12\cdot16^m+8}{5}\right]_{\mathbb Z},\qquad m\ge0.$$

Their lengths are $16^m+3$. Every other maximal equality run has length at most three. The first five long runs are:

| First index | Last index | Length |
|---:|---:|---:|
| 1 | 4 | 4 |
| 22 | 40 | 19 |
| 358 | 616 | 259 |
| 5,734 | 9,832 | 4,099 |
| 91,750 | 157,288 | 65,539 |

The last three intervals correct the endpoints in the retrieved OEIS examples. The note includes the uniform-bound argument needed for its self-contained proof and an exact recursion for the extreme forbidden-sum errors.

## Reproduce the finite checks

From this directory, using Python 3.10 or later with its standard library:

```bash
python3 verify_runs.py --terms 400000 --output verification.json
```

Keep `verify_greedy.py` beside `verify_runs.py`. The retained run generates **400,000 selected terms directly from the original rule** and verifies the error identities, extreme-set recurrences, and every completed long run in that prefix. The report includes a SHA-256 digest of the selected terms. These finite checks corroborate the implementation; the paper proves the infinite classification.

## Sources and research status

The sequence and recorded conjecture are due to **Hoang Xuan Thanh**, [OEIS A394676](https://oeis.org/A394676), May 11, 2026. The result establishes the recorded length formula for long runs and supplies their exact endpoints. The original general-bound note remains available at [the repository root](../../paper.pdf).

The proof, manuscript, and code were developed with substantial assistance from **OpenAI's ChatGPT**, with additional AI-assisted mathematical reviews. This version has **not received external human peer review or proof-assistant certification**. The literature check is limited, and **no priority or first-proof claim is made**.
