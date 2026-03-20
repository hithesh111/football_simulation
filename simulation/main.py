import pygame
import pymunk
import random
import os

# --- PATHS ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(path_in_assets):
    return os.path.join(BASE_PATH, "assets", path_in_assets)

# --- CONSTANTS ---
WIDTH, HEIGHT = 800, 600
PITCH_COLOR = (34, 139, 34)
FPS = 60

PLAYER_COLLISION_TYPE = 1
BALL_COLLISION_TYPE = 2

# --- TOURNAMENT SETTINGS ---
MATCH_TIME = 90  # 1.5 minutes in seconds
SIDEBAR_WIDTH = 300
TOTAL_WIDTH = WIDTH + SIDEBAR_WIDTH

# --- TEAM DATA ---
TEAMS = {
    "Real Madrid": {
        "logo": "real_madrid.jpg",
        "color": (255, 255, 255),
        "roster": [
            {"name": "Camavinga", "speed": 950, "reaction": 180, "intel": 0.92, "strength": 0.85},
            {"name": "Bellingham", "speed": 900, "reaction": 180, "intel": 0.95, "strength": 0.85},
            {"name": "Rodrygo", "speed": 1020, "reaction": 240, "intel": 0.86, "strength": 0.6},
            {"name": "Vini", "speed": 1050, "reaction": 220, "intel": 0.85, "strength": 0.7},
            {"name": "Mbappe", "speed": 1100, "reaction": 200, "intel": 0.90, "strength": 0.75}
        ]
    },
    "Barcelona": {
        "logo": "barcelona.png",
        "color": (165, 0, 68),
        "roster": [
            {"name": "Gavi", "speed": 900, "reaction": 160, "intel": 0.88, "strength": 0.9},
            {"name": "Yamal", "speed": 1000, "reaction": 200, "intel": 0.90, "strength": 0.6},
            {"name": "Pedri", "speed": 880, "reaction": 150, "intel": 0.98, "strength": 0.55},
            {"name": "Raphinha", "speed": 980, "reaction": 250, "intel": 0.85, "strength": 0.65},
            {"name": "Lewandowski", "speed": 820, "reaction": 220, "intel": 0.94, "strength": 0.85}
        ]
    },
    "Bayern": {
        "logo": "bayern.png",
        "color": (220, 5, 45),
        "roster": [
            {"name": "Goretzka", "speed": 880, "reaction": 180, "intel": 0.92, "strength": 0.95},
            {"name": "Musiala", "speed": 980, "reaction": 180, "intel": 0.96, "strength": 0.6},
            {"name": "Diaz", "speed": 1020, "reaction": 220, "intel": 0.80, "strength": 0.75},
            {"name": "Olise", "speed": 960, "reaction": 250, "intel": 0.85, "strength": 0.7},
            {"name": "Kane", "speed": 850, "reaction": 200, "intel": 0.95, "strength": 0.9}
        ]
    },
    "PSG": {
        "logo": "psg.png",
        "color": (0, 65, 122),
        "roster": [
            {"name": "Marquinhos", "speed": 920, "reaction": 150, "intel": 0.96, "strength": 0.9},
            {"name": "Barcola", "speed": 1040, "reaction": 240, "intel": 0.84, "strength": 0.6},
            {"name": "Vitinha", "speed": 920, "reaction": 180, "intel": 0.92, "strength": 0.8},
            {"name": "Dembele", "speed": 1080, "reaction": 280, "intel": 0.80, "strength": 0.6},
            {"name": "Kvara", "speed": 1000, "reaction": 220, "intel": 0.88, "strength": 0.7}
        ]
    },
    "Arsenal": {
        "logo": "arsenal.png",
        "color": (239, 1, 7),
        "roster": [
            {"name": "Saliba", "speed": 920, "reaction": 180, "intel": 0.94, "strength": 0.95},
            {"name": "Rice", "speed": 880, "reaction": 170, "intel": 0.96, "strength": 0.9},
            {"name": "Odegaard", "speed": 870, "reaction": 150, "intel": 0.98, "strength": 0.65},
            {"name": "Saka", "speed": 980, "reaction": 220, "intel": 0.90, "strength": 0.75},
            {"name": "Gyokeres", "speed": 940, "reaction": 200, "intel": 0.88, "strength": 0.9}
        ]
    },
    "Liverpool": {
        "logo": "liverpool.jpg",
        "color": (200, 16, 46),
        "roster": [
            {"name": "Van Dijk", "speed": 940, "reaction": 190, "intel": 0.98, "strength": 1.0},
            {"name": "Mac Allister", "speed": 860, "reaction": 160, "intel": 0.97, "strength": 0.7},
            {"name": "Szoboszlai", "speed": 950, "reaction": 200, "intel": 0.88, "strength": 0.85},
            {"name": "Wirtz", "speed": 930, "reaction": 170, "intel": 0.96, "strength": 0.65},
            {"name": "Salah", "speed": 1040, "reaction": 210, "intel": 0.90, "strength": 0.75}
        ]
    },
    "Manchester City": {
        "logo": "mancity.png",
        "color": (108, 173, 223),
        "roster": [
            {"name": "Rodri", "speed": 850, "reaction": 150, "intel": 0.98, "strength": 0.95},
            {"name": "Doku", "speed": 1120, "reaction": 280, "intel": 0.75, "strength": 0.7},
            {"name": "Foden", "speed": 970, "reaction": 180, "intel": 0.95, "strength": 0.65},
            {"name": "Cherki", "speed": 920, "reaction": 230, "intel": 0.88, "strength": 0.65},
            {"name": "Haaland", "speed": 1050, "reaction": 250, "intel": 0.85, "strength": 1.0}
        ]
    },
    "Manchester United": {
        "logo": "manutd.jpg",
        "color": (218, 41, 28),
        "roster": [
            {"name": "Maguire", "speed": 780, "reaction": 250, "intel": 0.85, "strength": 1.0},
            {"name": "Bruno", "speed": 880, "reaction": 180, "intel": 0.95, "strength": 0.7},
            {"name": "Sesko", "speed": 980, "reaction": 220, "intel": 0.85, "strength": 0.9},
            {"name": "Mbeumo", "speed": 1010, "reaction": 230, "intel": 0.82, "strength": 0.8},
            {"name": "Cunha", "speed": 960, "reaction": 220, "intel": 0.88, "strength": 0.8}
        ]
    }
}

def short_name(name):
    map = {
        "Real Madrid": "R. Madrid",
        "Barcelona": "Barca",
        "Manchester City": "Man City",
        "Manchester United": "Man Utd",
        "Liverpool": "L'pool"
    }
    return map.get(name, name)

class Tournament:
    def __init__(self, team_names):
        # Initial 8 teams
        teams = list(team_names)
        random.shuffle(teams)
        self.qf = [ (teams[0], teams[1]), (teams[2], teams[3]), (teams[4], teams[5]), (teams[6], teams[7]) ]
        self.sf = [ [None, None], [None, None] ]
        self.final = [None, None]
        self.winner = None
        
        self.qf_results = [None, None, None, None] # Format: (winner, score_str)
        self.sf_results = [None, None]
        self.final_result = None
        
        self.current_round = "QF"  # "QF", "SF", "FINAL", "COMPLETE"
        self.current_match_idx = 0
        
    def get_current_match(self):
        if self.current_round == "QF":
            return self.qf[self.current_match_idx]
        elif self.current_round == "SF":
            return self.sf[self.current_match_idx]
        elif self.current_round == "FINAL":
            return self.final
        return None

    def advance(self, match_winner, score_blue, score_white):
        score_str = f"{score_blue}-{score_white}"
        if self.current_round == "QF":
            self.qf_results[self.current_match_idx] = (match_winner, score_str)
            self.sf[self.current_match_idx // 2][self.current_match_idx % 2] = match_winner
            self.current_match_idx += 1
            if self.current_match_idx > 3:
                self.current_round = "SF"
                self.current_match_idx = 0
        elif self.current_round == "SF":
            self.sf_results[self.current_match_idx] = (match_winner, score_str)
            self.final[self.current_match_idx] = match_winner
            self.current_match_idx += 1
            if self.current_match_idx > 1:
                self.current_round = "FINAL"
                self.current_match_idx = 0
        elif self.current_round == "FINAL":
            self.final_result = (match_winner, score_str)
            self.winner = match_winner
            self.current_round = "COMPLETE"

    def draw_bracket(self, screen, font, large_font, ui_font, game):
        # Sidebar Background
        pygame.draw.rect(screen, (30, 30, 30), (800, 0, 300, HEIGHT))
        
        # 1. Live Scoreboard Header
        sb_x = 800
        header_h = 140
        pygame.draw.rect(screen, (45, 45, 45), (sb_x, 0, 300, header_h))
        pygame.draw.line(screen, (100, 100, 100), (sb_x, header_h), (sb_x + 300, header_h), 2)
        
        title_txt = ui_font.render("5v5 ELITE TOURNAMENT", True, (255, 215, 0))
        screen.blit(title_txt, (sb_x + 150 - title_txt.get_width()//2, 10))
        
        # Matchup & Score
        t1_c = TEAMS[game.team1_name]["color"]
        t2_c = TEAMS[game.team2_name]["color"]
        m_txt = font.render(f"{short_name(game.team1_name)} vs {short_name(game.team2_name)}", True, (255,255,255))
        screen.blit(m_txt, (sb_x + 150 - m_txt.get_width()//2, 40))
        
        score_txt = large_font.render(f"{game.score_blue} - {game.score_white}", True, (255,255,255))
        screen.blit(score_txt, (sb_x + 150 - score_txt.get_width()//2, 65))
        
        # Timer (90-minute game clock)
        game_mins = (MATCH_TIME * FPS - game.match_timer) // FPS
        timer_txt = font.render(f"TIME: {game_mins}'", True, (255, 255, 0))
        screen.blit(timer_txt, (sb_x + 150 - timer_txt.get_width()//2, 110))

        # 2. Tournament Bracket (Offset downwards)
        y_off = 160
        
        def draw_match(x, y, teams, result, active):
            winner = result[0] if result else None
            score = result[1] if result else ""
            
            w, h = 90, 60
            color = (50, 50, 50) if not active else (80, 80, 30)
            pygame.draw.rect(screen, color, (x, y, w, h), border_radius=5)
            pygame.draw.rect(screen, (150, 150, 150), (x, y, w, h), 1, border_radius=5)
            
            t1_name = str(teams[0]) if teams[0] else "???"
            t2_name = str(teams[1]) if teams[1] else "???"
            
            c1 = (255, 255, 255) if winner != t1_name else (0, 255, 0)
            c2 = (255, 255, 255) if winner != t2_name else (0, 255, 0)
            
            screen.blit(ui_font.render(short_name(t1_name), True, c1), (x + 5, y + 5))
            screen.blit(ui_font.render(short_name(t2_name), True, c2), (x + 5, y + 25))
            if score:
                s_txt = ui_font.render(score, True, (255, 255, 0))
                screen.blit(s_txt, (x + 5, y + 43))

        # Quarter Finals
        for i, match in enumerate(self.qf):
            draw_match(sb_x + 10, y_off + i * 110, match, self.qf_results[i], i == self.current_match_idx and self.current_round == "QF")
            
        # Semi Finals
        for i, match in enumerate(self.sf):
            draw_match(sb_x + 110, y_off + 55 + i * 220, match, self.sf_results[i], i == self.current_match_idx and self.current_round == "SF")
            
        # Final
        draw_match(sb_x + 210, y_off + 165, self.final, self.final_result, self.current_round == "FINAL")
        
        if self.winner:
            w_text = font.render(f"WINNER: {self.winner}", True, (255, 255, 0))
            screen.blit(w_text, (sb_x + SIDEBAR_WIDTH // 2 - w_text.get_width() // 2, HEIGHT - 50))

class Ball:
    def __init__(self, space, x, y):
        self.radius = 8  # Reduced for 5v5
        mass = 1.2
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        self.shape.collision_type = BALL_COLLISION_TYPE
        
        # Load and scale football image with circular mask
        try:
            raw_img = pygame.image.load(get_asset_path("football.png")).convert_alpha()
            size = self.radius * 2
            raw_img = pygame.transform.smoothscale(raw_img, (size, size))
            
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
            self.image.blit(raw_img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        except:
            self.image = None
            
        space.add(self.body, self.shape)
        
    def draw(self, surface):
        pos = (int(self.body.position.x), int(self.body.position.y))
        if self.image:
            rect = self.image.get_rect(center=pos)
            surface.blit(self.image, rect)
        else:
            pygame.draw.circle(surface, (255, 255, 255), pos, self.radius)
            pygame.draw.circle(surface, (0, 0, 0), pos, self.radius, 2)

class Player:
    def __init__(self, space, x, y, team_color, team, name="Player", speed=900, reaction=300, intel=0.7, strength=0.5, logo_file=None):
        self.space = space
        self.team_color = team_color
        self.name = name
        self.speed = speed
        self.reaction = reaction / 1000.0  # seconds
        self.intel = intel
        self.strength = strength
        self.team = team
        self.radius = 15  # Reduced for 5v5
        self.last_action = 0
        self.has_ball = False
        self.control_start_tick = 0
        self.stun_timer = 0
        self.is_chasing = False
        self.is_passing_option = False
        
        # Load and scale team logo with circular mask
        try:
            full_path = get_asset_path(logo_file)
            raw_img = pygame.image.load(full_path).convert_alpha()
            size = self.radius * 2
            raw_img = pygame.transform.smoothscale(raw_img, (size, size))
            
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
            self.image.blit(raw_img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        except:
            self.image = None
            
        # Pymunk Physics Body Setup
        mass = 1.0
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        self.shape.collision_type = PLAYER_COLLISION_TYPE
        
        self.space.add(self.body, self.shape)

    def draw(self, surface, font):
        pos = (int(self.body.position.x), int(self.body.position.y))
        
        # High-Contrast Border for better visibility
        border_color = (255, 255, 255) if self.team == 0 else (0, 0, 0)
        pygame.draw.circle(surface, border_color, pos, self.radius + 2, 2)
        
        if self.image:
            rect = self.image.get_rect(center=pos)
            surface.blit(self.image, rect)
            if self.stun_timer > 0:
                s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (100, 100, 100, 150), (self.radius, self.radius), self.radius)
                surface.blit(s, rect)
        else:
            current_coin = (150, 150, 150) if self.stun_timer > 0 else (230, 200, 150)
            pygame.draw.circle(surface, current_coin, pos, self.radius)
            
        pygame.draw.circle(surface, (200, 170, 120), pos, self.radius, 1)
        
        name_text = font.render(self.name, True, (255, 255, 255))
        bg_rect = name_text.get_rect(center=(pos[0], pos[1] - 45))
        pygame.draw.rect(surface, (0, 0, 0), bg_rect.inflate(4, 4))
        surface.blit(name_text, bg_rect)

    def update_ai(self, ball, teammates, opponents, tick, game):
        def is_path_clear(target_pos, threshold=40):
            start_p = self.body.position
            segment = target_pos - start_p
            seg_len = segment.length
            if seg_len == 0: return True
            seg_dir = segment.normalized()
            for opp in opponents:
                if opp.stun_timer > 0: continue 
                v = opp.body.position - start_p
                proj = v.dot(seg_dir)
                if 0 < proj < seg_len:
                    if abs(v.cross(seg_dir)) < threshold: return False
            return True
        ball_pos = ball.body.position
        dist_to_ball = self.body.position.get_distance(ball_pos)
        
        was_has_ball = getattr(self, "has_ball", False)
        
        if tick - self.last_action < 15:
            self.has_ball = False
        else:
            self.has_ball = dist_to_ball < self.radius + ball.radius + 12
        
        if self.has_ball:
            self.is_chasing = False
            if not was_has_ball:
                self.control_start_tick = tick
            
            front_dir = pymunk.Vec2d(1 if self.team == 0 else -1, 0)
            target_pos = self.body.position + front_dir * (self.radius + ball.radius + 2)
            error = target_pos - ball_pos
            ball.body.velocity = error * 10
        
        if not self.has_ball:
            # 1-2-2 Split Logic: 1 Chaser, 2 Passing Options, 2 Defenders
            my_curr_dist = self.body.position.get_distance(ball_pos)
            if getattr(self, "is_chasing", False): my_curr_dist -= 40
            
            teammates_with_eff_dist = []
            for p in teammates:
                d = p.body.position.get_distance(ball_pos)
                if getattr(p, "is_chasing", False): d -= 40
                teammates_with_eff_dist.append((p, d))
            
            sorted_teammates = sorted(teammates_with_eff_dist, key=lambda x: x[1])
            my_rank = next((i for i, (p, d) in enumerate(sorted_teammates) if p == self), 99)
            
            self.is_chasing = (my_rank == 0)
            self.is_passing_option = (my_rank == 1 or my_rank == 2)
            
            if self.is_chasing:
                self.body.activate() 
                direction = ball_pos - self.body.position
                if direction.length > 0:
                    self.body.velocity = direction.normalized() * (self.speed * 0.18)
            elif self.is_passing_option:
                # Two passing options on either side (Up/Down)
                offset_y = -120 if my_rank == 1 else 120
                # Lateral positioning: stay mostly level with the ball, only slightly ahead
                target_x = ball_pos.x + (30 if self.team == 0 else -30)
                target_x = max(50, min(WIDTH-50, target_x))
                target_y = ball_pos.y + offset_y
                target_y = max(50, min(HEIGHT-50, target_y))
                support_pos = pymunk.Vec2d(target_x, target_y)
                
                # Avoid other teammates
                for p in teammates:
                    if p != self and p.body.position.get_distance(support_pos) < 60:
                        support_pos += (support_pos - p.body.position).normalized() * 60

                dir_to_support = support_pos - self.body.position
                if dir_to_support.length > 20:
                    self.body.activate()
                    self.body.velocity = dir_to_support.normalized() * (self.speed * 0.15)
            else:
                own_goal_x = 0 if self.team == 0 else WIDTH
                own_goal_pos = pymunk.Vec2d(own_goal_x, HEIGHT//2)
                
                # The 2 non-chasers/options form the backline
                defenders = sorted([p for p in teammates if not p.is_chasing and not getattr(p, "is_passing_option", False)], 
                                  key=lambda p: p.body.position.get_distance(own_goal_pos))
                try:
                    my_def_rank = defenders.index(self)
                except ValueError:
                    my_def_rank = 0

                line_to_goal = own_goal_pos - ball_pos
                target_pos = ball_pos + line_to_goal * 0.7
                offset_y = (my_def_rank - 0.5) * 120 
                support_pos = pymunk.Vec2d(max(50, min(WIDTH-50, target_pos.x)), 
                                          max(50, min(HEIGHT-50, target_pos.y + offset_y)))
                
                dir_to_support = support_pos - self.body.position
                if dir_to_support.length > 20:
                    self.body.activate()
                    self.body.velocity = dir_to_support.normalized() * (self.speed * 0.12)

        if self.has_ball:
            # 1. Goal Scanning: Check 3 points on the goal
            goal_center = pymunk.Vec2d(WIDTH if self.team == 0 else 0, HEIGHT//2)
            goal_top = pymunk.Vec2d(goal_center.x, HEIGHT//2 - 90)
            goal_bottom = pymunk.Vec2d(goal_center.x, HEIGHT//2 + 90)
            
            shot_lanes = [
                is_path_clear(goal_center, threshold=20),
                is_path_clear(goal_top, threshold=20),
                is_path_clear(goal_bottom, threshold=20)
            ]
            shot_clear = any(shot_lanes)
            best_goal_point = goal_center
            if shot_lanes[1]: best_goal_point = goal_top
            elif shot_lanes[2]: best_goal_point = goal_bottom
            
            # 2. Snap Shot Logic: Bypass reaction if any lane is clear and in range
            dist_to_goal = self.body.position.get_distance(goal_center)
            has_reacted = (tick - self.last_action > self.reaction * FPS) and (tick - self.control_start_tick > self.reaction * FPS)
            snap_shot_opportunity = dist_to_goal < 450 and shot_clear
            
            if has_reacted or snap_shot_opportunity:
                valid_pass_targets = [tm for tm in teammates if tm != self and is_path_clear(tm.body.position, threshold=40)]
                under_pressure = any(opp.body.position.get_distance(self.body.position) < 120 and opp.stun_timer == 0 for opp in opponents)
                
                forward_vec = pymunk.Vec2d(250 if self.team == 0 else -250, 0)
                p_straight, p_up, p_down = self.body.position + forward_vec, self.body.position + forward_vec.rotated(0.6), self.body.position + forward_vec.rotated(-0.6)
                c_s = is_path_clear(p_straight)
                c_u = is_path_clear(p_up) if p_up.y > 30 and p_up.y < HEIGHT - 30 else False
                c_d = is_path_clear(p_down) if p_down.y > 30 and p_down.y < HEIGHT - 30 else False
                
                space_ahead = c_s or c_u or c_d
                best_dribble_dir = pymunk.Vec2d(1 if self.team == 0 else -1, 0)
                if c_s: best_dribble_dir = best_dribble_dir.rotated(random.uniform(-0.1, 0.1))
                elif c_u: best_dribble_dir = best_dribble_dir.rotated(0.6)
                elif c_d: best_dribble_dir = best_dribble_dir.rotated(-0.6)

                opp_goal_x = WIDTH if self.team == 0 else 0
                in_corner = abs(self.body.position.x - opp_goal_x) < 250 and abs(self.body.position.y - HEIGHT//2) > 180
                
                # Refined Decision Logic: Prioritize CROSS in tight corners
                if in_corner and (not shot_clear or not space_ahead or under_pressure):
                    center_targets = [t for t in valid_pass_targets if abs(t.body.position.y - HEIGHT//2) < 180]
                    if center_targets:
                        decision = "CROSS"
                        self.cross_target_pos = min(center_targets, key=lambda t: t.body.position.get_distance(self.body.position)).body.position
                    else:
                        decision = "CROSS"
                        self.cross_target_pos = pymunk.Vec2d(opp_goal_x, HEIGHT//2 + random.uniform(-100, 100))
                elif snap_shot_opportunity: decision = "SHOOT"
                elif dist_to_goal < 450 and (shot_clear or random.random() < 0.3): decision = "SHOOT"
                elif under_pressure and valid_pass_targets: decision = "PASS"
                elif not space_ahead and valid_pass_targets: decision = "PASS"
                elif space_ahead: decision = "DRIBBLE"
                elif valid_pass_targets: decision = "PASS"
                else: decision = "SHOOT"
                    
                # Killer Instinct for Elite players (Higher Intel reduces random diversion)
                if random.random() > (self.intel + 0.1): 
                    opts = ["SHOOT", "PASS", "DRIBBLE"]
                    if decision in opts: opts.remove(decision)
                    decision = random.choice(opts)

                if decision == "SHOOT":
                    ball.body.apply_impulse_at_local_point((best_goal_point - self.body.position).normalized() * 250)
                    if game.kick_sound: game.kick_sound.play()
                elif decision == "CROSS":
                    ball.body.apply_impulse_at_local_point((self.cross_target_pos - self.body.position).normalized() * 200)
                    if game.kick_sound: game.kick_sound.play()
                elif decision == "PASS":
                    tgt = min(valid_pass_targets if valid_pass_targets else [tm for tm in teammates if tm != self], key=lambda p: p.body.position.get_distance(self.body.position))
                    ball.body.apply_impulse_at_local_point((tgt.body.position - self.body.position).normalized() * 120)
                    if game.kick_sound: game.kick_sound.play()
                elif decision == "DRIBBLE":
                    ball.body.apply_impulse_at_local_point(best_dribble_dir * 70)
                    if tick % 20 == 0 and game.kick_sound: game.kick_sound.play() # Periodic taps for dribble
                self.last_action = tick

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("3v3 Elite Tournament")
        self.clock = pygame.time.Clock()
        self.name_font = pygame.font.SysFont('Arial', 12, bold=True)
        self.large_font = pygame.font.SysFont('Arial', 48)
        self.font = pygame.font.SysFont('Arial', 24)
        self.ui_font = pygame.font.SysFont('Arial', 16)
        
        # Load Audio Infrastructure (Safe-loading)
        try:
            self.kick_sound = pygame.mixer.Sound(get_asset_path("kick.wav"))
            self.kick_sound.set_volume(0.4)
            self.goal_sound = pygame.mixer.Sound(get_asset_path("goal.wav"))
            self.goal_sound.set_volume(0.6)
            self.crowd_sound = pygame.mixer.Sound(get_asset_path("crowd.wav"))
            self.crowd_sound.set_volume(0.2)
            self.crowd_sound.play(-1) # Loop indefinitely
        except:
            self.kick_sound = None
            self.goal_sound = None
            self.crowd_sound = None
        
        self.state = "START"
        self.score_blue = 0
        self.score_white = 0
        self.tick = 0
        self.match_timer = MATCH_TIME * FPS
        self.countdown_timer = 0
        self.auto_start_timer = 0
        
        self.tournament = Tournament(list(TEAMS.keys()))
        self.setup_physics()
        self.setup_next_match()

    def setup_next_match(self):
        match = self.tournament.get_current_match()
        if match:
            self.team1_name = match[0]
            self.team2_name = match[1]
            self.score_blue = 0
            self.score_white = 0
            self.match_timer = MATCH_TIME * FPS
            if hasattr(self, 'space'):
                self.reset_pitch()
        else:
            self.state = "TOURNAMENT_OVER"

    def setup_physics(self):
        self.space = pymunk.Space()
        self.space.damping = 0.8  
        handler = self.space.add_collision_handler(PLAYER_COLLISION_TYPE, PLAYER_COLLISION_TYPE)
        
        def begin_player_collision(arbiter, space, data):
            p1_shape, p2_shape = arbiter.shapes
            player1 = next((p for p in self.players if getattr(p, "shape", None) == p1_shape), None)
            player2 = next((p for p in self.players if getattr(p, "shape", None) == p2_shape), None)
            if player1 and player2 and player1.team != player2.team:
                p1_near = player1.has_ball or player1.body.position.get_distance(self.ball.body.position) < 100
                p2_near = player2.has_ball or player2.body.position.get_distance(self.ball.body.position) < 100
                if p1_near or p2_near and player1.stun_timer <= 0 and player2.stun_timer <= 0:
                    p1_s = player1.strength / (player1.strength + player2.strength)
                    if player1.has_ball:
                        p2_wins = random.random() < 0.7 * (1 - p1_s)
                    elif player2.has_ball:
                        p2_wins = random.random() > 0.7 * p1_s
                    else:
                        p2_wins = random.random() > p1_s
                    winner, loser = (player2, player1) if p2_wins else (player1, player2)
                    loser.stun_timer, loser.has_ball = int(FPS * 1.0), False
            return True
        handler.begin = begin_player_collision
        
        static = self.space.static_body
        walls = [
            pymunk.Segment(static, (0, -10), (WIDTH, -10), 20),
            pymunk.Segment(static, (0, HEIGHT+10), (WIDTH, HEIGHT+10), 20),
            pymunk.Segment(static, (-11, 0), (-11, HEIGHT//2-100), 20),
            pymunk.Segment(static, (-11, HEIGHT//2+100), (-11, HEIGHT), 20),
            pymunk.Segment(static, (WIDTH+11, 0), (WIDTH+11, HEIGHT//2-100), 20),
            pymunk.Segment(static, (WIDTH+11, HEIGHT//2+100), (WIDTH+11, HEIGHT), 20),
            pymunk.Segment(static, (-40, HEIGHT//2-100), (-40, HEIGHT//2+100), 20),
            pymunk.Segment(static, (-11, HEIGHT//2-100), (-40, HEIGHT//2-100), 20),
            pymunk.Segment(static, (-11, HEIGHT//2+100), (-40, HEIGHT//2+100), 20),
            pymunk.Segment(static, (WIDTH+40, HEIGHT//2-100), (WIDTH+40, HEIGHT//2+100), 20),
            pymunk.Segment(static, (WIDTH+11, HEIGHT//2-100), (WIDTH+40, HEIGHT//2-100), 20),
            pymunk.Segment(static, (WIDTH+11, HEIGHT//2+100), (WIDTH+40, HEIGHT//2+100), 20)
        ]
        for w in walls: w.elasticity, w.friction = 0.8, 0.5
        self.space.add(*walls)

    def reset_pitch(self):
        for b in list(self.space.bodies):
            if b.body_type == pymunk.Body.DYNAMIC: self.space.remove(b, *b.shapes)
        self.ball = Ball(self.space, WIDTH//2, HEIGHT//2)
        self.players = []
        def e(): return random.uniform(-5, 5)
        t1, t2 = TEAMS[self.team1_name], TEAMS[self.team2_name]
        # Tactical 5v5 Layout (GK, 2 Def, 1 Mid, 1 Fwd)
        offsets = [
            (50, 300),   # GK
            (150, 150),  # Def L
            (150, 450),  # Def R
            (260, 300),  # Mid
            (360, 300)   # Fwd
        ]
        for i, p in enumerate(t1["roster"]):
            off_x, off_y = offsets[i]
            self.players.append(Player(self.space, off_x+e(), off_y+e(), t1["color"], 0, p["name"], p["speed"], p["reaction"], p["intel"], p["strength"], t1["logo"]))
        
        for i, p in enumerate(t2["roster"]):
            off_x, off_y = offsets[i]
            # Mirror for team 2
            self.players.append(Player(self.space, (WIDTH-off_x)+e(), off_y+e(), t2["color"], 1, p["name"], p["speed"], p["reaction"], p["intel"], p["strength"], t2["logo"]))

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.state in ("START", "GOAL", "MATCH_OVER"): self.state = "PLAYING"
                    elif self.state == "PLAYING": self.state = "PAUSED"
                    elif self.state == "PAUSED": self.state = "PLAYING"
            
            self.update()

            self.screen.fill(PITCH_COLOR)
            pygame.draw.rect(self.screen, (255, 255, 255), (0, HEIGHT//2-100, 15, 200), 2)
            pygame.draw.rect(self.screen, (255, 255, 255), (WIDTH-15, HEIGHT//2-100, 15, 200), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (WIDTH//2, HEIGHT//2), 60, 2)
            pygame.draw.line(self.screen, (255, 255, 255), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
            for p in self.players: p.draw(self.screen, self.name_font)
            self.ball.draw(self.screen)
            
            # Draw Tournament Bracket & Sidebar UI
            self.tournament.draw_bracket(self.screen, self.font, self.large_font, self.ui_font, self)

            if self.state == "PAUSED":
                title = self.large_font.render("PAUSED", True, (255,255,255))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 50))
                sub = self.font.render("Press SPACE to Resume", True, (200,200,200))
                self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
            elif self.state == "START":
                title = self.large_font.render(f"TOURNAMENT START", True, (255,255,255))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 50))
                sub = self.font.render("Press SPACE for First Match", True, (200,200,200))
                self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
            elif self.state == "GOAL":
                sub = self.font.render("GOAL!", True, (255, 255, 0))
                self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
            elif self.state == "MATCH_OVER":
                sub = self.font.render("MATCH OVER!", True, (200,255,200))
                self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
            elif self.state == "COUNTDOWN":
                val = (self.countdown_timer // FPS) + 1
                c_txt = self.large_font.render(str(val), True, (255, 255, 255))
                self.screen.blit(c_txt, (WIDTH//2 - c_txt.get_width()//2, HEIGHT//2 - 50))
            elif self.state == "TOURNAMENT_OVER":
                title = self.large_font.render("TOURNAMENT OVER", True, (255, 255, 0))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 50))
                winner_txt = self.font.render(f"WINNER: {self.tournament.winner}", True, (255, 255, 255))
                self.screen.blit(winner_txt, (WIDTH//2 - winner_txt.get_width()//2, HEIGHT//2 + 10))
            
            pygame.display.flip()

    def update(self):
        if self.state == "PLAYING":
            self.tick += 1
            self.space.step(1.0 / FPS)
            t0 = [p for p in self.players if p.team == 0]
            t1 = [p for p in self.players if p.team == 1]
            for p in self.players:
                if p.stun_timer > 0:
                    p.stun_timer -= 1
                    p.body.velocity *= 0.5
                else:
                    p.update_ai(self.ball, t0 if p.team == 0 else t1, t1 if p.team == 0 else t0, self.tick, self)
            
            bx, by = self.ball.body.position.x, self.ball.body.position.y
            if HEIGHT//2-100 < by < HEIGHT//2+100:
                delta_score = False
                if bx <= 0: 
                    self.score_white += 1
                    delta_score = True
                elif bx >= WIDTH: 
                    self.score_blue += 1
                    delta_score = True
                
                if delta_score:
                    if self.goal_sound: self.goal_sound.play()
                    if self.match_timer <= 0: # Golden Goal
                        self.tournament.advance(self.team1_name if bx >= WIDTH else self.team2_name, self.score_blue, self.score_white)
                        self.setup_next_match()
                        self.state = "MATCH_OVER"
                    else:
                        self.state = "GOAL"
                    self.auto_start_timer = FPS * 2 # 2s delay before countdown
                    self.reset_pitch()

            # Timer logic
            if self.match_timer > 0:
                self.match_timer -= 1
                if self.match_timer <= 0:
                    if self.score_blue != self.score_white:
                        winner = self.team1_name if self.score_blue > self.score_white else self.team2_name
                        self.tournament.advance(winner, self.score_blue, self.score_white)
                        self.setup_next_match()
                        self.state = "MATCH_OVER"
                    # Else: Golden Goal mode (timer stays at 0, game continues)
                    if self.state == "MATCH_OVER":
                         self.auto_start_timer = FPS * 2

        elif self.state in ("GOAL", "MATCH_OVER"):
            if self.state == "MATCH_OVER" and self.tournament.winner:
                pass # Tournament Over, stay here
            else:
                self.auto_start_timer -= 1
                if self.auto_start_timer <= 0:
                    self.state = "COUNTDOWN"
                    self.countdown_timer = FPS * 3

        elif self.state == "COUNTDOWN":
            self.countdown_timer -= 1
            if self.countdown_timer <= 0:
                self.state = "PLAYING"


if __name__ == "__main__":
    Game().run()
