import requests
from bs4 import BeautifulSoup


filename = "reviewed_questions.txt"  # set filename to the name of the text file to read
with open(filename, "r") as file:
    num_lines = sum(1 for line in file)
    number = num_lines
    n = number  # set n to the desired number of lines to read
    for i in range(n):
     with open(filename, "r") as file:
      lines = file.readline()
      line3 = lines[i]     
      question = line3
      print(question)
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
      print(results[0].get_text())
      
      
         

         
         

         

     else:
         print("Sorry, I couldn't find an answer to that question.")
        















