class Computer:
    def __init__(self, name):
        self.name = name

        self.deck = []
        self.current_index = 0

    def add_card(self, card):
        self.deck.append(card)

    def select_stat(self, card):
        pass


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

    def display_card(self, card):
        print(f'''
----------------
Name: {card.name}
Owner(s): {card.owners}

Size: {card.size}
Speed: {card.speed}
Firepower: {card.fire_power}
Maneuvering: {card.maneuvering}
Force Factor: {card.force_factor}
----------------''')

    def select_stat(self, valid_stats):
        user_choice_valid = False
        user_choice = None

        while not user_choice_valid:
            user_choice = input("\nSelect your stat: ")
            if user_choice.lower().replace(' ', '') in valid_stats:
                user_choice_valid = True
            else:
                print("\nInvalid choice.")
