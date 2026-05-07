# deck.py --> Supports Infinite Deck, Single Deck, and Shoe Deck
import random

BASE_DECK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

class Deck:
    def __init__(self, deck_type='infinite'):
        self.deck_type = deck_type
        
        if self.deck_type == 'single':
            self.__init__single_deck()

        elif self.deck_type == "shoe":
            self.__init__shoe()
    
    def __init__single_deck(self):
        self.cards = BASE_DECK * 4  # 4 suits
        random.shuffle(self.cards)
    
    def __init__shoe(self):
        num_decks = 6   # Change if desired
        self.cards = BASE_DECK * 4 * num_decks
        random.shuffle(self.cards)

    def draw(self):
        if self.deck_type == 'infinite':
            return random.choice(BASE_DECK)
        
        elif self.deck_type == 'single':
            if not self.cards:
                self.__init__single_deck()
            return self.cards.pop()
        elif self.deck_type == 'shoe':
            if not self.cards:
                self.__init__shoe()
            return self.cards.pop()
        
        else:
            raise ValueError("Invalid deck type. Use 'infinite', 'single', or 'shoe'.")
            
