import random
import time

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

is_playing = True
is_player_turn = True

# Stats
rounds_played = 0
highest_won_bet = 0
highest_lost_bet = 0
blackjacks = 0


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


class Hand:
    def __init__(self) -> None:
        self.cards = []
        self.value = 0
        self.aces = 0

    def __str__(self) -> str:
        cards_str = ''
        for card in self.cards:
            cards_str += f'\n{card}'

        hand_str = f'Hand has: {cards_str} \n-> Total value: {self.value}'

        return hand_str

    def add_card(self, card) -> None:
        self.cards.append(card)
        self.value += VALUES[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chip:
    def __init__(self) -> None:
        self.total = 100
        self.bet = 0

    def __str__(self) -> str:
        return f'Total chips: {self.total}'

    def add_bet(self, bet) -> None:
        self.bet += bet

    def remove_bet(self) -> None:
        self.bet = 0

    def win_bet(self) -> None:
        global highest_won_bet

        if self.bet > highest_won_bet:
            highest_won_bet = self.bet

        self.total += self.bet
        self.bet = 0

    def lose_bet(self) -> None:

        global highest_lost_bet

        if self.bet > highest_lost_bet:
            highest_lost_bet = self.bet

        self.total -= self.bet
        self.bet = 0


def take_bet(chip):
    while True:
        try:
            bet_value = int(
                input(f'How many chips would you like to bet? (1-{chip.total}): '))
        except ValueError:
            print('Sorry, a bet must be a valid number!')
        else:
            if bet_value <= 0:
                print('Sorry, a bet must be greater than 0!')
            elif bet_value > chip.total:
                print(f"Sorry, your bet can't exceed {chip.total}")
            else:
                chip.add_bet(bet_value)
                break


def hit(deck, hand):
    # Add delay
    print('Dealing card...')
    time.sleep(2)

    hand.add_card(deck.deal())


def hit_or_stand(deck, hand):
    global is_player_turn

    while True:
        x = input('Hit or Stand? Enter h or s: ')

        if(x[0].lower() == 'h'):
            hit(deck, hand)

        elif(x[0].lower() == 's'):
            print('--------------------------------------')
            print('Player stands. Dealer is playing.')
            print('--------------------------------------')
            is_player_turn = False
        else:
            print('Sorry, please try again.')
            continue
        break


def show_cards(player_hand, dealer_hand):
    global is_player_turn

    if is_player_turn == True:
        # Show one card of dealer if it's not player's turn
        print("\nDealer's Hand:")
        for i, card in enumerate(dealer_hand.cards):
            if i == 0:
                print(card)
            else:
                print('Hidden card')
    else:
        # Show all cards of dealer
        print(f"\nDealer's {dealer_hand}")

    # Show all cards of player
    print(f"\nPlayer's {player_hand}")

    print('\n')


def end_round(result, player_chip):
    global is_playing

    bet = player_chip.bet
    bet_result = 'TIED'

    if result == 'Player busts' or result == 'Dealer wins' or result == 'BLACKJACK! Dealer wins!':
        player_chip.lose_bet()
        bet_result = 'LOST'
    elif result == 'Player wins' or result == 'Dealer busts' or result == 'BLACKJACK! Player wins!':
        player_chip.win_bet()
        bet_result = 'WON'
    else:
        print("It's a tie!")
        player_chip.remove_bet()

    is_playing = False

    result_str = ''
    if bet_result == 'WON':
        result_str = f'(+{bet})'
    elif bet_result == 'LOST':
        result_str = f'(-{bet})'

    print('======================================')
    print(result)
    print(
        f'Player total chips: {player_chip.total} {result_str}')
    print('======================================')

    coninue_game(player_chip)


def coninue_game(player_chip):

    if player_chip.total <= 0:
        return end_game(player_chip)

    while True:
        x = input('\nWould you like to play another round? Enter y or n: ')

        if(x[0].lower() == 'y'):
            start_round(player_chip)
        elif(x[0].lower() == 'n'):
            end_game(player_chip)
        else:
            print('Sorry, please try again.')
            continue
        break


def end_game(player_chip):
    global rounds_played
    global blackjacks
    global highest_won_bet
    global highest_lost_bet

    print('**************************************')
    print('Thanks for playing!')
    print('---------------------')
    print(f'Player total chips: {player_chip.total}')
    print(f'Total rounds played: {rounds_played}')
    print(f'Number of Blackjacks: {blackjacks}')
    print(f"Highest won bet: {highest_won_bet} chips")
    print(f"Highest lost bet: {highest_lost_bet} chips")
    print('**************************************')
    exit()


def start_round(player_chip):
    global is_playing
    global is_player_turn
    global rounds_played
    global blackjacks

    print("Now starting a new round...")
    rounds_played += 1

    is_playing = True
    is_player_turn = True

    deck = Deck()
    deck.shuffle()

    # Initialize player's hand
    player_hand = Hand()
    # Initialize dealer's hand
    dealer_hand = Hand()

    # Take bet
    take_bet(player_chip)

    # Dealing cards to player
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Dealing cards to dealer
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Check if BLACKJACK
    if player_hand.value == 21 or dealer_hand.value == 21:
        is_player_turn = False
        show_cards(player_hand, dealer_hand)
        if(player_hand.value == 21):
            blackjacks += 1
            end_round('BLACKJACK! Player wins!', player_chip)
        else:
            end_round('BLACKJACK! Dealer wins!', player_chip)

    while is_player_turn:
        if player_hand.value < 21:
            # Show cards
            show_cards(player_hand, dealer_hand)
            # Prompt player to hit or stand
            hit_or_stand(deck, player_hand)

        # Check if player busts
        if player_hand.value > 21:
            # Show cards before ending round
            show_cards(player_hand, dealer_hand)

            end_round('Player busts', player_chip)
            break

    if is_playing:
        while dealer_hand.value < player_hand.value:
            # Show cards
            show_cards(player_hand, dealer_hand)

            # Dealer hits
            hit(deck, dealer_hand)

        # Show cards before ending round
        show_cards(player_hand, dealer_hand)
        if dealer_hand.value > 21:
            end_round('Dealer busts', player_chip)
        elif dealer_hand.value > player_hand.value:
            end_round('Dealer wins', player_chip)
        else:
            end_round("It's a tie!", player_chip)


def start_game():
    print('**************************************')
    print('Welcome to Blackjack!')
    print('**************************************')

    player_chip = Chip()

    start_round(player_chip)


start_game()
