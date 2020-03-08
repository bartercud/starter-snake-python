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
         foodtuple = (int(f['x']), int(f['y']))
         food.append(foodtuple)

    #collect my info
    me = data['you']
    body = []
    for b in me['body']:
        bodytuple = (int(b['x']), int(b['y']))
        body.append(bodytuple)
    myhead = body[0]
    mytail = body[-1]
    mysize = len(body)
    myhealth = me['health']

    #collect others info
    othersnakes = data["board"]["snakes"]
    # for s in othersnakes:


    #Make a move
    validmoves = []
    foodmoves = []
    wallsafemoves = []
    othersnakebodysafemoves = []
    othersnakeheadsafemoves = []
    finalmoves = []

    print("calling time_to_eat")
    time_to_eat(othersnakes, me, food, myhead, foodmoves)
    wall_detection(boardsize, myhead, wallsafemoves)
    snake_body_detection(myhead, othersnakebodysafemoves, othersnakes)
    snake_head_detection(myhead, othersnakeheadsafemoves, othersnakes)

    if ("left" in wallsafemoves) and ("left" in othersnakebodysafemoves) and ("left" in othersnakeheadsafemoves):
        validmoves.append("left")
    elif ("right" in wallsafemoves) and ("right" in othersnakebodysafemoves) and ("right" in othersnakeheadsafemoves):
        validmoves.append("right")
    elif ("up" in wallsafemoves) and ("up" in othersnakebodysafemoves) and ("up" in othersnakeheadsafemoves):
        validmoves.append("up")
    elif ("down" in wallsafemoves) and ("down" in othersnakebodysafemoves) and ("down" in othersnakeheadsafemoves):
        validmoves.append("down")

    if me['health'] < 20:

        time_to_eat(othersnakes, me, food, myhead, foodmoves)

        if ("left" in foodmoves) and ("left" in validmoves):
            finalmoves.append("left")
        elif ("right" in foodmoves) and ("right" in validmoves):
            finalmoves.append("right")
        elif ("up" in foodmoves) and ("up" in validmoves):
            finalmoves.append("up")
        elif ("down" in foodmoves) and ("down" in validmoves):
            finalmoves.append("down")
    else:
        finalmoves = validmoves

    try:
        direction = random.choice(finalmoves)
        return move_response(direction)
    except IndexError:
        dead = "left"
        return move_response(dead)

def time_to_eat(othersnakes, me, food, myhead, foodmoves):
    print("in time_to_eat")
    if not is_other_closer(othersnakes, myhead, food):
        for f in food:
            if (f[0] - myhead[0]) < 0:
                foodmoves.append("left")
            elif (f[0] - myhead[0]) > 0:
                foodmoves.append("right")
            elif (f[1] - myhead[1]) < 0:
                foodmoves.append("up")
            elif (f[1] - myhead[1]) > 0:
                foodmoves.append("down")



def is_other_closer(othersnakes, myhead, food):
    result = False
    smallestdist = 1000.0
    count = 0
    closestfoodindex = 0
    for f in food:
        myxdist = f[0] - myhead[0]
        myydist = f[1] - myhead[1]
        mydist = ((myxdist)**2 + (myydist**2))**(1/2)
        if (mydist< smallestdist):
            smallestdist = mydist
            closestfoodindex = count
        count += 1
    for s in othersnakes:
        head = s['body'][0]
        otherxdist = food[closestfoodindex][0] - head["x"]
        otherydist = food[closestfoodindex][1] - head["y"]
        otherdist = ((otherxdist)**2 + (otherydist**2))**(1/2)
        if (otherdist < smallestdist):
            result = True

    return result

def wall_detection(boardsize, myhead, wallsafemoves):
    if (myhead[0] != 0):
        wallsafemoves.append('left')
    elif (myhead[0] != boardsize):
        wallsafemoves.append('right')
    elif (myhead[1] != 0):
        wallsafemoves.append('up')
    elif (myhead[1] != boardsize):
        wallsafemoves.append('down')

def snake_body_detection(myhead, othersnakebodysafemoves, othersnakes):
    xleftcount = 0
    xrightcount = 0
    yupcount = 0
    ydowncount = 0
    for s in othersnakes:
        for b in s['body']:
            if (((b['x'] - 1) == myhead[0]) and (b['y'] == myhead[1])):
                xrightcount += 1
            elif (((b['x'] + 1) == myhead[0]) and (b['y'] == myhead[1])):
                xleftcount += 1
            elif (((b['y'] - 1) == myhead[1]) and (b['x'] == myhead[0])):
                yupcount += 1
            elif (((b['y'] + 1) == myhead[1]) and (b['x'] == myhead[0])):
                ydowncount += 1
    if (xleftcount == 0):
        othersnakebodysafemoves.append('left')
    elif (xrightcount == 0):
        othersnakebodysafemoves.append('right')
    elif (yupcount == 0):
        othersnakebodysafemoves.append('up')
    elif (ydowncount == 0):
        othersnakebodysafemoves.append('down')



def snake_head_detection(myhead, othersnakeheadsafemoves, othersnakes):
    xleftcount = 0
    xrightcount = 0
    yupcount = 0
    for s in othersnakes:
        if ((s['body'][0]['x'] == myhead[0]-1) and (s['body'][0]['y'] == myhead[1]+1)):
            xleftcount += 1
        elif ((s['body'][0]['x'] == myhead[0]-1) and (s['body'][0]['y'] == myhead[1])):
            xleftcount += 1
        elif ((s['body'][0]['x'] == myhead[0]-2) and (s['body'][0]['y'] == myhead[1])):
            xleftcount += 1
        elif ((s['body'][0]['x'] == myhead[0]-1) and (s['body'][0]['y'] == myhead[1]-1)):
            xleftcount += 1
            yupcount += 1
        elif ((s['body'][0]['x'] == myhead[0]) and (s['body'][0]['y'] == myhead[1]-1)):
            yupcount += 1
        elif ((s['body'][0]['x'] == myhead[0]) and (s['body'][0]['y'] == myhead[1]-2)):
            yupcount += 1
        elif ((s['body'][0]['x'] == myhead[0]+1) and (s['body'][0]['y'] == myhead[1]-1)):
            yupcount += 1
            xrightcount += 1
        elif ((s['body'][0]['x'] == myhead[0]+1) and (s['body'][0]['y'] == myhead[1])):
            xrightcount += 1
        elif ((s['body'][0]['x'] == myhead[0]+2) and (s['body'][0]['y'] == myhead[1])):
            xrightcount += 1
        elif ((s['body'][0]['x'] == myhead[0]+1) and (s['body'][0]['y'] == myhead[1]+1)):
            xrightcount += 1
    if (xleftcount == 0):
        othersnakeheadsafemoves.append('left')
    elif (xrightcount == 0):
        othersnakeheadsafemoves.append('right')
    elif (yupcount == 0):
        othersnakeheadsafemoves.append('up')
    elif (ydowncount == 0):
        othersnakeheadsafemoves.append('down')







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
