import time


def false_position(f, a, b, tol=1e-6, max_iter=10000):
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    errors = []
    start = time.perf_counter()
    prev = None

    for i in range(max_iter):
        fa, fb = f(a), f(b)
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        if prev is not None:
            errors.append(abs(c - prev))
        prev = c

        if abs(fc) <= tol:
            elapsed = time.perf_counter() - start
            return {"root": c, "iterations": i + 1, "errors": errors,
                    "time": elapsed, "converged": True}

        if fa * fc < 0:
            b = c
        else:
            a = c

    elapsed = time.perf_counter() - start
    return {"root": c, "iterations": max_iter, "errors": errors,
            "time": elapsed, "converged": False}
