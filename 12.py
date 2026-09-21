import turtle
import random

try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

GAME_VERSION = "1.17.0.0"
GAME_AUTHOR = "Siavash Aalami Far"
GAME_AUTHOR_FA = "سیاوش اعلمی فر"

screen = turtle.Screen()
screen.title(f"🏎️ Racing Game v{GAME_VERSION} 🏁")
screen.bgcolor("gray")
screen.setup(width=600, height=700)
screen.tracer(0)

# جاده
road = turtle.Turtle()
road.shape("square")
road.color("darkgray")
road.shapesize(stretch_wid=70, stretch_len=20)
road.penup()
road.goto(0, 0)

road_lines = []
for i in range(8):
    line = turtle.Turtle()
    line.shape("square")
    line.color("white")
    line.shapesize(stretch_wid=2, stretch_len=0.2)
    line.penup()
    line.goto(0, 300 - i * 100)
    road_lines.append(line)

# ماشین‌ها
player = turtle.Turtle()
player.shape("square")
player.color("red")
player.shapesize(stretch_wid=3, stretch_len=1.5)
player.penup()
player.goto(0, -280)
player.hideturtle()

car_light = turtle.Turtle()
car_light.shape("circle")
car_light.color("yellow")
car_light.shapesize(4)
car_light.penup()
car_light.hideturtle()

headlight = turtle.Turtle()
headlight.shape("circle")
headlight.color("white")
headlight.shapesize(2)
headlight.penup()
headlight.hideturtle()

player1_bottom = turtle.Turtle()
player1_bottom.shape("square")
player1_bottom.color("orange")
player1_bottom.shapesize(stretch_wid=1.5, stretch_len=1.5)
player1_bottom.penup()
player1_bottom.hideturtle()

player1_top = turtle.Turtle()
player1_top.shape("square")
player1_top.color("yellow")
player1_top.shapesize(stretch_wid=1.5, stretch_len=1.5)
player1_top.penup()
player1_top.hideturtle()

player2 = turtle.Turtle()
player2.shape("square")
player2.color("red")
player2.shapesize(stretch_wid=3, stretch_len=1.5)
player2.penup()
player2.hideturtle()

player2_nose = turtle.Turtle()
player2_nose.shape("triangle")
player2_nose.color("yellow")
player2_nose.shapesize(stretch_wid=1, stretch_len=1)
player2_nose.penup()
player2_nose.setheading(90)
player2_nose.hideturtle()

# لیست‌ها
enemies = []
powerups = []
grow_powerups = []
oil_spills = []
stars_items = []
bullet_powerups = []
bullets = []
trucks = []
particles = []
speed_bumps = []

# متغیرها
score = 0
speed = 5
game_state = "start"
frame_count = 0
spawn_rate = 60
road_width = 20
last_width_change = 0
boost_active = False
boost_speed = 15
lives = 2
max_lives = 4
invincible = False
invincible_timer = 0
powerup_spawn_rate = 180
grow_powerup_spawn_rate = 240
oil_spawn_rate = 300
star_spawn_rate = 200
bullet_powerup_spawn_rate = 250
truck_spawn_rate = 600
speed_bump_spawn_rate = 400
player_size = 1.0
max_player_size = 2.5
slippery = False
slippery_timer = 0
bullets_count = 0
max_bullets = 3
truck_active = False
truck_timer = 0
truck_hp = 4
truck_spawn_time = 0
total_stars = 0
current_car = 0
owned_cars = [0]
shop_open = False
headlight_on = False

environments = ["day", "night", "rain", "desert", "snow"]
env_names = {
    "day": "🌅 DAY",
    "night": "🌙 NIGHT",
    "rain": "🌧️ RAIN",
    "desert": "🏜️ DESERT",
    "snow": "❄️ SNOW"
}
env_settings = {
    "day": {"bg": "gray", "road": "darkgray", "line": "white"},
    "night": {"bg": "black", "road": "#333333", "line": "#666666"},
    "rain": {"bg": "#445566", "road": "#555555", "line": "#888888"},
    "desert": {"bg": "#D2B48C", "road": "#8B7355", "line": "#F5DEB3"},
    "snow": {"bg": "#E8E8E8", "road": "#BBBBBB", "line": "#FFFFFF"}
}
current_env = "day"
last_env_change = 0

cars_info = {
    0: {"name": "Default Red", "price": 0, "owned": True},
    1: {"name": "Orange-Yellow", "price": 30, "owned": False},
    2: {"name": "Red + Nose", "price": 50, "owned": False}
}

enemy_colors = ["blue", "green", "yellow", "purple", "orange", "pink", "cyan"]

# ✅ متغیرهای پیام برای نگهداری وضعیت
message_text = ""
message_pos = (0, 0)
message_color = "yellow"
message_font = ("Courier", 24, "bold")
show_message = False

# توابع صدا
def play_engine_sound():
    if SOUND_AVAILABLE:
        try: winsound.Beep(200, 100)
        except: pass

def play_star_sound():
    if SOUND_AVAILABLE:
        try: winsound.Beep(800, 150)
        except: pass

def play_shoot_sound():
    if SOUND_AVAILABLE:
        try: winsound.Beep(400, 50)
        except: pass

def play_truck_sound():
    if SOUND_AVAILABLE:
        try: winsound.Beep(150, 300)
        except: pass

def play_env_sound():
    if SOUND_AVAILABLE:
        try: winsound.Beep(600, 200)
        except: pass

def play_horn_sound():
    if SOUND_AVAILABLE:
        try:
            winsound.Beep(350, 300)
            winsound.Beep(300, 300)
        except: pass

def play_bump_sound():
    if SOUND_AVAILABLE:
        try: winsound.Beep(100, 400)
        except: pass

def toggle_headlight():
    global headlight_on
    if game_state == "playing":
        headlight_on = not headlight_on
        if headlight_on:
            headlight.showturtle()
        else:
            headlight.hideturtle()

def honk_horn():
    global show_message, message_text, message_pos, message_color, message_font
    if game_state == "playing":
        play_horn_sound()
        show_message = True
        message_text = "📢 BEEP BEEP!"
        message_pos = (0, 0)
        message_color = "yellow"
        message_font = ("Courier", 30, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 2000)

def apply_environment(env_name):
    global current_env
    current_env = env_name
    settings = env_settings[env_name]
    
    screen.bgcolor(settings["bg"])
    road.color(settings["road"])
    for line in road_lines:
        line.color(settings["line"])
    
    if env_name == "night":
        car_light.showturtle()
    else:
        car_light.hideturtle()
    
    for p in particles:
        p["turtle"].hideturtle()
    particles.clear()
    
    if env_name == "rain":
        for _ in range(40):
            p = turtle.Turtle()
            p.shape("circle")
            p.color("lightblue")
            p.shapesize(0.3, 0.1)
            p.penup()
            p.speed(0)
            p.goto(random.randint(-300, 300), random.randint(-350, 350))
            particles.append({"turtle": p, "type": "rain", "speed": random.uniform(12, 18)})
    elif env_name == "snow":
        for _ in range(30):
            p = turtle.Turtle()
            p.shape("circle")
            p.color("white")
            p.shapesize(random.uniform(0.2, 0.5))
            p.penup()
            p.speed(0)
            p.goto(random.randint(-300, 300), random.randint(-350, 350))
            particles.append({"turtle": p, "type": "snow", "speed": random.uniform(2, 5), "drift": random.uniform(-1, 1)})
    elif env_name == "desert":
        for _ in range(25):
            p = turtle.Turtle()
            p.shape("circle")
            p.color("#C19A6B")
            p.shapesize(random.uniform(0.2, 0.4))
            p.penup()
            p.speed(0)
            p.goto(random.randint(-300, 300), random.randint(-350, 350))
            particles.append({"turtle": p, "type": "sand", "speed": random.uniform(5, 10), "drift": random.uniform(-2, 2)})

def change_environment():
    global last_env_change, show_message, message_text, message_pos, message_color, message_font
    available = [e for e in environments if e != current_env]
    new_env = random.choice(available)
    apply_environment(new_env)
    last_env_change = score
    
    show_message = True
    message_text = f"ENVIRONMENT: {env_names[new_env]}"
    message_pos = (0, 150)
    message_color = "cyan"
    message_font = ("Courier", 28, "bold")
    screen.ontimer(lambda: globals().update({'show_message': False}), 3000)
    play_env_sound()

def update_particles():
    for p in particles[:]:
        t = p["turtle"]
        ptype = p["type"]
        
        if ptype == "rain":
            t.sety(t.ycor() - p["speed"])
            if t.ycor() < -350:
                t.goto(random.randint(-300, 300), 350)
        elif ptype == "snow":
            t.sety(t.ycor() - p["speed"])
            t.setx(t.xcor() + p["drift"])
            if t.ycor() < -350:
                t.goto(random.randint(-300, 300), 350)
            if abs(t.xcor()) > 300:
                t.setx(-t.xcor())
        elif ptype == "sand":
            t.setx(t.xcor() + p["drift"])
            t.sety(t.ycor() - p["speed"] * 0.3)
            if t.ycor() < -350 or abs(t.xcor()) > 300:
                t.goto(random.choice([-300, 300]), random.randint(-350, 350))

def get_env_effects():
    effects = {"slippery": False, "visibility": 1.0, "speed_mod": 1.0}
    if current_env == "rain":
        effects["slippery"] = True
        effects["visibility"] = 0.7
    elif current_env == "snow":
        effects["slippery"] = True
        effects["speed_mod"] = 0.85
    elif current_env == "desert":
        effects["visibility"] = 0.8
    elif current_env == "night":
        effects["visibility"] = 0.6
    return effects

def change_road_width():
    global road_width, last_width_change
    new_width = random.randint(12, 25)
    road_width = new_width
    road.shapesize(stretch_wid=70, stretch_len=road_width)
    last_width_change = score

def get_lanes():
    lane_width = road_width * 10
    num_lanes = 3
    lanes = []
    for i in range(num_lanes):
        lane_pos = -lane_width + (i * lane_width)
        lanes.append(lane_pos)
    return lanes

def move_left():
    if game_state == "playing":
        x = get_player_x()
        max_x = road_width * 10 - 20
        move_amount = 15
        env_effects = get_env_effects()
        if env_effects["slippery"] or slippery:
            move_amount = random.choice([-20, -10, 10, 20])
        if x > -max_x:
            set_player_x(x - move_amount)

def move_right():
    if game_state == "playing":
        x = get_player_x()
        max_x = road_width * 10 - 20
        move_amount = 15
        env_effects = get_env_effects()
        if env_effects["slippery"] or slippery:
            move_amount = random.choice([-20, -10, 10, 20])
        if x < max_x:
            set_player_x(x + move_amount)

def get_player_x():
    if current_car == 0:
        return player.xcor()
    elif current_car == 1:
        return player1_bottom.xcor()
    elif current_car == 2:
        return player2.xcor()
    return 0

def set_player_x(x):
    if current_car == 0:
        player.setx(x)
    elif current_car == 1:
        player1_bottom.setx(x)
        player1_top.setx(x)
    elif current_car == 2:
        player2.setx(x)
        player2_nose.setx(x)

def get_player_y():
    if current_car == 0:
        return player.ycor()
    elif current_car == 1:
        return player1_bottom.ycor()
    elif current_car == 2:
        return player2.ycor()
    return -280

def hide_all_players():
    player.hideturtle()
    player1_bottom.hideturtle()
    player1_top.hideturtle()
    player2.hideturtle()
    player2_nose.hideturtle()
    car_light.hideturtle()
    headlight.hideturtle()

def show_current_player():
    hide_all_players()
    if current_car == 0:
        player.showturtle()
    elif current_car == 1:
        player1_bottom.showturtle()
        player1_top.showturtle()
    elif current_car == 2:
        player2.showturtle()
        player2_nose.showturtle()
    
    if current_env == "night":
        car_light.showturtle()
    if headlight_on:
        headlight.showturtle()

def update_car1_colors():
    if boost_active:
        player1_bottom.color("yellow")
        player1_top.color("orange")
    else:
        player1_bottom.color("orange")
        player1_top.color("yellow")

def update_car2_colors():
    if boost_active:
        player2.color("yellow")
        player2_nose.showturtle()
    else:
        player2.color("red")
        if current_env != "night":
            player2_nose.hideturtle()

def toggle_boost():
    global boost_active
    if game_state == "playing":
        boost_active = not boost_active
        if current_car == 0:
            player.color("yellow" if boost_active else "red")
        elif current_car == 1:
            update_car1_colors()
        elif current_car == 2:
            update_car2_colors()
        if boost_active:
            play_engine_sound()

def shoot_bullet():
    global bullets_count
    if game_state == "playing" and bullets_count > 0:
        bullets_count -= 1
        bullet = turtle.Turtle()
        bullet.shape("circle")
        bullet.color("brown")
        bullet.shapesize(0.5)
        bullet.penup()
        bullet.speed(0)
        bullet.goto(get_player_x(), get_player_y() + 30)
        bullets.append({"turtle": bullet, "speed": 10})
        play_shoot_sound()

def spawn_enemy():
    enemy = turtle.Turtle()
    enemy.shape("square")
    enemy.color(random.choice(enemy_colors))
    enemy.shapesize(stretch_wid=3, stretch_len=1.5)
    enemy.penup()
    enemy.speed(0)
    lanes = get_lanes()
    enemy.goto(random.choice(lanes), 350)
    enemies.append({"turtle": enemy, "speed": speed + random.uniform(-1, 1)})

def spawn_powerup():
    powerup = turtle.Turtle()
    powerup.shape("circle")
    powerup.color("red")
    powerup.shapesize(1.5)
    powerup.penup()
    powerup.speed(0)
    lanes = get_lanes()
    powerup.goto(random.choice(lanes), 350)
    powerups.append({"turtle": powerup, "speed": speed})

def spawn_grow_powerup():
    grow_p = turtle.Turtle()
    grow_p.shape("circle")
    grow_p.color("orange")
    grow_p.shapesize(1.5)
    grow_p.penup()
    grow_p.speed(0)
    lanes = get_lanes()
    grow_p.goto(random.choice(lanes), 350)
    grow_powerups.append({"turtle": grow_p, "speed": speed})

def spawn_oil_spill():
    oil = turtle.Turtle()
    oil.shape("circle")
    oil.color("black")
    oil.shapesize(2)
    oil.penup()
    oil.speed(0)
    lanes = get_lanes()
    oil.goto(random.choice(lanes), 350)
    oil_spills.append({"turtle": oil, "speed": speed})

def spawn_star():
    star = turtle.Turtle()
    star.shape("circle")
    star.color("gold")
    star.shapesize(1.2)
    star.penup()
    star.speed(0)
    lanes = get_lanes()
    star.goto(random.choice(lanes), 350)
    stars_items.append({"turtle": star, "speed": speed})

def spawn_bullet_powerup():
    bp = turtle.Turtle()
    bp.shape("circle")
    bp.color("brown")
    bp.shapesize(1.5)
    bp.penup()
    bp.speed(0)
    lanes = get_lanes()
    bp.goto(random.choice(lanes), 350)
    bullet_powerups.append({"turtle": bp, "speed": speed})

def spawn_truck():
    global truck_active, truck_timer, truck_hp, truck_spawn_time, show_message, message_text, message_pos, message_color, message_font
    if not truck_active:
        truck = turtle.Turtle()
        truck.shape("square")
        truck.color("darkgreen")
        truck.shapesize(stretch_wid=8, stretch_len=3)
        truck.penup()
        truck.speed(0)
        lanes = get_lanes()
        truck.goto(random.choice(lanes), 350)
        trucks.append(truck)
        truck_active = True
        truck_timer = 1800
        truck_hp = 4
        truck_spawn_time = frame_count
        play_truck_sound()
        
        show_message = True
        message_text = "🚛 TRUCK! SHOOT IT!"
        message_pos = (0, 0)
        message_color = "red"
        message_font = ("Courier", 30, "bold")

def spawn_speed_bump():
    bump = turtle.Turtle()
    bump.shape("square")
    bump.color("orange")
    bump.shapesize(stretch_wid=1, stretch_len=road_width)
    bump.penup()
    bump.speed(0)
    bump.goto(0, 350)
    speed_bumps.append({"turtle": bump, "speed": speed})

def start_game():
    global score, speed, game_state, frame_count, spawn_rate
    global road_width, last_width_change, boost_active
    global lives, invincible, invincible_timer
    global player_size, slippery, slippery_timer
    global bullets_count, truck_active, truck_timer, truck_hp
    global enemies, powerups, grow_powerups, oil_spills, stars_items
    global bullet_powerups, bullets, trucks, speed_bumps
    global current_env, last_env_change, headlight_on
    global show_message
    
    for e in enemies: e["turtle"].hideturtle()
    enemies.clear()
    for p in powerups: p["turtle"].hideturtle()
    powerups.clear()
    for g in grow_powerups: g["turtle"].hideturtle()
    grow_powerups.clear()
    for o in oil_spills: o["turtle"].hideturtle()
    oil_spills.clear()
    for s in stars_items: s["turtle"].hideturtle()
    stars_items.clear()
    for bp in bullet_powerups: bp["turtle"].hideturtle()
    bullet_powerups.clear()
    for b in bullets: b["turtle"].hideturtle()
    bullets.clear()
    for t in trucks: t.hideturtle()
    trucks.clear()
    for sb in speed_bumps: sb["turtle"].hideturtle()
    speed_bumps.clear()
    for p in particles: p["turtle"].hideturtle()
    particles.clear()
    
    score = 0
    speed = 5
    frame_count = 0
    spawn_rate = 60
    road_width = 20
    last_width_change = 0
    boost_active = False
    lives = 2
    invincible = False
    invincible_timer = 0
    player_size = 1.0
    slippery = False
    slippery_timer = 0
    bullets_count = 0
    truck_active = False
    truck_timer = 0
    truck_hp = 4
    current_env = "day"
    last_env_change = 0
    headlight_on = False
    show_message = False
    game_state = "playing"
    
    apply_environment("day")
    
    road.shapesize(stretch_wid=70, stretch_len=road_width)
    road.showturtle()
    
    player.shapesize(stretch_wid=3, stretch_len=1.5)
    player1_bottom.shapesize(stretch_wid=1.5, stretch_len=1.5)
    player1_top.shapesize(stretch_wid=1.5, stretch_len=1.5)
    player2.shapesize(stretch_wid=3, stretch_len=1.5)
    
    show_current_player()
    
    if current_car == 0:
        player.color("red")
        player.goto(0, -280)
    elif current_car == 1:
        update_car1_colors()
        player1_bottom.goto(0, -295)
        player1_top.goto(0, -265)
    elif current_car == 2:
        player2.color("red")
        player2.goto(0, -280)
        player2_nose.goto(0, -240)
    
    screen.onkeypress(move_left, "Left")
    screen.onkeypress(move_right, "Right")
    screen.onkeypress(toggle_boost, "space")
    screen.onkeypress(open_shop, "Tab")
    screen.onkeypress(shoot_bullet, "z")
    screen.onkeypress(toggle_headlight, "l")
    screen.onkeypress(honk_horn, "g")

def game_over():
    global game_state, show_message, message_text, message_pos, message_color, message_font
    game_state = "over"
    hide_all_players()
    
    for p in particles:
        p["turtle"].hideturtle()
    particles.clear()
    
    show_message = True
    message_text = f"💥 GAME OVER 💥\nDistance: {score} m\nStars: ⭐{total_stars}\n\nPress ENTER to Restart\n\nv{GAME_VERSION} | Made with ❤️ by {GAME_AUTHOR_FA}"
    message_pos = (0, 0)
    message_color = "yellow"
    message_font = ("Courier", 20, "bold")

def handle_crash(enemy_obj):
    global lives, invincible, invincible_timer, boost_active, show_message, message_text, message_pos, message_color, message_font
    enemy_obj["turtle"].hideturtle()
    enemies.remove(enemy_obj)
    lives -= 1
    if lives <= 0:
        game_over()
        return True
    else:
        invincible = True
        invincible_timer = 120
        boost_active = False
        
        show_message = True
        message_text = "⚠️ CRASH! ⚠️"
        message_pos = (0, 0)
        message_color = "red"
        message_font = ("Courier", 36, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 2000)
        return False

def handle_bump_collision(bump_obj):
    global lives, total_stars, game_state, show_message, message_text, message_pos, message_color, message_font
    
    bump_obj["turtle"].hideturtle()
    speed_bumps.remove(bump_obj)
    
    if boost_active or speed > 10:
        lives -= 1
        play_bump_sound()
        
        show_message = True
        message_text = "🚧 TECHNICAL PROBLEMS! 🚧"
        message_pos = (0, 0)
        message_color = "red"
        message_font = ("Courier", 24, "bold")
        
        if lives <= 0:
            game_state = "broke_down"
            hide_all_players()
            
            show_message = True
            message_text = f"💥 CAR BROKE DOWN 💥\nTechnical failure from speed bump!\nDistance: {score} m | Stars: ⭐{total_stars}\n\nPress [P] to pay 60⭐ and continue\nPress [ENTER] to restart\n\nv{GAME_VERSION} | Made with ❤️ by {GAME_AUTHOR_FA}"
            message_pos = (0, 0)
            message_color = "yellow"
            message_font = ("Courier", 16, "bold")
            
            screen.onkeypress(None, "Left")
            screen.onkeypress(None, "Right")
            screen.onkeypress(None, "space")
            screen.onkeypress(None, "Tab")
            screen.onkeypress(None, "z")
            screen.onkeypress(None, "l")
            screen.onkeypress(None, "g")
            screen.onkeypress(pay_to_continue, "p")
            screen.onkeypress(start_game, "Return")
            return True
        else:
            screen.ontimer(lambda: globals().update({'show_message': False}), 2500)
            return False
    else:
        show_message = True
        message_text = "✅ Safe passage!"
        message_pos = (0, 0)
        message_color = "green"
        message_font = ("Courier", 24, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 1500)
        return False

def pay_to_continue():
    global total_stars, lives, game_state, show_message, message_text, message_pos, message_color, message_font
    
    if total_stars >= 60:
        total_stars -= 60
        lives = 2
        game_state = "playing"
        
        screen.onkeypress(move_left, "Left")
        screen.onkeypress(move_right, "Right")
        screen.onkeypress(toggle_boost, "space")
        screen.onkeypress(open_shop, "Tab")
        screen.onkeypress(shoot_bullet, "z")
        screen.onkeypress(toggle_headlight, "l")
        screen.onkeypress(honk_horn, "g")
        
        show_current_player()
        
        show_message = True
        message_text = "✅ REPAIRED! -60⭐"
        message_pos = (0, 0)
        message_color = "green"
        message_font = ("Courier", 30, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 2500)
    else:
        show_message = True
        message_text = "❌ Not enough stars!"
        message_pos = (0, 0)
        message_color = "red"
        message_font = ("Courier", 24, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 2000)

def collect_powerup(powerup_obj):
    global lives, show_message, message_text, message_pos, message_color, message_font
    powerup_obj["turtle"].hideturtle()
    powerups.remove(powerup_obj)
    if lives < max_lives:
        lives += 1
        show_message = True
        message_text = "+1 ❤️ LIFE!"
        message_pos = (0, 100)
        message_color = "green"
        message_font = ("Courier", 30, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 2000)

def collect_grow_powerup(grow_obj):
    global player_size, show_message, message_text, message_pos, message_color, message_font
    grow_obj["turtle"].hideturtle()
    grow_powerups.remove(grow_obj)
    if player_size < max_player_size:
        player_size += 0.3
        if current_car == 0:
            player.shapesize(stretch_wid=3 * player_size, stretch_len=1.5 * player_size)
        elif current_car == 1:
            player1_bottom.shapesize(stretch_wid=1.5 * player_size, stretch_len=1.5 * player_size)
            player1_top.shapesize(stretch_wid=1.5 * player_size, stretch_len=1.5 * player_size)
        elif current_car == 2:
            player2.shapesize(stretch_wid=3 * player_size, stretch_len=1.5 * player_size)
        
        show_message = True
        message_text = "🟠 BIGGER!"
        message_pos = (0, 50)
        message_color = "orange"
        message_font = ("Courier", 30, "bold")
        screen.ontimer(lambda: globals().update({'show_message': False}), 2000)

def hit_oil_spill(oil_obj):
    global slippery, slippery_timer, show_message, message_text, message_pos, message_color, message_font
    oil_obj["turtle"].hideturtle()
    oil_spills.remove(oil_obj)
    slippery = True
    slippery_timer = 120
    
    show_message = True
    message_text = "🛢️ OIL! SLIPPERY!"
    message_pos = (0, 0)
    message_color = "black"
    message_font = ("Courier", 30, "bold")

def collect_star(star_obj):
    global total_stars, show_message, message_text, message_pos, message_color, message_font
    star_obj["turtle"].hideturtle()
    stars_items.remove(star_obj)
    star_value = random.choice([5, 50])
    total_stars += star_value
    play_star_sound()
    
    show_message = True
    message_text = f"⭐ +{star_value} STARS!"
    message_pos = (0, 0)
    message_color = "gold"
    message_font = ("Courier", 30, "bold")
    screen.ontimer(lambda: globals().update({'show_message': False}), 2000)

def collect_bullet_powerup(bp_obj):
    global bullets_count, show_message, message_text, message_pos, message_color, message_font
    bp_obj["turtle"].hideturtle()
    bullet_powerups.remove(bp_obj)
    bullets_count = min(bullets_count + 3, max_bullets)
    
    show_message = True
    message_text = "🔫 +3 BULLETS!"
    message_pos = (0, 50)
    message_color = "brown"
    message_font = ("Courier", 30, "bold")
    screen.ontimer(lambda: globals().update({'show_message': False}), 2000)

def truck_defeated():
    global total_stars, truck_active, truck_timer, trucks, show_message, message_text, message_pos, message_color, message_font
    total_stars += 100
    truck_active = False
    truck_timer = 0
    for t in trucks:
        t.hideturtle()
    trucks.clear()
    
    show_message = True
    message_text = "✅ TRUCK DEFEATED! +100⭐"
    message_pos = (0, 0)
    message_color = "green"
    message_font = ("Courier", 30, "bold")
    screen.ontimer(lambda: globals().update({'show_message': False}), 3000)

def truck_timeout():
    global lives, total_stars, player_size, truck_active, truck_timer, trucks, show_message, message_text, message_pos, message_color, message_font
    player_size = 3.5
    if current_car == 0:
        player.shapesize(stretch_wid=3 * player_size, stretch_len=1.5 * player_size)
    elif current_car == 1:
        player1_bottom.shapesize(stretch_wid=1.5 * player_size, stretch_len=1.5 * player_size)
        player1_top.shapesize(stretch_wid=1.5 * player_size, stretch_len=1.5 * player_size)
    elif current_car == 2:
        player2.shapesize(stretch_wid=3 * player_size, stretch_len=1.5 * player_size)
    lives = 1
    total_stars = max(0, total_stars - 50)
    truck_active = False
    truck_timer = 0
    for t in trucks:
        t.hideturtle()
    trucks.clear()
    
    show_message = True
    message_text = "💥 TRUCK TIMEOUT! PENALTY!"
    message_pos = (0, 0)
    message_color = "red"
    message_font = ("Courier", 30, "bold")
    screen.ontimer(lambda: globals().update({'show_message': False}), 3000)

def open_shop():
    global game_state, shop_open
    if game_state in ["playing", "over", "start"]:
        game_state = "shop"
        shop_open = True
        road.hideturtle()
        for line in road_lines:
            line.hideturtle()
        for p in particles:
            p["turtle"].hideturtle()
        draw_shop()
        screen.onkeypress(close_shop, "Escape")
        screen.onkeypress(buy_car_1, "1")
        screen.onkeypress(buy_car_2, "2")
        screen.onkeypress(select_car_0, "q")
        screen.onkeypress(select_car_1, "w")
        screen.onkeypress(select_car_2, "e")

def close_shop():
    global game_state, shop_open
    shop_open = False
    shop_pen.clear()
    road.showturtle()
    for line in road_lines:
        line.showturtle()
    if game_state == "shop":
        game_state = "start"
    screen.onkeypress(None, "Escape")
    screen.onkeypress(None, "1")
    screen.onkeypress(None, "2")
    screen.onkeypress(None, "q")
    screen.onkeypress(None, "w")
    screen.onkeypress(None, "e")
    if game_state == "start":
        screen.onkeypress(start_game, "Return")
        screen.onkeypress(open_shop, "Tab")

def draw_shop():
    shop_pen.clear()
    shop_pen.goto(0, 280)
    shop_pen.write("🛒 CAR SHOP 🛒", align="center", font=("Courier", 36, "bold"))
    shop_pen.goto(0, 230)
    shop_pen.write(f"Your Stars: ⭐ {total_stars}", align="center", font=("Courier", 20, "bold"))
    shop_pen.goto(-200, 150)
    owned_text = "✅ OWNED" if 0 in owned_cars else ""
    selected_text = " 👈 SELECTED" if current_car == 0 else ""
    shop_pen.write(f"[Q] Default Red {owned_text}{selected_text}", align="left", font=("Courier", 16, "bold"))
    shop_pen.goto(-200, 125)
    shop_pen.write("Free", align="left", font=("Courier", 14, "normal"))
    shop_pen.goto(-200, 60)
    owned_text = "✅ OWNED" if 1 in owned_cars else ""
    selected_text = " 👈 SELECTED" if current_car == 1 else ""
    shop_pen.write(f"[1] Buy Orange-Yellow {owned_text}{selected_text}", align="left", font=("Courier", 16, "bold"))
    shop_pen.goto(-200, 35)
    shop_pen.write("Price: ⭐ 30 | [W] Select", align="left", font=("Courier", 14, "normal"))
    shop_pen.goto(-200, 10)
    shop_pen.write("Colors swap when boosting!", align="left", font=("Courier", 12, "italic"))
    shop_pen.goto(-200, -50)
    owned_text = "✅ OWNED" if 2 in owned_cars else ""
    selected_text = " 👈 SELECTED" if current_car == 2 else ""
    shop_pen.write(f"[2] Buy Red + Nose {owned_text}{selected_text}", align="left", font=("Courier", 16, "bold"))
    shop_pen.goto(-200, -75)
    shop_pen.write("Price: ⭐ 50 | [E] Select", align="left", font=("Courier", 14, "normal"))
    shop_pen.goto(-200, -100)
    shop_pen.write("Yellow + triangle when boosting!", align="left", font=("Courier", 12, "italic"))
    shop_pen.goto(0, -200)
    shop_pen.write("Press [ESC] to exit shop", align="center", font=("Courier", 18, "bold"))

def buy_car_1():
    global total_stars, owned_cars
    if 1 not in owned_cars and total_stars >= 30:
        total_stars -= 30
        owned_cars.append(1)
        cars_info[1]["owned"] = True
        draw_shop()

def buy_car_2():
    global total_stars, owned_cars
    if 2 not in owned_cars and total_stars >= 50:
        total_stars -= 50
        owned_cars.append(2)
        cars_info[2]["owned"] = True
        draw_shop()

def select_car_0():
    global current_car
    if 0 in owned_cars:
        current_car = 0
        draw_shop()

def select_car_1():
    global current_car
    if 1 in owned_cars:
        current_car = 1
        draw_shop()

def select_car_2():
    global current_car
    if 2 in owned_cars:
        current_car = 2
        draw_shop()

def show_start_screen():
    global show_message, message_text, message_pos, message_color, message_font
    show_message = True
    message_text = f"🏎️ RACING GAME 🏁\n\n⭐ Stars: {total_stars}\n\n← → : Move | SPACE : Boost\nZ : Shoot | TAB : Shop\nL : Headlight | G : Horn\n\n🌆 Environment changes every 200m!\n🚧 Speed bumps: Slow = OK, Fast = Damage!\n\nPress ENTER to Start\n\nVersion {GAME_VERSION}\nMade with ❤️ by {GAME_AUTHOR_FA}\n({GAME_AUTHOR})"
    message_pos = (0, 0)
    message_color = "yellow"
    message_font = ("Courier", 16, "bold")

# ✅ حلقه اصلی با رسم پیام در هر فریم
def game_loop():
    global score, speed, game_state, frame_count, spawn_rate
    global boost_active, invincible, invincible_timer
    global slippery, slippery_timer
    global truck_active, truck_timer, truck_hp
    
    screen.update()
    
    if game_state == "playing":
        current_speed = boost_speed if boost_active else speed
    else:
        current_speed = 3
    
    for line in road_lines:
        if line.isvisible():
            line.sety(line.ycor() - current_speed)
            if line.ycor() < -350:
                line.goto(0, 350)
    
    if game_state == "playing":
        update_particles()
    
# ✅ حلقه اصلی با رسم پیام در هر فریم
def game_loop():
    global score, speed, game_state, frame_count, spawn_rate
    global boost_active, invincible, invincible_timer
    global slippery, slippery_timer
    global truck_active, truck_timer, truck_hp
    
    screen.update()
    
    if game_state == "playing":
        current_speed = boost_speed if boost_active else speed
    else:
        current_speed = 3
    
    for line in road_lines:
        if line.isvisible():
            line.sety(line.ycor() - current_speed)
            if line.ycor() < -350:
                line.goto(0, 350)
    
    if game_state == "playing":
        update_particles()
    
    # ✅ فراخوانی show_start_screen وقتی در صفحه شروع هستیم
    if game_state == "start":
        show_start_screen()
    
    # ✅ رسم پیام در هر فریم (بعد از update)
    if show_message:
        msg_pen.clear()
        msg_pen.color(message_color)
        msg_pen.goto(message_pos)
        msg_pen.write(message_text, align="center", font=message_font)
    
    if game_state == "playing":
        frame_count += 1
        
        if score > 0 and score - last_env_change >= 200:
            change_environment()
        
        if invincible:
            invincible_timer -= 1
            if invincible_timer % 10 < 5:
                if current_car == 0:
                    player.color("white")
                elif current_car == 1:
                    player1_bottom.color("white")
                    player1_top.color("white")
                elif current_car == 2:
                    player2.color("white")
            else:
                if current_car == 0:
                    player.color("yellow" if boost_active else "red")
                elif current_car == 1:
                    update_car1_colors()
                elif current_car == 2:
                    update_car2_colors()
            if invincible_timer <= 0:
                invincible = False
                if current_car == 0:
                    player.color("red")
                elif current_car == 1:
                    update_car1_colors()
                elif current_car == 2:
                    update_car2_colors()
        
        if slippery:
            slippery_timer -= 1
            if slippery_timer <= 0:
                slippery = False
        
        if truck_active:
            truck_timer -= 1
            if truck_timer <= 0:
                truck_timeout()
        
        if score > 0 and score - last_width_change >= 50:
            change_road_width()
        
        if frame_count % spawn_rate == 0:
            spawn_enemy()
        if frame_count % powerup_spawn_rate == 0:
            spawn_powerup()
        if frame_count % grow_powerup_spawn_rate == 0:
            spawn_grow_powerup()
        if frame_count % oil_spawn_rate == 0:
            spawn_oil_spill()
        if frame_count % star_spawn_rate == 0:
            spawn_star()
        if frame_count % bullet_powerup_spawn_rate == 0:
            spawn_bullet_powerup()
        if frame_count % truck_spawn_rate == 0 and not truck_active:
            spawn_truck()
        if frame_count % speed_bump_spawn_rate == 0:
            spawn_speed_bump()
        
        px = get_player_x()
        py = get_player_y()
        
        if current_env == "night":
            car_light.goto(px, py)
        
        if headlight_on:
            headlight.goto(px, py + 40)
        
        for enemy in enemies[:]:
            enemy["turtle"].sety(enemy["turtle"].ycor() - enemy["speed"])
            if enemy["turtle"].ycor() < -350:
                enemy["turtle"].hideturtle()
                enemies.remove(enemy)
                score += 10
                if score % 100 == 0:
                    speed += 0.5
                    if spawn_rate > 30:
                        spawn_rate -= 5
            if not invincible and enemy["turtle"].distance(px, py) < 40 * player_size:
                is_game_over = handle_crash(enemy)
                if is_game_over:
                    screen.ontimer(game_loop, 16)
                    return
        
        for bullet in bullets[:]:
            bullet["turtle"].sety(bullet["turtle"].ycor() + bullet["speed"])
            if bullet["turtle"].ycor() > 350:
                bullet["turtle"].hideturtle()
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if bullet["turtle"].distance(enemy["turtle"]) < 30:
                        enemy["turtle"].hideturtle()
                        enemies.remove(enemy)
                        bullet["turtle"].hideturtle()
                        bullets.remove(bullet)
                        score += 20
                        break
                if truck_active and bullet in bullets:
                    for truck in trucks:
                        if bullet["turtle"].distance(truck) < 60:
                            truck_hp -= 1
                            bullet["turtle"].hideturtle()
                            bullets.remove(bullet)
                            if truck_hp <= 0:
                                truck_defeated()
                            break
        
        for powerup in powerups[:]:
            powerup["turtle"].sety(powerup["turtle"].ycor() - powerup["speed"])
            if powerup["turtle"].ycor() < -350:
                powerup["turtle"].hideturtle()
                powerups.remove(powerup)
            elif powerup["turtle"].distance(px, py) < 35 * player_size:
                collect_powerup(powerup)
        
        for grow_p in grow_powerups[:]:
            grow_p["turtle"].sety(grow_p["turtle"].ycor() - grow_p["speed"])
            if grow_p["turtle"].ycor() < -350:
                grow_p["turtle"].hideturtle()
                grow_powerups.remove(grow_p)
            elif grow_p["turtle"].distance(px, py) < 35 * player_size:
                collect_grow_powerup(grow_p)
        
        for oil in oil_spills[:]:
            oil["turtle"].sety(oil["turtle"].ycor() - oil["speed"])
            if oil["turtle"].ycor() < -350:
                oil["turtle"].hideturtle()
                oil_spills.remove(oil)
            elif oil["turtle"].distance(px, py) < 40 * player_size:
                hit_oil_spill(oil)
        
        for star in stars_items[:]:
            star["turtle"].sety(star["turtle"].ycor() - star["speed"])
            if star["turtle"].ycor() < -350:
                star["turtle"].hideturtle()
                stars_items.remove(star)
            elif star["turtle"].distance(px, py) < 35 * player_size:
                collect_star(star)
        
        for bp in bullet_powerups[:]:
            bp["turtle"].sety(bp["turtle"].ycor() - bp["speed"])
            if bp["turtle"].ycor() < -350:
                bp["turtle"].hideturtle()
                bullet_powerups.remove(bp)
            elif bp["turtle"].distance(px, py) < 35 * player_size:
                collect_bullet_powerup(bp)
        
        for truck in trucks[:]:
            truck.sety(truck.ycor() - speed * 0.5)
            if truck.ycor() < -350:
                truck.hideturtle()
                trucks.remove(truck)
                truck_active = False
        
        for bump in speed_bumps[:]:
            bump["turtle"].sety(bump["turtle"].ycor() - bump["speed"])
            
            bump_y = bump["turtle"].ycor()
            
            if bump_y < -350:
                bump["turtle"].hideturtle()
                speed_bumps.remove(bump)
            elif abs(bump_y - py) < 60 * player_size:
                is_game_over = handle_bump_collision(bump)
                if is_game_over:
                    screen.ontimer(game_loop, 16)
                    return
        
        hud.clear()
        current_speed = boost_speed if boost_active else speed
        status = ""
        if boost_active:
            status += "🚀"
        if slippery:
            status += " 🛢️"
        if headlight_on:
            status += " 💡"
        
        hearts = "❤️" * lives + "🖤" * (max_lives - lives)
        bullet_text = f"🔫{bullets_count}" if bullets_count > 0 else ""
        truck_text = f"🚛{truck_timer//60}s" if truck_active else ""
        env_text = env_names[current_env]
        
        hud.write(f"{env_text} | {hearts} | ⭐{total_stars} | {bullet_text} | {score}m | {int(current_speed * 10)}km/h {status} {truck_text}", 
                  align="center", font=("Courier", 11, "bold"))
    
    screen.ontimer(game_loop, 16)
# ✅ ایجاد قلم‌ها در آخر (بالاترین لایه)
hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("white")
hud.goto(0, 310)

msg_pen = turtle.Turtle()
msg_pen.hideturtle()
msg_pen.penup()
msg_pen.color("yellow")

shop_pen = turtle.Turtle()
shop_pen.hideturtle()
shop_pen.penup()
shop_pen.color("white")

screen.listen()
screen.onkeypress(start_game, "Return")
screen.onkeypress(open_shop, "Tab")
game_loop()
screen.mainloop()
