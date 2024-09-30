import random
import time
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def get_number_range():
    ranges = {
        1: (1, 9),
        2: (10, 99),
        3: (100, 999),
        4: (1000, 9999),
        5: (10000, 99999)
    }
    print(Style.BRIGHT + Fore.WHITE + "Select the range of numbers:")
    for key, value in ranges.items():
        print(Fore.YELLOW + f"{key}. {value[0]}-{value[1]}")
    while True:
        try:
            choice = int(input(Fore.MAGENTA + "Enter your choice (1-5): "))
            if 1 <= choice <= 5:
                return ranges[choice]
        except ValueError:
            pass
        print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 5.")

def get_difficulty_level():
    print(Style.BRIGHT + Fore.WHITE + "\nSelect the difficulty level:")
    print(Fore.YELLOW + "1. Only addition")
    print(Fore.YELLOW + "2. Mix of additions and subtractions")
    print(Fore.YELLOW + "3. Mostly +/-, with four × or ÷")
    while True:
        try:
            choice = int(input(Fore.MAGENTA + "Enter your choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
        except ValueError:
            pass
        print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 3.")

def get_num_questions():
    print(Style.BRIGHT + Fore.WHITE + "\nEnter the number of questions you want to answer:")
    while True:
        try:
            num_questions = int(input(Fore.MAGENTA + "Number of questions (1-100): "))
            if 1 <= num_questions <= 100:
                return num_questions
            else:
                print(Fore.YELLOW + "Please enter a number between 1 and 100.")
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a whole number.")

def get_time_interval():
    print(Style.BRIGHT + Fore.WHITE + "\nSelect the time interval between numbers:")
    print(Fore.YELLOW + "1. 1.5 seconds")
    print(Fore.YELLOW + "2. 1 second")
    print(Fore.YELLOW + "3. 0.8 seconds")
    print(Fore.YELLOW + "4. 0.5 seconds")
    print(Fore.YELLOW + "5. 0.3 seconds")
    print(Fore.YELLOW + "6. 0.2 seconds")
    while True:
        try:
            choice = int(input(Fore.MAGENTA + "Enter your choice (1-6): "))
            if 1 <= choice <= 6:
                intervals = [1.5, 1, 0.8, 0.5, 0.3, 0.2]
                return intervals[choice - 1]
        except ValueError:
            pass
        print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 6.")

def generate_question(num_range, difficulty):
    while True:
        numbers = [random.randint(num_range[0], num_range[1]) for _ in range(10)]
        operators = []
        
        if difficulty == 1:
            operators = ['+' for _ in range(9)]
        elif difficulty == 2:
            operators = [random.choice(['+', '-']) for _ in range(9)]
        else:  # difficulty == 3
            operators = ['+'] * 3 + ['-'] * 2 + ['*'] * 2 + ['/'] * 2
            random.shuffle(operators)

        question = f"{numbers[0]}"
        current_result = numbers[0]
        valid = True

        for num, op in zip(numbers[1:], operators):
            if op == '+':
                current_result += num
            elif op == '-':
                if current_result <= num:  # Ensure subtraction doesn't lead to negative
                    valid = False
                    break
                current_result -= num
            elif op == '*':
                current_result *= num
            elif op == '/':
                if current_result % num != 0:  # Ensure division results in an integer
                    valid = False
                    break
                current_result //= num

            question += f" {op} {num}"

            if current_result <= 0:  # Ensure result is always positive
                valid = False
                break

        if valid:
            return question, current_result

def flash_question(question, time_interval):
    parts = question.split()
    sys.stdout.write('\r' + ' ' * 50)  # Clear the line initially
    sys.stdout.flush()
    for i in range(0, len(parts), 2):
        if i == 0:
            display = parts[i]
        else:
            display = f"{parts[i-1]} {parts[i]}"
        sys.stdout.write('\r' + ' ' * 50)  # Clear the line
        sys.stdout.flush()
        sys.stdout.write('\r' + Fore.CYAN + display)
        sys.stdout.flush()
        time.sleep(time_interval)
    sys.stdout.write('\r' + ' ' * 50)  # Clear the line at the end
    sys.stdout.flush()
    print(Fore.YELLOW + "\nTime to answer!")

def regular_math_game():
    num_range = get_number_range()
    difficulty = get_difficulty_level()
    num_questions = get_num_questions()
    time_interval = get_time_interval()
    user_answers = []
    correct_answers = []
    questions = []
    
    print(Style.BRIGHT + Fore.WHITE + "\nWelcome to the Advanced Math Calculation Game!")
    print(Fore.YELLOW + f"You'll have {num_questions} questions. Each question involves 10 numbers.")
    print(Fore.YELLOW + "Numbers and operators will be shown one by one.")
    print(Fore.YELLOW + "Try to calculate as quickly as you can.")
    print(Fore.YELLOW + "Enter your answer after all numbers are shown.")
    input(Fore.MAGENTA + "Press Enter to start...")

    print(Fore.YELLOW + "\nPrepare yourself. The first question will appear in 3 seconds...")
    time.sleep(3)  
    
    start_time = time.time()
    
    for i in range(num_questions):
        question, correct_answer = generate_question(num_range, difficulty)
        questions.append(question)
        correct_answers.append(correct_answer)
        
        print(Style.BRIGHT + Fore.WHITE + f"\nQuestion {i+1}:")
        flash_question(question, time_interval)
        
        user_answer = input(Fore.MAGENTA + "Your answer: ")
        
        try:
            user_answer = int(user_answer)
            user_answers.append(user_answer)
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Treating as incorrect.")
            user_answers.append(None)
    
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    # Calculate score and show results
    score = sum(1 for ua, ca in zip(user_answers, correct_answers) if ua == ca)
    
    print(Style.BRIGHT + Fore.WHITE + "\n--- Game Over ---")
    print(Fore.YELLOW + f"Your score: {Style.BRIGHT + Fore.WHITE}{score}/{num_questions}")
    print(Fore.YELLOW + f"Total time: {Style.BRIGHT + Fore.WHITE}{total_time} seconds")
    print(Fore.YELLOW + f"Average time per question: {Style.BRIGHT + Fore.WHITE}{round(total_time/num_questions, 2)} seconds")
    
    print(Style.BRIGHT + Fore.WHITE + "\nDetailed Results:")
    for i, (question, user_answer, correct_answer) in enumerate(zip(questions, user_answers, correct_answers), 1):
        status = "Correct" if user_answer == correct_answer else "Incorrect"
        status_color = Fore.GREEN if status == "Correct" else Fore.RED
        print(Fore.CYAN + f"Question {i}: {question} = {correct_answer}")
        print(Fore.GREEN + f"Your answer: {user_answer}")
        print(status_color + f"Status: {status}\n")

def get_multiplication_mode():
    print(Style.BRIGHT + Fore.WHITE + "\nMultiplication Enthusiast Mode")
    print(Fore.YELLOW + "Choose the type of multiplication:")
    print(Fore.YELLOW + "1. 1-digit × 1-digit")
    print(Fore.YELLOW + "2. 2-digit × 2-digit")
    print(Fore.YELLOW + "3. 3-digit × 3-digit")
    print(Fore.YELLOW + "4. 4-digit × 4-digit")
    print(Fore.YELLOW + "5. 5-digit × 5-digit")
    print(Fore.YELLOW + "6. 6-digit × 6-digit")
    print(Fore.YELLOW + "7. 7-digit × 7-digit")
    while True:
        try:
            choice = int(input(Fore.MAGENTA + "Enter your choice (1-7): "))
            if 1 <= choice <= 7:
                return choice
        except ValueError:
            pass
        print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 7.")

def generate_multiplication_question(mode):
    if mode == 1:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
    elif mode == 2:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
    elif mode == 3:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
    elif mode == 4:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
    elif mode == 5:
        a = random.randint(10000, 99999)
        b = random.randint(10000, 99999)
    elif mode == 6:
        a = random.randint(100000, 999999)
        b = random.randint(100000, 999999)
    else:  # mode == 7
        a = random.randint(1000000, 9999999)
        b = random.randint(1000000, 9999999)
    
    return f"{a} × {b}", a * b

def multiplication_enthusiast_game():
    mode = get_multiplication_mode()
    num_questions = get_num_questions()
    user_answers = []
    correct_answers = []
    questions = []
    
    print(Style.BRIGHT + Fore.WHITE + "\nWelcome to the Multiplication Enthusiast Mode!")
    print(Fore.YELLOW + f"You'll have {num_questions} multiplication questions.")
    print(Fore.YELLOW + "Answer as quickly as you can. Results will be shown at the end.")
    input(Fore.MAGENTA + "Press Enter to start...")
    
    print(Fore.YELLOW + "\nPrepare yourself. The first question will appear in 3 seconds...")
    time.sleep(3)  # 3-second pause before the first question
    
    start_time = time.time()
    
    for i in range(num_questions):
        question, correct_answer = generate_multiplication_question(mode)
        questions.append(question)
        correct_answers.append(correct_answer)
        
        print(Style.BRIGHT + Fore.WHITE + f"\nQuestion {i+1}:")
        print(Fore.CYAN + question + " = ?")
        user_answer = input(Fore.MAGENTA + "Your answer: ")
        
        try:
            user_answer = int(user_answer)
            user_answers.append(user_answer)
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Treating as incorrect.")
            user_answers.append(None)
    
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    # Calculate score and show results
    score = sum(1 for ua, ca in zip(user_answers, correct_answers) if ua == ca)
    
    print(Style.BRIGHT + Fore.WHITE + "\n--- Game Over ---")
    print(Fore.YELLOW + f"Your score: {Style.BRIGHT + Fore.WHITE}{score}/{num_questions}")
    print(Fore.YELLOW + f"Total time: {Style.BRIGHT + Fore.WHITE}{total_time} seconds")
    print(Fore.YELLOW + f"Average time per question: {Style.BRIGHT + Fore.WHITE}{round(total_time/num_questions, 2)} seconds")
    
    print(Style.BRIGHT + Fore.WHITE + "\nDetailed Results:")
    for i, (question, user_answer, correct_answer) in enumerate(zip(questions, user_answers, correct_answers), 1):
        status = "Correct" if user_answer == correct_answer else "Incorrect"
        status_color = Fore.GREEN if status == "Correct" else Fore.RED
        print(Fore.CYAN + f"Question {i}: {question} = {correct_answer}")
        print(Fore.GREEN + f"Your answer: {user_answer}")
        print(status_color + f"Status: {status}\n")

def get_division_mode():
    print(Style.BRIGHT + Fore.WHITE + "\nDivision Enthusiast Mode")
    print(Fore.YELLOW + "Choose the type of division:")
    print(Fore.YELLOW + "1. 3 digits ÷ 1 digit")
    print(Fore.YELLOW + "2. 4 digits ÷ 1 digit")
    print(Fore.YELLOW + "3. 4 digits ÷ 2 digits")
    print(Fore.YELLOW + "4. 5 digits ÷ 2 digits")
    print(Fore.YELLOW + "5. 7 digits ÷ 2 digits")
    print(Fore.YELLOW + "6. 5 digits ÷ 3 digits")
    print(Fore.YELLOW + "7. 6 digits ÷ 3 digits")
    print(Fore.YELLOW + "8. 7 digits ÷ 3 digits")
    print(Fore.YELLOW + "9. 7 digits ÷ 4 digits")
    while True:
        try:
            choice = int(input(Fore.MAGENTA + "Enter your choice (1-9): "))
            if 1 <= choice <= 9:
                return choice
        except ValueError:
            pass
        print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 9.")

def generate_division_question(mode):
    if mode == 1:
        divisor = random.randint(2, 9)
        dividend = random.randint(100, 999)
    elif mode == 2:
        divisor = random.randint(2, 9)
        dividend = random.randint(1000, 9999)
    elif mode == 3:
        divisor = random.randint(10, 99)
        dividend = random.randint(1000, 9999)
    elif mode == 4:
        divisor = random.randint(10, 99)
        dividend = random.randint(10000, 99999)
    elif mode == 5:
        divisor = random.randint(10, 99)
        dividend = random.randint(1000000, 9999999)
    elif mode == 6:
        divisor = random.randint(100, 999)
        dividend = random.randint(10000, 99999)
    elif mode == 7:
        divisor = random.randint(100, 999)
        dividend = random.randint(100000, 999999)
    elif mode == 8:
        divisor = random.randint(100, 999)
        dividend = random.randint(1000000, 9999999)
    else:  # mode == 9
        divisor = random.randint(1000, 9999)
        dividend = random.randint(1000000, 9999999)
    
    # Ensure the division results in an integer
    dividend = dividend - (dividend % divisor)
    
    return f"{dividend} ÷ {divisor}", dividend // divisor

def division_enthusiast_game():
    mode = get_division_mode()
    num_questions = get_num_questions()
    user_answers = []
    correct_answers = []
    questions = []
    
    print(Style.BRIGHT + Fore.WHITE + "\nWelcome to the Division Enthusiast Mode!")
    print(Fore.YELLOW + f"You'll have {num_questions} division questions.")
    print(Fore.YELLOW + "Answer as quickly as you can. Results will be shown at the end.")
    input(Fore.MAGENTA + "Press Enter to start...")
    
    print(Fore.YELLOW + "\nPrepare yourself. The first question will appear in 3 seconds...")
    time.sleep(3)  # 3-second pause before the first question
    
    start_time = time.time()
    
    for i in range(num_questions):
        question, correct_answer = generate_division_question(mode)
        questions.append(question)
        correct_answers.append(correct_answer)
        
        print(Style.BRIGHT + Fore.WHITE + f"\nQuestion {i+1}:")
        print(Fore.CYAN + question + " = ?")
        user_answer = input(Fore.MAGENTA + "Your answer: ")
        
        try:
            user_answer = int(user_answer)
            user_answers.append(user_answer)
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Treating as incorrect.")
            user_answers.append(None)
    
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    # Calculate score and show results
    score = sum(1 for ua, ca in zip(user_answers, correct_answers) if ua == ca)
    
    print(Style.BRIGHT + Fore.WHITE + "\n--- Game Over ---")
    print(Fore.YELLOW + f"Your score: {Style.BRIGHT + Fore.WHITE}{score}/{num_questions}")
    print(Fore.YELLOW + f"Total time: {Style.BRIGHT + Fore.WHITE}{total_time} seconds")
    print(Fore.YELLOW + f"Average time per question: {Style.BRIGHT + Fore.WHITE}{round(total_time/num_questions, 2)} seconds")
    
    print(Style.BRIGHT + Fore.WHITE + "\nDetailed Results:")
    for i, (question, user_answer, correct_answer) in enumerate(zip(questions, user_answers, correct_answers), 1):
        status = "Correct" if user_answer == correct_answer else "Incorrect"
        status_color = Fore.GREEN if status == "Correct" else Fore.RED
        print(Fore.CYAN + f"Question {i}: {question} = {correct_answer}")
        print(Fore.GREEN + f"Your answer: {user_answer}")
        print(status_color + f"Status: {status}\n")

def math_game():
    while True:
        print(Style.BRIGHT + Fore.WHITE + "\nChoose the game mode:")
        print(Fore.YELLOW + "1. Regular Math Game")
        print(Fore.YELLOW + "2. Multiplication Enthusiast Mode")
        print(Fore.YELLOW + "3. Division Enthusiast Mode")
        print(Fore.YELLOW + "4. Exit")
        
        try:
            choice = int(input(Fore.MAGENTA + "Enter your choice (1-4): "))
            if choice == 1:
                regular_math_game()
            elif choice == 2:
                multiplication_enthusiast_game()
            elif choice == 3:
                division_enthusiast_game()
            elif choice == 4:
                print(Fore.YELLOW + "Thank you for playing! Goodbye!")
                break
            else:
                print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 4.")
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number between 1 and 4.")
        

if __name__ == "__main__":
    math_game()