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


filename = "answers.txt"
with open(filename, "w") as file:
    file.write("")



filename = "reviewed_questions.txt"
with open(filename, "r") as file:
    lines = file.readlines()
    n = len(lines) # number of lines in file
    
    for i in range(n):
        line = lines[i].strip() # get line i from the list and strip any whitespace
        # do something with the line here
    
        question = line        
        if not lines:  # stop the loop if end of file is reached
         break
        

        
     # Fetch Google search results page
        
        url = f"https://www.google.com/search?q={question}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        html_content = response.text
 
        # Parse search results page
        soup = BeautifulSoup(html_content, 'html.parser')
        results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')

        # Print top search result
        if len(results) > 0:
          filenamea = "answers.txt"
          
          with open(filenamea, 'a', encoding='utf-8') as file:
            file.write(results[0].get_text())
            file.write("\n\n")

      
         

         
         

         

        else:
          print("Sorry, I couldn't find an answer to that question.") 
