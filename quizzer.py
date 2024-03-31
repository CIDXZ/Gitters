import tkinter as tk
import webbrowser
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def on_button_click():
    user_input = text_box.get("1.0", tk.END).strip()
    if user_input.lower() in ['exit', 'quit', 'bye']:
        root.destroy()
    else:
        response = f"You entered: {user_input}"
        result_label.config(text=response)

        # Save the text to a file named "site.txt"
        with open("site.txt", "w") as file:
            file.write(user_input)

        if user_input.startswith("http://") or user_input.startswith("https://"):
            open_in_browser(user_input)
            mark_and_save_questions(user_input)
        else:
            result_label.config(text="Invalid URL. Please enter a valid URL.")

def open_in_browser(url):
    webbrowser.open_new(url)

def mark_and_save_questions(url):
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Identify and mark lines ending with a question mark
        questions = []
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'li', 'td']):
            text = element.get_text()
            if text.endswith('?'):
                questions.append(text.strip())

        # Writing the questions to a file named "questions.txt"
        with open("questions.txt", "w") as file:
            for question in questions:
                file.write(question + "\n")

        result_label.config(text=f"{len(questions)} questions marked. Press 'Questions' button to view.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def open_questions():
    try:
        with open("questions.txt", "r") as questions_file:
            questions_content = questions_file.readlines()

        for question in questions_content:
            answer = search_google(question.strip())
            save_answer(answer)

        result_label.config(text=f"{len(questions_content)} questions Googled and answers saved.")
    except FileNotFoundError:
        result_label.config(text="No questions file found. Please submit a URL first.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def search_google(query):
    try:
        # Perform a Google search for responses related to the provided query
        response = list(search(query + " answer", num=1, stop=1, pause=2))
        return response[0]
    except Exception as e:
        return f"Error: {str(e)}"

def save_answer(answer):
    with open("answers.txt", "a") as answers_file:
        answers_file.write(answer + "\n")

def open_answers():
    try:
        with open("answers.txt", "r") as answers_file:
            answers_content = answers_file.readlines()

        # Display answers content in a separate Tkinter window
        answers_window = tk.Toplevel(root)
        answers_window.title("Saved Answers")

        answers_text_box = tk.Text(answers_window, height=15, width=50)
        answers_text_box.insert(tk.END, "\n".join(answers_content))
        answers_text_box.config(state="disabled")  # Disable editing
        answers_text_box.pack(pady=10)

    except FileNotFoundError:
        result_label.config(text="No answers file found. Please submit a URL and chat with the bot first.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Text Box Example")

# Create a text box
text_box = tk.Text(root, height=15, width=50)
text_box.pack(pady=10)

# Create a button
button = tk.Button(root, text="Submit / Config", command=on_button_click)
button.pack()

# Create buttons for "Questions" and "Answers"
questions_button = tk.Button(root, text="Questions", command=open_questions)
questions_button.pack(side=tk.LEFT, padx=5)

answers_button = tk.Button(root, text="Answers", command=open_answers)
answers_button.pack(side=tk.LEFT, padx=5)

# Create a label for displaying the result
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()




































