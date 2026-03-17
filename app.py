import math
import cmath
import streamlit as st
import matplotlib.pyplot as plt

from methods.muller import muller
from methods.bisection import bisection

st.set_page_config(page_title="RootLab", layout="centered")

st.title("RootLab")
st.caption("Numerical Root-Finding Dashboard")

# ── Inputs ────────────────────────────────────────────────────────────────────
st.subheader("Function")
expr = st.text_input("f(x) =", value="x**3 - x - 2",
                     help="Use Python syntax: x**2, math.sin(x), math.exp(x), etc.")

st.subheader("Initial Points")
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


# ── Solve ─────────────────────────────────────────────────────────────────────
if st.button("Solve", type="primary", use_container_width=True):
    try:
        f = make_func(expr)
    except Exception as e:
        st.error(f"Invalid function: {e}")
        st.stop()

    results = []

    # ── Run methods (add others here as implemented) ──────────────────────────
    methods = [
        ("Bisection",            lambda: bisection(f, x0, x2)),
        ("False Position",       None),
        ("Fixed-Point Iteration",None),
        ("Newton",               None),
        ("Secant",               None),
        ("Müller",               lambda: muller(f, x0, x1, x2)),
    ]

    convergence = {}

    for name, fn in methods:
        if fn is None:
            results.append({"Method": name, "Root": "—", "Iterations": "—",
                            "Time (ms)": "—", "Converged": "—"})
            continue
        try:
            res = fn()
            root = res["root"]
            root_str = (f"{root.real:.8f}+{root.imag:.6f}j"
                        if isinstance(root, complex) else f"{root:.10f}")
            results.append({
                "Method":      name,
                "Root":        root_str,
                "Iterations":  res["iterations"],
                "Time (ms)":   f"{res['time'] * 1000:.4f}",
                "Converged":   "Yes" if res["converged"] else "No",
            })
            if res["errors"]:
                convergence[name] = res["errors"]
        except Exception as e:
            results.append({"Method": name, "Root": f"Error: {e}",
                            "Iterations": "—", "Time (ms)": "—", "Converged": "No"})

    # ── Results table ─────────────────────────────────────────────────────────
    st.subheader("Results")
    st.table(results)

    # ── Convergence curves ────────────────────────────────────────────────────
    if convergence:
        st.subheader("Convergence")
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
