from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

GRID_SIZE = 20
SNAKE_START = [(10, 10)]
FOOD_START = (15, 15)
DIRECTION_START = (1, 0)  # Bergerak ke kanan

snake = SNAKE_START[:]
food = FOOD_START
direction = DIRECTION_START
game_over = False
score = 0

def is_collision(head):
    return (
        not (0 <= head[0] < GRID_SIZE and 0 <= head[1] < GRID_SIZE) or
        head in snake[:-1]
    )

def generate_food():
    while True:
        new_food = (random.randrange(GRID_SIZE), random.randrange(GRID_SIZE))
        if new_food not in snake:
            return new_food

def get_game_speed(current_score):
    if current_score < 5:
        return 250
    elif current_score < 10:
        return 200
    elif current_score < 15:
        return 150
    else:
        return 100

@app.route('/')
def index():
    return render_template('index.html', grid_size=GRID_SIZE)

@app.route('/update', methods=['POST'])
def update():
    global snake, food, direction, game_over, score

    if game_over:
        return jsonify({'game_over': True, 'score': score})

    new_direction = request.form.get('direction')
    if new_direction == 'up' and direction != (0, 1):
        direction = (0, -1)
    elif new_direction == 'down' and direction != (0, -1):
        direction = (0, 1)
    elif new_direction == 'left' and direction != (1, 0):
        direction = (-1, 0)
    elif new_direction == 'right' and direction != (-1, 0):
        direction = (1, 0)

    head_x, head_y = snake[-1]
    new_head = (head_x + direction[0], head_y + direction[1])
    snake.append(new_head)

    eaten = False
    if new_head == food:
        food = generate_food()
        score += 1
        eaten = True
    else:
        snake.pop(0)

    if is_collision(new_head):
        game_over = True

    return jsonify({
        'snake': snake,
        'food': food,
        'game_over': game_over,
        'score': score,
        'speed': get_game_speed(score),
        'eaten': eaten # Flag untuk efek makan (belum diimplementasikan visualnya)
    })

@app.route('/reset', methods=['POST'])
def reset():
    global snake, food, direction, game_over, score
    snake = SNAKE_START[:]
    food = FOOD_START
    direction = DIRECTION_START
    game_over = False
    score = 0
    return jsonify({'message': 'Game reset'})

if __name__ == '__main__':
    app.run(debug=True)
