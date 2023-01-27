import requests
from bs4 import BeautifulSoup

# Send GET request to Google search page
response = requests.get("https://www.google.com/search", params={
    "q": "dog breeders MA",  # search term and desired state
    "tbm": "isch",  # search for images
})

# Parse HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all search result titles and links
results = soup.find_all("div", class_="r")

# Extract data and store in list
breeders = []
for result in results:
    title_element = result.find("h3")
    link_element = result.find("a")
    if title_element and link_element:
        title = title_element.text
        link = link_element["href"]
        breeders.append({"title": title, "link": link})

# Sort breeders by number of search results
breeders.sort(key=lambda x: x["title"], reverse=True)

# Print top breeders
for breeder in breeders[:5]:
    print(breeder["title"])
    print(breeder["link"])

