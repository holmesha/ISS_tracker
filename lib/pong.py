from machine import Pin
import time
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

# Setup display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

# Paddle settings
paddle_height = 40
paddle_width = 5
paddle_speed = 5

# Ball settings
ball_size = 5
ball_speed_x = 3
ball_speed_y = 2

# Paddle positions (left and right walls)
left_paddle_y = 100
right_paddle_y = 100

# Ball position and direction
ball_x = 160  # Start in the middle
ball_y = 120
ball_dx = -ball_speed_x  # Always starts toward Player 1
ball_dy = ball_speed_y

# Scores
left_score = 0
right_score = 0

# Buttons
button_A = Pin(12, Pin.IN, Pin.PULL_UP)  # Move left paddle up
button_B = Pin(13, Pin.IN, Pin.PULL_UP)  # Move left paddle down
button_X = Pin(14, Pin.IN, Pin.PULL_UP)  # Move right paddle up (2-player mode)
button_Y = Pin(15, Pin.IN, Pin.PULL_UP)  # Move right paddle down (2-player mode)

# Player mode (1 or 2)
player_mode = 1  # Default to 1-player mode

# AI settings (used only in 1-player mode)
ai_speed = 3  # Speed of AI movement

# X + Y button hold tracking
exit_hold_start = 0


# Draw paddles
def draw_paddles():
    display.set_pen(WHITE)
    display.rectangle(10, left_paddle_y, paddle_width, paddle_height)  # Left paddle
    display.rectangle(305, right_paddle_y, paddle_width, paddle_height)  # Right paddle


# Draw ball
def draw_ball():
    display.set_pen(WHITE)
    display.circle(ball_x, ball_y, ball_size)


# Draw scores
def draw_scores():
    display.text(str(left_score), 40, 10, scale=3)
    display.text(str(right_score), 260, 10, scale=3)


# Update ball position
def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, left_score, right_score

    # Move ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= 240:
        ball_dy *= -1

    # Ball collision with paddles
    if (ball_x - ball_size <= 15 and left_paddle_y <= ball_y <= left_paddle_y + paddle_height):
        ball_dx *= -1
    elif (ball_x + ball_size >= 305 and right_paddle_y <= ball_y <= right_paddle_y + paddle_height):
        ball_dx *= -1

    # Score points if ball goes past paddles
    if ball_x <= 0:
        right_score += 1
        reset_ball()
    elif ball_x >= 320:
        left_score += 1
        reset_ball()


# Reset ball
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = 160, 120
    ball_dx = -ball_speed_x  # Always start toward Player 1
    ball_dy = ball_speed_y


# Update paddles
def update_paddles():
    global left_paddle_y, right_paddle_y

    # Left paddle controls
    if button_A.value() == 0 and left_paddle_y > 0:  # Move up
        left_paddle_y -= paddle_speed
    if button_B.value() == 0 and left_paddle_y < 200:  # Move down
        left_paddle_y += paddle_speed

    # Right paddle (AI or manual)
    if player_mode == 1:  # AI mode
        if right_paddle_y + paddle_height / 2 < ball_y:
            right_paddle_y += ai_speed
        elif right_paddle_y + paddle_height / 2 > ball_y:
            right_paddle_y -= ai_speed
    else:  # 2-player mode
        if button_X.value() == 0 and right_paddle_y > 0:  # Move up
            right_paddle_y -= paddle_speed
        if button_Y.value() == 0 and right_paddle_y < 200:  # Move down
            right_paddle_y += paddle_speed


# Display mode selection screen
def select_mode():
    global player_mode
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.text("Select Mode:", 50, 40, scale=3)
    display.text("A - 1 Player", 50, 100, scale=2)
    display.text("B - 2 Player", 50, 150, scale=2)
    display.update()

    while True:
        if button_A.value() == 0:  # 1 Player
            player_mode = 1
            break
        if button_B.value() == 0:  # 2 Players
            player_mode = 2
            break

    time.sleep(0.5)  # Debounce


# Check for holding X + Y to exit
def check_exit():
    global exit_hold_start

    # Check if both X and Y are pressed
    if button_X.value() == 0 and button_Y.value() == 0:
        if exit_hold_start == 0:  # Start timing
            exit_hold_start = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), exit_hold_start) > 2000:  # 2 seconds
            return True
    else:
        exit_hold_start = 0  # Reset timer if released

    return False


# Main loop
def pong():
    global left_score, right_score

    # Select player mode
    select_mode()

    while True:
        # Clear the screen
        display.set_pen(BLACK)
        display.clear()

        # Update game elements
        update_paddles()
        update_ball()

        # Draw game elements
        draw_paddles()
        draw_ball()
        draw_scores()

        # Update the display
        display.update()

        # Check for exit using X + Y hold
        if check_exit():
            break

        # Delay for smooth gameplay
        time.sleep(0.05)

    # Return to ISS Tracker after game ends
    reset_ball()

