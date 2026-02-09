from ddgs import DDGS
import json

def test_image_search(query):
    print(f"Searching images for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=3))
            print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_image_search("SpaceX Starship launch")
