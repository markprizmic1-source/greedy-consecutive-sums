# Uniform bounds for greedy sequences avoiding consecutive sums

**Mark Vladimir Prizmic · Research note · Version 0.1 · November 27, 2026**

[Read the paper](paper.pdf) · [LaTeX source](paper.tex) · [Verification code](code/verify.py) · [Source audit](SOURCE_AUDIT.md)

Starting at 1, choose each next integer greedily while excluding sums of a fixed number of consecutive earlier terms. This note gives an elementary proof of explicit bounds for every window length `r >= 2`. The four-term case establishes the inequality recorded as Conjecture 1 in [OEIS A394676](https://oeis.org/A394676).

## Main theorem

Fix $r\ge2$ and let

$$b_j=\sum_{t=0}^{r-1}a_{j+t},\qquad C_r=\frac{r(r-1)}2-1.$$

Then, for every $j,n\ge1$,

$$(r+1)j\le b_j\le(r+1)j+C_r,$$

and

$$\left\lfloor\frac{(r+1)n-C_r-1}{r}\right\rfloor\le a_n\le\left\lfloor\frac{(r+1)n-1}{r}\right\rfloor.$$

For **A394676**, set $r=4$:

$$\boxed{\left\lfloor\frac{5n-6}{4}\right\rfloor\le a_n\le\left\lfloor\frac{5n-1}{4}\right\rfloor.}$$

In particular $a_n/n\to5/4$. The general selected set has natural density $r/(r+1)$.

The proof uses the fact that the selected sequence and its increasing sequence of forbidden sums partition the positive integers. Strong induction controls the forbidden sums and then counts the selected values. Every induction boundary case is included in the paper.

## Reproduce the computations

The scripts require Python 3.10 or later and use only the standard library.

```bash
python3 -m unittest discover -s code -p 'test_*.py' -v
python3 code/verify.py --terms 200000 --window 4 --output results/window4_200000.json
```

Other fixed window lengths can be checked with the same program:

```bash
python3 code/verify.py --terms 10000 --window 7
```

The generator uses the original greedy definition, without using the theorem to determine terms. Verification checks both sides of the selected-term bound, all generated forbidden-sum bounds, and the complementary partition. A separate reference implementation is used in the tests. The JSON report records an exact sequence-prefix SHA-256 digest. It is a finite reproducibility check, not a formal proof certificate.

## Build the paper

The PDF is included. To rebuild it with a standard LaTeX installation:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```

The paper uses standard LaTeX packages: `amsmath`, `amssymb`, `amsthm`, `geometry`, `lmodern`, `microtype`, `xcolor`, `booktabs`, `needspace`, and `hyperref`.

## Scope and research status

- The note contains a complete written proof of the displayed theorem.
- The four-term inequality is Conjecture 1 in A394676. The separate equality-block conjecture is not established here.
- The three-term result is also recorded in related work by Dev D. Goyal; that case is not claimed as new.
- The literature check remains incomplete. **No priority claim or claim of a first solution is made.** See [SOURCE_AUDIT.md](SOURCE_AUDIT.md).
- This version has not received external human peer review or proof-assistant certification.

## Attribution and AI assistance

The OEIS entries attribute the sequences to **Hoang Xuan Thanh**. The paper, proof development, generalization, and code were prepared with substantial assistance from **OpenAI's ChatGPT**. Additional AI-assisted reviews examined the proof. This disclosure does not represent those checks as external human review.

## Citation

```bibtex
@misc{prizmic2026greedy,
  author = {Prizmic, Mark Vladimir},
  title = {Uniform bounds for greedy sequences avoiding consecutive sums},
  year = {2026},
  note = {Research note, version 0.1, November 27. AI-assisted draft; priority unverified}
}
```

Machine-readable citation metadata is provided in [CITATION.cff](CITATION.cff).
