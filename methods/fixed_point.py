import time


def fixed_point(g, x0, tol=1e-6, max_iter=10000):
    errors = []
    start = time.perf_counter()
    x = x0

    for i in range(max_iter):
        x_new = g(x)
        err = abs(x_new - x)
        errors.append(err)

        if err <= tol:
            elapsed = time.perf_counter() - start
            return {"root": x_new, "iterations": i + 1, "errors": errors,
                    "time": elapsed, "converged": True}

        x = x_new

    elapsed = time.perf_counter() - start
    return {"root": x, "iterations": max_iter, "errors": errors,
            "time": elapsed, "converged": False}
