from functools import wraps
import time
import datetime

def timer(func):
    """Print the runtime of the decorated function"""
    wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        run_time_minutes = datetime.timedelta(seconds=run_time)
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs {run_time_minutes}")
        return value
    return wrapper_timer