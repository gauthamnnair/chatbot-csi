from fuzzywuzzy import process
from spellchecker import SpellChecker
import random

# Initialize spell checker
spell = SpellChecker()

# Load questions from a list
def load_questions():
    return [
        {"question": "I have no legs, yet I may run, I hold great power, yet weigh none. Kings have sought me, warriors wielded me, Yet in the wrong hands, I bring tragedy. What am I?", "answer": "sword"},
    ]

# Correct spelling in the user's answer
def correct_spelling(input_text):
    words = input_text.split()
    corrected_words = [spell.correction(word) for word in words]
    return " ".join(corrected_words)

# Function to check if the answer is correct or similar using fuzzy matching
def check_answer(user_input, correct_answer):
    normalized_user_input = user_input.lower().strip()
    normalized_correct_answer = correct_answer.lower().strip()

    if normalized_user_input == normalized_correct_answer:
        return True, None  # Exact match, no correction needed

    corrected_input = correct_spelling(user_input).lower().strip()
    if corrected_input == normalized_correct_answer:
        # Find the word that was corrected
        user_words = user_input.lower().split()
        corrected_words = corrected_input.split()
        corrected_word = None
        if len(user_words) == len(corrected_words):
            for i in range(len(user_words)):
                if user_words[i] != corrected_words[i]:
                    corrected_word = corrected_words[i]
                    break
        elif len(corrected_words) == 1 and len(user_words) > 0:
            best_match, score = process.extractOne(corrected_words[0], user_words)
            if score < 100:
                corrected_word = corrected_words[0]
        elif len(user_words) == 1 and len(corrected_words) > 0:
            corrected_word = " ".join(corrected_words)
        return True, normalized_correct_answer  # Correct after spelling correction
    else:
        # Fuzzy matching for similar answers
        best_match, score = process.extractOne(corrected_input, [normalized_correct_answer])
        if score >= 90:  # You can adjust this threshold
            return True, normalized_correct_answer # Consider it correct enough
        else:
            return False, None

def main():
    participants = []
    while True:
        try:
            num_players = int(input("Enter the number of people in your team: "))
            if num_players > 0:
                break
            else:
                print("Please enter a positive number of players.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Enter the names of your team members:")
    for i in range(num_players):
        name = input(f"Player {i + 1}: ").strip()
        participants.append(name)

    questions = load_questions()
    score = 0

    print("\nWelcome to the Riddle Game!")

    for i, q_data in enumerate(questions):
        question = q_data['question']
        correct_answer = q_data['answer']

        print(f"\nQuestion {i + 1}: {question}")

        while True:
            user_input = input("Your answer: ").strip()
            is_correct, meant_answer = check_answer(user_input, correct_answer)

            if is_correct:
                if meant_answer:
                    print(f"You meant '{meant_answer}', that's correct!")
                else:
                    print("Correct!")
                score += 1
                break  # Move to the next question
            else:
                print("Incorrect. Try again.")

    print("The stone gate creaks open, a narrow path beyond. But beware, for only the bold step forward. To leave now is to embrace fate, for better… or worse. Do you dare?")

    while True:
        choice = input("Choose your fate:\n1:Dare\n2:Proceed\nYour choice: ").lower()
        if choice == "1":
            print("Brave, yet foolish. The path you have chosen is shrouded in uncertainty. As you step forward, a heavy silence falls… One of you vanishes into the abyss of time, lost forever.")
            # Simulate a random "vanishing"
            vanished = random.choice(participants)
            print(f"It seems... {vanished} has been lost to the abyss.")
            break
        elif choice == "2":
            print("You have chosen the safer path. The journey continues...")
            break
        else:
            print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
