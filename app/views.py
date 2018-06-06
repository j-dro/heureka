from flask import Flask, request, render_template
from app.libs.api import CachedApi
from app.models import Pagination

app = Flask(__name__)

PRODUCTS_PER_CATEGORY_PAGE = 5
CATEGORY_PER_HOMEPAGE = 9
PRODUCT_SHORT_DESCRIPTION_LENGTH = 250


PAGE_404_TEXTS = {
    'title': 'Ooops, něco není dobře',
    'text': 'Zdá se, že hledáte stranku, která tu není',
    'suggestion': 'Zkusme začít od začátku',
    'button_text': 'Na začátek'
}

PAGE_500_TEXTS = {
    'title': 'Ooops, zdá se, že se něco pokazilo',
    'text': 'Slibujeme, že se to stává maximálně jednou za deset let!',
    'suggestion': 'Zkuste akci opakovat',
    'button_text': 'Opakovat'
}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('oops.html', url='/', **PAGE_404_TEXTS), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('oops.html', url=request.url, **PAGE_500_TEXTS), 500


@app.route('/')
def homepage():
    page_number = request.args.get('page', default=1, type=int)

    api = CachedApi()
    all_categories = api.fetch_all_categories()
    pagination = Pagination(len(all_categories.categories), CATEGORY_PER_HOMEPAGE, page_number)

    offset = (pagination.current_page - 1) * CATEGORY_PER_HOMEPAGE
    limit = CATEGORY_PER_HOMEPAGE

    categories = all_categories.categories[offset:offset + limit + 1]

    return render_template('categories.html',
                           all_categories=all_categories,
                           categories=categories,
                           pagination=pagination)


@app.route('/categories/<category_id>')
def category_page(category_id):
    page_number = request.args.get('page', default=1, type=int)

    api = CachedApi()
    all_categories = api.fetch_all_categories()

    product_count = api.fetch_product_count(category_id)
    pagination = Pagination(product_count, PRODUCTS_PER_CATEGORY_PAGE, page_number)

    products = api.fetch_products(category_id,
                                  offset=(pagination.current_page - 1) * PRODUCTS_PER_CATEGORY_PAGE,
                                  limit=PRODUCTS_PER_CATEGORY_PAGE)

    category = api.fetch_category(category_id)

    return render_template('category.html',
                           all_categories=all_categories,
                           category=category,
                           product_short_description_length=PRODUCT_SHORT_DESCRIPTION_LENGTH,
                           products=products,
                           pagination=pagination)


@app.route('/products/<product_id>')
def product_page(product_id):
    api = CachedApi()
    product = api.fetch_product(product_id)
    category = api.fetch_category(product.category_id)

    return render_template('product.html',
                           product=product,
                           category=category,
                           product_short_description_length=PRODUCT_SHORT_DESCRIPTION_LENGTH)
