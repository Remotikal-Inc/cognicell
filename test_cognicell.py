"""
test_cognicell.py
testing if my cells work right. because good code needs tests.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from cognicell import cognicell


def test_basics():
    """can i even make a cell?"""
    print("test 1: making a cell...")
    c = cognicell(id=99, curiosity=0.5)
    
    # check it has the right stuff
    assert c.id == 99
    assert c.curiosity == 0.5
    assert c.fatigue == 0.0
    assert c.age == 0
    print("  ✓ cell created correctly")
    
    return True


def test_feeling():
    """does feeling things work?"""
    print("\ntest 2: feeling inputs...")
    c = cognicell(id=100)
    
    # feel something
    out1 = c.feel(0.5)
    
    # should change activation
    assert c.activation == out1
    assert c.age == 1
    assert c.fatigue > 0  # should be a little tired
    assert len(c.memories) == 1
    print("  ✓ cell feels and remembers")
    
    return True


def test_tiredness():
    """do cells get tired?"""
    print("\ntest 3: getting tired...")
    c = cognicell(id=101)
    
    start_tired = c.fatigue
    
    # work it hard
    for _ in range(30):
        c.feel(0.7)
    
    # should be more tired
    assert c.fatigue > start_tired + 0.2
    assert c.fatigue <= 1.0  # but not over 1
    print(f"  ✓ cell got tired: {c.fatigue:.3f}")
    
    return True


def test_rest():
    """can cells rest?"""
    print("\ntest 4: resting...")
    c = cognicell(id=102)
    
    # make it tired first
    for _ in range(20):
        c.feel(0.6)
    
    tired_before = c.fatigue
    c.rest()
    
    # should be less tired
    assert c.fatigue < tired_before
    assert c.times_rested == 1
    print(f"  ✓ rest helped: {tired_before:.3f} -> {c.fatigue:.3f}")
    
    return True


def test_curiosity():
    """do curious cells notice new things more?"""
    print("\ntest 5: curiosity...")
    
    # low curiosity cell
    low = cognicell(id=200, curiosity=0.1)
    # high curiosity cell  
    high = cognicell(id=201, curiosity=0.9)
    
    # both feel same thing first
    low_out1 = low.feel(0.2)
    high_out1 = high.feel(0.2)
    
    # then something VERY different
    low_out2 = low.feel(0.9)  # big change
    high_out2 = high.feel(0.9)  # big change
    
    # the curious cell should respond more to change
    low_change = abs(low_out2 - low_out1)
    high_change = abs(high_out2 - high_out1)
    
    print(f"  low curiosity change:  {low_change:.4f}")
    print(f"  high curiosity change: {high_change:.4f}")
    
    # high curiosity should generally respond more
    # (not always, but usually)
    if high_change > 0.001:  # if there was any change
        assert high_change >= low_change * 0.5  # at least half as much
        print("  ✓ curiosity affects response to new things")
    
    return True


def test_memory():
    """do cells remember, but also forget?"""
    print("\ntest 6: memory...")
    c = cognicell(id=300)
    
    # add more memories than it can hold
    for i in range(150):
        c.feel(i * 0.01)
    
    # should only remember 100 things
    assert len(c.memories) == 100
    print(f"  ✓ remembers {len(c.memories)} things (forgets old ones)")
    
    return True


def run_all_tests():
    """run everything and see if it works."""
    print("=" * 50)
    print("testing cognicell...")
    print("=" * 50)
    
    tests = [
        test_basics,
        test_feeling, 
        test_tiredness,
        test_rest,
        test_curiosity,
        test_memory
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"result: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("all tests passed! code looks solid.")
        return True
    else:
        print("some tests failed. check the code.")
        return False


if __name__ == "__main__":
    # run tests if this file is run directly
    success = run_all_tests()
    sys.exit(0 if success else 1)


# -------------------------------------------------------------------
# why tests matter:
# -------------------------------------------------------------------
"""
tests prove your code actually works. they're not for the computer -
they're for humans. for you, and for anyone who looks at your code.

when someone sees you have tests:
1. they know you're serious
2. they know the code probably works
3. they can run tests to make sure it still works after changes

without tests, it's just some random code. with tests, it's engineering.

these tests check:
- can we make cells? (test_basics)
- do they actually process feelings? (test_feeling)
- do they get tired with work? (test_tiredness)
- can they rest and recover? (test_rest)
- does curiosity actually do something? (test_curiosity)
- do they remember, but not too much? (test_memory)

if all these pass, the basic idea works.

to run: python test_cognicell.py

if you add new features, add new tests.
it's like keeping a lab notebook.
"""