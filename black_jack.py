# THIS IS A PLAYER VS DEALER CARD GAME

import random
import sys

suits = ('Hearts','Diamonds','Clubs','Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}


playing = True

# Card class
class Card:

    def __init__(self,suit,rank):
        
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    
    def __str__(self):
        return self.rank + " of " + self.suit

# Deck class
class Deck:

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                # CREATE THE CARD OBJECT 
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.deck)
   
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += card.__str__()
        

    def deal(self):

        single_card = self.deck.pop()
        return single_card
        


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0     

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21:
            self.value -= 10
            self.aces -= 1
          

class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet



# FUNCTIONS

# TAKING BETS
def take_bet(chips):

    print(f"\nYour current Balance is: {chips.total.__str__()}\n")
    
    while True:
        try: 

            bet = int(input("Please enter the amount you would like to bet... "))

            if bet == 0:
                print("You cannot bet nothing Brother")
                continue
            elif bet < 0:
                print("My Brother you cannot bet a negative amount")
                continue
            else:
                chips.bet = bet
        
        except ValueError:
            print("Sorry the amount must be an integer")
        else: 
            if chips.bet > chips.total:
                print("Insufficient funds, avaliable balance: " + chips.total.__str__())
            else:
                break


# TAKING HITS
def hit(deck,hand):
    
    temp_card = deck.deal()
    hand.add_card(temp_card)
    
    if temp_card.rank == 'Ace':
        hand.adjust_for_ace()

    


# PROMPTING PLAYER HIT OR STAND
def hit_or_stand(deck,hand):
   
    global playing
    
    while True:
        x = input("Would you like to Hit or Stand?  Enter 'h' or 's' ")
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player is standing. Dealer is playing ")
            playing = False
        else:
            print("Sorry please try again")
            continue
        break
        

# TO DISPLAY CARDS
def show_some(player,dealer):
    print("\nDealer's hand:")
    print("<Hidden Card>")
    print('' + dealer.cards[1].__str__())
    print("\nPlayer's hand: ", *player.cards, sep='\n')

def show_all(player,dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n')
    print("Dealer's hand= ", dealer.value)
    print("\nPlayer's hand: ", *player.cards, sep='\n')
    print("Player's hand= ", player.value)

# HANGLE END GAME 

def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


# GAME LOGIC 
player_chips = Chips() 

while True:

    print('\nWelcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until he reaches 17. Aces count as 1 or 11.')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    

    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)


    while playing:

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand) 
        
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)  
        print()
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_chips)
            break   
        
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif player_hand.value > 21:
            player_busts(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        

        else:
            push(player_hand,dealer_hand)        
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)

    if player_chips.total <= 0:
        print("You lost all your money to a computer, broke ass \n")
        new_game = input("Would you like to restart the game? Enter 'y' or any other key to exit the application ")
        
        if new_game[0].lower()=='y':
            playing=True
            player_chips = Chips()
            continue
        else:
            print("Thanks for playing!")
            sys.exit()
    
    else: # Ask to play again
        new_game = input("Would you like to play another hand? Enter 'y' or any other key to exit the application ")
    
        if new_game[0].lower()=='y':
            playing=True
            continue
        else:
            print("Thanks for playing!")
            break      
            
        




        









    