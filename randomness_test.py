"""
test_randomness.py
proving why cognicell gives identical results.
"""
import random
import time

print("=== Testing Python's Randomness ===")

# Test 1: Default random behavior
print("\n1. Normal random.random():")
for i in range(3):
    print(f"   Run {i}: {random.random()}")  # Same each program run!

# Test 2: With time-based seed
print("\n2. With time-based seed:")
random.seed(int(time.time() * 1000) % 1000000)
print(f"   Seeded with time: {random.random()}")  # Different each time!

# Test 3: What cognicell.py actually uses
print("\n3. cognicell's random.uniform(0.3, 0.9):")
print(f"   First call: {random.uniform(0.3, 0.9)}")
print(f"   Second call: {random.uniform(0.3, 0.9)}")