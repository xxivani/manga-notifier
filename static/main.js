document.addEventListener("DOMContentLoaded", function() {
    fetchManga();  // Fetch manga data on page load
});

// Function to fetch manga data from the backend
function fetchManga() {
    fetch('/manga')
        .then(response => response.json())
        .then(mangaData => renderManga(mangaData))
        .catch(error => console.error('Error fetching manga:', error));
}

// Function to render manga on the page
function renderManga(mangaList) {
    const mangaGrid = document.getElementById('manga-grid');
    mangaGrid.innerHTML = '';  // Clear previous content

    mangaList.forEach(manga => {
        let card = `
            <div class="col-md-3 mb-4">
                <div class="card">
                    <img src="${manga.cover_url}" class="card-img-top" alt="${manga.title}">
                    <div class="card-body">
                        <h5 class="card-title">${manga.title}</h5>
                        <a href="${manga.manga_url}" target="_blank" class="btn btn-primary">Read</a>
                    </div>
                </div>
            </div>
        `;
        mangaGrid.innerHTML += card;
    });
}
