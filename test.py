import time
from matplotlib import pyplot as plt


def timed(f, *args, n_iter=100):
    acc = float('inf')
    for i in range(n_iter):
        t0 = time.perf_counter()
        f(*args)
        t1 = time.perf_counter()
        acc = min(acc, t1 - t0)

    return acc


def fib1(n):  # slow Fibonacci numbers
    assert n >= 0
    return n if n <= 1 else fib1(n - 1) + fib1(n - 2)


print(fib1(8))
print(timed(fib1, 8), 'seconds')
#print(fib1(80))  # very SLOW

old_fib1 = fib1
cashe = {}


def fib2(n):  # recursive Fibonacci numbers, can't recursive inf
    assert n >= 0
    if n not in cashe:
        cashe[n] = n if n <= 1 else fib1(n - 1) + fib1(n - 2)
    return cashe[n]


print(fib2(30))
print(timed(fib2, 30), 'seconds')
#print(fib2(800))  # very SLOW


def memo(f):
    cashe = {}
    def inner(n):
        if n not in cashe:
            cashe[n] = f(n)
        return cashe[n]
    return inner


fib1 = memo(old_fib1)
print(fib1(80))  # now speed fib1 > fib2, but we have recursive
print(timed(fib1, 80), 'seconds')
#print(fib1(800))  # can't recursive self to infinity


def fib3(n):
    assert n >= 0
    f0, f1 = 0, 1
    for i in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


print(fib3(800))  # very fast and not recursive
print(timed(fib3, 800), 'seconds')


def compare(fs, args):
    for f in fs:
        plt.plot(args, [timed(f, arg) for arg in args], label=f.__name__)
    plt.legend()
    plt.grid(True)


compare([fib1, fib3], list(range(300)))
fib1 = old_fib1
compare([fib1, fib2], list(range(20)))
compare([fib2, fib3], list(range(30)))
compare([fib1, fib3], list(range(10)))
