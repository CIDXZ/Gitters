import subprocess
import time
import random
from random_word import RandomWords
import pyautogui

# Function to generate a random search query using the 'random-word' library
def generate_random_query():
    r = RandomWords()
    return r.get_random_word()

# Function to perform a search on Bing by typing the query in the search bar
def search_on_bing(query):
    # Wait for a random amount of time (to mimic human behavior)
    time.sleep(random.randint(3, 7))
    
    # Simulate typing the query into the search bar
    pyautogui.typewrite(query)
    pyautogui.press('enter')

# Main function to perform searches based on user's choice
def main():
    print("Choose an option:")
    print("1. Search 33 times in 5 minutes")
    print("2. Search 33 times in 2 minutes")
    print("3. Search 10 times in 1 minute")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        searches_per_minute = 5
        for _ in range(33):
            query = generate_random_query()
            search_on_bing(query)
            print("Search performed for:", query)
            time.sleep(300 / searches_per_minute)  # Sleep for 2 minutes divided by the number of searches
    elif choice == '2':
        searches_per_day = 33
        for _ in range(searches_per_day):
            query = generate_random_query()
            search_on_bing(query)
            print("Search performed for:", query)
            time.sleep(120 / searches_per_day)  # Sleep for a day divided by the number of searches
    elif choice == '3':
        for _ in range(10):
            query = generate_random_query()
            search_on_bing(query)
            print("Search performed for:", query)
            time.sleep(6)  # Sleep for 1 minute divided by the number of searches (10 searches in 1 minute)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
















