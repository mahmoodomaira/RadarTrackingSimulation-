# core/radar_object.py
from abc import ABC, abstractmethod

class RadarObject(ABC):
    """
    Abstract base for anything that appears on the radar screen.
    All radar objects have a position, an id, and must be updatable.
    """

    def __init__(self, obj_id: str, x: float, y: float):
        self.obj_id = obj_id
        self.x = x
        self.y = y

    @abstractmethod
    def update(self, delta_time: float):
        """
        Advance the object's state by one timestep.
        delta_time: seconds elapsed since last frame.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Return a string label for this object's type.
        e.g. 'aircraft', 'noise', 'unknown'
        """
        pass

    def get_position(self) -> tuple:
        """Return current (x, y) position."""
        return (self.x, self.y)
    
"""    
### Two Things Worth Noticing

**1. `delta_time` in `update()`**

Rather than moving a fixed number of pixels per frame, we'll move by `speed × delta_time`. This means:
```
# Bad — speed depends on frame rate
x += 5

# Good — speed is consistent regardless of frame rate
x += speed * delta_time
```

If your computer runs at 30fps instead of 60fps, the aircraft still travels the same distance per second. This is standard engineering practice.

**2. `get_position()` is NOT abstract**

It's a concrete method on the base class because every subclass implements position the same way — as `(self.x, self.y)`. Only methods that *differ* between subclasses need to be abstract. This is **Interface Segregation** — don't force subclasses to re-implement what they all share identically.

---

### Next: `core/aircraft.py`

Now we build the first concrete subclass. Before I show it, think about this:

> An `Aircraft` has a position, a speed, and a direction. But *how it moves* — straight line, random, zigzag — should NOT be hardcoded inside `Aircraft`.

Why? Because if you want to experiment with 5 different movement algorithms, you don't want 5 different `Aircraft` classes. You want **one** `Aircraft` class that accepts a **behavior object** telling it how to move.

This is the **Strategy Pattern** — and it's how we'll satisfy the Open/Closed principle.

It looks like this:
```
Aircraft
  └── has a → Behavior
                └── StraightBehavior   (for now)
                └── RandomBehavior     (later)
                └── ZigzagBehavior     (later)
                
"""