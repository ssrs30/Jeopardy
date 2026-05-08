import random
import pygame

class AIPlayer:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.is_ai = True
        self.score = 0
        self.locked_out = False  # 如果答错了，这道题就不能再抢了
        
        # 这些是每次出题时用来记录当前这题状态的变量
        self.target_time = 0         # 预计在哪个时间点抢答 (毫秒)
        self.will_answer = None      # 预先决定好的要选的选项内容
        self.is_ready_to_answer = False # 是否处于等待抢答状态

    def prepare_choice(self, correct_option_index, options, current_time):
      
        self.locked_out = False
        self.is_ready_to_answer = True

        if self.difficulty == 1:
            accuracy = 0.3
            time_start, time_end = 2, 4
        elif self.difficulty == 2:
            accuracy = 0.5
            time_start, time_end = 5, 8
        else:
            accuracy = 0.7
            time_start, time_end = 7, 9
            
        # 2. 计算出具体会在几毫秒后抢答
        delay_seconds = random.uniform(time_start, time_end)
        self.target_time = current_time + int(delay_seconds * 1000)

        if random.random() < accuracy:
            # 命中正确选项
            self.will_answer = options[correct_option_index]
        else:
            wrong_options = [opt for i, opt in enumerate(options) if i != correct_option_index]
            self.will_answer = random.choice(wrong_options)

    def check_time_and_answer(self, current_time):
        """
        在 Pygame 的主循环里不断调用，检查 AI 到没到设定的抢答时间
        """
        if self.is_ready_to_answer and not self.locked_out:
            if current_time >= self.target_time:
                self.is_ready_to_answer = False # 动作执行完毕，取消就绪状态
                return self.will_answer # 返回它之前准备好的答案
        return None