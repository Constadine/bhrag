"""This script serves as a skeleton template for synchronous AgentQL scripts."""

import logging
import pandas as pd 
import agentql
from agentql.ext.playwright.sync_api import Page
from playwright.sync_api import sync_playwright

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    perfumes = pd.read_csv('perfumes/brands/yves-saint-laurent.csv')

    for index, row in perfumes.iterrows():
        url = row['URL']
        
        with sync_playwright() as p, p.chromium.launch(headless=False) as browser:
            # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
            page = agentql.wrap(browser.new_page())

            # Navigate to the desired URL
            page.goto(url)

            json_data = get_response(page)

            # Flatten JSON into a single-row DataFrame
            data = {
                "name": json_data["name"],
                "brand": json_data["brand"],
                "photo_url": json_data["photo_url"],
                "family": json_data["Olfactive_classification"][0]["family"],
                "subfamily": json_data["Olfactive_classification"][0]["subfamily"],
                "description": json_data["Description"],
                "ingredients": json_data["ingredients"],
                "origin": json_data["Data_Sheet"][0]["origin"],
                "gender": json_data["Data_Sheet"][0]["gender"],
                "year": json_data["Data_Sheet"][0]["year"],
                "concepts": json_data["Data_Sheet"][0]["concepts"],
            }

            df = pd.DataFrame([data])
            # Save to CSV
            csv_file_path = f"perfumes/list_of_perfumes/{data['name']}.csv"
            df.to_csv(csv_file_path, index=False)


def get_response(page: Page):
    query = """
    {
    name
    brand
    photo_url
    Olfactive_classification[] {
        family
        subfamily
    }
    Description
    ingredients(all the ingredients listed for the perfume)[]
    Data_Sheet[] {
        origin
        gender
        year
        concepts[]
    }
    }
    """

    response = page.query_data(query)

    # For more details on how to consume the response, refer to the documentation at https://docs.agentql.com/intro/main-concepts
    return response


if __name__ == "__main__":
    main()
