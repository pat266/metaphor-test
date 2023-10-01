from metaphor_python import Metaphor
from unidecode import unidecode
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
from chatgpt import summarize_destination, create_plan

load_dotenv()

def remove_multiple_newlines(text: str) -> str:
    return re.sub(r'\n+', '\n', text)

def convert_to_ascii(s: str) -> str:
    return unidecode(s)

def strip_html_tags(content: str) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()


def main():
    # Initialize the API client
    metaphor_api = Metaphor(os.getenv('METAPHORAI_API_KEY'))
    
    # 1. Create a dictionary to store the contents of each destination
    destination_data = {}
    summarized_destination_list = []

    # 2. Accept the user input of where to go
    destination = input("Enter your destination: ")
    num_days = input("Enter number of days: ")

    # 3. Search for attractions near the user input
    print(f"Searching for popular attractions near {destination}...")
    search_query = f"Popular attractions near {destination}"
    search_response = metaphor_api.search(
        query=search_query,
        use_autoprompt=True
    )

    # 4. For each result, find similar links and get their contents
    for result in search_response.results:
        # Find 2 similar websites for the current result
        similar_response = metaphor_api.find_similar(url=result.url, num_results=2)

        # Extract the IDs from the initial search result and its similar results
        ids = [result.id] + [res.id for res in similar_response.results]

        # Get contents of these 3 links
        contents_response = metaphor_api.get_contents(ids)

        # Combine all the content extracts into a single string
        combined_contents = " ".join([convert_to_ascii(strip_html_tags(content.extract)) for content in contents_response.contents])
        combined_contents = remove_multiple_newlines(combined_contents)

        # Add the combined contents to the dictionary using the result's title as the key
        destination_data[result.title] = combined_contents

    # 5. Summarize the contents of each destination
    for title, contents in destination_data.items():
        summarized_destination_list.append(summarize_destination(title, contents))

    # 6 Create a plan for the user
    generated_plan = create_plan(destination=destination, summarized_destinations=summarized_destination_list, num_days=num_days)
    plan = f"Here is your plan to go to {destination} for {num_days} days: {generated_plan}"
    print(plan)
    with open("generated_plan.txt", "w") as text_file:
        text_file.write(plan)
        

if __name__ == "__main__":
    main()