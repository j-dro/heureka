from math import inf, ceil

NO_PICTURE_TEXT = 'Žadný obrázek'
PAGES_COUNT_IN_PAGINATION = 10


class Category:

    def __init__(self, obj_id, title):
        self.obj_id = obj_id
        self.title = title


class AllCategories:

    def __init__(self, categories):
        self.categories = categories
        self.category_ids = [category.obj_id for category in categories]


class Offer:
    def __init__(self, offer_id, shop_name, price, url):
        self.id = offer_id
        self.shop_name = shop_name
        self.price = price
        self.url = url


class Product:
    def __init__(self, product_id, category_id, title, description, image_urls, offers):
        self.id = product_id
        self.category_id = category_id
        self.title = title
        self.description = description
        self.image_urls = image_urls
        self.offers = offers

        self.min_price = inf
        self.max_price = -inf

        for offer in self.offers:
            if offer.price < self.min_price:
                self.min_price = offer.price

            if offer.price > self.max_price:
                self.max_price = offer.price

        if not self.image_urls:
            self.image_urls = ['http://via.placeholder.com/100x100?text=' + NO_PICTURE_TEXT]

    @property
    def sorted_offers(self):
        return sorted(self.offers, key=lambda offer: offer.price)


class Pagination:
    def __init__(self, items_count, items_per_page, current_page, show_pages_count=PAGES_COUNT_IN_PAGINATION):
        self.current_page = current_page
        self.total_pages_count = ceil(items_count / items_per_page)

        # calculate available pages for pagination
        start_page = self.current_page - (show_pages_count // 2)
        if start_page < 1:
            start_page = 1

        end_page = start_page + show_pages_count - 1
        if end_page > self.total_pages_count:
            end_page = self.total_pages_count
            start_page = end_page - show_pages_count + 1

        prepare_pages = list(range(start_page, end_page+1))
        self.available_pages = [page for page in prepare_pages if page > 0]

        # calculate prev and next page
        self.prev_page = self.current_page - 1
        if self.prev_page < 1:
            self.prev_page = None

        self.next_page = self.current_page + 1
        if self.next_page > self.total_pages_count:
            self.next_page = None
