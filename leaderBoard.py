from score import Score


class LeaderBoard:
    def __init__(self):
        self.Scores = [Score() for i in range(10)]

    def register(self, score):
        for i, v in enumerate(self.Scores):
            if score.Points >= v.Points:
                self.Scores.insert(i, score)
                self.Scores.pop()
                break
