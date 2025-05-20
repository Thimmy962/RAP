let API_URL = "http://127.0.0.1:8080/articles?limit=500";

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("container");

    fetch(API_URL)
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            data.forEach(article => {
                const div = document.createElement("div");
                div.className = "post";
                const h2 = document.createElement("h2");
                h2.textContent = article.title;
                const p = document.createElement("p");
                p.textContent = article.abstract;
                div.appendChild(h2);
                div.appendChild(p);
                container.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Fetch error:", err);
        });
});