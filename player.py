from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self,color):
        self.color=color
        
    @abstractmethod
    def make_move(self,game):
        pass
    

class HumanPlayer(Player):
    def make_move(self,game):
        print(game.board)
        print(game.get_available_moves())
        return int(input("Choose column: "))

class RandomAI(Player):
    def make_move(self,game):
        return random.choice(game.get_available_moves())
    
class AIPlayer(Player):
    def make_move(self,game):
        return game.get_available_moves()[0]