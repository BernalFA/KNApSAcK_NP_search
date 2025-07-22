import time
from functools import wraps


def timer(func):
    """Decorator for time execution measurements"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if execution_time < 1:
            # short run time
            print(f"\nExecution time for {func.__name__}: {execution_time:.4f} s\n")
        else:
            # run time above 1 s
            execution_time = time.gmtime(execution_time)
            fmt_time = time.strftime("%H:%M:%S", execution_time)
            print(f"\nExecution time: {fmt_time}\n")

        return result
    return wrapper
