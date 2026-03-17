import time


def newton(f, x0, tol=1e-6, max_iter=10000, h=1e-7):
    errors = []
    start = time.perf_counter()
    x = x0

    for i in range(max_iter):
        fx = f(x)
        fpx = (f(x + h) - f(x - h)) / (2 * h)

        if fpx == 0:
            raise ValueError("Derivative is zero at x = {x}")

        dx = fx / fpx
        x = x - dx
        errors.append(abs(dx))

        if abs(dx) <= tol:
            elapsed = time.perf_counter() - start
            return {"root": x, "iterations": i + 1, "errors": errors,
                    "time": elapsed, "converged": True}

    elapsed = time.perf_counter() - start
    return {"root": x, "iterations": max_iter, "errors": errors,
            "time": elapsed, "converged": False}
