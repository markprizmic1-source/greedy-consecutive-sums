# Source and priority audit

Audit date: November 27, 2026. This is a record of the scope and limitations of the search, not a certification of novelty.

## Original problem records

1. **Hoang Xuan Thanh, OEIS A394676** — <https://oeis.org/A394676>
   - The retrieved entry defines the greedy sequence avoiding sums of four consecutive sequence terms.
   - It records Conjecture 1 as `a(n) <= floor((5*n-1)/4)`.
   - It attributes the sequence to Hoang Xuan Thanh, May 11, 2026.
   - It also records a distinct conjecture about equality blocks. The paper makes no claim to establish that conjecture.
   - Direct retrieval sometimes returned HTTP 403; indexed primary-source text was available. A retained conjecture label alone does not establish that no proof exists.

2. **Hoang Xuan Thanh, OEIS A394576** — <https://oeis.org/A394576>
   - Three-term analogue, attributed to the same contributor and date.
   - Its upper-bound conjecture is a special case of the theorem in this note.
   - Related work below already records this three-term bound; we do not claim priority for that case.

## Closest related work found

3. **Dev D. Goyal, A greedy sequence that avoids sums of three consecutive terms**
   - Manuscript map: <https://github.com/dvgyl/oeis-proofs/blob/main/CONTENTS.md>
   - Repository metadata: <https://github.com/dvgyl/oeis-proofs/blob/main/lean/formalization.yaml>
   - The readable manuscript map explicitly records the bounds `floor((4*n-3)/3) <= a(n) <= floor((4*n-1)/3)` and describes a block-based proof for A394576.
   - The repository reports a Lean formalization for that result. Its formalization was not independently compiled during this project.
   - The source map and metadata were inspected; the complete associated manuscript was not successfully retrieved in this audit.

4. **Hoang Xuan Thanh, Algorithm for OEIS A394576, A394676 and generalized forbidden sums**
   - DOI: <https://doi.org/10.5281/zenodo.22674326>
   - The title, author, and DOI were located in the primary metadata of Goyal's repository. That record describes the deposit as software used for comparison.
   - The deposit itself could not be retrieved, so its complete mathematical contents have not been checked.

## Search scope

Searches included exact sequence identifiers, the four-term inequality, fixed-window greedy forbidden sums, complementary sequence bounds, and the referenced algorithm title and DOI. No additional indexed four-term or general-window proof was located in that search scope. This statement is limited to the sources retrieved and is not evidence of an exhaustive literature search.

## Claims supported by this version

- A self-contained proof of the displayed uniform bounds for each fixed integer window length `r >= 2`.
- The A394676 upper bound as a corollary.
- A lower bound, bounded discrepancy, asymptotic slope, and natural density.
- Reproducible finite computations checking implementation consistency.

## Claims not made

- First proof, unique proof, or verified priority.
- External human peer review, journal acceptance, or formal proof certification.
- A solution of the equality-block conjecture in A394676.
- A resolution of the other conjectures discussed in the surrounding project.

Before a claim of novelty is added, inspect the complete Thanh deposit and Goyal manuscript and obtain independent mathematical review. Any newly located prior result should be cited and the claimed contribution adjusted accordingly.
