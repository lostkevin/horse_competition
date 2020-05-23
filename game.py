class Game:
    RUN = True
    SKILL = False

    def __init__(self, players, console=True, game_length=20):
        super().__init__()
        self.players = players
        self.console_mode = True
        self.game_length = 20

    @property
    def is_terminal(self):
        #检查第一名是否到达终点
        return max(self.players, key=lambda player: player.pos).pos >= self.game_length

    def step(self, run_step):
        if run_step:
            for player in self.players:
                player.run()
            return '第{}轮跑步后\n' + self.get_current_state()
        skill_results = [player.use_skill() for player in self.players]
        return skill_results

    def flush_players_buff(self):
        for player in self.players:
            player.flush_buff()

    def get_current_state(self):
        if self.console_mode:
            return self._plain_text_output()
        # 高级输出,暂时用不到
        pass

    def _plain_text_output(self):
        # 文本输出, console模式
        def make_single_line(player):
            progress = ''
            # 人物初始pos为1
            pos = self.game_length - min(player.pos, self.game_length ) #[0, 19]
            for i in range(0, self.game_length):
                progress += player.icon if pos == i else '='
            return progress
        return '\n'.join([make_single_line(player) for player in self.players])
