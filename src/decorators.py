import functools
import os
import scipy
import time


def cache(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            path = "./cache/%s.npy" % name
            if os.path.isfile(path):
                return scipy.load(path)
            os.makedirs("./cache", exist_ok=True)
            value = func(*args, **kwargs)
            scipy.save(path, value)
            return value
        return wrapper
    return decorator


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} seconds")
        return value
    return wrapper
