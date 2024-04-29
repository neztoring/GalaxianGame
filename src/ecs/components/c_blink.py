

class CBlink:
    def __init__(self, blink_rate:str)->None:
        self.blink_rate = blink_rate
        self.visible = True
        self.timer = 0