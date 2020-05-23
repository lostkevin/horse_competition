import os, time
from game import Game
from character import CharacterFactory

def display(data):
    os.system('cls')
    print(data)
cf = CharacterFactory(None)
game_size = 5
game = Game(cf.select_players(5))

display(game.get_current_state())       #各选手准备就绪
while not game.is_terminal:
    game.flush_players_buff()           #更新BUFF/ DEBUFF
    display(game.step(game.RUN))        #跑步后
    display(game.step(game.SKILL))      #技能描述文本
    display(game.get_current_state())   #技能发动后
    time.sleep(1)                       #延时
