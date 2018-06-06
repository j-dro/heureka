from app.models import Pagination, Product, Offer, Category, AllCategories


class TestCategory:
    def test_init(self):
        category = Category(1, 'Category 1')
        assert category.obj_id == 1
        assert category.title == 'Category 1'


class TestAllCategories:
    def test_init(self):
        categories =[Category(1, 'Category 1'), Category(2, 'Category 2')]
        all_categories = AllCategories(categories)
        assert all_categories.categories == categories
        assert all_categories.category_ids == [1, 2]


class TestOffer:
    def test_init(self):
        offer = Offer(1, 'Shop Name', 30.5, 'https://shopurl')

        assert offer.id == 1
        assert offer.shop_name == 'Shop Name'
        assert offer.price == 30.5
        assert offer.url == 'https://shopurl'


class TestProduct:
    @classmethod
    def setup_class(cls):
        cls.offer1 = Offer(1, 'Shop 1', 1000.5, 'https://url1')
        cls.offer2 = Offer(2, 'Shop 2', 500.0, 'https://url2')
        cls.offer3 = Offer(3, 'Shop 3', 700.0, 'https://url3')
        cls.product = Product(1, 2, 'Product', 'Description',
                              ['https://image1', 'https://image2'],
                              [cls.offer1, cls.offer2, cls.offer3])

    def test_init(self):
        assert self.product.id == 1
        assert self.product.category_id == 2
        assert self.product.title == 'Product'
        assert self.product.description == 'Description'
        assert self.product.image_urls == ['https://image1', 'https://image2']
        assert self.product.offers == [self.offer1, self.offer2, self.offer3]

    def test_min_price(self):
        assert self.product.min_price == 500.0

    def test_max_price(self):
        assert self.product.max_price == 1000.5

    def test_sorted_offers(self):
        assert self.product.sorted_offers == [self.offer2, self.offer3, self.offer1]


class TestPagination:
    def test_beginning(self):
        pagination = Pagination(items_count=200,
                                items_per_page=5,
                                current_page=1,
                                show_pages_count=5)

        assert pagination.total_pages_count == 40
        assert pagination.show_pages_count == 5
        assert pagination.current_page == 1
        assert pagination.available_pages == [1, 2, 3, 4, 5]
        assert pagination.prev_page is None
        assert pagination.next_page == 2

    def test_beginning2(self):
        pagination = Pagination(items_count=15,
                                items_per_page=5,
                                current_page=1,
                                show_pages_count=5)

        assert pagination.total_pages_count == 3
        assert pagination.current_page == 1
        assert pagination.show_pages_count == 5
        assert pagination.available_pages == [1, 2, 3]
        assert pagination.prev_page is None
        assert pagination.next_page == 2

    def test_middle(self):
        pagination = Pagination(items_count=201,
                                items_per_page=5,
                                current_page=33,
                                show_pages_count=5)

        assert pagination.total_pages_count == 41
        assert pagination.current_page == 33
        assert pagination.show_pages_count == 5
        assert pagination.available_pages == [31, 32, 33, 34, 35]
        assert pagination.prev_page == 32
        assert pagination.next_page == 34

    def test_middle2(self):
        pagination = Pagination(items_count=14,
                                items_per_page=5,
                                current_page=2,
                                show_pages_count=5)

        assert pagination.total_pages_count == 3
        assert pagination.current_page == 2
        assert pagination.show_pages_count == 5
        assert pagination.available_pages == [1, 2, 3]
        assert pagination.prev_page == 1
        assert pagination.next_page == 3

    def test_end(self):
        pagination = Pagination(items_count=199,
                                items_per_page=5,
                                current_page=40,
                                show_pages_count=5)

        assert pagination.total_pages_count == 40
        assert pagination.current_page == 40
        assert pagination.show_pages_count == 5
        assert pagination.available_pages == [36, 37, 38, 39, 40]
        assert pagination.prev_page == 39
        assert pagination.next_page is None

    def test_end2(self):
        pagination = Pagination(items_count=13,
                                items_per_page=5,
                                current_page=3,
                                show_pages_count=5)

        assert pagination.total_pages_count == 3
        assert pagination.current_page == 3
        assert pagination.show_pages_count == 5
        assert pagination.available_pages == [1, 2, 3]
        assert pagination.prev_page == 2
        assert pagination.next_page is None

    def test_page_out_of_range(self):
        pagination = Pagination(items_count=13,
                                items_per_page=5,
                                current_page=4,
                                show_pages_count=5)
        assert pagination.current_page == 1

    def test_page_out_of_range2(self):
        pagination = Pagination(items_count=13,
                                items_per_page=5,
                                current_page=0,
                                show_pages_count=5)
        assert pagination.current_page == 1
