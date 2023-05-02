import secrets
import hashlib
import json
import random


class Game:
    def __init__(self):
        self.desk = []
        self.players = []
        self.board = []
        self.points = []
        self.cards_played = 0
        
    
    def shuffle_deck(self):
        shuffle_deck(self.desk)

    def start(self):
        shuffle_deck(self.desk)
        self.players = ['Oleg', 'Danil', 'Vadim']
        self.cards_played = 12
        self.board = get_cards(self.desk, self.cards_played)
        self.points = [1, 5, 10]
              
    def add_player(self, player):
        self.players.append(player)
        self.points.append(0)
        return json.dumps({"success": true,
                           "exception": null
                           })


    def get_players(self):
        return self.players

    
    def get_board(self):
        return self.board

    def get_board_json(self):
        card = cards_generation()
        buf = []
        for i in range(len(self.board)):
            buf.append({"id": self.board[i],
                          "color": card[self.board[i]][0],
                          "shape": card[self.board[i]][1],
                          "fill": card[self.board[i]][2],
                          "count": card[self.board[i]][3]
                          })
        status_game = self.chech_end()
        status = "ongoing"
        if status_game:
            status = "ended"
        
        buf1 = json.dumps({"cards": buf,
                           "status": status}) 
        return buf1

    def get_point(self, player):
        
        return self.points[self.players.index(player)]


    def get_all_points(self):

        users = []

        for i in range(len(self.players)):
            users.append({"name": self.players[i],
                          "score": self.get_point(self.players[i])})
        buf_all_points = json.dumps({"success": 'true',
                                     "exception": 'null',
                                     "users": users                                
                                     })
        return buf_all_points


    def turn(self, choose_cards=[], player=""):
        status = self.choose_set(choose_cards)
        if status:
            if self.cards_played < (len(self.desk) - len(self.board)):
                for i in self.board:
                    if i in choose_cards:
                        new_card = get_cards(self.desk, 1, self.cards_played)
                        self.cards_played += 1
                        self.board[self.board.index(i)] = new_card[0]
            else:
                for i in choose_cards:
                    self.board.remove(i)
                    self.cards_played += 1
            if len(player) > 0:
                points[self.players.index(player)] += 1


    def get_cards(self):
        for i in range(3):
            if self.cards_played < (len(self.desk) - len(self.board)):
                new_card = get_cards(self.desk, 1, self.cards_played)
                self.cards_played += 1
                self.board.append(new_card[0])
    
    
    def choose_set(self, choose_cards=[]):
        card = cards_generation()
        cards = []
        if choose_cards[0] in self.board and choose_cards[1] in self.board and choose_cards[2] in self.board:
            for i in range(3):
                cards.append(card[choose_cards[i]])
            status = check_set(cards)
            return status
        return False

    def chech_end(self):
        card = cards_generation()
        cards = []
        for i in range(len(self.board)):
            cards.append(card[self.board[i]])
        if (len(self.desk) - len(self.board) - self.cards_played) >= 21 :
            return False
        elif self.board == 0:
            return True
        elif len(set_found(cards)) == 0:
            return True
        else:
            return False


def registration(nickname, password, users={}, tokens={}):

    if nickname in users: #such user already exists
        return json.dumps({"success": 'false',
                            "exception": {
                                "message": "This user already exists"
                                }
                            }) 
    else:
        token = secrets.token_urlsafe(16)
        users.fromkeys(nickname, password)
        tokens.fromkeys(nickname, token)
        return json.dumps({"nickname": nickname,
                           "accessToken":token})


def authorization(nickname, password, users={}, tokens={}):
    if nickname in users and users[nickname] == password:
        #new_token = secrets.token_urlsafe(16)
        #tokens[nickname] = new_token
        return json.dumps({"nickname": nickname,
                           "accessToken":tokens[nickname]})
    else:
        return json.dumps({"success": 'false',
                            "exception": {
                                "message": "Nickname or password is incorrect"
                                }
                            })        


def cards_generation(cards=[]):
    for color in range(3):
        for shape in range(3):
            for fill in range(3):
                for count in range(3):
                    cards.append([color, shape, fill, count])
    
    return cards


def shuffle_deck(desk=[]):
    len_desk = 81
    if len(desk) > 0:
        len_desk = len(desk)
    else:
        for i in range(len_desk):
            desk.append(i)
    #print(desk)
    random.seed() 
    for i in range(len_desk-1):
        rand = int(random.random()*100%(len_desk-i-1))
        buf = desk[rand]
        desk[rand]=desk[len_desk-i-1]
        desk[len_desk-i-1] = buf
    return desk


def get_cards(desk, count=3, drawn_cards=0):
    deal_cards = []
    for i in range(drawn_cards, drawn_cards+count):
        deal_cards.append(desk[i])
    return deal_cards

        
def check_set(buf=[]):
    for k in range(3):
        if not((int(buf[0][k]) == int(buf[1][k]) and
                int(buf[0][k]) == int(buf[2][k])) or
               (buf[0][k] != buf[1][k] and
                buf[0][k] != buf[2][k] and
                buf[2][k] != buf[1][k])):
                            return False
    return True


def set_found(cards=[]):
    bj = cards

    buf_options = ["color", "shape", "fill", "count"]
    answer = []
    flag = True
    count_card = int(len(bj))
    if len(cards) > 0:
        for i in range(count_card):
            if not flag: break
            for j in range(i+1, count_card):
                if not flag: break
                for l in range(j+1, count_card):
                    flag = False
                    for k in range(4):
                        if not((int(bj[i][k]) == int(bj[j][k]) and
                                int(bj[i][k]) == int(bj[l][k])) or
                               (bj[i][k] != bj[j][k] and
                                bj[i][k] != bj[l][k] and
                                bj[l][k] != bj[j][k])):
                            flag = True
                            break
                    if not flag:
                        answer = [i, j, l]
                        break


    return answer


def set_found_json(jf, context):
    bj = json.loads(jf['body'])

    buf_options = ["color", "shape", "fill", "count"]
    answer = []
    flag = True

    count_card = int(len(bj['cards']))

    for i in range(count_card):
        if not flag: break
        for j in range(i+1, count_card):
            if not flag: break
            for l in range(j+1, count_card):
                flag = False
                for k in buf_options:
                    if not((int(bj["cards"][i][k]) == int(bj["cards"][j][k]) and
                    int(bj["cards"][i][k]) == int(bj["cards"][l][k])) or
                    (bj["cards"][i][k] != bj["cards"][j][k] and
                    bj["cards"][i][k] != bj["cards"][l][k] and
                    bj["cards"][l][k] != bj["cards"][j][k])):
                        flag = True
                        break
                if not flag:
                    answer = [i, j, l]
                    break


    return {
        'statusCode': 200,
        'body': answer,
    }

def create_game_table(tables=[]):
    newTable = Game()
    tables.append(newTable)
    return tables

def connecting_players(player, tables=[], number_game=0):
    tables[number_game].add_player(player)
    pass


def set_found_json111(jf):
    bj = json.loads(jf)

    buf_options = ["color", "shape", "fill", "count"]
    answer = ""
    flag = True

    count_card = int(len(bj['cards']))

    for i in range(count_card):
        if not flag: break
        for j in range(i+1, count_card):
            if not flag: break
            for l in range(j+1, count_card):
                flag = False
                for k in buf_options:
                    if not((int(bj["cards"][i][k]) == int(bj["cards"][j][k]) and
                    int(bj["cards"][i][k]) == int(bj["cards"][l][k])) or
                    (bj["cards"][i][k] != bj["cards"][j][k] and
                    bj["cards"][i][k] != bj["cards"][l][k] and
                    bj["cards"][l][k] != bj["cards"][j][k])):
                        flag = True
                        break
                if not flag:
                    answer = str(bj["cards"][i]["id"]) + ' ' + str(bj["cards"][j]["id"]) + ' ' + str(bj["cards"][l]["id"])
                    break


    return answer


