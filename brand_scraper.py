"""This script serves as a skeleton template for synchronous AgentQL scripts."""

import logging
import pandas as pd 
import agentql
from agentql.ext.playwright.sync_api import Page
from playwright.sync_api import sync_playwright

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set the URL to the desired website
BRAND = "creed"
URL = f"https://www.wikiparfum.com/en/brands/{BRAND}"


def main():

        
        with sync_playwright() as p, p.chromium.launch(headless=False) as browser:
            # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
            page = agentql.wrap(browser.new_page())

            # Navigate to the desired URL
            page.goto(URL)

            QUERY = """
            {
                cookies_form {
                    accept_all_cookies
                }
            }
            """
            response = page.query_elements(QUERY)

            
            print(response.cookies_form.accept_all_cookies)
            response.cookies_form.accept_all_cookies.click()

            # do->while 
            QUERY = """
            {
                all_the_fragrances {
                    load_more
                }
            }
            """

            response = page.query_elements(QUERY)
            response.all_the_fragrances.load_more.click()


            # print("What you;re really trying to print is :")
            # print("================")
            # print(response.all_the_fragrances.load_more)
            # print("================")

            while response.all_the_fragrances.load_more is not None:
                QUERY = """
                {
                    all_the_fragrances {
                        load_more
                    }
                }
                """

                response = page.query_elements(QUERY)
                if response.all_the_fragrances.load_more is None:
                    break
                response.all_the_fragrances.load_more.click()

            


            response = get_response(page)

            print(response)
            urls = [item["url"] for item in response["All_the_fragrances"]]
            df = pd.DataFrame({"URL": urls})
            print(df)

            # Save to CSV
            csv_file_path = f"perfumes/brands/{BRAND}.csv"
            df.to_csv(csv_file_path, index=False)



def get_response(page: Page):
    query = """
{
  All_the_fragrances[] {
    url
  }
}
    """

    response = page.query_data(query)

    # For more details on how to consume the response, refer to the documentation at https://docs.agentql.com/intro/main-concepts
    return response


if __name__ == "__main__":
    main()
