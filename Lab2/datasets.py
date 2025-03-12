import random

def nearly_sorted_array(n, k, min_val, max_val):
    arr = sorted(random.randint(min_val, max_val) for _ in range(n))
    for i in range(n):
        swap = random.randint(max(0, i - k), min(n - 1, i + k))
        arr[i], arr[swap] = arr[swap], arr[i]
    return arr

def sorted_array(n, min_val, max_val):
    arr = sorted(random.randint(min_val, max_val) for _ in range(n))
    return arr

def reverse_sorted_array(n, min_val, max_val):
    arr = sorted([random.randint(min_val, max_val) for _ in range(n)], reverse=True)
    return arr

def random_array(n, min_val, max_val):
    arr = [random.randint(min_val, max_val) for _ in range(n)]
    return arr