import time


def secant(f, x0, x1, tol=1e-6, max_iter=10000):
    errors = []
    start = time.perf_counter()

    for i in range(max_iter):
        f0, f1 = f(x0), f(x1)

        if f1 - f0 == 0:
            raise ValueError("Division by zero: f(x1) == f(x0)")

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        dx = abs(x2 - x1)
        errors.append(dx)

        if dx <= tol:
            elapsed = time.perf_counter() - start
            return {"root": x2, "iterations": i + 1, "errors": errors,
                    "time": elapsed, "converged": True}

        x0, x1 = x1, x2

    elapsed = time.perf_counter() - start
    return {"root": x1, "iterations": max_iter, "errors": errors,
            "time": elapsed, "converged": False}
