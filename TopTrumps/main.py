import random
import csv

from players import *
from card import Card


class Main:
    def __init__(self):
        self.menu = Menu()
        self.menu.menu_loop()


class Menu:
    def __init__(self):
        self.game = Game()

    def display_menu(self):
        print('Welcome to Top Trumps!\n\nOptions:'
              '\n\t1: Play Game'
              '\n\t2: Quit')

    def get_input(self):
        user_choice = None
        user_choice_valid = False

        while not user_choice_valid:
            user_choice = input('\nEnter your choice: ')
            if user_choice.isnumeric() and int(user_choice) in range(1, 3):
                user_choice_valid = True
            else:
                print('\nInvalid input. Try again.')

        return user_choice

    def check_input(self, input):
        if input == '1':
            self.game.play()
        elif input == '2':
            exit()

    def menu_loop(self):
        while True:
            self.display_menu()

            user_choice = self.get_input()
            self.check_input(user_choice)


class Game:
    def __init__(self):
        self.running = True

        self.deck = []
        self.valid_stats = []

        self.computer_names = ['Alfie', 'Ben', 'Charlie']
        self.players = []
        self.winner = None

    def clean_stat(self, stat):
        return stat.lower().replace(' ', '')

    def generate_players(self):
        computer_name = random.choice(self.computer_names)
        computer = Computer(computer_name)
        self.players.append(computer)

        print('\n' * 32)
        user_name = input('\nEnter your name: ')

        user = User(user_name)
        self.players.append(user)

    def load_deck(self):
        with open('deck.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)

            self.valid_stats = list(map(self.clean_stat, reader.__next__()[2:]))

            for row in reader:
                card = Card(*row)
                self.deck.append(card)

    def deal_cards(self):
        deck_size = len(self.deck)

        for i in range(int(deck_size / 2)):
            index = random.randint(0, len(self.deck) - 1)
            card = self.deck[index]
            self.players[0].add_card(card)
            self.deck.pop(index)

        for i in range(int(deck_size / 2)):
            index = random.randint(0, len(self.deck) - 1)
            card = self.deck[index]
            self.players[1].add_card(card)
            self.deck.pop(index)

    def transfer_card(self, user, computer, user_stat, computer_stat):
        print('\n' * 32)
        if user_stat > computer_stat:
            print(f'{user.name} wins!')
            user.deck.append(computer.deck[computer.current_index])
            computer.deck.remove(computer.deck[computer.current_index])
        elif user_stat < computer_stat:
            print(f'{computer.name} wins!')
            computer.deck.append(user.deck[user.current_index])
            user.deck.remove(user.deck[user.current_index])
        else:
            print('Insert draw logic here.')

    def check_for_win(self, user, computer):
        if len(user.deck) == 0 or len(computer.deck) == 0:
            return True
        else:
            return False

    def display_game_over(self, user, computer):
        print('\n' * 32)
        print('Game over!')
        if len(user.deck) == 0:
            print(f'{user.name} lost.')
        else:
            print(f'{computer.name} wins!')

    def game_setup(self):
        self.load_deck()
        self.generate_players()
        self.deal_cards()

    def game_loop(self):
        computer = self.players[0]
        user = self.players[1]

        while self.running:
            print('\n' * 32)

            current_card = user.deck[user.current_index]
            user.display(current_card)
            user_stat_name = user.select_stat(current_card, self.valid_stats)
            user_stat = getattr(current_card, user_stat_name)

            current_card = computer.deck[computer.current_index]
            computer_stat = getattr(current_card, user_stat_name)


            self.transfer_card(user, computer, user_stat, computer_stat)
            print(user_stat, computer_stat)
            input('\nEnter to continue: ')

            if self.check_for_win(user, computer):
                self.running = False

            user.current_index += 1
            computer.current_index += 1

    def play(self):
        self.game_setup()
        self.game_loop()


if __name__ == "__main__":
    main = Main()
