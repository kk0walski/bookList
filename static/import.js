var local_books = []
var current_page = 1
const pages_items = 7

function range(start, stop, step) {
    if (typeof stop == 'undefined') {
        // one param defined
        stop = start;
        start = 0;
    }

    if (typeof step == 'undefined') {
        step = 1;
    }

    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }

    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        result.push(i);
    }

    return result;
};

function paginator(items, current_page, per_page_items) {
    let page = current_page || 1,
        per_page = per_page_items || 10,
        offset = (page - 1) * per_page,

        paginatedItems = items.slice(offset).slice(0, per_page_items),
        total_pages = Math.ceil(items.length / per_page);

    const min = page - 2 > 1 ? page - 2 : 1
    const max = page + 2 < total_pages + 1 ? page + 2 : total_pages + 1
    let pages_array = range(min, max)

    return {
        page: page,
        per_page: per_page,
        pre_page: page - 1 ? page - 1 : null,
        next_page: (total_pages > page) ? page + 1 : null,
        total: items.length,
        total_pages: total_pages,
        pages_array: pages_array,
        data: paginatedItems
    };
}

function create_link(book, index) {
    if (book.frontPage === '#') {
        return `<div id="${index}"
        class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
        <div class="flex-column">
            ${book.title} <small>by ${book.author}</small>
            <p><small>Pub date: ${book.date}</small></p>
            <p>ISBN: ${book.isbn}</p>
            <span class="badge bg-primary">pageCount: ${book.pages}</span>
            <span class="badge bg-secondary">lang: ${book.language}</span>
            <button type="button" class="btn btn-danger" onClick=remove_book(${index})>Remove</button>
        </div>
        <svg class="bd-placeholder-img img-thumbnail" width="100" height="150" xmlns="http://www.w3.org/2000/svg"
         role="img" preserveAspectRatio="xMidYMid slice" focusable="false">
            <rect width="100" height="150" fill="#868e96"></rect>
            <text x="10%" y="50%" fill="#dee2e6" dy=".3em">100x150</text>
        </svg>
    </div>`
    } else {
        return `<div id="${index}"
        class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
        <div class="flex-column">
            ${book.title} <small>by ${book.author}</small>
            <p><small>Pub date: ${book.date}</small></p>
            <p>ISBN: ${book.isbn}</p>
            <span class="badge bg-primary">pageCount: ${book.pages}</span>
            <span class="badge bg-secondary">lang: ${book.language}</span>
            <button type="button" class="btn btn-danger" onClick=remove_book(${index})>Remove</button>
        </div>
        <figure class="figure">
            <img src="${book.frontPage}" class="img-thumbnail" width="100" height="150" alt="front page">
        </figure>
    </div>`
    }

}

function change_page(page_number) {
    current_page = page_number
    let paginate_item = paginator(local_books, current_page, pages_items)
    generate_html(paginate_item)
}

function generate_pagination(pagination_item) {
    current_page = pagination_item['page']
    let nav = document.createElement("nav")
    let ul = document.createElement("ul")
    ul.classList.add("pagination")
    if (pagination_item['pre_page']) {
        let prev_page = document.createElement('li')
        prev_page.classList.add('page-item')
        prev_page.innerHTML = `<a class="page-link" onClick=change_page(${current_page - 1}) href="#">Previous</a>`
        ul.appendChild(prev_page)
    }
    for (var page of pagination_item['pages_array']) {
        list_element = document.createElement('li')
        list_element.classList.add('page-item')
        if (page == current_page) {
            list_element.classList.add('active')
            list_element.ariaCurrent = "page"
        }
        list_element.innerHTML = `<a class="page-link" onClick=change_page(${page}) href="#">${page}</a>`
        ul.appendChild(list_element)
    }
    if (pagination_item['next_page']) {
        let next_page = document.createElement('li')
        next_page.classList.add('page-item')
        next_page.innerHTML = `<a class="page-link" onClick=change_page(${current_page + 1}) href="#">Next</a>`
        ul.appendChild(next_page)
    }
    nav.appendChild(ul)
    return nav
}

function generate_html(pagination_item) {
    let books = document.getElementById('books');
    books.innerHTML = ""
    let list = document.createElement("ul")
    list.classList.add('list-group')
    list.id = 'book-list'
    list.innerHTML = `${pagination_item['data'].map((book, index) => create_link(book, index)).join('')}`
    books.appendChild(list)
    books.appendChild(document.createElement("br"))
    if (pagination_item['total_pages'] > 1) {
        let pagination_html = generate_pagination(pagination_item)
        books.appendChild(pagination_html)
    }
}

function no_books_html() {
    books = document.getElementById('books');
    books.innerHTML = `<p class="text-info bg-dark" > No images</p>`
}

function remove_book(index) {
    local_books.splice(index, 1)
    let paginate_item = paginator(local_books, current_page, pages_items)
    generate_html(paginate_item)
}

function put_books(books) {
    for (var book of books) {
        local_books.push(book)
    }
    if (local_books.length > 0) {
        let paginate_item = paginator(local_books, current_page, pages_items)
        generate_html(paginate_item)
    } else {
        no_books_html()
    }
}