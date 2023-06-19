import requests
from bs4 import BeautifulSoup
import csv

url = "https://book.douban.com/top250"

# Send a request to the website
response = requests.get(url)

# Parsing the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Finding all book rows in the table
book_rows = soup.find_all("tr", class_="item")

# Creating a list to store the results
results = []

# Looping through each book row and extracting required attributes
for row in book_rows:
    # Extracting book title
    title = row.find("div", class_="pl2").a["title"]
    
    # Extracting author and translator
    author_info = row.find("div", class_="pl").get_text().strip()
    author, *translator = author_info.split("/")
    
    # Extracting publisher, publication year, price, rating, rating count and review
    publisher_info = row.find("div", class_="pl").find_next_sibling("div").get_text().strip()
    publisher, pub_year, price, rating, rating_count = publisher_info.split("/")
    
    # Extracting review
    review = row.find("p", class_="quote").get_text().strip() if row.find("p", class_="quote") else ""
    
    # Storing the attributes in a dictionary
    book_dict = {"title": title,
                "author": author,
                "translator": translator,
                "publisher": publisher,
                "publication_year": pub_year,
                "price": price,
                "rating": rating,
                "rating_count": rating_count,
                "review": review}
    
    # Adding the dictionary to the results list
    results.append(book_dict)

# Saving the results as a CSV file
with open("douban_250_booklist.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "author", "translator", "publisher", "publication_year", "price", "rating", "rating_count", "review"])
    writer.writeheader()
    for result in results:
        writer.writerow(result)