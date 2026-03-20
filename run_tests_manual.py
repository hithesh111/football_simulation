import sys
from unittest.mock import MagicMock

# CRITICAL: Mocking must happen before any other imports
mock = MagicMock()
sys.modules["pygame"] = mock
sys.modules["pygame.locals"] = mock
sys.modules["pygame.image"] = mock
sys.modules["pygame.transform"] = mock
sys.modules["pygame.font"] = mock
sys.modules["pygame.mixer"] = mock
sys.modules["pygame.display"] = mock
sys.modules["pygame.event"] = mock
sys.modules["pygame.time"] = mock
sys.modules["pygame.draw"] = mock
sys.modules["pymunk"] = mock

# Define a minimal Vec2d-like behavior for the mock
import math
class MockVec2d(tuple):
    def __new__(cls, x=0, y=0):
        if isinstance(x, (tuple, list)):
            return super(MockVec2d, cls).__new__(cls, (x[0], x[1]))
        return super(MockVec2d, cls).__new__(cls, (x, y))
    @property
    def x(self): return self[0]
    @property
    def y(self): return self[1]
    def get_distance(self, other):
        return math.sqrt((self[0] - other[0])**2 + (self[1] - other[1])**2)
    def __sub__(self, other):
        return MockVec2d(self[0] - other[0], self[1] - other[1])
    def __add__(self, other):
        return MockVec2d(self[0] + other[0], self[1] + other[1])
    def __mul__(self, other):
        return MockVec2d(self[0] * other, self[1] * other)
    def normalized(self):
        mag = math.sqrt(self[0]**2 + self[1]**2)
        if mag == 0: return MockVec2d(0, 0)
        return MockVec2d(self[0]/mag, self[1]/mag)
    def dot(self, other):
        return self[0] * other[0] + self[1] * other[1]
    @property
    def length(self):
        return math.sqrt(self[0]**2 + self[1]**2)
    def rotated(self, angle):
        return MockVec2d(self[0]*math.cos(angle) - self[1]*math.sin(angle),
                         self[0]*math.sin(angle) + self[1]*math.cos(angle))

mock.Vec2d = MockVec2d
mock.Body.DYNAMIC = 0

import pytest
if __name__ == "__main__":
    # Add root to sys.path
    import os
    sys.path.insert(0, os.getcwd())
    sys.exit(pytest.main(["simulation/tests/test_simulation.py"]))
