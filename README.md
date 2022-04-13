# Language
[Englsh](README.md)

[한국어](README.ko.md)

# ipydoodle

![image](docs/images/ipydoodle.png)

ipydoodle is 2D visualization library for student running on Jupyter environment.

# Goals

ipydoodle is made for students who are not familiar with coding. So our goal is helping them learn coding easily and joyfully.

## Immediate Feedback

In order for students to be interested, even a very simple code need to be responsive when they are executed, like "Hello, World" In ipydoodle, "Hello, World" is:

![image](docs/images/helloworld.png)

## Object Based Render

When you define an object ipydoodle renders the object similar to the real world. This intuitive structure helps students understand ipydoodle easily.

For example, the following code slowly moves the circle in the center of the screen to the right:
```python
from ipydoodle import *
import time
World()
ball = Circle()
for _ in range(100):
    ball.x += 1
    time.sleep(0.05)
```

# Documentation

Documentation is [here](https://github.com/team-monolith-product/ipydoodle/wiki).

# Installation

Just use pip.

```
pip install ipydoodle
```

# Examples

## Free Fall Simulation

![image](docs/images/example1.gif)