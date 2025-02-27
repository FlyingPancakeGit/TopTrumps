import random

class Computer:
    def __init__(self, name):
        self.name = name

        self.deck = []
        self.current_index = 0

    def add_card(self, card):
        self.deck.append(card)

    def select_stat(self, card, valid_stats):
        computer_choice = random.choice(valid_stats)
        return getattr(card, computer_choice)


class User:
    def __init__(self, name):
        self.name = name

        self.deck = []
        self.current_index = 0

    def increment_index(self):
        if self.current_index < len(self.deck) - 1:
            self.current_index += 1
        else:
            self.current_index = 0

    def add_card(self, card):
        self.deck.append(card)

    def display_stats(self):
        print(f'Card Count: {len(self.deck)}')

    def display_card(self, card):
        print(f'''
----------------
Name: {card.name}
Owner(s): {card.owners}

Size: {card.size}
Speed: {card.speed}
Firepower: {card.firepower}
Maneuvering: {card.maneuvering}
Force Factor: {card.forcefactor}
----------------''')

    def display(self, card):
        self.display_stats()
        self.display_card(card)

    def select_stat(self, card, valid_stats):
        user_choice_valid = False
        user_choice = None

        while not user_choice_valid:
            user_choice = input("\nSelect your stat: ").lower().replace(' ', '')
            if user_choice in valid_stats:
                user_choice_valid = True
            else:
                print('\nInvalid choice.')
        
        return getattr(card, user_choice)

