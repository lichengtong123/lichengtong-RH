"""Reproduce the strict decimal bounds in note 16 with FLINT ball arithmetic.

Dependency: python-flint 0.9.0. Run: python3 认证示例.py
The wider decimal endpoints include all displayed rounding errors.
"""
import flint
from flint import acb, arb, ctx


def hardy_z(t):
    theta = acb(arb("0.25"), t / 2).lgamma().imag - t * arb.pi().log() / 2
    value = acb(0, theta).exp() * acb(arb("0.5"), t).zeta()
    assert value.imag.contains(0)
    return value.real


def verify(bits):
    with ctx.workprec(bits):
        euler = arb.const_euler()
        log4pi = (4 * arb.pi()).log()
        assert arb("0.57721") < euler < arb("0.57722")
        assert arb("2.53102") < log4pi < arb("2.53103")
        values = [
            ("lambda_1", 1 + euler / 2 - log4pi / 2,
             "0.02309570896612", "0.02309570896613"),
            ("Z(14.1347)", hardy_z(arb("14.1347")),
             "-0.000019941389", "-0.000019941387"),
            ("Z(14.1348)", hardy_z(arb("14.1348")),
             "0.000059374978", "0.000059374981"),
        ]
        for name, value, lo, hi in values:
            assert arb(lo) < value < arb(hi), (bits, name, value)
            print(f"{bits} bits: {lo} < {name} < {hi}; ball={value.str(40)}")


if __name__ == "__main__":
    print("python-flint", flint.__version__)
    for precision in (160, 224):
        verify(precision)
