import pytest
from unittest.mock import MagicMock, patch
import pymunk
import pygame

# Import the simulation module. We need to do this after the mock in conftest.py
# However, for clarity and to ensure mocks are applied, we can use a fixture.

import simulation.main as main

@pytest.fixture
def tournament():
    team_names = list(main.TEAMS.keys())[:8]
    return main.Tournament(team_names)

def test_tournament_initialization(tournament):
    assert len(tournament.qf) == 4
    assert tournament.current_round == "QF"
    assert tournament.current_match_idx == 0
    assert tournament.winner is None

def test_tournament_advance_qf(tournament):
    match = tournament.get_current_match()
    assert match is not None
    tournament.advance(match[0], 2, 1)
    assert tournament.qf_results[0] == (match[0], "2-1")
    assert tournament.sf[0][0] == match[0]
    assert tournament.current_match_idx == 1

def test_tournament_advance_to_sf(tournament):
    for i in range(4):
        match = tournament.get_current_match()
        tournament.advance(match[0], 1, 0)
    
    assert tournament.current_round == "SF"
    assert tournament.current_match_idx == 0
    assert all(res is not None for res in tournament.qf_results)
    assert all(tm is not None for tm in tournament.sf[0])
    assert all(tm is not None for tm in tournament.sf[1])

def test_tournament_advance_to_final(tournament):
    # Pass QF
    for i in range(4):
        match = tournament.get_current_match()
        tournament.advance(match[0], 1, 0)
    
    # Pass SF
    for i in range(2):
        match = tournament.get_current_match()
        tournament.advance(match[0], 1, 0)
        
    assert tournament.current_round == "FINAL"
    assert tournament.current_match_idx == 0
    assert all(tm is not None for tm in tournament.final)

def test_tournament_complete(tournament):
    # Pass QF
    for i in range(4): tournament.advance(tournament.get_current_match()[0], 1, 0)
    # Pass SF
    for i in range(2): tournament.advance(tournament.get_current_match()[0], 1, 0)
    # Pass Final
    match = tournament.get_current_match()
    tournament.advance(match[0], 1, 0)
    
    assert tournament.current_round == "COMPLETE"
    assert tournament.winner == match[0]

def test_short_name():
    assert main.short_name("Real Madrid") == "R. Madrid"
    assert main.short_name("Barcelona") == "Barca"
    assert main.short_name("Manchester City") == "Man City"
    assert main.short_name("Unknown Team") == "Unknown Team"

@pytest.fixture
def mock_space():
    return MagicMock(spec=pymunk.Space)

def test_ball_initialization(mock_space):
    with patch("simulation.main.pygame.image.load"), \
         patch("simulation.main.pygame.Surface"), \
         patch("simulation.main.get_asset_path"):
        ball = main.Ball(mock_space, 100, 200)
    
    assert ball.radius == 8
    mock_space.add.assert_called()
    assert ball.body.position == (100, 200)

def test_player_initialization(mock_space):
    with patch("simulation.main.pygame.image.load"), \
         patch("simulation.main.pygame.Surface"), \
         patch("simulation.main.get_asset_path"):
        player = main.Player(mock_space, 300, 400, (255, 0, 0), 0, "Test Player")
    
    assert player.name == "Test Player"
    assert player.team == 0
    assert player.radius == 15
    mock_space.add.assert_called()
    assert player.body.position == (300, 400)

def test_player_update_ai_has_ball(mock_space):
    ball = MagicMock()
    ball.body.position = pymunk.Vec2d(310, 400)
    ball.radius = 8
    
    player = main.Player(mock_space, 300, 400, (255, 0, 0), 0)
    player.radius = 15
    
    teammates = [player]
    opponents = []
    game = MagicMock()
    
    # Distance is 10, which is < 15 + 8 + 12 = 35
    player.update_ai(ball, teammates, opponents, 100, game)
    
    assert player.has_ball is True
    # Check that ball velocity is set to keep it in front
    assert ball.body.velocity != (0, 0)

def test_player_update_ai_positioning_chaser(mock_space):
    ball = MagicMock()
    ball.body.position = pymunk.Vec2d(500, 300)
    
    player = main.Player(mock_space, 100, 100, (255, 0, 0), 0)
    teammates = [player]
    opponents = []
    game = MagicMock()
    
    # As the only teammate, he should be the chaser (rank 0)
    player.update_ai(ball, teammates, opponents, 100, game)
    
    assert player.is_chasing is True
    assert player.is_passing_option is False
    # Check that velocity is directed towards the ball
    expected_dir = (ball.body.position - player.body.position).normalized()
    assert player.body.velocity.normalized().dot(expected_dir) > 0.9

def test_player_update_ai_positioning_passing_option(mock_space):
    ball = MagicMock()
    ball.body.position = pymunk.Vec2d(500, 300)
    
    p1 = main.Player(mock_space, 490, 300, (255, 0, 0), 0) # Chaser
    p2 = main.Player(mock_space, 100, 100, (255, 0, 0), 0) # Option
    
    teammates = [p1, p2]
    opponents = []
    game = MagicMock()
    
    # p2 should be rank 1 -> is_passing_option
    p2.update_ai(ball, teammates, opponents, 100, game)
    
    assert p2.is_chasing is False
    assert p2.is_passing_option is True
    
    # Verify lateral positioning (my fix)
    # target_x = ball_pos.x + 30 = 530
    # target_y = ball_pos.y - 120 = 180 (since rank is 1)
    # Support pos should be around (530, 180)
    expected_support_x = ball.body.position.x + 30
    expected_support_y = ball.body.position.y - 120
    
    # Check if velocity is towards support pos
    dir_to_support = pymunk.Vec2d(expected_support_x, expected_support_y) - p2.body.position
    assert p2.body.velocity.normalized().dot(dir_to_support.normalized()) > 0.9

def test_player_update_ai_positioning_defender(mock_space):
    ball = MagicMock()
    ball.body.position = pymunk.Vec2d(500, 300)
    
    p1 = main.Player(mock_space, 490, 300, (255, 0, 0), 0) # Chaser
    p2 = main.Player(mock_space, 495, 300, (255, 0, 0), 0) # Option 1
    p3 = main.Player(mock_space, 496, 300, (255, 0, 0), 0) # Option 2
    p4 = main.Player(mock_space, 100, 100, (255, 0, 0), 0) # Defender
    
    teammates = [p1, p2, p3, p4]
    opponents = []
    game = MagicMock()
    
    # p4 should be rank 3 -> Defender
    p4.update_ai(ball, teammates, opponents, 100, game)
    
    assert p4.is_chasing is False
    assert p4.is_passing_option is False
    # Defender should be moving towards own goal area
    # Team 0 own goal is at x=0
    assert p4.body.velocity.x < 0

def test_player_update_ai_decision_shoot(mock_space):
    ball = MagicMock()
    ball.body.position = pymunk.Vec2d(780, 300) # Close to goal
    
    player = main.Player(mock_space, 770, 300, (255, 0, 0), 0)
    player.has_ball = True
    player.last_action = 0
    player.control_start_tick = 0
    
    teammates = [player]
    opponents = [] # No opponents, so path is clear
    game = MagicMock()
    game.kick_sound = MagicMock()
    
    # Force decision to SHOOT by mocking random and ensuring conditions are met
    # With no opponents, snap_shot_opportunity will be True
    with patch("random.random", return_value=0.0): # High intel effect
        player.update_ai(ball, teammates, opponents, 100, game)
        
    # Check if ball.body.apply_impulse_at_local_point was called with a shot vector
    # Toward goal_center (WIDTH, HEIGHT//2) = (800, 300)
    ball.body.apply_impulse_at_local_point.assert_called()
    impulse = ball.body.apply_impulse_at_local_point.call_args[0][0]
    assert impulse.x > 0 # Shooting towards right goal

def test_player_update_ai_decision_pass(mock_space):
    ball = MagicMock()
    ball.body.position = pymunk.Vec2d(400, 300)
    
    p1 = main.Player(mock_space, 390, 300, (255, 0, 0), 0)
    p1.has_ball = True
    p1.last_action = 0
    p1.control_start_tick = 0
    
    p2 = main.Player(mock_space, 450, 200, (255, 0, 0), 0) # Teammate to pass to
    
    teammates = [p1, p2]
    opponents = [MagicMock()] # Add an opponent to block shots/dribble
    opponents[0].body.position = pymunk.Vec2d(500, 300) # Directly ahead
    opponents[0].stun_timer = 0
    
    game = MagicMock()
    
    # Force decision to "PASS" by mocking random.choice if necessary, 
    # but under pressure and with targets, PASS is likely.
    with patch("random.random", return_value=0.0), \
         patch("random.choice", return_value="PASS"):
        p1.update_ai(ball, teammates, opponents, 100, game)
        
    ball.body.apply_impulse_at_local_point.assert_called()
    impulse = ball.body.apply_impulse_at_local_point.call_args[0][0]
    # Check if impulse is towards p2
    dir_to_p2 = (p2.body.position - p1.body.position).normalized()
    assert impulse.normalized().dot(dir_to_p2) > 0.9

@patch("simulation.main.pygame.display.set_mode")
@patch("simulation.main.pygame.font.SysFont")
@patch("simulation.main.pygame.mixer.init")
@patch("simulation.main.pygame.mixer.Sound")
def test_game_initialization(mock_sound, mock_mixer_init, mock_font, mock_display, mock_space):
    with patch("simulation.main.pymunk.Space", return_value=mock_space):
        game = main.Game()
    
    assert game.score_blue == 0
    assert game.state == "START"
    assert len(game.players) == 10 # 5v5

def test_game_goal_scoring(mock_space):
    with patch("simulation.main.pygame.display.set_mode"), \
         patch("simulation.main.pygame.font.SysFont"), \
         patch("simulation.main.pygame.mixer.init"), \
         patch("simulation.main.pygame.mixer.Sound"), \
         patch("simulation.main.pymunk.Space", return_value=mock_space):
        game = main.Game()
    
    game.state = "PLAYING"
    # Move ball into right goal
    game.ball.body.position = pymunk.Vec2d(main.WIDTH + 1, main.HEIGHT // 2)
    
    with patch("simulation.main.Game.reset_pitch"):
        game.update()
        
    assert game.score_blue == 1
    assert game.state == "GOAL"

def test_game_countdown_transition(mock_space):
    with patch("simulation.main.pygame.display.set_mode"), \
         patch("simulation.main.pygame.font.SysFont"), \
         patch("simulation.main.pygame.mixer.init"), \
         patch("simulation.main.pygame.mixer.Sound"), \
         patch("simulation.main.pymunk.Space", return_value=mock_space):
        game = main.Game()
    
    game.state = "GOAL"
    game.auto_start_timer = 1
    
    game.update()
    assert game.state == "COUNTDOWN"
    assert game.countdown_timer == main.FPS * 3

def test_game_countdown_to_playing(mock_space):
    with patch("simulation.main.pygame.display.set_mode"), \
         patch("simulation.main.pygame.font.SysFont"), \
         patch("simulation.main.pygame.mixer.init"), \
         patch("simulation.main.pygame.mixer.Sound"), \
         patch("simulation.main.pymunk.Space", return_value=mock_space):
        game = main.Game()
    
    game.state = "COUNTDOWN"
    game.countdown_timer = 1
    
    game.update()
    assert game.state == "PLAYING"





