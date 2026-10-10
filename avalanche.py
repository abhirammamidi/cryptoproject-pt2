"""Task 2.5 - avalanche experiment for SHA-256 and SHA3-256.

Flip ONE random input bit of 1000 random messages, count the changed output
bits, report mean / SD, and draw a histogram. Everything is computed when you
run it; nothing is hard-coded.
Run:  python avalanche.py [--n 1000] [--seed 2026] [--len 64]
"""
import argparse
import math
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sha2 import SHA256
from sha3 import SHA3_256


def changed_bits(cls, msg, bit):
    flipped = bytearray(msg)
    flipped[bit // 8] ^= 1 << (bit % 8)
    a = int.from_bytes(cls(msg).digest(), "big")
    b = int.from_bytes(cls(bytes(flipped)).digest(), "big")
    return bin(a ^ b).count("1")


def run(cls, n, length, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        msg = rng.randbytes(length)
        out.append(changed_bits(cls, msg, rng.randrange(length * 8)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--len", type=int, default=64, help="message length in bytes")
    args = ap.parse_args()
    if args.n < 2:
        ap.error("--n must be at least 2 so the sample standard deviation is defined")
    if args.len < 1:
        ap.error("--len must be at least 1 byte")

    data = {}
    for name, cls in (("SHA-256", SHA256), ("SHA3-256", SHA3_256)):
        v = run(cls, args.n, args.len, args.seed)
        data[name] = v
        mean, sd = statistics.mean(v), statistics.stdev(v)
        se = 8 / math.sqrt(len(v))            # std. error of the mean if SD = 8
        print(f"{name}: n={len(v)}  mean={mean:.3f}  SD={sd:.3f}  min={min(v)}  max={max(v)}")
        print(f"   ideal (Binomial(256, 1/2)): mean 128, SD 8; |mean-128| = {abs(mean - 128):.3f}"
              f"  ({abs(mean - 128) / se:.2f} standard errors)")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: histogram skipped")
        return
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, (name, v) in zip(axes, data.items()):
        ax.hist(v, bins=range(96, 162, 2), color="#2A7F8E", edgecolor="white")
        ax.axvline(128, color="#C0392B", ls="--", label="ideal mean = 128")
        ax.axvline(statistics.mean(v), color="#E0A030", label=f"measured mean = {statistics.mean(v):.1f}")
        ax.set_title(f"{name}: changed bits after a 1-bit flip (n={len(v)})")
        ax.set_xlabel("number of output bits changed (of 256)")
        ax.legend()
    axes[0].set_ylabel("count")
    plt.tight_layout()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avalanche_histogram.png")
    plt.savefig(path, dpi=200)
    print("wrote", path)


if __name__ == "__main__":
    main()
