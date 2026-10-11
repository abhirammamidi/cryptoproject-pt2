# Cryptography Assignment 1 - Discrete Logarithms and Hash Functions

Group: <N>    Members and roll numbers: <FILL IN>

## Quick start (Python 3.9+, standard library only)

```
python run_all.py                     # Part 1: required tasks + the A-H comparison table (about 2 minutes)
python run_all.py --required-only     # only the tasks the assignment asks to be solved (about 30 seconds)
python part1/test_part1.py            # 29 unit + end-to-end tests (about 15 seconds)
python part2/test_hashes.py           # Part 2 validation: PASS/FAIL, exit status 0 only if everything passes
```
`matplotlib` is optional and is used ONLY to draw the experiment plots (`pip install matplotlib`).
`part1/run_all.py` can be run directly as well (from any folder).

## Using a different assignment_data.py (for example the examiner's)

Replace `assignment_data.py` in the project root (or run `python run_all.py --data PATH`, or set the
environment variable `ASSIGNMENT_DATA`). Nothing else has to change:

* `part1/data_loader.py` finds the instances whatever the layout: a dict of dicts (any variable name), a dict of
  tuples `(p, g, h[, order])`, one variable per instance (`A = {...}`), one variable per field (`A_p`, `A_g`, `A_h`),
  a list of dicts with a `name` / `label`, or a `get_instances()` function. Labels are case-insensitive
  (`A`, `c2`, `Instance C2`). Field names such as `p|prime|modulus`, `g|generator`, `h|target`, `order|n` are accepted.
* Only `p`, `g`, `h` are required. The group order is checked and replaced by the TRUE order of `g`; the
  factorisation of the order is computed (Pollard rho) when not supplied. Secret exponents are never read.
* If the file cannot be understood, `run_all.py` prints a clear message and exits with status 2 (no traceback).
* If an instance is missing (for example no `C2`), the tasks that need it are simply skipped and reported.

## What `run_all.py` prints

1. a progress line per run, 2. **TABLE 1** (instance, algorithm, status, recovered x, time, group operations,
memory, parameters), 3. **TABLE 2**, the Task 1.6 matrix (algorithm x instance: a measured time, or
`infeasible` / `n/a` / `extrapolated` with a numbered reason). Files written to `part1/experiments/results/`:
`results.csv`, `summary.csv`, `summary.md`, `details.json`.
Every recovered x is checked with `pow(g, x, p) == h`. Exit status 0 means every REQUIRED task passed.

Statuses: **PASS** (solved and verified) - **NOT RUN** (feasible, but above the per-cell budget: the estimated time
or memory is printed; raise `--cell-seconds` / `--ram-fraction` to measure it) - **INFEASIBLE** (estimated above
`--infeasible-years`, default 1 year, or more memory than the machine has) - **EXTRAPOLATED** (brute force on D:
timed on D-sized numbers, never run to completion) - **N/A** (the algorithm does not apply, e.g. index calculus
needs a safe prime p = 2q+1 and a generator g) - **FAIL / TIMEOUT** (a real problem; the reason is printed).

Useful options: `--cell-seconds 600` (measure more of the optional cells), `--required-only`, `--out DIR`,
`--timeout S` (per rho / index-calculus / linear-sieve run), `--use-instance-params`, `--seed N`.
Time estimates use the multiplication speed measured on each instance's own number size.

## Parameters (one source of truth: `part1/params.py`)
Index calculus: F -> B = 500, G -> B = 2000. Linear sieve: B = 700, M = 900. These are the assignment's starting
values. B_ic / B_ls / M_ls stored in a data file are ignored unless `--use-instance-params` is given.
The linear sieve raises M (and, as a last resort, B) automatically if a choice gives too few relations; the run
table then shows e.g. `B=220, M=700->1278`, so the parameters actually used are always visible.

## Experiments (`part1/experiments/`, each writes CSV and, if matplotlib is installed, a PNG into `results/`)
`exp_bruteforce_extrapolate.py` (Task 1.0) - `exp_bsgs_memory.py` (1.1, 8 GB arithmetic) - `exp_rho_runs.py` (1.2,
ten seeds on C and C2) - `exp_ph_scaling.py` (1.3 scaling study) - `exp_ic_B.py` (1.4, B sweep; options
`--instances F,G --bounds 100,180,220,...`) - `exp_ls_vs_ic.py` (1.5) - `exp_previously_failed.py` (re-runs every case
that used to fail and prints PASS/FAIL).

## Design notes and assumptions (state them in the report)
* group_ops counts modular multiplications; `pow(a, e, p)` is charged its square-and-multiply cost (`common.pow_cost`).
  Pohlig-Hellman reports outer and inner (BSGS) operations separately and their sum.
* Rho: the three rules S0/S1/S2 are the assignment's. Which rule applies is decided by a keyed hash of x with a fresh
  random key per seed and per restart, so each run is an independent random walk. Non-invertible denominators
  d = gcd(b2-b1, n) are handled by enumerating and verifying the d candidates, or restarting when d = n.
* Index calculus / linear sieve solve the linear system modulo q (p = 2q+1) with sparse elimination and recover
  the parity bit with Euler's criterion. Reported ranks are the measured ones; a linear-sieve system may be
  rank-deficient in the auxiliary log(H+c) columns while every small-prime logarithm is determined and verified.
* Brute force on D is an extrapolation (seconds per multiplication measured on D-sized numbers), not a run.
* `part1/common.py` holds shared helpers; none of them solves a discrete logarithm. Its Miller-Rabin test uses the
  first 13 prime bases, which is a proof of primality for every n < 3.3*10^24 (Sorenson-Webster 2015).
* Every `solve()` has the same interface and a docstring listing its statistics and how group_ops is counted.
* Part 2: `hashlib` appears only in `test_hashes.py` and in the verification step of `length_extension.py`.

## AI assistance and references (REQUIRED - complete this section before submitting)
Parts of this code were produced with the help of Claude (Anthropic) and then reviewed and tested by the group:
<state exactly which parts you wrote yourselves and which were adapted>.
References: FIPS 180-4, FIPS 202, Menezes-van Oorschot-Vanstone ch. 3 and 9, <others you used>.

## Runtimes
<Fill in from part1/experiments/results/summary.md after running on your own machine.>
