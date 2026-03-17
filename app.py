import math
import cmath
import streamlit as st
import matplotlib.pyplot as plt

from methods.muller import muller
from methods.bisection import bisection
from methods.false_position import false_position
from methods.fixed_point import fixed_point
from methods.newton import newton
from methods.secant import secant

st.set_page_config(page_title="RootLab", layout="centered")

st.title("RootLab")
st.caption("Numerical Root-Finding Dashboard")

# Function section
st.subheader("Function")
st.caption("The equation you want to solve, written as f(x) = 0.")
expr = st.text_input("f(x) =", value="x**3 - x - 2",
                     help="Use Python syntax: x**2, math.sin(x), math.exp(x), etc.")

# Fixed-Point g(x) 
st.subheader("Fixed-Point Iteration")
st.caption(
    "Optional. Fixed-point iteration requires rewriting f(x) = 0 as x = g(x) by hand — "
    "there is no single automatic way to do it, and the wrong rearrangement will diverge. "
    "Leave this blank to skip Fixed-Point Iteration and run the other 5 methods."
)
fp_col, _ = st.columns([2, 1])
g_expr = fp_col.text_input("g(x) =", value="",
                            placeholder="e.g. (x + 2) ** (1/3)",
                            help="Rewrite f(x)=0 as x=g(x). Convergence depends on |g'(x)| < 1 near the root.")

# Initial Points 
st.subheader("Initial Points")
st.caption(
    "x₀ and x₂ are used as the bracket [a, b] by Bisection, False Position, and Secant — "
    "f(x₀) and f(x₂) must have opposite signs. "
    "All three points are used by Müller. Fixed-Point Iteration and Newton start from x₀."
)
col1, col2, col3 = st.columns(3)
x0 = col1.number_input("x₀", value=0.0)
x1 = col2.number_input("x₁", value=1.0)
x2 = col3.number_input("x₂", value=2.0)


def make_func(expression):
    ns = {
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
        "pi": math.pi, "e": math.e, "abs": abs,
        "math": math, "cmath": cmath,
    }
    def f(x):
        ns["x"] = x
        return eval(expression, {"__builtins__": {}}, ns)
    return f


# Solve button
if st.button("Solve", type="primary", use_container_width=True):
    try:
        f = make_func(expr)
    except Exception as e:
        st.error(f"Invalid function: {e}")
        st.stop()

    g = None
    if g_expr.strip():
        try:
            g = make_func(g_expr)
        except Exception as e:
            st.error(f"Invalid g(x): {e}")
            st.stop()

    results = []

    # Run methods 
    methods = [
        ("Bisection",             lambda: bisection(f, x0, x2)),
        ("False Position",        lambda: false_position(f, x0, x2)),
        ("Fixed-Point Iteration", (lambda: fixed_point(g, x0)) if g else None),
        ("Newton",                lambda: newton(f, x0)),
        ("Secant",                lambda: secant(f, x0, x2)),
        ("Müller",                lambda: muller(f, x0, x1, x2)),
    ]

    convergence = {}

    for name, fn in methods:
        if fn is None:
            results.append({"Method": name, "Root": "no g(x) provided", "Iterations": "—",
                            "Time (ms)": "—", "Converged": "—"})
            continue
        try:
            res = fn()
            root = res["root"]
            root_str = (f"{root.real:.8f}+{root.imag:.6f}j"
                        if isinstance(root, complex) else f"{root:.10f}")
            results.append({
                "Method":     name,
                "Root":       root_str,
                "Iterations": res["iterations"],
                "Time (ms)":  f"{res['time'] * 1000:.4f}",
                "Converged":  "Yes" if res["converged"] else "No",
            })
            if res["errors"]:
                convergence[name] = res["errors"]
        except Exception as e:
            results.append({"Method": name, "Root": f"Error: {e}",
                            "Iterations": "—", "Time (ms)": "—", "Converged": "No"})

    # Results table
    st.subheader("Results")
    st.table(results)

    # Convergence curves diagram
    if convergence:
        st.subheader("Convergence")
        st.caption("Error per iteration on a log scale. Steeper drop = faster convergence.")
        fig, ax = plt.subplots(figsize=(8, 4))
        for name, errors in convergence.items():
            ax.semilogy(range(1, len(errors) + 1), errors, marker="o", markersize=3, label=name)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("|Δx| (log scale)")
        ax.set_title("Error per Iteration")
        ax.legend()
        ax.grid(True, which="both", linestyle="--", alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)
