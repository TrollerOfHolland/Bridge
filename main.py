import random
from enum import IntEnum

SUIT_ICONS  = ["♣", "♦", "♥", "♠"]


class Suit(IntEnum):
  clubs = 0
  diamonds = 1
  hearts = 2
  spades = 3
 

class Bid:
  suit: Suit
  tricks: int

  def __init__(self, suit :Suit, tricks: int):
    self.suit = suit
    self.tricks = tricks
  
  @staticmethod
  def legal_bids(highest_bid):
    legal_bids : list[Bid] = []
    for suit in Suit:
      for i in range(highest_bid.tricks, 7):
        if(highest_bid.suit < suit or i > highest_bid.tricks):
          legal_bids.append(Bid(suit, i))
    legal_bids.sort(key=lambda bid: bid.tricks)
    return legal_bids
  
  def __repr__(self):
    return SUIT_ICONS[self.suit] + str(self.tricks)



    


class Card:
  suit : Suit
  value : int # 1 to 12

  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

class CardSet(list):

  @staticmethod
  def deck():
    deck = CardSet()
    for suit in range(4):
      for value in range(13):
        deck.append(Card(suit, value))
    return deck
  
  @staticmethod
  def deal(deck):
    hands : list[CardSet] = [CardSet() for x in range(4)]
    while(deck):
      for i in range(4):
        hands[i].append(deck.pop(random.randrange(len(deck))))
    return hands

  def show_cards(self):
    for card in self:
      match card.suit: 
        case Suit.clubs:
          print("♣" + str(card.value))
        case Suit.diamonds:
          print("♦" + str(card.value))
        case Suit.hearts:
          print("♥" + str(card.value) )
        case Suit.spades:
          print("♠" + str(card.value))
  
  def sort_hand(self):
    self.sort(key= lambda card: card.suit)


  def count(self, suit:Suit):
    return(len([card for card in self if card.suit == suit]))
  
  def __init__(self):
    return super().__init__()


class Player:
  hand: CardSet

  def __init__(self, hand: CardSet):
    self.hand = hand

  def determine_strength_points(self, suit = None, is_responder = False):
    #honours
    ace_points = len([card for card in self.hand if card.value == 12]) * 4
    king_points = len([card for card in self.hand if card.value == 11]) * 3
    queen_points = len([card for card in self.hand if card.value == 10]) * 2
    jack_points = len([card for card in self.hand if card.value == 9])
    honours_points = ace_points + king_points + queen_points + jack_points

    #length in suit
    suit_points = 0
    if(suit):
        suit_points = max(len([card for card in self.hand if card.suit == suit]) - 4, 0 )
    
    gap_points = 0
    if(is_responder and len([card for card in self.hand if card.suit == suit]) >= 4):
      for gap_suit in Suit:
        match(len([card for card in self.hand if card.suit == gap_suit])):
          case 0:
            gap_points += 5
          case 1:
            gap_points += 3
          case 2:
            gap_points += 1
    
    return gap_points + suit_points + honours_points

    



def game():
  deck = CardSet.deck()
  hands: list[CardSet] = CardSet.deal(deck)
  players = [Player(hand) for hand in hands]
  for player in players:
    player.hand.sort_hand()
    print("Strength of hand: " + str(player.determine_strength_points()))
    player.hand.show_cards()
    
bid = Bid(Suit.spades, 2)
print(Bid.legal_bids(bid))