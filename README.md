# Radar Tracking Simulation

A real-time radar tracking simulation built with Python and Pygame. Users can interact with radar blips by clicking to classify them as either real aircraft or noise signals. The system evaluates performance and logs all interactions for analysis.

## Features

- **Real-time Simulation**: Aircraft move with realistic physics and behaviors
- **Interactive Tagging**: Click radar blips to classify them as "real" or "noise"
- **Multiple Behaviors**: Straight-line flight and random erratic movement patterns
- **Performance Scoring**: Automatic evaluation of tagging accuracy
- **Session Logging**: Complete interaction history saved to JSON files
- **Extensible Architecture**: Plugin system for new behaviors and renderers

## Project Structure

```
radar_sim/
├── main.py                 # Application entry point
├── config.py              # Game constants and configuration
├── behaviors/             # Movement behavior system
│   ├── __init__.py
│   ├── base_behavior.py   # Abstract behavior interface
│   ├── straight_behavior.py # Straight-line movement
│   └── random_behavior.py # Erratic random movement
├── core/                  # Core simulation components
│   ├── __init__.py
│   ├── aircraft.py        # Real radar targets
│   ├── noise_blip.py      # False radar signals
│   ├── radar_object.py    # Abstract base for radar entities
│   ├── simulation.py      # Main simulation engine
│   ├── tagger.py          # Click handling and tagging logic
│   ├── scorer.py          # Performance evaluation system
│   └── logger.py          # Session logging and persistence
└── rendering/             # Display and rendering system
    ├── __init__.py
    ├── base_renderer.py   # Abstract renderer interface
    └── pygame_renderer.py # Pygame-based implementation
```

## Class Diagram

```plantuml
@startuml
abstract class RadarObject {
    +obj_id: str
    +x: float
    +y: float
    +tag: str
    +{abstract} cycle_tag()
    +{abstract} update(delta_time: float)
    +{abstract} get_type(): str
    +get_position(): tuple
}

class Aircraft {
    +speed: float
    +direction: float
    +behavior: BaseBehavior
    +update(delta_time: float)
    +get_type(): str
    -_wrap_around()
}

class NoiseBlip {
    +speed: float
    +behavior: BaseBehavior
    +flicker_chance: float
    +visible: bool
    +update(delta_time: float)
    +get_type(): str
}

abstract class BaseBehavior {
    +{abstract} move(x, y, speed, direction, delta_time): tuple
}

class StraightBehavior {
    +move(x, y, speed, direction, delta_time): tuple
}

class RandomBehavior {
    -_drift: float
    -_current_direction: float
    +move(x, y, speed, direction, delta_time): tuple
}

class Simulation {
    -_objects: list[RadarObject]
    +add_object(obj: RadarObject)
    +update(delta_time: float)
    +get_objects(): list[RadarObject]
}

class Tagger {
    +hit_radius: float
    +handle_click(click_x, click_y, objects): RadarObject
    -_distance(x1, y1, x2, y2): float
}

class Scorer {
    +history: list[dict]
    +evaluate_live(obj: RadarObject): str
    +evaluate_session(objects: list[RadarObject])
    +get_summary(): dict
    -_classify(tag: str, truth: str): str
}

class Logger {
    +output_dir: str
    +click_events: list[dict]
    +session_start: datetime
    +log_click(obj_id: str, tag: str, result: str)
    +save_session(summary: dict, history: list[dict])
    -_elapsed_seconds(): float
    -_build_filename(): str
}

abstract class BaseRenderer {
    +{abstract} initialize()
    +{abstract} clear()
    +{abstract} draw_radar_background()
    +{abstract} present()
    +{abstract} draw_object(x, y, obj_type, visible, tag)
    +{abstract} get_delta_time(): float
}

class PygameRenderer {
    +OBJECT_COLORS: dict
    +TAG_COLORS: dict
    +screen: Surface
    +clock: Clock
    -_delta_time: float
    +initialize()
    +clear()
    +draw_radar_background()
    +present()
    +draw_object(x, y, obj_type, visible, tag)
    +get_delta_time(): float
}

RadarObject <|-- Aircraft
RadarObject <|-- NoiseBlip
BaseBehavior <|-- StraightBehavior
BaseBehavior <|-- RandomBehavior
Simulation o-- RadarObject
Aircraft o-- BaseBehavior
NoiseBlip o-- BaseBehavior
BaseRenderer <|-- PygameRenderer
@enduml
```

## Sequence Diagram

```plantuml
@startuml
participant Main
participant Simulation
participant Aircraft
participant NoiseBlip
participant Tagger
participant Scorer
participant Logger
participant Renderer

Main->>Renderer: initialize()
Main->>Simulation: new Simulation()
Main->>Tagger: new Tagger()
Main->>Scorer: new Scorer()
Main->>Logger: new Logger()

loop Create Objects
    Main->>Simulation: add_object(Aircraft)
    Main->>Simulation: add_object(NoiseBlip)
end

loop Game Loop
    Main->>Renderer: get_delta_time()
    Renderer-->>Main: delta_time

    alt Mouse Click
        Main->>Tagger: handle_click(x, y, objects)
        Tagger->>Simulation: get_objects()
        Simulation-->>Tagger: objects
        Tagger-->>Main: tagged_object
        alt Object Tagged
            Main->>Scorer: evaluate_live(tagged_object)
            Scorer-->>Main: result
            Main->>Logger: log_click(obj_id, tag, result)
        end
    end

    Main->>Simulation: update(delta_time)
    loop Update Each Object
        Simulation->>Aircraft: update(delta_time)
        Aircraft->>StraightBehavior: move(x, y, speed, direction, delta_time)
        StraightBehavior-->>Aircraft: new_position
        Aircraft->>Aircraft: _wrap_around()

        Simulation->>NoiseBlip: update(delta_time)
        NoiseBlip->>RandomBehavior: move(x, y, speed, direction, delta_time)
        RandomBehavior-->>NoiseBlip: new_position
    end

    Main->>Renderer: clear()
    Main->>Renderer: draw_radar_background()
    loop Draw Each Object
        Main->>Simulation: get_objects()
        Simulation-->>Main: objects
        Main->>Renderer: draw_object(x, y, type, visible, tag)
    end
    Main->>Renderer: present()
end

Main->>Scorer: evaluate_session(objects)
Scorer->>Scorer: _classify() for each object
Main->>Scorer: get_summary()
Scorer-->>Main: summary
Main->>Logger: save_session(summary, history)
@enduml
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd RadarTrackingSimulation
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the simulation:**
   ```bash
   python radar_sim/main.py
   ```

2. **Game Controls:**
   - **Left Click**: Click on radar blips to cycle through tags (None → Real → Noise → None)
   - **Close Window**: Exit the simulation

3. **Visual Feedback:**
   - Green blips: Aircraft (real targets)
   - Red blips: Noise (false signals)
   - Cyan ring: Tagged as "real"
   - Orange ring: Tagged as "noise"
   - Flickering: Noise blips randomly appear/disappear

## Architecture Patterns

### Strategy Pattern (Behaviors)
Movement behaviors are interchangeable strategies that can be injected into radar objects:

```python
# Different behaviors for different objects
aircraft = Aircraft("AC001", 400, 300, 80, 45, StraightBehavior())
noise = NoiseBlip("N001", 300, 500, 40, RandomBehavior(drift_degrees=45))
```

### Abstract Factory (Renderers)
Multiple rendering backends can be swapped:

```python
# Could easily add OpenGLRenderer, TerminalRenderer, etc.
renderer = PygameRenderer()  # or WebGLRenderer(), etc.
```

### Observer Pattern (Logging/Scoring)
Multiple observers can watch and react to tagging events:

```python
# Logger and Scorer both observe the same events
logger.log_click(obj_id, tag, result)
scorer.evaluate_live(obj)
```

## Configuration

Edit `radar_sim/config.py` to customize:

- Window dimensions
- Radar radius
- Frame rate
- Colors

## Session Data

Each session creates a JSON file in the `sessions/` directory containing:

- Session metadata (start time, duration)
- Performance summary (true positives, false positives, etc.)
- Final object classifications
- Complete click history with timestamps

## Extending the System

### Adding New Behaviors
1. Create a new class inheriting from `BaseBehavior`
2. Implement the `move()` method
3. Use it when creating radar objects

### Adding New Object Types
1. Create a new class inheriting from `RadarObject`
2. Implement `update()` and `get_type()` methods
3. Add appropriate colors to the renderer

### Adding New Renderers
1. Create a new class inheriting from `BaseRenderer`
2. Implement all abstract methods
3. Update `main.py` to use the new renderer

## Dependencies

- **pygame**: Graphics and input handling
- **Python 3.8+**: Core language features

## License

[Add your license information here]