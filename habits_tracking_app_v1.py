from datetime import datetime

class UserAuth:
    def __init__(self):
        self.login_count = 0
        self.password_match_count = 0
        self.current_user = None

    def login_signup(self):
        print("Welcome to the Habit App Tracker\n")
        print("Please, signup or if you are already a user signin\n")
        while self.current_user is None:
            user_choice = input("For signup insert 1. If you are already a user insert 2: ")
            if user_choice == "1":
                self.signup()
            elif user_choice == "2":
                self.login()
            else:
                print("We didn't get a correct answer. Please, try again")

    def signup(self):
        self.new_username = input("Please, enter your username: ")
        new_user_password_1 = input("Please, enter your password: ")
        new_user_password_2 = input("Please, enter your password again: ")
        if new_user_password_1 == new_user_password_2:
            self.new_user_password = new_user_password_1
            self.current_user = self.new_username
            print(f"Correct pin and password. Welcome to the Habit App, {self.new_username}")
        else:
            self.password_match_count += 1
            if self.password_match_count == 3:
                print("Sorry! You exceeded your available attempts. Please, try again later")
                exit()
            print("Passwords didn't match. Please, reenter your password again")
            self.signup()

    def login(self):
        while self.login_count < 3 and self.current_user is None:
            print("Please, enter your login information")
            username = input("Please, enter your username: ")
            password = input("Please, enter your password: ")

            if username == "mohamed_elzeini" and password == "1234":
                self.current_user = username
                print(f"Welcome, {username} to the Habit App")
                return True
            else:
                self.login_count += 1
                if self.login_count == 3:
                    print("Sorry! You exceeded your available attempts. Please, try again later")
                    exit()
                print("Sorry! Wrong entered information. Please try again!")
        return False

class Habits:
    def __init__(self):
        self.auth = UserAuth()
        self.habits = []
        self.auth.login_signup()
        if self.auth.current_user:
            self.user_options()

    def user_options(self):
        while True:
            print("\n--- User Options ---")
            print("1. Add New Habit")
            print("2. Show Existing Habits")
            print("3. Edit Existing Habit")
            print("4. Habit Analysis")
            print("5. Check Off Habit")
            print("6. Show Streak")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_habit()
            elif choice == "2":
                self.show_habits()
            elif choice == "3":
                self.edit_habit()
            elif choice == "4":
                self.analyze_habits()
            elif choice == "5":
                self.check_off_habit()
            elif choice == "6":
                self.streak()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_habit(self):
        if not self.auth.current_user:
            print("You need to login first.")
            return
        habit_name = input("Enter the name of the habit: ")
        periodicity = int(input("Enter the periodicity of the habit (in days): "))
        specification = input("Enter the specifications for the habit (e.g., 30 minutes, 5 times a week): ")
        habit = {
            'name': habit_name,
            'periodicity': periodicity,
            'specification': specification,
            'completed_dates': [],
            'current_streak': 0,
            'longest_streak': 0,
            'user': self.auth.current_user
        }
        self.habits.append(habit)
        print(f"Habit '{habit_name}' added for user {self.auth.current_user}.")

    def show_habits(self):
        if not self.auth.current_user:
            print("You need to login first.")
            return
        print(f"Habits for user {self.auth.current_user}:")
        user_habits = [habit for habit in self.habits if habit['user'] == self.auth.current_user]
        if not user_habits:
            print("No habits found.")
            return
        for idx, habit in enumerate(user_habits, start=1):
            print(f"{idx}. {habit['name']} (every {habit['periodicity']} days)")
            print(f"   Specification: {habit['specification']}")
            print(f"   Completed Dates: {', '.join(habit['completed_dates'])}")
            print(f"   Current Streak: {habit['current_streak']} days")
            print(f"   Longest Streak: {habit['longest_streak']} days")

    def edit_habit(self):
        if not self.auth.current_user:
            print("You need to login first.")
            return
        self.show_habits()
        try:
            habit_number = int(input("Enter the number of the habit you want to edit or remove: ")) - 1
            user_habits = [habit for habit in self.habits if habit['user'] == self.auth.current_user]
            if habit_number < 0 or habit_number >= len(user_habits):
                print("Invalid habit number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        habit = user_habits[habit_number]
        print("1. Edit Habit")
        print("2. Remove Habit")
        edit_choice = input("Enter your choice: ")

        if edit_choice == "1":
            print("Enter new values (leave blank to keep current value):")
            new_name = input(f"Name ({habit['name']}): ")
            new_periodicity = input(f"Periodicity ({habit['periodicity']}): ")
            new_specification = input(f"Specification ({habit['specification']}): ")

            habit['name'] = new_name if new_name else habit['name']
            habit['periodicity'] = int(new_periodicity) if new_periodicity else habit['periodicity']
            habit['specification'] = new_specification if new_specification else habit['specification']
            print("Habit updated successfully.")
        elif edit_choice == "2":
            confirm = input("Are you sure you want to remove this habit? (yes/no): ").lower()
            if confirm == "yes":
                self.habits.remove(habit)
                print("Habit removed successfully.")
            else:
                print("Removal canceled.")
        else:
            print("Invalid choice.")

    def check_off_habit(self):
        if not self.auth.current_user:
            print("You need to login first.")
            return
        self.show_habits()
        try:
            habit_number = int(input("Enter the number of the habit you want to check off: ")) - 1
            user_habits = [habit for habit in self.habits if habit['user'] == self.auth.current_user]
            if habit_number < 0 or habit_number >= len(user_habits):
                print("Invalid habit number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        habit = user_habits[habit_number]
        today = datetime.today().strftime('%Y-%m-%d')
        if today in habit['completed_dates']:
            print(f"Habit '{habit['name']}' is already checked off for today.")
        else:
            habit['completed_dates'].append(today)
            habit['completed_dates'].sort()  # Ensure dates are sorted
            self.update_streak(habit)
            print(f"Habit '{habit['name']}' checked off for today.")

    def update_streak(self, habit):
        if not habit['completed_dates']:
            habit['current_streak'] = 0
            return

        streak = 1
        longest_streak = habit['longest_streak']
        previous_date = datetime.strptime(habit['completed_dates'][0], '%Y-%m-%d')

        for date_str in habit['completed_dates'][1:]:
            current_date = datetime.strptime(date_str, '%Y-%m-%d')
            if (current_date - previous_date).days <= habit['periodicity']:
                streak += 1
            else:
                streak = 1
            if streak > longest_streak:
                longest_streak = streak
            previous_date = current_date

        habit['current_streak'] = streak
        habit['longest_streak'] = longest_streak

    def streak(self):
        if not self.auth.current_user:
            print("You need to login first.")
            return
        self.show_habits()

        habit_name = input("Enter the name of the habit to check streak: ")
        habit = next((h for h in self.habits if h['name'] == habit_name and h['user'] == self.auth.current_user), None)
        if not habit:
            print("Habit not found.")
            return

        print(f"Current streak for habit '{habit_name}': {habit['current_streak']} days")
        print(f"Longest streak for habit '{habit_name}': {habit['longest_streak']} days")

    def analyze_habits(self):
        if not self.auth.current_user:
            print("You need to login first.")
            return
        self.show_habits()

        # Implement additional analysis functionalities here, like broken habits, check-offs, etc.


# Create an instance of the Habits class
habits_app = Habits()
