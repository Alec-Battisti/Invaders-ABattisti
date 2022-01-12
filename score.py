from datetime import date


class Score:
    def __init__(self):
        self.Points = 0
        self.Time = 0
        today = date.today()
        self.Date = today.strftime("%d/%m/%Y")
