import instructor
from pydantic import BaseModel, Field
from pydantic_data_models import OutfitClassification
from openai import OpenAI
import os 
import logging
from dotenv import load_dotenv

load_dotenv()

# Add logger
logging.basicConfig()
logger = logging.getLogger("app")
logger.setLevel("INFO")


# Define clients
client_image = instructor.from_openai(
    OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
        ),
    mode=instructor.Mode.MD_JSON
    )

client_copy = instructor.from_openai(
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")), mode=instructor.Mode.TOOLS
)

OUTFIT_URL = "https://images.halloweencostumes.eu/products/83291/1-1/adult-lemon-slice-costume.jpg"

rezponz = client_image.chat.completions.create(
        model="gpt-4o-mini",
        response_model=OutfitClassification,
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                            Role: You are an expert outfit stylist. 
                            Task: Your task is to assign a value from 0 to 1 to each of the categories.
                            Context: Higher values means that the outfit resembles more to the name of the category.
                            """
                    },
                    {
                        "type": "image_url", 
                        "image_url": {"url": OUTFIT_URL}
                    },
                ],
            }
        ],
    )

concepts_weight = list(rezponz.dict().values())