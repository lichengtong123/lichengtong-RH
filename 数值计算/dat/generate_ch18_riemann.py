"""Generate the N=100 cosine model, calibrated at x=16.

The data ordinate is pi_N(x)-C-6; plot tick labels restore the baseline 6.
Zero midpoints are read from the chapter 19 interval certificates.
"""

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORDER = 100


def load_zeros():
    source = ROOT / "numerical/ch19/results/zeros.json"
    records = json.loads(source.read_text(encoding="utf-8"))["intervals"]
    return [float(row["gamma"].split()[0].lstrip("["))
            for row in records[:ORDER]]


def model(x, heights):
    logx = math.log(x)
    correction = sum(
        2 * math.sqrt(x) / (math.hypot(0.5, g) * logx)
        * math.cos(g * logx - math.atan2(g, 0.5))
        for g in heights
    )
    return x / logx + x / logx**2 - correction


if __name__ == "__main__":
    heights = load_zeros()
    assert len(heights) == ORDER
    calibration = model(16, heights) - 6
    output = Path(__file__).with_name("riemann_data.dat")
    with output.open("w", encoding="ascii") as stream:
        stream.write("x y\n")
        for i in range(1000):
            x = 10 + 25 * i / 999
            y = model(x, heights) - calibration - 6
            stream.write(f"{x:.6f} {y:.6f}\n")
    print(f"Generated {output.name}: N={ORDER}, C={calibration:.12g}")
