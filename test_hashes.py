"""Task 2.4 - validate sha2.py / sha3.py against the official vectors and hashlib.

Run:  python test_hashes.py        (exit status 0 = all PASS, 1 = any FAIL)
hashlib is used here ONLY as an independent reference; the implementations
under test never import it.
"""
import hashlib
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.dirname(_HERE)):          # part2/ and the project root (assignment_data.py)
    if _p not in sys.path:
        sys.path.insert(0, _p)
from sha2 import SHA256, SHA512, SHA512_256
from sha3 import SHA3_256, SHAKE128

# name -> (our class, reference function returning a hex digest)
ALGOS = {
    "SHA-256": (SHA256, lambda m: hashlib.sha256(m).hexdigest()),
    "SHA-512": (SHA512, lambda m: hashlib.sha512(m).hexdigest()),
    "SHA3-256": (SHA3_256, lambda m: hashlib.sha3_256(m).hexdigest()),
}
BONUS = {   # extra algorithms: run too, but clearly labelled as bonus
    "SHA-512/256": (SHA512_256, lambda m: hashlib.new("sha512_256", m).hexdigest()),
    "SHAKE128(32B)": (SHAKE128, lambda m: hashlib.shake_128(m).hexdigest(32)),
}
KEY = {"sha256": "SHA-256", "sha512": "SHA-512", "sha3": "SHA3-256"}

_results = []       # (section, passed, total)


def section(name, checks):
    """checks = iterable of (ok, description). Prints the failures only."""
    passed = total = 0
    for ok, desc in checks:
        total += 1
        passed += bool(ok)
        if not ok:
            print(f"   FAIL: {desc}")
    _results.append((name, passed, total))
    print(f"[{'PASS' if passed == total else 'FAIL'}] {name}: {passed}/{total}")


# ---------------------------------------------------------------- official vectors
def _to_bytes(m):
    return m.encode() if isinstance(m, str) else bytes(m)


def load_vectors():
    """THIS REQUIRES assignment_data.py. Supported layouts of SHA_VECTORS:
      (1) {'sha256': {msg_bytes: hexdigest, ...}, 'sha512': {...}, 'sha3_256': {...}}   <- your file
      (2) a list of tuples (message, sha256_hex, sha512_hex, sha3_256_hex)
    Without assignment_data.py a clearly labelled hashlib-only fallback is used."""
    try:
        from assignment_data import SHA_VECTORS
    except ImportError:
        print("NOTE: assignment_data.SHA_VECTORS not found -> FALLBACK messages "
              "(reference = hashlib only; NOT the official vectors)")
        msgs = [b"", b"abc", b"abcdef", b"a" * 55, b"a" * 56, b"a" * 111, b"a" * 112, b"a" * 1000,
                b"The quick brown fox jumps over the lazy dog"]
        return [(m, {n: ref(m) for n, (_, ref) in ALGOS.items()}) for m in msgs], False
    if isinstance(SHA_VECTORS, dict):
        by_msg = {}
        for key, table in SHA_VECTORS.items():
            name = ("SHA3-256" if "3" in key else "SHA-512" if "512" in key else "SHA-256")
            for m, digest in table.items():
                by_msg.setdefault(_to_bytes(m), {})[name] = digest.lower()
        return list(by_msg.items()), True
    return [(_to_bytes(m), {"SHA-256": a.lower(), "SHA-512": b.lower(), "SHA3-256": c.lower()})
            for m, a, b, c in SHA_VECTORS], True


def test_vectors():
    vecs, official = load_vectors()
    checks = []
    for i, (m, exp) in enumerate(vecs):
        for name, (cls, ref) in ALGOS.items():
            if name in exp:
                got = cls(m).hexdigest()
                checks.append((got == exp[name], f"{name} vector #{i} (len {len(m)})"))
                checks.append((got == ref(m), f"{name} vs hashlib, vector #{i}"))
    section(f"{len(vecs)} specified messages x all algorithms" + ("" if official else " [FALLBACK]"), checks)


# ---------------------------------------------------------------- the rest
def test_boundaries():
    checks = []
    for n in (0, 1, 55, 56, 57, 63, 64, 65, 111, 112, 113, 127, 128, 129, 135, 136, 137):
        m = b"a" * n
        for name, (cls, ref) in {**ALGOS, **BONUS}.items():
            checks.append((cls(m).hexdigest() == ref(m), f"{name} length {n}"))
    section("boundary lengths (incl. 55/56/111/112 'a')", checks)


def test_random(seed=2026, count=1000):
    rng = random.Random(seed)
    checks = []
    for i in range(count):
        m = rng.randbytes(rng.randint(0, 300))
        for name, (cls, ref) in {**ALGOS, **BONUS}.items():
            checks.append((cls(m).hexdigest() == ref(m), f"{name} random #{i} len {len(m)}"))
    section(f"{count} random messages, lengths 0-300 (seed {seed})", checks)


def test_streaming(seed=7, count=300):
    rng = random.Random(seed)
    checks = []
    for name, (cls, _) in {**ALGOS, **BONUS}.items():
        a = cls()
        a.update(b"abc")
        a.update(b"def")
        checks.append((a.hexdigest() == cls(b"abcdef").hexdigest(), f"{name} abc+def"))
        h = cls(b"abc")
        checks.append((h.hexdigest() == h.hexdigest(), f"{name} digest() repeatable"))
        h.update(b"def")
        checks.append((h.hexdigest() == cls(b"abcdef").hexdigest(), f"{name} update after digest()"))
        for i in range(count):
            m = rng.randbytes(rng.randint(0, 400))
            s, pos = cls(), 0
            while pos < len(m):                       # random chunk sizes (including 0 and 1)
                k = rng.randint(0, 150)
                s.update(m[pos:pos + k])
                pos += k
            checks.append((s.hexdigest() == cls(m).hexdigest(), f"{name} chunked #{i} len {len(m)}"))
    section(f"streaming: random chunk sizes vs one-shot ({count} per algorithm)", checks)


if __name__ == "__main__":
    test_vectors()
    test_boundaries()
    test_random()
    test_streaming()
    bad = [r for r in _results if r[1] != r[2]]
    print("\n" + "=" * 50)
    print(f"SUMMARY: {len(_results) - len(bad)}/{len(_results)} sections passed -> "
          + ("ALL PASS" if not bad else "FAILURES PRESENT"))
    sys.exit(1 if bad else 0)
