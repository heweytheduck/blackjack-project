import asyncio
import random
from deck import Deck

# Helper function to display hands
def show_hand(name, hand, deck, hide_second_card=False):
    if hide_second_card:
        display_cards = [f"{hand[0][0]}{hand[0][1]}", "??"]
        return f"{name}: {' '.join(display_cards)}"
    else:
        cards_str = ' '.join([f"{r}{s}" for r, s in hand])
        return f"{name}: {cards_str} (Value: {deck.calculate_hand_value(hand)})"

# Player coroutine
async def player(name, hand, deck, decision_func):
    while True:
        print(show_hand(name, hand, deck))
        if deck.calculate_hand_value(hand) >= 21:
            break
        move = await decision_func(hand)
        if move == 'hit':
            hand.append(deck.draw())
        else:
            break
    return hand

# Dealer coroutine
async def dealer(hand, deck):
    while deck.calculate_hand_value(hand) < 17:
        await asyncio.sleep(1)
        print("Dealer hits.")
        hand.append(deck.draw())
        print(show_hand("Dealer", hand, deck))
    return hand

# User decision coroutine
async def user_decision_func(hand):
    while True:
        move = input("Hit or stand? ").strip().lower()
        if move in ('hit', 'stand'):
            return move
        print("Invalid choice. Please type 'hit' or 'stand'.")

# Full game coroutine
async def game():
    deck = Deck()

    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    # Show initial hands
    print(show_hand("Dealer", dealer_hand, deck, hide_second_card=True))
    print(show_hand("Player", player_hand, deck))

    # Check for blackjack
    if deck.is_blackjack(player_hand):
        if deck.is_blackjack(dealer_hand):
            print("\nBoth have Blackjack! Tie!")
        else:
            print("\nPlayer has Blackjack! Player wins!")
        return
    elif deck.is_blackjack(dealer_hand):
        print(show_hand("Dealer", dealer_hand, deck))
        print("\nDealer has Blackjack! Dealer wins!")
        return

    # Player turn
    final_player_hand = await player("Player", player_hand, deck, user_decision_func)
    final_player_score = deck.calculate_hand_value(final_player_hand)

    if final_player_score > 21:
        print("Player busts! Dealer wins.")
        return

    # Dealer turn
    print("\nDealer's turn:")
    print(show_hand("Dealer", dealer_hand, deck))
    final_dealer_hand = await dealer(dealer_hand, deck)
    final_dealer_score = deck.calculate_hand_value(final_dealer_hand)

    # Show results
    print("\nFinal Hands:")
    print(show_hand("Player", final_player_hand, deck))
    print(show_hand("Dealer", final_dealer_hand, deck))

    if final_dealer_score > 21 or final_player_score > final_dealer_score:
        print("Player wins!")
    elif final_player_score < final_dealer_score:
        print("Dealer wins!")
    else:
        print("Tie!")

# Run game
asyncio.run(game())

