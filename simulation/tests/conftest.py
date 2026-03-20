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

def pytest_configure(config):
    """Initial configuration for pytest."""
    pass
