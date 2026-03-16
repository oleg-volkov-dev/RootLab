import cmath
import time


def muller(f, x0, x1, x2, tol=1e-6, max_iter=10000):
    v1, v2, v3 = x0, x1, x2
    errors = []
    start = time.perf_counter()

    for i in range(max_iter):
        h1 = v2 - v1
        h2 = v3 - v2
        f1, f2, f3 = f(v1), f(v2), f(v3)

        s1 = (f2 - f1) / h1
        s2 = (f3 - f2) / h2

        a = (s2 - s1) / (h2 + h1)
        b = a * h2 + s2
        c = f3

        disc = cmath.sqrt(b ** 2 - 4 * a * c)
        denom = (b + disc) if abs(b + disc) > abs(b - disc) else (b - disc)

        if denom == 0:
            break

        dx = -2 * c / denom
        root = v3 + dx
        errors.append(abs(dx))

        if abs(dx) <= tol:
            elapsed = time.perf_counter() - start
            root_val = root.real if abs(root.imag) < 1e-10 else root
            return {"root": root_val, "iterations": i + 1, "errors": errors,
                    "time": elapsed, "converged": True}

        v1, v2, v3 = v2, v3, root

    elapsed = time.perf_counter() - start
    return {"root": v3, "iterations": max_iter, "errors": errors,
            "time": elapsed, "converged": False}
