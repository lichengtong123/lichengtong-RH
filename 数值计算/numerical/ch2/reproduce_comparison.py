"""Recompute chapter 2's comparison data on its existing sampling grid."""
from pathlib import Path
import csv
import math
import mpmath as mp


def main():
    path = Path(__file__).resolve().parents[2] / "dat/pi_x_comparison.dat"
    with path.open() as stream:
        rows = list(csv.DictReader(stream, delimiter=" "))
    xs = [int(row["x"]) for row in rows]
    limit = max(xs)
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p*p::p] = b"\x00" * ((limit-p*p)//p + 1)
    counts = {}
    targets = set(xs)
    count = 0
    for n in range(limit + 1):
        count += sieve[n]
        if n in targets:
            counts[n] = count
    output = ["x pi Li xlog"]
    for x in xs:
        with mp.workdps(50):
            li50 = mp.li(x) - mp.li(2)
            xlog50 = mp.mpf(x) / mp.log(x)
            li_text = f"{float(li50):.6f}"
            xlog_text = f"{float(xlog50):.6f}"
        with mp.workdps(80):
            assert abs(mp.mpf(li_text) - (mp.li(x)-mp.li(2))) <= mp.mpf("0.0000005")
            assert abs(mp.mpf(xlog_text) - mp.mpf(x)/mp.log(x)) <= mp.mpf("0.0000005")
        output.append(f"{x} {counts[x]} {li_text} {xlog_text}")
    path.write_text("\n".join(output) + "\n")
    print(f"Verified and regenerated {len(xs)} samples; Li uses integral from 2.")


if __name__ == "__main__":
    main()
