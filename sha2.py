"""SHA-256, SHA-512 (and SHA-512/256) from the FIPS 180-4 specification.

One parameterised implementation serves both word sizes. Every constant is
GENERATED from prime numbers with exact integer arithmetic (no pasted tables),
and hashlib is never used here.
"""
import struct


# --------------------------------------------------------------- constants
def _first_primes(n):
    ps, c = [], 2
    while len(ps) < n:
        if all(c % p for p in ps if p * p <= c):
            ps.append(c)
        c += 1
    return ps


def _icbrt(n):
    """Exact floor of the cube root of n (Newton iteration on integers)."""
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            return x
        x = y


def _frac_sqrt(p, w):     # first w bits of the fractional part of sqrt(p)
    from math import isqrt
    return isqrt(p << (2 * w)) & ((1 << w) - 1)


def _frac_cbrt(p, w):     # first w bits of the fractional part of cbrt(p)
    return _icbrt(p << (3 * w)) & ((1 << w) - 1)


_P = _first_primes(80)
_IV32 = [_frac_sqrt(p, 32) for p in _P[:8]]
_K32 = [_frac_cbrt(p, 32) for p in _P[:64]]
_IV64 = [_frac_sqrt(p, 64) for p in _P[:8]]
_K64 = [_frac_cbrt(p, 64) for p in _P[:80]]


# --------------------------------------------------------------- compression
def _make_compress(w, K, S0, S1, s0, s1):
    """Build the compression function for word size w (32 or 64 bits).
    S0, S1 = three rotation amounts of Sigma0 / Sigma1;
    s0, s1 = two rotations and one right shift of sigma0 / sigma1."""
    M = (1 << w) - 1
    rounds = len(K)
    fmt = ">16I" if w == 32 else ">16Q"
    a0, a1, a2 = S0
    e0, e1, e2 = S1
    p0, p1, h0 = s0
    q0, q1, h1 = s1

    def compress(H, block):
        W = list(struct.unpack(fmt, block))
        for i in range(16, rounds):                     # message schedule
            x, y = W[i - 15], W[i - 2]
            W.append((W[i - 16] + W[i - 7]
                      + (((x >> p0) | (x << (w - p0))) ^ ((x >> p1) | (x << (w - p1))) ^ (x >> h0))
                      + (((y >> q0) | (y << (w - q0))) ^ ((y >> q1) | (y << (w - q1))) ^ (y >> h1))) & M)
        a, b, c, d, e, f, g, h = H
        for i in range(rounds):                         # compression rounds
            t1 = (h + K[i] + W[i] + ((e & f) ^ (~e & g))
                  + (((e >> e0) | (e << (w - e0))) ^ ((e >> e1) | (e << (w - e1))) ^ ((e >> e2) | (e << (w - e2)))))
            t2 = ((((a >> a0) | (a << (w - a0))) ^ ((a >> a1) | (a << (w - a1))) ^ ((a >> a2) | (a << (w - a2))))
                  + ((a & b) ^ (a & c) ^ (b & c)))
            h, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
        return [(x + y) & M for x, y in zip(H, (a, b, c, d, e, f, g, h))]   # feed-forward
    return compress


_compress32 = _make_compress(32, _K32, (2, 13, 22), (6, 11, 25), (7, 18, 3), (17, 19, 10))
_compress64 = _make_compress(64, _K64, (28, 34, 39), (14, 18, 41), (1, 8, 7), (19, 61, 6))


# --------------------------------------------------------------- the hash classes
class _SHA2:
    _W = _IV = _compress = _BS = _LF = _OUT = None     # set by the subclasses

    def __init__(self, data=b"", *, _state=None, _count=0):
        # _state / _count let length_extension.py resume from a known digest.
        self._h = list(self._IV if _state is None else _state)
        self._buf = b""
        self._len = _count                              # total bytes hashed so far
        if data:
            self.update(data)

    @classmethod
    def padding(cls, msg_len):
        """0x80, zeros, then the bit length as a big-endian integer."""
        zeros = (-(msg_len + 1 + cls._LF)) % cls._BS
        return b"\x80" + b"\x00" * zeros + (msg_len * 8).to_bytes(cls._LF, "big")

    def update(self, data):
        data = bytes(data)
        self._len += len(data)
        buf, bs, comp, h = self._buf + data, self._BS, self._compress, self._h
        end = len(buf) - len(buf) % bs
        for i in range(0, end, bs):
            h = comp(h, buf[i:i + bs])
        self._h, self._buf = h, buf[end:]

    def digest(self):
        tail = self._buf + self.padding(self._len)      # pad a COPY: object stays usable
        h, comp, bs = self._h, self._compress, self._BS
        for i in range(0, len(tail), bs):
            h = comp(h, tail[i:i + bs])
        return b"".join(x.to_bytes(self._W // 8, "big") for x in h)[:self._OUT]

    def hexdigest(self):
        return self.digest().hex()

    def copy(self):
        c = type(self)(_state=self._h, _count=self._len)
        c._buf = self._buf
        return c


class SHA256(_SHA2):
    _W, _IV, _compress, _BS, _LF, _OUT = 32, _IV32, staticmethod(_compress32), 64, 8, 32


class SHA512(_SHA2):
    _W, _IV, _compress, _BS, _LF, _OUT = 64, _IV64, staticmethod(_compress64), 128, 16, 64


def _sha512_t_iv(t):
    """FIPS 180-4 section 5.3.6: derive the SHA-512/t initial value."""
    class _Gen(SHA512):
        _IV = [x ^ 0xA5A5A5A5A5A5A5A5 for x in _IV64]
    return list(struct.unpack(">8Q", _Gen(b"SHA-512/%d" % t).digest()))


class SHA512_256(SHA512):
    """SHA-512/256: SHA-512 with a different (derived) IV, output cut to 256 bits."""
    _IV = _sha512_t_iv(256)
    _OUT = 32


if __name__ == "__main__":
    print(SHA256(b"abc").hexdigest())
    print(SHA512(b"abc").hexdigest())
