"""SHA3-256 and SHAKE128 built from Keccak-f[1600] (FIPS 202). No hashlib.

State = 25 lanes of 64 bits, stored in a flat list with index x + 5*y.
The 24 round constants and the 25 rotation offsets are GENERATED, not pasted.
"""
import struct

_M64 = (1 << 64) - 1


def _round_constants():
    def lfsr(t):                        # bit t of the degree-8 LFSR
        if t % 255 == 0:
            return 1
        r = 1
        for _ in range(t % 255):
            r <<= 1
            if r & 0x100:
                r ^= 0x171              # x^8 + x^6 + x^5 + x^4 + 1
        return r & 1
    return [sum(lfsr(7 * i + j) << ((1 << j) - 1) for j in range(7)) for i in range(24)]


def _rotation_offsets():
    r = [0] * 25                        # r[x + 5y]; lane (0,0) is not rotated
    x, y = 1, 0
    for t in range(24):
        r[x + 5 * y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    return r


_RC = _round_constants()
_RHO = _rotation_offsets()
# pi: lane (x, y) moves to (y, 2x + 3y).  _PI[i] = destination index of lane i.
_PI = [(i // 5) + 5 * ((2 * (i % 5) + 3 * (i // 5)) % 5) for i in range(25)]
# chi uses the next two lanes in the same row.
_CH1 = [(i // 5) * 5 + (i % 5 + 1) % 5 for i in range(25)]
_CH2 = [(i // 5) * 5 + (i % 5 + 2) % 5 for i in range(25)]
_ROT = [(r, 64 - r) for r in _RHO]          # (left shift, right shift) per lane


def keccak_f(A):
    """Apply the 24 rounds Theta -> Rho -> Pi -> Chi -> Iota to a 25-lane list."""
    for rc in _RC:
        # Theta: XOR each lane with the parities of two neighbouring columns
        C = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
        D = [C[(x - 1) % 5] ^ (((C[(x + 1) % 5] << 1) | (C[(x + 1) % 5] >> 63)) & _M64) for x in range(5)]
        # Rho + Pi: rotate every lane by its offset and move it to its new place
        B = [0] * 25
        for i in range(25):
            v = A[i] ^ D[i % 5]
            left, right = _ROT[i]
            B[_PI[i]] = ((v << left) | (v >> right)) & _M64
        # Chi: the only non-linear step, applied along each row
        A = [B[i] ^ (~B[_CH1[i]] & B[_CH2[i]]) for i in range(25)]
        # Iota: break symmetry with the round constant (lane 0,0)
        A[0] ^= rc
    return A


class _Sponge:
    _RATE = _SUFFIX = _OUT = None

    def __init__(self, data=b""):
        self._A = [0] * 25
        self._buf = b""
        if data:
            self.update(data)

    def update(self, data):
        buf, rate = self._buf + bytes(data), self._RATE
        end = len(buf) - len(buf) % rate
        A, nl = self._A, rate // 8
        for i in range(0, end, rate):                   # absorb full blocks
            lanes = struct.unpack("<%dQ" % nl, buf[i:i + rate])
            for j in range(nl):
                A[j] ^= lanes[j]
            A = keccak_f(A)
        self._A, self._buf = A, buf[end:]

    def _final_state(self):
        rate = self._RATE
        block = bytearray(self._buf) + bytearray(rate - len(self._buf))
        block[len(self._buf)] ^= self._SUFFIX           # domain bits + first pad bit
        block[rate - 1] ^= 0x80                         # last pad bit (pad10*1)
        A, nl = list(self._A), rate // 8
        lanes = struct.unpack("<%dQ" % nl, bytes(block))
        for j in range(nl):
            A[j] ^= lanes[j]
        return keccak_f(A)

    def _squeeze(self, n):
        A, out = self._final_state(), b""
        while True:
            out += struct.pack("<%dQ" % (self._RATE // 8), *A[:self._RATE // 8])
            if len(out) >= n:
                return out[:n]
            A = keccak_f(A)                             # squeeze more

    def hexdigest(self, n=None):
        return self.digest(n).hex()

    def copy(self):
        c = type(self)()
        c._A, c._buf = list(self._A), self._buf
        return c


class SHA3_256(_Sponge):
    _RATE, _SUFFIX, _OUT = 136, 0x06, 32               # rate 1088 bits, capacity 512

    def digest(self):
        return self._squeeze(32)

    def hexdigest(self):
        return self.digest().hex()


class SHAKE128(_Sponge):
    _RATE, _SUFFIX = 168, 0x1F                          # rate 1344 bits, capacity 256

    def digest(self, n=32):
        return self._squeeze(n)

    def hexdigest(self, n=32):
        return self.digest(n).hex()


if __name__ == "__main__":
    print(SHA3_256(b"abc").hexdigest())
    print(SHAKE128(b"abc").hexdigest(32))
