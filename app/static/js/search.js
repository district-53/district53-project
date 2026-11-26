(function () {
    const input = document.getElementById("search-input");
    const list = document.getElementById("search-results");
    if (!input || !list) return;

    const searchUrl = input.dataset.searchUrl;
    let timer = null;
    let lastQuery = "";

    function hide() {
        list.classList.remove("show");
        list.innerHTML = "";
    }

    function message(text) {
        const li = document.createElement("li");
        const span = document.createElement("span");
        span.className = "dropdown-item-text text-secondary fst-italic";
        span.textContent = text;
        li.appendChild(span);
        list.appendChild(li);
    }

    function showResults(items) {
        list.innerHTML = "";
        if (items.length === 0) message("No such name in the book");

        for (const item of items) {
            const li = document.createElement("li");
            const link = document.createElement("a");
            link.className = "dropdown-item";
            link.href = item.url;
            link.textContent = item.name;

            const details = document.createElement("small");
            details.className = "d-block text-secondary";
            details.textContent = item.role + (item.house ? " · " + item.house : "");

            link.appendChild(details);
            li.appendChild(link);
            list.appendChild(li);
        }
        list.classList.add("show");
    }

    async function runSearch() {
        const q = input.value.trim();
        lastQuery = q;
        if (!q) {
            hide();
            return;
        }
        try {
            const response = await fetch(searchUrl + "?q=" + encodeURIComponent(q));
            if (!response.ok) throw new Error(response.status);
            const data = await response.json();
            if (q !== lastQuery) return;
            showResults(data);
        } catch (error) {
            list.innerHTML = "";
            message("Search failed");
            list.classList.add("show");
        }
    }

    input.addEventListener("input", () => {
        clearTimeout(timer);
        timer = setTimeout(runSearch, 300);
    });

    input.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            input.value = "";
            hide();
            input.blur();
        }
    });

    input.addEventListener("focus", () => {
        if (input.value.trim()) runSearch();
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".position-relative")) hide();
    });
})();