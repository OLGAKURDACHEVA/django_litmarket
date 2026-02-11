const booksData = [
  {
    id: 1,
    title: "Мастер и Маргарита",
    author: "Михаил Булгаков",
    price: 850,
    genres: ["классика", "роман"],
    category: "Художественная литература",
  },
  {
    id: 2,
    title: "Преступление и наказание",
    author: "Фёдор Достоевский",
    price: 720,
    genres: ["классика", "роман"],
    category: "Художественная литература",
  },
  {
    id: 3,
    title: "1984",
    author: "Джордж Оруэлл",
    price: 690,
    genres: ["классика", "фантастика"],
    category: "Художественная литература",
  },
  {
    id: 4,
    title: "Убить пересмешника",
    author: "Харпер Ли",
    price: 780,
    genres: ["классика", "роман"],
    category: "Художественная литература",
  },
  {
    id: 5,
    title: "Маленький принц",
    author: "Антуан де Сент-Экзюпери",
    price: 450,
    genres: ["классика", "сказки"],
    category: "Детская литература",
  },
  {
    id: 6,
    title: "Гарри Поттер и философский камень",
    author: "Джоан Роулинг",
    price: 950,
    genres: ["фэнтези", "подростковая"],
    category: "Детская литература",
  },
  {
    id: 7,
    title: "Властелин колец",
    author: "Дж. Р. Р. Толкин",
    price: 1200,
    genres: ["фэнтези"],
    category: "Художественная литература",
  },
  {
    id: 8,
    title: "Семь навыков высокоэффективных людей",
    author: "Стивен Кови",
    price: 890,
    genres: ["бизнес", "психология"],
    category: "Бизнес и экономика",
  },
  {
    id: 9,
    title: "Богатый папа, бедный папа",
    author: "Роберт Кийосаки",
    price: 750,
    genres: ["бизнес", "финансы"],
    category: "Бизнес и экономика",
  },
  {
    id: 10,
    title: "Думай и богатей",
    author: "Наполеон Хилл",
    price: 680,
    genres: ["бизнес", "психология"],
    category: "Бизнес и экономика",
  },
  {
    id: 11,
    title: "Краткая история времени",
    author: "Стивен Хокинг",
    price: 820,
    genres: ["наука"],
    category: "Нехудожественная литература",
  },
  {
    id: 12,
    title: "Сапиенс: Краткая история человечества",
    author: "Юваль Ной Харари",
    price: 950,
    genres: ["история", "наука"],
    category: "Нехудожественная литература",
  },
  {
    id: 13,
    title: "Английский для начинающих",
    author: "Марк Смит",
    price: 550,
    genres: ["языки", "учебники"],
    category: "Образование",
  },
  {
    id: 14,
    title: "Современный детектив",
    author: "Алексей Иванов",
    price: 620,
    genres: ["детектив"],
    category: "Художественная литература",
  },
  {
    id: 15,
    title: "Маркетинг от А до Я",
    author: "Ирина Петрова",
    price: 780,
    genres: ["маркетинг", "бизнес"],
    category: "Бизнес и экономика",
  },
];

// Переменные состояния
let currentBooks = [...booksData];
let selectedGenres = new Set();
let minPrice = 0;
let maxPrice = Infinity;
let currentSort = "title-asc";
let currentPage = 1;
const booksPerPage = 8;

// Инициализация
document.addEventListener("DOMContentLoaded", function () {
  initCategories();
  renderBooks();
  setupEventListeners();
});

// Инициализация категорий
function initCategories() {
  // Раскрытие/скрытие жанров
  document.querySelectorAll(".toggle-genres").forEach((arrow) => {
    arrow.addEventListener("click", function (e) {
      e.stopPropagation();
      const header = this.closest(".category-header");
      header.classList.toggle("active");
    });
  });

  // Клик по заголовку категории
  document.querySelectorAll(".category-header").forEach((header) => {
    header.addEventListener("click", function () {
      this.classList.toggle("active");
    });
  });
}

// Настройка обработчиков событий
function setupEventListeners() {
  // Переключение сайдбара
  document
    .getElementById("toggleFilters")
    .addEventListener("click", toggleSidebar);
  document
    .getElementById("toggleSidebar")
    .addEventListener("click", toggleSidebar);

  // Выбор жанров
  document.querySelectorAll(".genre-checkbox input").forEach((checkbox) => {
    checkbox.addEventListener("change", updateSelectedGenres);
  });

  // Фильтр по цене
  document
    .getElementById("priceMin")
    .addEventListener("input", updatePriceFilter);
  document
    .getElementById("priceMax")
    .addEventListener("input", updatePriceFilter);

  // Применение фильтров
  document
    .getElementById("applyFilters")
    .addEventListener("click", applyFilters);
  document
    .getElementById("resetFilters")
    .addEventListener("click", resetFilters);

  // Поиск
  document
    .getElementById("searchInput")
    .addEventListener("input", handleSearch);

  // Сортировка
  document.getElementById("sortSelect").addEventListener("change", handleSort);

  // Пагинация
  document.querySelectorAll(".pagination-btn").forEach((btn) => {
    btn.addEventListener("click", handlePagination);
  });

  // Добавление в корзину
  document.addEventListener("click", function (e) {
    if (e.target.closest(".add-to-cart")) {
      addToCart(e.target.closest(".book-card").dataset.id);
    }
  });
}

// Переключение сайдбара
function toggleSidebar() {
  document.getElementById("catalogSidebar").classList.toggle("active");
}

// Обновление выбранных жанров
function updateSelectedGenres(e) {
  const genre = e.target.value;

  if (e.target.checked) {
    selectedGenres.add(genre);
  } else {
    selectedGenres.delete(genre);
  }
}

// Обновление фильтра по цене
function updatePriceFilter() {
  const min = document.getElementById("priceMin").value;
  const max = document.getElementById("priceMax").value;

  minPrice = min ? parseInt(min) : 0;
  maxPrice = max ? parseInt(max) : Infinity;
}

// Применение фильтров
function applyFilters() {
  filterBooks();
  toggleSidebar();
}

// Сброс фильтров
function resetFilters() {
  // Сброс чекбоксов
  document.querySelectorAll(".genre-checkbox input").forEach((checkbox) => {
    checkbox.checked = false;
  });

  // Сброс полей цены
  document.getElementById("priceMin").value = "";
  document.getElementById("priceMax").value = "";

  // Сброс состояния
  selectedGenres.clear();
  minPrice = 0;
  maxPrice = Infinity;

  // Обновление отображения
  filterBooks();
  toggleSidebar();
}

// Поиск
function handleSearch(e) {
  filterBooks();
}

// Сортировка
function handleSort(e) {
  currentSort = e.target.value;
  sortBooks();
  renderBooks();
}

// Пагинация
function handlePagination(e) {
  const btn = e.target.closest(".pagination-btn");
  if (btn.classList.contains("prev")) {
    if (currentPage > 1) {
      currentPage--;
      renderBooks();
    }
  } else if (btn.classList.contains("next")) {
    const totalPages = Math.ceil(currentBooks.length / booksPerPage);
    if (currentPage < totalPages) {
      currentPage++;
      renderBooks();
    }
  }
}

// Фильтрация книг
function filterBooks() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();

  currentBooks = booksData.filter((book) => {
    // Поиск по названию и автору
    const matchesSearch =
      searchTerm === "" ||
      book.title.toLowerCase().includes(searchTerm) ||
      book.author.toLowerCase().includes(searchTerm);

    // Фильтр по жанрам
    const matchesGenres =
      selectedGenres.size === 0 ||
      book.genres.some((genre) => selectedGenres.has(genre));

    // Фильтр по цене
    const matchesPrice = book.price >= minPrice && book.price <= maxPrice;

    return matchesSearch && matchesGenres && matchesPrice;
  });

  sortBooks();
  renderBooks();
}

// Сортировка книг
function sortBooks() {
  currentBooks.sort((a, b) => {
    switch (currentSort) {
      case "title-asc":
        return a.title.localeCompare(b.title, "ru");
      case "title-desc":
        return b.title.localeCompare(a.title, "ru");
      case "price-asc":
        return a.price - b.price;
      case "price-desc":
        return b.price - a.price;
      case "author-asc":
        return a.author.localeCompare(b.author, "ru");
      case "author-desc":
        return b.author.localeCompare(a.author, "ru");
      default:
        return 0;
    }
  });
}
