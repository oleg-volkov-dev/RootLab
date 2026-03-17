import time


def bisection(f, a, b, tol=1e-6, max_iter=10000):
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    errors = []
    start = time.perf_counter()

    for i in range(max_iter):
        mid = (a + b) / 2.0
        fm = f(mid)
        errors.append(abs(b - a) / 2.0)

        if abs(b - a) / 2.0 <= tol or fm == 0:
            elapsed = time.perf_counter() - start
            return {"root": mid, "iterations": i + 1, "errors": errors,
                    "time": elapsed, "converged": True}

        if f(a) * fm < 0:
            b = mid
        else:
            a = mid

    elapsed = time.perf_counter() - start
    return {"root": (a + b) / 2.0, "iterations": max_iter, "errors": errors,
            "time": elapsed, "converged": False}
