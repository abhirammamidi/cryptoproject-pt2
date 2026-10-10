"""Task 2.4 - validate sha2.py / sha3.py against the official vectors and hashlib.

Run:  python test_hashes.py        (exit status 0 = all PASS, 1 = any FAIL)
hashlib is used here ONLY as an independent reference; the implementations
under test never import it.
"""
import hashlib
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    """Load assignment_data.SHA_VECTORS in either per-algorithm or row-based form.

    Supported per-algorithm form (used by the supplied assignment_data.py):
        {"sha256": {message: hex_digest}, "sha512": {...}, "sha3_256": {...}}
    Also accepts a list of row dictionaries or tuples. If unavailable, clearly
    labelled fallback cases are compared against hashlib (not official vectors).
    """
    try:
        from assignment_data import SHA_VECTORS
    except (ImportError, AttributeError):
        print("NOTE: assignment_data.SHA_VECTORS not found -> using FALLBACK messages "
              "(reference = hashlib only; NOT the official vectors)")
        msgs = [b"", b"abc", b"abcdef", b"a" * 55, b"a" * 56, b"a" * 111,
                b"a" * 112, b"a" * 1000,
                b"The quick brown fox jumps over the lazy dog"]
        return [(m, {n: ref(m) for n, (_, ref) in ALGOS.items()}) for m in msgs], False

    out = {}
    if isinstance(SHA_VECTORS, dict) and any(str(k).lower().replace('-', '').replace('_', '')
                                             in ('sha256', 'sha512', 'sha3256')
                                             for k in SHA_VECTORS):
        key_map = {
            'sha256': 'SHA-256', 'sha512': 'SHA-512', 'sha3256': 'SHA3-256',
            'sha3': 'SHA3-256',
        }
        for algorithm_key, mapping in SHA_VECTORS.items():
            norm = str(algorithm_key).lower().replace('-', '').replace('_', '')
            name = key_map.get(norm)
            if not name or not isinstance(mapping, dict):
                continue
            for message, digest in mapping.items():
                out.setdefault(_to_bytes(message), {})[name] = str(digest).lower()
        if out:
            return list(out.items()), True

    items = SHA_VECTORS.values() if isinstance(SHA_VECTORS, dict) else SHA_VECTORS
    for entry in items:
        if isinstance(entry, dict):
            message_key = next((k for k in entry if str(k).lower() in
                                ('msg', 'message', 'input', 'data', 'm')), None)
            if message_key is None:
                continue
            message = _to_bytes(entry[message_key])
            expected = {}
            for key, value in entry.items():
                if key == message_key:
                    continue
                low = str(key).lower().replace('_', '').replace('-', '')
                name = ('SHA3-256' if 'sha3' in low or low == 'sha3256' else
                        'SHA-512' if 'sha512' in low or low == '512' else
                        'SHA-256' if 'sha256' in low or low == '256' else None)
                if name:
                    expected[name] = str(value).lower()
            if expected:
                out.setdefault(message, {}).update(expected)
        elif isinstance(entry, (tuple, list)) and len(entry) == 4:
            message, s256, s512, s3 = entry
            out[_to_bytes(message)] = {'SHA-256': str(s256).lower(),
                                       'SHA-512': str(s512).lower(),
                                       'SHA3-256': str(s3).lower()}
    if not out:
        raise ValueError('SHA_VECTORS was found, but no supported test vectors were parsed.')
    return list(out.items()), True


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
            s.update(b"")                            # empty updates must be harmless
            while pos < len(m):                       # random positive chunk sizes
                k = rng.randint(1, 150)
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
