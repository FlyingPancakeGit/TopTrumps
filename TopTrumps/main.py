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
        self.display_stats = []
        self.stat_dict = {}

        self.computer_names = ['Alfie', 'Ben', 'Charlie']
        self.computer = None
        self.user = None

        self.current_chooser = 'user'
        self.winner = None

    def clean_stat(self, stat):
        return stat.lower().replace(' ', '')

    def generate_players(self):
        computer_name = random.choice(self.computer_names)
        self.computer = Computer(computer_name)

        print('\n' * 32)
        user_name = input('\nEnter your name: ')

        self.user = User(user_name)

    def load_deck(self):
        with open('deck.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            stats = reader.__next__()[2:]

            self.valid_stats = list(map(self.clean_stat, stats))
            self.display_stats = list(stats)
            self.stat_dict = dict(zip(self.valid_stats, self.display_stats))

            for row in reader:
                card = Card(*row)
                self.deck.append(card)

    def deal_cards(self):
        deck_size = len(self.deck)

        for i in range(int(deck_size / 2)):
            index = random.randint(0, len(self.deck) - 1)
            card = self.deck[index]
            self.computer.add_card(card)
            self.deck.pop(index)

        for i in range(int(deck_size / 2)):
            index = random.randint(0, len(self.deck) - 1)
            card = self.deck[index]
            self.user.add_card(card)
            self.deck.pop(index)

    def transfer_card(self, user_stat, computer_stat):
        print('\n' * 32)
        if user_stat > computer_stat:
            print(f'{self.user.name} wins!')
            self.user.deck.append(self.computer.deck[self.computer.current_index])
            self.computer.deck.remove(self.computer.deck[self.computer.current_index])
            self.current_chooser = 'user'
        elif user_stat < computer_stat:
            print(f'{self.computer.name} wins!')
            self.computer.deck.append(self.user.deck[self.user.current_index])
            self.user.deck.remove(self.user.deck[self.user.current_index])
            self.current_chooser = 'computer'
        else:
            print('Insert draw logic here.')

    def check_for_win(self):
        if len(self.user.deck) == 0 or len(self.computer.deck) == 0:
            return True
        else:
            return False

    def display_game_over(self, user, computer):
        print('\n' * 32)
        print('Game over!')
        if len(user.deck) == 0:
            print(f'{user.name} lost.')
        else:
            print(f'{user.name} wins!')

    def game_setup(self):
        self.load_deck()
        self.generate_players()
        self.deal_cards()

    def game_loop(self):
        while self.running:
            print('\n' * 32)

            user_stat = None
            computer_stat = None
            
            if self.current_chooser == 'user':
                current_card = self.user.deck[self.user.current_index]
                self.user.display(current_card)
                user_stat_name = self.user.select_stat(current_card, self.valid_stats)
                user_stat = getattr(current_card, user_stat_name)

                current_card = self.computer.deck[self.computer.current_index]
                computer_stat = getattr(current_card, user_stat_name)

                self.current_chooser = self.computer
            elif self.current_chooser == 'computer':
                current_card = self.computer.deck[self.computer.current_index]
                computer_stat_name = self.computer.select_stat(current_card, self.valid_stats)
                computer_stat = getattr(current_card, computer_stat_name)

                current_card = self.user.deck[self.user.current_index]
                user_stat = getattr(current_card, user_stat_name)

                print(f'{self.computer.name} chose {self.stat_dict[computer_stat_name]}.')
                input('\nEnter to continue: ')
            else:
                print('Error.')

            self.transfer_card(user_stat, computer_stat)
            input('\nEnter to continue: ')

            if self.check_for_win():
                self.running = False

            self.user.current_index += 1
            self.computer.current_index += 1

    def play(self):
        self.game_setup()
        self.game_loop()


if __name__ == "__main__":
    main = Main()
