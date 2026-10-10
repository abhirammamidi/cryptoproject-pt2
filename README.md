# Cryptography Assignment — Part 2

Python standard-library implementation and experiments for SHA-256, SHA-512,
SHA3-256, SHA-512/256 (bonus), and SHAKE128 (bonus). The SHA-2 and Keccak
implementations are written in Python; `hashlib` is used only by the test and
comparison scripts as an independent reference.

## Files

- `assignment_data.py` — supplied assignment test vectors. Keep this file in
  the project root so `part2/test_hashes.py` can import it.
- `part2/sha2.py` — SHA-256, SHA-512, SHA-512/256.
- `part2/sha3.py` — SHA3-256, SHAKE128, and Keccak-f[1600].
- `part2/test_hashes.py` — assignment vectors, boundary cases, deterministic
  random tests, and streaming/update tests.
- `part2/avalanche.py` — reproducible avalanche-effect experiment; writes a
  histogram PNG if Matplotlib is installed (optional).
- `part2/length_extension.py` — demonstrates a SHA-256 secret-prefix MAC
  length-extension forgery, compares SHA3-256 behavior, and checks HMAC-SHA256.

## Run (Python 3.9+)

From this folder:

```bash
python -m py_compile assignment_data.py part2/*.py
python part2/test_hashes.py
python part2/avalanche.py --n 1000 --seed 2026 --len 64
python part2/length_extension.py --secret-len 16 --seed 1
```

Matplotlib is optional. If it is unavailable, the avalanche script still prints
its numeric results and skips only the plot.

## Important interpretation notes

- A passing comparison against `hashlib` is useful independent validation, but
  it does not replace a written explanation of the algorithm or the instructor's
  required analysis.
- The fallback vectors in `test_hashes.py` are used only if `assignment_data.py`
  or `SHA_VECTORS` is missing. The script labels that fallback clearly. With the
  included assignment data, it loads the supplied SHA-256, SHA-512, and SHA3-256
  vectors.
- SHA-256 length extension applies to a naive `SHA256(secret || message)` tag,
  not to HMAC-SHA256. Do not use a secret-prefix hash as a message authentication
  construction in real systems; use HMAC or a suitable standardized MAC.
- The pure-Python implementations are educational and are not constant-time;
  use vetted cryptographic libraries for production security.
- Review and understand the implementation, adapt it to the exact assignment
  requirements, and disclose AI/reference assistance as required by your course.
