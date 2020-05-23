
class BUFF:
    def __init__(self,name="",persist_turn=1):
        self.name = name
        self.persist_turn = persist_turn

    def effect(self,owner):
        pass


class BUFF_SLEEP(BUFF):
    def effect(self,owner):
        owner.sleep = True
