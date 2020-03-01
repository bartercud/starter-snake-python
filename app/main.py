import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
    return


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json
    # print(json.dumps(data))

    return {
        "color": "#AA0004",
        "headType": "shades",
        "tailType": "block-bum"
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
     # print(json.dumps(data))

     #collect board info
     boardsize = data['board']['height']
     food = []
     for f in data['board']['food']:
         foodtuple = (f['x'], f['y'])
         food.append(foodtuple)

    #collect my info
     me = data['you']
     body = []
     for b in me['body']:
         bodytuple = (b['x'], b['y'])
         body.append(bodytuple)
    myhead = body[0]
    mytail = body[-1]
    mysize = len(body)
    myhealth = me['health']

    #collect others info
    othersnakes = data['board']['snakes']
    # for s in othersnakes:


    #Make a move
    moves = []
    wallsafemoves = []
    othersnakebodysafemoves = []
    othersnakeheadsafemoves = []


    direction = random.choice(moves)
    return move_response(direction)

def time_to_eat(othersnakes, me, food, myhead, moves):
    # if me['health'] < 20: (if statement in move function)
        if not is_other_closer(othersnkaes, me, food):
            if (food[0] - myhead[0]) < 0:
                moves.append("left")
            else if (food[0] - myhead[0]) > 0:
                moves.append("right")
            else if (food[1] - myhead[1]) < 0):
                moves.append("up")
            else if (food[1] - myhead[1]) > 0):
                moves.append("down")



def is_other_closer(othersnakes, myhead, food):
    result = False
    for f in food:
        for s in othersnakes:
            head = othersnakes['body'][0]
            otherxdist = food[0] - head[0]
            otherydist = food[1] - head[1]
            otherdist = ((otherxdist)^2 + (otherydist^2))^(1/2)
            myxdist = food[0] - myhead[0]
            myydist = food[1] - myhead[1]
            mydist = ((myxdist)^2 + (myydist^2))^(1/2)
            if otherdist < mydist:
                result = True
    return result

def wall_detection(boardsize, myhead, wallsafemoves):
    if (myhead[0] != 0):
        wallsafemoves.append('left')
    else if (myhead[0] != boardsize):
        wallsafemoves.append('right')
    else if (myhead[1] != 0):
        wallsafemoves.append('up')
    else if (myhead[1] != boardsize):
        wallsafemoves.append('down')

def snake_body_detection(myhead, othersnakebodysafemoves, othersnakes):
    xleftcount = 0
    xrightcount = 0
    yupcount = 0
    ydowncount = 0
    for s in othersnakes:
        for b in s['body']:
            if (((b[0] - 1) == myhead[0]) and (b[1] == myhead[1])):
                xrightcount += 1
            else if (((b[0] + 1) == myhead[0]) and (b[1] == myhead[1])):
                xleftcount += 1
            else if (((b[1] - 1) == myhead[1]) and (b[0] == myhead[0])):
                yupcount += 1
            else if (((b[1] + 1) == myhead[1]) and (b[0] == myhead[0])):
                ydowncount += 1
    if (xleftcount == 0):
        othersnakebodysafemoves.append('left')
    else if (xrightcount == 0):
        othersnakebodysafemoves.append('right')
    else if (yupcount == 0):
        othersnakebodysafemoves.append('up')
    else if (ydowncount == 0):
        othersnakebodysafemoves.append('down')

def snake_head_detection(myhead, othersnakeheadsafemoves, othersnakes):

    
# {
#   "game": {
#     "id": "game-id-string"
#   },
#   "turn": 4,
#   "board": {
#     "height": 15,
#     "width": 15,
#     "food": [
#       {
#         "x": 1,
#         "y": 3
#       }
#     ],
#     "snakes": [
#       {
#         "id": "snake-id-string",
#         "name": "Sneky Snek",
#         "health": 90,
#         "body": [
#           {
#             "x": 1,
#             "y": 3
#           }
#         ],
#         "shout": "Hello my name is Sneky Snek"
#       }
#     ]
#   },
#   "you": {
#     "id": "snake-id-string",
#     "name": "Sneky Snek",
#     "health": 90,
#     "body": [
#       {
#         "x": 1,
#         "y": 3
#       }
#     ],
#     "shout": "Hello my name is Sneky Snek"
#   }
# }



@bottle.post('/end')
def end():
    data = bottle.request.json
    # print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
