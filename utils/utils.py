import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret_value = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return ret_value
    
    return wrapper