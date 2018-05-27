from flask import Flask, request, render_template
import app.libs.api as api
from app.models import Pagination
from app.libs.data_loader import DataLoader

app = Flask(__name__)

PRODUCTS_PER_CATEGORY_PAGE = 5
CATEGORY_PER_HOMEPAGE = 9
PRODUCT_SHORT_DESCRIPTION_LENGTH = 500


@app.route('/')
def homepage():
    page_number = request.args.get('page', default=1, type=int)
    offset = (page_number - 1) * CATEGORY_PER_HOMEPAGE
    limit = CATEGORY_PER_HOMEPAGE

    loader = DataLoader()
    all_categories = loader.load_all_categories()
    categories = all_categories.categories[offset:offset + limit + 1]

    pagination = Pagination(len(categories), CATEGORY_PER_HOMEPAGE, page_number)
    return render_template('categories.html', categories=categories, pagination=pagination)


@app.route('/categories/<category_id>')
def category_page(category_id):
    page_number = request.args.get('page', default=1, type=int)

    product_count = api.fetch_product_count(category_id)
    pagination = Pagination(product_count, PRODUCTS_PER_CATEGORY_PAGE, page_number)

    products = api.fetch_products(category_id,
                                  offset=(page_number - 1) * PRODUCTS_PER_CATEGORY_PAGE,
                                  limit=PRODUCTS_PER_CATEGORY_PAGE)

    category = api.fetch_category(category_id)

    return render_template('category.html',
                           category=category,
                           products=products,
                           pagination=pagination)


@app.route('/products/<product_id>')
def product_page(product_id):
    section = request.args.get('section', default='compare', type=str)

    product = api.fetch_product(product_id)
    category = api.fetch_category(product.category_id)

    return render_template('product.html',
                           product=product,
                           category=category,
                           product_short_description_length=PRODUCT_SHORT_DESCRIPTION_LENGTH,
                           section=section)
