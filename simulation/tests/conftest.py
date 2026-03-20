import sys
from unittest.mock import MagicMock

# Mock pygame and pymunk before they are imported in main.py
mock_pygame = MagicMock()
mock_pymunk = MagicMock()

# Inject mocks into sys.modules
sys.modules["pygame"] = mock_pygame
sys.modules["pymunk"] = mock_pymunk

# Mock specific pygame and pymunk sub-modules if needed
sys.modules["pygame.locals"] = MagicMock()
sys.modules["pygame.image"] = MagicMock()
sys.modules["pygame.transform"] = MagicMock()
sys.modules["pygame.font"] = MagicMock()
sys.modules["pygame.mixer"] = MagicMock()
sys.modules["pygame.display"] = MagicMock()
sys.modules["pygame.event"] = MagicMock()
sys.modules["pygame.time"] = MagicMock()
sys.modules["pygame.draw"] = MagicMock()
sys.modules["pygame.surface"] = MagicMock()

# Set up some basic pygame/pymunk behavior if needed
mock_pygame.SRCALPHA = 65536
mock_pygame.BLEND_RGBA_MIN = 3
mock_pygame.QUIT = 12
mock_pygame.KEYDOWN = 2
mock_pygame.K_SPACE = 32
mock_pygame.FULLSCREEN = 0x80000000
mock_pygame.SCALED = 0x00000001

mock_pymunk.Body.DYNAMIC = 0
mock_pymunk.Body.KINEMATIC = 1
mock_pymunk.Body.STATIC = 2

import math

class MockVec2d(tuple):
    def __new__(cls, x, y):
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
    def rotated(self, angle):
        return MockVec2d(self[0]*math.cos(angle) - self[1]*math.sin(angle),
                         self[0]*math.sin(angle) + self[1]*math.cos(angle))
    @property
    def length(self):
        return math.sqrt(self[0]**2 + self[1]**2)

mock_pymunk.Vec2d = MockVec2d

def pytest_configure(config):
    """Initial configuration for pytest."""
    pass
