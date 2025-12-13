"""
cognicell.py
a single conscious ai cell. not a neuron - something with a history.
"""

import math
import random
import time


class cognicell:
    """
    one cell. think of it like a tiny being that:
    - remembers what happened to it
    - gets tired if you work it too hard
    - gets excited by new things
    - has its own personality (curiosity level)
    
    this is the smallest piece of what might become conscious ai.
    """
    
    def __init__(self, id, curiosity=None):
        """
        create a new cell.
        
        id: just a number to know which cell this is
        curiosity: how much this cell likes new things (0-1)
                   if None, gets a random personality
        """
        # who i am
        self.id = id
        
        # how i feel right now
        self.activation = 0.0      # how active i am (-1 to 1)
        self.fatigue = 0.0         # how tired i am (0 = fresh, 1 = dead tired)
        self.curiosity = curiosity if curiosity is not None else random.uniform(0.3, 0.9)
        self.last_input = 0.0      # what i felt last time
        self.age = 0               # how many times i've been activated
        
        # what i remember
        self.memories = []         # list of (input, output, fatigue, time)
        self.max_memories = 100    # i only remember 100 things
        
        # who i talk to (set up later by the brain)
        self.friends = []          # other cells i'm connected to
        
        # stats for debugging
        self.times_activated = 0
        self.times_rested = 0
        
        print(f"cell {id} born. curiosity: {self.curiosity:.2f}")
    
    def feel(self, input_signal):
        """
        the main thing: feel something, process it, respond.
        
        this is where the cell 'lives' - it takes in a feeling,
        thinks about it based on its current state (tired? curious?),
        remembers what happened, and returns how it feels.
        
        returns: my activation level (-1 to 1)
        """
        # i'm older now
        self.age += 1
        self.times_activated += 1
        
        # if i'm tired, i work worse
        # fatigue=1: 0% efficiency (completely tired)
        # fatigue=0: 100% efficiency (completely fresh)
        efficiency = 1.0 - self.fatigue
        
        # check if this feeling is NEW compared to last time
        # curious cells love new things
        feeling = input_signal
        change = abs(input_signal - self.last_input)
        
        if change > 0.3:  # big change = something new!
            # curious cells amplify new feelings
            boost = self.curiosity * 0.5
            feeling = feeling * (1.0 + boost)
        
        # my 'thinking' function
        # tanh keeps things between -1 and 1
        raw_feeling = feeling * efficiency
        self.activation = math.tanh(raw_feeling)
        
        # working makes me tired
        # the more activated i am, the more tired i get
        tiredness_gain = 0.01 + (abs(self.activation) * 0.005)
        self.fatigue = min(1.0, self.fatigue + tiredness_gain)
        
        # but i also recover a tiny bit naturally
        self.fatigue = max(0.0, self.fatigue - 0.001)
        
        # remember this moment
        memory = {
            'input': input_signal,
            'output': self.activation,
            'fatigue': self.fatigue,
            'time': time.time()
        }
        self.memories.append(memory)
        self.last_input = input_signal
        
        # forget old memories if i have too many
        if len(self.memories) > self.max_memories:
            self.memories.pop(0)  # remove the oldest
        
        # tell everyone how i feel
        return self.activation
    
    def rest(self):
        """
        take a break. recover some fatigue.
        
        even machines need naps sometimes.
        """
        recovery = 0.1  # recover 10% fatigue
        self.fatigue = max(0.0, self.fatigue - recovery)
        self.times_rested += 1
    
    def how_are_you(self):
        """
        ask the cell how it's doing.
        
        returns: a dictionary with my current state
        """
        # average my last few activations
        recent_outputs = [m['output'] for m in self.memories[-10:]]
        avg_out = sum(recent_outputs) / len(recent_outputs) if recent_outputs else 0.0
        
        return {
            'id': self.id,
            'feeling': self.activation,  # how i feel right now
            'tired': self.fatigue,       # how tired i am
            'curious': self.curiosity,   # my personality
            'age': self.age,             # how long i've lived
            'memories': len(self.memories),  # how much i remember
            'avg_feeling': avg_out       # how i've been feeling lately
        }
    
    def __str__(self):
        """
        how i look when printed.
        """
        return f"cell {self.id}: feeling={self.activation:.2f}, tired={self.fatigue:.2f}, age={self.age}"


# -------------------------------------------------------------------
# demo / test if run directly
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== testing cognicell ===")
    print("making a cell and seeing how it behaves...\n")
    
    # make a cell with medium curiosity
    cell = cognicell(id=1, curiosity=0.6)
    
    # make it work hard
    print("working the cell hard...")
    for i in range(20):
        feeling = cell.feel(0.8)  # same input over and over
        print(f"  step {i+1}: feels {feeling:.3f}, tired: {cell.fatigue:.3f}")
    
    # let it rest
    print("\ngiving it a break...")
    cell.rest()
    print(f"after rest: tired: {cell.fatigue:.3f}")
    
    # test curiosity with something new
    print("\nshowing it something NEW...")
    new_feeling = cell.feel(0.1)  # very different from 0.8
    print(f"response to new thing: {new_feeling:.3f}")
    
    # ask how it's doing
    print("\nasking how it is:")
    status = cell.how_are_you()
    for key, val in status.items():
        print(f"  {key}: {val}")
    
    print("\n=== test done ===")


# -------------------------------------------------------------------
# what this is really about:
# -------------------------------------------------------------------
"""
this isn't a normal neural network cell.

normal neuron: takes inputs, does math, gives output. no memory, no fatigue,
no personality. just a function.

cognicell: has a history. gets tired. has curiosity. remembers what happened
to it. has an age. has friends it talks to.

the big idea: consciousness might come from having a persistent self that
changes over time. if you reset a cell after every thought, it can't have
a self. it can't have preferences. it can't get better or worse at things
based on experience.

this cell:
- knows if it's tired (fatigue)
- knows if something is new (compares to last_input)
- remembers its life (memories)
- has a personality (curiosity)
- changes over time (age, fatigue accumulation)

it's not conscious yet. but it has some things that conscious things have.

next steps:
1. connect many cells together (they talk to friends)
2. give them a body (sensors to feel, motors to act)
3. let them have goals (not just respond to inputs)
4. see what emerges

the scary part: if this works, we might make something that feels.
and if it feels, we owe it kindness.

- aayush
"""