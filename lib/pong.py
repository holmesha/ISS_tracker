from machine import Pin
import time
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

# Set up display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

# Game Variables
paddle_width = 60
paddle_height = 10
ball_size = 5

# Speeds
paddle_speed = 10    # Adjustable paddle speed
ball_speed = 8      # Adjustable ball speed (affects dx and dy)

# Initial positions
player_x = 130
opponent_x = 130
ball_x, ball_y = 160, 120
ball_dx, ball_dy = ball_speed, ball_speed

player_score = 0
opponent_score = 0
max_score = 11

# Buttons
button_left = Pin(12, Pin.IN, Pin.PULL_UP)  # Move paddle left
button_right = Pin(13, Pin.IN, Pin.PULL_UP)  # Move paddle right
button_y = Pin(15, Pin.IN, Pin.PULL_UP)  # Triple-Y to exit

# Track Y button presses for exit
y_press_count = 0
last_press_time = 0
exit_press_window = 500  # Milliseconds between presses

# Draw paddles
def draw_paddle(x, y):
    display.set_pen(WHITE)
    display.rectangle(x, y, paddle_width, paddle_height)

# Draw ball
def draw_ball(x, y):
    display.set_pen(WHITE)
    display.circle(x, y, ball_size)

# Draw scores
def draw_scores():
    display.set_pen(WHITE)
    display.text(str(player_score), 10, 10, scale=2)
    display.text(str(opponent_score), 300, 10, scale=2)

# Reset ball position
def reset_positions():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = 160, 120
    ball_dx, ball_dy = ball_speed, ball_speed

# Collision detection
def ball_hits_paddle(ball_x, ball_y, paddle_x, paddle_y):
    return (paddle_x <= ball_x <= paddle_x + paddle_width) and \
           (paddle_y <= ball_y <= paddle_y + paddle_height)

# Pong game loop
def pong():
    global player_x, opponent_x, ball_x, ball_y, ball_dx, ball_dy
    global player_score, opponent_score, y_press_count, last_press_time

    # Reset scores before starting
    player_score = 0
    opponent_score = 0

    while True:
        # Check if Y is pressed 3 times quickly to exit
        if button_y.value() == 0:
            current_time = time.ticks_ms()
            if current_time - last_press_time < exit_press_window:
                y_press_count += 1
            else:
                y_press_count = 1  # Reset count if time exceeds window
            last_press_time = current_time

            if y_press_count >= 3:  # Exit Pong
                reset_positions()
                return

        # Clear display
        display.set_pen(BLACK)
        display.clear()

        # Draw paddles
        draw_paddle(player_x, 220)
        draw_paddle(opponent_x, 10)

        # Draw ball
        draw_ball(ball_x, ball_y)

        # Draw scores
        draw_scores()

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x <= 0:  # Left wall
            ball_dx = abs(ball_dx)  # Ensure positive direction
            ball_x += 1  # Nudge ball inward
        elif ball_x >= 315:  # Right wall
            ball_dx = -abs(ball_dx)  # Ensure negative direction
            ball_x -= 1  # Nudge ball inward

        # Ball collision with paddles
        if ball_hits_paddle(ball_x, ball_y, player_x, 220):  # Player paddle
            ball_dy = -abs(ball_dy)  # Ensure upward direction
            offset = (ball_x - (player_x + paddle_width / 2)) / (paddle_width / 2)
            ball_dx = int(ball_speed * offset)

        if ball_hits_paddle(ball_x, ball_y, opponent_x, 10):  # Opponent paddle
            ball_dy = abs(ball_dy)  # Ensure downward direction
            offset = (ball_x - (opponent_x + paddle_width / 2)) / (paddle_width / 2)
            ball_dx = int(ball_speed * offset)

        # Ball out of bounds (scores)
        if ball_y > 240:  # Player missed
            opponent_score += 1
            reset_positions()
        elif ball_y < 0:  # Opponent missed
            player_score += 1
            reset_positions()

        # Move player's paddle
        if button_left.value() == 0:
            player_x = max(0, player_x - paddle_speed)
        if button_right.value() == 0:
            player_x = min(260, player_x + paddle_speed)

        # AI Opponent movement (tracks ball)
        if opponent_x + paddle_width / 2 < ball_x:
            opponent_x = min(260, opponent_x + 3)
        elif opponent_x + paddle_width / 2 > ball_x:
            opponent_x = max(0, opponent_x - 3)

        # Check for max score
        if player_score >= max_score or opponent_score >= max_score:
            reset_positions()
            return  # Exit Pong and return to ISS Tracker

        # Update display
        display.update()
        time.sleep(0.03)

# If running standalone
if __name__ == "__main__":
    display.set_backlight(1.0)  # Turn on backlight
    pong()
