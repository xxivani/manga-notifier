import requests

base_url = "https://api.mangadex.org/manga/tag"

resp = requests.get(base_url)

if(resp.status_code==200):
    tags = resp.json()["data"]

    # Categorize tags by type (genre, theme, demographic, etc.)
    categorized_tags = {
        "genres": [],
        "themes": [],
        "demographics": []
    }
    for tag in tags:
        tag_name = tag["attributes"]["name"]["en"]
        tag_id = tag["id"]
        tag_type = tag["attributes"]["group"]

        # Sort tags by their group (genre, theme, demographic)
        if tag_type == "genre":
            categorized_tags["genres"].append((tag_name, tag_id))
        elif tag_type == "theme":
            categorized_tags["themes"].append((tag_name, tag_id))
        elif tag_type == "demographic":
            categorized_tags["demographics"].append((tag_name, tag_id))

    # Print the categorized tags
    print("Genres:")
    for genre in categorized_tags["genres"]:
        print(f"- {genre[0]} (ID: {genre[1]})")

    print("\nThemes:")
    for theme in categorized_tags["themes"]:
        print(f"- {theme[0]} (ID: {theme[1]})")

    print("\nDemographics:")
    for demographic in categorized_tags["demographics"]:
        print(f"- {demographic[0]} (ID: {demographic[1]})")

else:
    print(f"Failed to fetch tags: {resp.status_code}")


