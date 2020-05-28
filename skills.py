import random
import buffs
import copy

class Skill:
    def __init__(self, owner, skill_content):
        self.skill_name = skill_content['Name']
        self.description = skill_content['Description']
        self.prob = skill_content['Prob']
        self.action = self.make_action_seq(skill_content['ActionSequence'])


    def effect(self, owner, players):
        for action in self.action_seq:
            action(owner, players)
        self.actions = list(filter(lambda x: hasattr(x, 'persist_turn') and x.persist_turn > 0, self.buffs))

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
            elif target_configs[0] == 'SELF':
                return [owner]
        actions = []
        # 对于施术对象, 有以下格式
        # Configs['Target'] = ['SELF'], 对自身使用
        # Configs['Target'] = ['ALL'], 对除自身外所有人使用
        # Configs['Target'] = ['RANDOM', k], 对除自身外随机K人使用
        # Configs['Target'] = ['ID', 1, 2, 5] 指定赛道, 对第1, 2, 5号使用, 若参赛选手不足会忽略超出的编号
        # Configs['Target'] = ['RANK', 1, 2, 5] 指定名次, 对某几名使用
        # 位移类技能 提供位移 Configs['Offset'] = (minspeed, maxspeed) 指定位移范围
        # Configs['Offset'] = offset 固定位移
        for action in action_seq:
            def func(owner, players):
                for target in choice_recipient(owner, players, action['Configs']['Target']):
                    if action['Type'] == 'move':
                        if type(action['Configs']['Offset']) is tuple:
                            target.move(random.randint(*action['Configs']['Offset']))
                        else: target.move(action['Configs']['Offset'])
                    elif action['Type'] == 'buff':
                        # 支持的buff有: 睡眠, 禁锢(速度为0), 加减速(速度乘以固定倍率)
                        # 睡眠: Configs['BuffDetail'] = ('Sleep', 5) 睡眠5回合
                        # 禁锢: Configs['BuffDetail'] = ('Imprison', 5) 禁锢5回合
                        # 加减速: Configs['BuffDetail'] = ('Speed', 5, k) 速度设置为k, 持续5回合, 为0时相当于禁锢
                        func.persist_turn = action['Configs'][1]
                        target.Sleep = True
                        target.Speed = 1
                        if action['Configs']['BuffDetail'][0] == 'Sleep':
                            if func.persist_turn > 0:
                                target.Sleep = True
                                func.persist_turn -= 1
                        elif action['Configs']['BuffDetail'][0] == 'Imprison':
                            if func.persist_turn > 0:
                                target.Speed = 0
                                func.persist_turn -= 1
                        elif action['Configs']['BuffDetail'][0] == 'Speed':
                            if func.persist_turn == -1:
                                target.Speed = action['Configs'][2]
                            elif func.persist_turn > 0:
                                target.Speed = action['Configs'][2]
                                func.persist_turn -= 1
            actions.append(func)
        return actions
