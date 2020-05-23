import random
import buffs
import copy
class Skill:
    def __init__(self, owner, skill_content):
        self.skill_name = skill_content['Name']
        self.description = skill_content['Description']
        self.prob = skill_content['Prob']
        self.action_seq = self.make_action_seq(skill_content['ActionSequence'])


    def effect(self, owner, players):
        for action in self.action_seq:
            action(owner, players)

    @staticmethod
    def make_action_seq(action_seq):
        def choice_recipient(owner, players, target_configs):
            targets = copy.deepcopy(players)
            if target_configs[0] == 'ALL':
                return targets
            elif target_configs[0] == 'RANDOM':
                targets.remove(owner)
                return random.sample((targets, min(len(targets), target_configs[1])))
            elif target_configs[0] == 'ID':
                return [players[i - 1] for i in target_configs[1:] if i <= len(players)]
            elif target_configs[0] == 'RANK':
                targets.sort(key=lambda x: x.pos, reversed=True)
                return [targets[i - 1] for i in target_configs[1:] if i <= len(targets)]
        actions = []
        # 对于施术对象, 有以下格式
        # Configs['Target'] = ['ALL'], 对除自身外所有人使用
        # Configs['Target'] = ['RANDOM', k], 对除自身外随机K人使用
        # Configs['Target'] = ['ID', 1, 2, 5] 指定赛道, 对第1, 2, 5号使用, 若参赛选手不足会忽略超出的编号
        # Configs['Target'] = ['RANK', 1, 2, 5] 指定名次, 对某几名使用
        for action in action_seq:
            def func(owner, players):
                for target in choice_recipient(owner, players, action['Configs']['Target']):
                    if action['Type'] == 'position':
                        pass
                    elif action['Type'] == 'buff':
                        pass
            actions.append(func)
        return actions


# class RUSH(SKILL):
#     def __init__(self,name="",describe= "",step = 1):
#         super().__init__(name,describe)
#         self.step = step

#     def effect(self,owner,others):
#         owner.go_ahead(self.step)

# class PUT_ALL_BACK(SKILL):
#     def __init__(self,name="",describe= "",step = 1):
#         super().__init__(name,describe)
#         self.step = step

#     def effect(self,owner,others):
#         for c in others:
#             c.go_back(self.step)

# class PUT_SOMEONE_BACK(SKILL):
#     def __init__(self,name="",describe= "",step = 1,select = 'random'):
#         super().__init__(name,describe)
#         self.step = step
#         self.select = select

#     def effect(self,owner,others):
#         if self.select == 'random':
#             c = random.choice(others)
#         else:
#             c = get_first(others)
#         c.go_back(self.step)

# class SET_SLEEP(SKILL):
#     def __init__(self,name="",describe= "",persist_turn=1):
#         super().__init__(name,describe)
#         self.persist_turn = persist_turn
#     def effect(self,owner,others):
#         for c in others:
#             c.add_buff(buffs.BUFF_SLEEP(persist_turn=self.persist_turn))
