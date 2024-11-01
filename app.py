from flask import Flask, render_template, request, redirect, Response
import requests

app = Flask(__name__)

EXCLUDED_TAGS = [
    "423e2eae-a7a2-4a8b-ac03-a8351462d71d",  # Romance
    "5920b825-4181-4a17-beeb-9918b0ff7a30",  # Boys' Love
    "2d1f5d56-a1e5-4d0d-a961-2193588b08ec",  # Loli
    "ddefd648-5140-4e5f-ba18-4eca4071d19b",  # Shota
    "a3c67850-4684-404e-9b7f-c69850ee5da6",  # Girls' Love
    "dd1f77c5-dea9-4e2b-97ae-224af09caf99"   # Monster Girls
]

INCLUDED_CONTENT_RATINGS = ["safe"]

def fetch_cover_filename(cover_id):
    """Fetch the cover filename using the /cover/{id} endpoint."""
    # print(f"Fetching cover for ID: {cover_id}")
    response = requests.get(f"https://api.mangadex.org/cover/{cover_id}")
    if response.status_code == 200:
        data = response.json().get("data", {})
        file_name = data["attributes"]["fileName"]
        # print(f"Fetched cover filename: {file_name}")
        return file_name
    else:
        # print(f"Error fetching cover {cover_id}: {response.status_code}")
        return None

def fetch_manga(offset=0):
    """Fetch manga data."""
    print(f"Fetching manga with offset: {offset}")
    base_url = "https://api.mangadex.org/manga"
    params = {
        "excludedTags[]": EXCLUDED_TAGS,
        "limit": 100,
        "offset": offset,
        "contentRating[]": INCLUDED_CONTENT_RATINGS,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json().get("data", [])
        #print(f"Fetched {len(data)} manga entries.")
        return data
    else:
        #print(f"Error fetching manga: {response.status_code}")
        return []

@app.route('/proxy/<path:url>')
def proxy_image(url):
    """Proxy the image request through the backend."""
    image_url = f"https://{url}"
    response = requests.get(image_url)
    if response.status_code == 200:
        return Response(response.content, content_type=response.headers['Content-Type'])
    else:
        return "Image not found", 404

@app.route('/')
def index():
    """Render the main page."""
    page = int(request.args.get('page', 1))
    offset = (page - 1) * 100
    manga_data = fetch_manga(offset)

    manga_list = []
    for manga in manga_data:
        title = manga["attributes"]["title"].get("en", "Unknown Title")
        manga_id = manga["id"]
        manga_url = f"https://mangadex.org/title/{manga_id}"

        cover_id = next(
            (rel["id"] for rel in manga.get("relationships", []) if rel["type"] == "cover_art"), None
        )

        if cover_id:
            cover_file = fetch_cover_filename(cover_id)
            if cover_file:
                cover_url = f"{request.host_url}proxy/uploads.mangadex.org/covers/{manga_id}/{cover_file}"
            else:
                cover_url = "/static/placeholder.png"
        else:
            cover_url = "/static/placeholder.png"

        manga_list.append({
            "title": title,
            "cover_url": cover_url,
            "manga_url": manga_url
        })

    #print(f"Rendering {len(manga_list)} manga entries.")
    return render_template('index.html', manga_list=manga_list, page=page)

if __name__ == '__main__':
    app.run(debug=True)
