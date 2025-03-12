import time
import copy
import gc
import matplotlib.pyplot as plt
import numpy as np
import sys
from sort import quick_sort, merge_sort, bubble_sort, heap_sort
from datasets import nearly_sorted_array, sorted_array, reverse_sorted_array, random_array

def measure_execution_time(algorithm, data):
    data_copy = copy.deepcopy(data)
    gc.collect()
    start_time = time.time()
    algorithm(data_copy)
    end_time = time.time()
    return end_time - start_time

def run_experiment(sizes, algorithms, data_generator, data_name, min_val=0, max_val=1000, k_factor=0.1):
    results = {algo_name: [] for algo_name, _ in algorithms}
    print(f"Running experiments for {data_name} data...")
    for size in sizes:
        if data_name == "Nearly Sorted":
            k = max(1, int(size * k_factor))
            data = data_generator(size, k, min_val, max_val)
        else:
            data = data_generator(size, min_val, max_val)
        for algo_name, algorithm in algorithms:
            if algo_name == "Bubble Sort" and size > 10000 and data_name != "Sorted":
                results[algo_name].append(float('nan'))
                print(f"  Skipped {algo_name} for size {size} (too large)")
                continue
            try:
                if algo_name == "Quick Sort" and size > 50000:
                    current_limit = sys.getrecursionlimit()
                    sys.setrecursionlimit(max(current_limit, size + 100))
                print(f"  Testing {algo_name} on {data_name} data of size {size}")
                execution_time = measure_execution_time(algorithm, data)
                results[algo_name].append(execution_time)
                if algo_name == "Quick Sort" and size > 50000:
                    sys.setrecursionlimit(current_limit)
            except (RecursionError, MemoryError) as e:
                print(f"  Error with {algo_name} for size {size}: {e}")
                results[algo_name].append(float('nan'))
    return results

def plot_results(sizes, all_results):
    dataset_types = ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted"]
    
    for dataset in dataset_types:
        plt.figure(figsize=(10, 8))
        
        results = all_results[dataset]
        for algo_name, times in results.items():
            valid_indices = ~np.isnan(times)
            valid_sizes = [sizes[j] for j in range(len(sizes)) if valid_indices[j]]
            valid_times = [times[j] for j in range(len(times)) if valid_indices[j]]
            if len(valid_sizes) > 0:
                plt.plot(valid_sizes, valid_times, marker='o', label=algo_name, linewidth=2)
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Array Size', fontsize=12)
        plt.ylabel('Execution Time (s)', fontsize=12)
        plt.title(f'Sorting Algorithm Performance on {dataset} Arrays', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.xticks(sizes, [str(size) for size in sizes], rotation=45)
        
        plt.tight_layout()
        
        plt.savefig(f'Lab2/sorting_performance_{dataset.lower().replace(" ", "_")}.png', dpi=300)
        print(f"Plot saved as 'sorting_performance_{dataset.lower().replace(' ', '_')}.png'")
        
        plt.close()

algorithms = [
    ("Quick Sort", quick_sort),
    ("Merge Sort", merge_sort),
    ("Bubble Sort", bubble_sort),
    ("Heap Sort", heap_sort)
]
data_generators = [
    ("Random", random_array),
    ("Sorted", sorted_array),
    ("Reverse Sorted", reverse_sorted_array),
    ("Nearly Sorted", nearly_sorted_array)
]
sizes = [100, 500, 1000, 5000, 10000, 50000, 100000, 250000]
all_results = {}
for data_name, data_generator in data_generators:
    all_results[data_name] = run_experiment(
        sizes, algorithms, data_generator, data_name
    )
plot_results(sizes, all_results)