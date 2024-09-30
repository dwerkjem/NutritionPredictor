# test_search.py

from pyfatsecret import Fatsecret
from dotenv import load_dotenv
import os


def initialize_fatsecret():
    load_dotenv()
    consumer_key = os.getenv("FATSECRET_CONSUMER_KEY")
    consumer_secret = os.getenv("FATSECRET_CONSUMER_SECRET")

    if not consumer_key or not consumer_secret:
        print("Error: FatSecret API credentials not found in environment variables.")
        exit(1)

    return Fatsecret(consumer_key, consumer_secret)


def search_food(fs, search_expression, max_results=5):
    response = fs.foods_search(
        search_expression=search_expression, max_results=max_results
    )
    foods = response.get("foods", {}).get("food", [])
    return foods


def main():
    fs = initialize_fatsecret()

    # Test search
    search_expression = "Frosted Flakes Kellogg's"
    print(f"Searching for: {search_expression}")
    foods = search_food(fs, search_expression)

    if not foods:
        print("No matching food items found.")
    else:
        for idx, food in enumerate(foods, start=1):
            print(
                f"{idx}. {food.get('food_name')} (Brand: {food.get('brand_name', 'N/A')}, Food ID: {food.get('food_id')})"
            )


if __name__ == "__main__":
    main()
