import random

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:
    def __init__(self, suit, rank) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self) -> None:
        self.cards = []
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(suit, rank))

    def __str__(self) -> str:
        deck_str = f'Deck has {len(self.cards)} cards'
        for card in self.cards:
            deck_str += f'\n{card}'
        return deck_str

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()


deck = Deck()
deck.shuffle()

print(deck)
