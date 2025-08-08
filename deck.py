import asyncio
import random

class Deck:
    # Create and shuffle the deck(s)
    def __init__(self, num_decks=1):
        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.values = {**{str(n): n for n in range(2, 11)},
                       'J': 10, 'Q': 10, 'K': 10, 'A': 11}

        self.cards = [(rank, suit) for suit in self.suits for rank in self.ranks] * num_decks
        self.shuffle()

    # Shuffle function
    def shuffle(self):
        random.shuffle(self.cards)

    # Draw function
    def draw(self):
        return self.cards.pop()
    
    # Calculate hand value function
    def calculate_hand_value(self, hand):
        value = sum(self.values[card[0]] for card in hand)
        aces = sum(1 for card in hand if card[0] == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    
    # Check for blackjack
    def is_blackjack(self, hand):
        return self.calculate_hand_value(hand) == 21 and len(hand) == 2

    def __len__(self):
        return len(self.cards)