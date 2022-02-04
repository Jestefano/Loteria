import numpy as np

class Playboard():
    def __init__(self, rng, num_squares, num_cards):
        self.num_squares = num_squares
        self.values = rng.choice(np.arange(num_cards),num_squares,replace=False)
        self.marked = [False for i in range(num_squares)]
    
    def winner(self):
        return sum(self.marked) == self.values.shape[0]

    def passed_mid(self):
        return sum(self.marked) >= self.values.shape[0] // 2

    def mark(self,value):
        if value in self.values:
            idx = np.argwhere(self.values == value)[0][0]
            self.marked[idx] = True
        return (self.winner(), self.passed_mid())

    def restart(self):
        self.marked = [False for i in range(self.num_squares)]

class Game():
    def __init__(self, rng, num_players = 3, num_squares = 16, num_cards = 54):
        self.num_players = num_players
        self.first_mid = []
        self.concluded = False
        self.players = [Playboard(rng, num_squares, num_cards) \
            for i in range(num_players)]
    
    def mark(self, value):
        winners = []
        temp_mid = []
        for i, player in enumerate(self.players):
            temp_winner, temp_first_mid = player.mark(value)
            if(temp_winner): winners.append(i)
            if((not self.first_mid) and temp_first_mid): temp_mid.append(i)
        
        if(not self.first_mid): self.first_mid = temp_mid
        if(not winners): self.concluded = True
        
        return winners

    def is_concluded(self):
        return self.concluded

    def get_first_mid(self):
        if(not self.is_concluded()): raise Exception ("The game is not concluded")
        return self.first_mid
    
    def restart(self):
        if(not self.is_concluded()): raise Exception ("The game is not concluded")
        self.concluded = False
        self.first_mid = []
        for player in self.players:
            player.restart()
