"""Task 2.6 - SHA-256 length-extension forgery (and why SHA3-256 / HMAC resist it).

Attacker knows: tag = SHA256(secret || message), message, len(secret).
Attacker does NOT use: the secret itself.
Run:  python length_extension.py [--secret-len 16] [--seed 1]
"""
import argparse
import hashlib
import hmac as std_hmac
import os
import random
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sha2 import SHA256
from sha3 import SHA3_256, keccak_f


def forge_sha256(tag_hex, message, secret_len, extra):
    """Return (forged_message, forged_tag_hex) without knowing the secret."""
    state = list(struct.unpack(">8I", bytes.fromhex(tag_hex)))      # digest == final state
    glue = SHA256.padding(secret_len + len(message))                # padding the server added
    consumed = secret_len + len(message) + len(glue)                # a multiple of 64
    h = SHA256(_state=state, _count=consumed)                       # resume the compression
    h.update(extra)
    return message + glue + extra, h.hexdigest(), glue


def naive_sha3_attempt(tag, secret_len, message, extra):
    """Try the same trick on SHA3-256: load the 32 digest bytes as the first 4 lanes of the
    state and guess the other 21 lanes (including the 512-bit capacity) are zero."""
    A = [0] * 25
    A[:4] = struct.unpack("<4Q", tag)
    h = SHA3_256()
    h._A = keccak_f(A)          # the best an attacker can do: one more permutation
    h.update(extra)
    return h.hexdigest()


def hmac_sha256(key, msg):
    key = SHA256(key).digest() if len(key) > 64 else key
    key = key.ljust(64, b"\x00")
    inner = SHA256(bytes(b ^ 0x36 for b in key) + msg).digest()
    return SHA256(bytes(b ^ 0x5C for b in key) + inner).digest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--secret-len", type=int, default=16)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    secret = rng.randbytes(args.secret_len)        # the server's key (never given to the attacker)
    message = b"amount=100&to=alice"
    extra = b"&amount=1000000&to=mallory"

    tag = SHA256(secret + message).hexdigest()     # what the victim publishes
    assert tag == hashlib.sha256(secret + message).hexdigest()
    print("original message :", message)
    print("original tag     :", tag)

    forged_msg, forged_tag, glue = forge_sha256(tag, message, args.secret_len, extra)
    print("\n--- SHA-256 forgery (attacker used only tag, message, len(secret)) ---")
    print("glue padding     :", glue)
    print("forged message   :", forged_msg)
    print("forged message hex:", forged_msg.hex())
    print("forged tag       :", forged_tag)
    real = hashlib.sha256(secret + forged_msg).hexdigest()      # verification with hashlib
    print("hashlib(secret || forged_message):", real)
    print("FORGERY VERIFIED :", real == forged_tag)

    print("\n--- same attack on SHA3-256 ---")
    t3 = SHA3_256(secret + message).digest()
    guess = naive_sha3_attempt(t3, args.secret_len, message, extra)
    real3 = hashlib.sha3_256(secret + message + extra).hexdigest()
    print("attacker's guess :", guess)
    print("true SHA3-256    :", real3)
    print("ATTACK WORKS     :", guess == real3, "(expected False: the capacity bits are hidden)")

    print("\n--- HMAC-SHA256 ---")
    mac = hmac_sha256(secret, message)
    print("matches stdlib hmac:", mac == std_hmac.new(secret, message, hashlib.sha256).digest())
    print("a length-extended message has an unrelated HMAC; the outer hash hides the inner state.")


if __name__ == "__main__":
    main()
