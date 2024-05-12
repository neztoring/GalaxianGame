from typing import List


class CAnimation:
    def __init__(self, animations: dict, is_finite: bool = False, entity: int = None) -> None:
        self.number_frames = animations["number_frames"]
        self.animation_list:List[AnimationData] = []
        for anim in animations["list"]:
            anim_data = AnimationData(anim["name"],anim["start"],anim["end"],anim["framerate"])
            self.animation_list.append(anim_data)
        self.curr_anim = 0
        self.current_animation_time = 0
        self.curr_frame = self.animation_list[self.curr_anim].start
        self.is_finite = is_finite
        self.entity = entity
            
class AnimationData:
    def __init__(self, name:str, start:int, end:int, framerate:float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate