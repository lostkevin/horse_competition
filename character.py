
from skills import *
import random
import json
import copy

class Character:
    START_POS = 1
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

        self.sleep = False
        self.speed = 1

        self.pos = self.START_POS

        self.buffs = []


    def move(self, step):
        self.pos = max(self.START_POS, self.pos + step)

    def add_buff(self,buff):
        self.buffs.append(buff)

    def use_skill(self, players):
        reply = 'zZZ...'
        if not self.sleep:
            reply = '未发动技能'
            p = random.random()
            tp = 0
            for skill in self.skills:
                tp += skill.prob
                if tp >= p:
                    skill.effect(players)
                    reply = skill.get_description()
                    break
        return reply

    def flush_buff(self):
        #recover status
        self.sleep = False
        self.speed = 1

        remain_buff = []
        for buff in self.buffs:
            buff.effect(self)
            buff.persist_turn -= 1
        self.buffs = list(filter(lambda buff: buff.persist_turn > 0, self.buffs))

    def run(self, other):
        if not self.sleep:
            self.move(self.speed)

class CharacterFactory:
    def __init__(self, dataPath):
        super().__init__()
        self._dataPath = dataPath
        with open(dataPath, 'r') as f:
            data = json.load(f)
            f.close()
        self.character_list = self.deserialize(data)

    @staticmethod
    def deserialize(data: list) -> list:
        return [Character(player['Name'], [Skill(skill_content) for skill_content in player['Skill']]) for player in data]


    def select_players(self, game_size=5, fixed_player: list = []):
        remain_character_list = list(set(copy.deepcopy(self.character_list)) - set(fixed_player))
        return fixed_player + random.sample(remain_character_list, game_size-len(fixed_player))

# def get_chara(name):
#     if name == 'kasumi':
#         kasumi_skill_1 = [PUT_ALL_BACK(step = 1),RUSH(step = 2)]
#         kasumi_skill_2 = [SET_SLEEP(persist_turn = 1)]
#         kasumi_skills = [kasumi_skill_1 , kasumi_skill_2]
#         skill_p = [0.1,0.1,1]  # last given 1 , would always use normal rush
#         desc = ['UB，冲','让其他人睡觉','None'] #最后一个是普通技能
#         kasumi = CHARACTER('kasumi',kasumi_skills,skill_p,desc)
#         return kasumi
