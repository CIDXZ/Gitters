import tkinter as tk
from tkinter import filedialog
from azure.cognitiveservices.search.websearch import WebSearchClient
from msrest.authentication import CognitiveServicesCredentials

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            questions = file.readlines()
            return questions
    except FileNotFoundError:
        print("File not found.")
        return None

def search_answers(question):
    subscription_key = "43aefa3571e948f5a0c2ee3221380351"  # Replace with your subscription key
    client = WebSearchClient(endpoint="https://api.bing.microsoft.com/", credentials=CognitiveServicesCredentials(subscription_key))
    result = client.web.search(query=question)
    if result.web_pages.value:
        return result.web_pages.value[0].snippet
    else:
        return "No answer found."

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        questions = read_text_file(file_path)
        if questions:
            for question in questions:
                answer = search_answers(question)
                text_box.insert(tk.END, f"Question: {question}\n")
                text_box.insert(tk.END, f"Answer: {answer}\n\n")

def main():
    global text_box
    root = tk.Tk()
    root.title("Text File Reader and Bing AI Search")

    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.pack(pady=10)

    text_box = tk.Text(root, height=20, width=80)
    text_box.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
