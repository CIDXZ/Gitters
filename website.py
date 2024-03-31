import sys
sys.setrecursionlimit(10000) # or any other higher value
import openai_secret_manager
import requests
from bs4 import BeautifulSoup





# Fetching website content
url = "http://www.freepubquiz.co.uk/simple-quiz-questions.html#:~:text=Simple%20Quiz%20Questions%201%20Name%20the%20longest%20river,a%20pirate%20ship%20about%20to%20attack%3F%20More%20items"
res = requests.get(url)
html_content = res.text

# Parsing the website content
soup = BeautifulSoup(html_content, "html.parser")

# Extracting the questions
questions = []
for li in soup.find_all("ol", class_="listpadding"):
    for question in li.find_all("li"):
        text = question.get_text()
        if text.endswith("?"):
            questions.append(text.strip())

# Writing the questions to a file
with open("reviewed_questions.txt", "w") as file:
    for question in questions:
        file.write(question + "\n")