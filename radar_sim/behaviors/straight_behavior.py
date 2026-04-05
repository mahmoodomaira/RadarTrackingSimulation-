import math
from behaviors.base_behavior import BaseBehavior

class StraightBehavior(BaseBehavior):
    def move(self, x, y, speed, direction, delta_time) -> tuple[float, float, float]:
        radians = math.radians(direction)
        new_x = x + math.cos(radians) * speed * delta_time
        new_y = y + math.sin(radians) * speed * delta_time
        return (new_x, new_y, direction)
    
"""

### The Math — Don't Skip This

This is the key formula you'll reuse everywhere:
```
new_x = x + cos(direction) * speed * delta_time
new_y = y + sin(direction) * speed * delta_time
```

Visualized:
```
        0° (right)
             │
  270°───────┼───────90°
  (up)       │        (down)
             │
           180° (left)

  An aircraft at direction=45° moves
  diagonally down-right each frame.
"""