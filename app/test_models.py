import json
from app.models import Pagination, Category


class TestCategory:
    def test_json(self):
        category = Category(12, 'Name')
        category_dict = json.loads(category.json)
        assert category_dict == {'id': 12, 'title': 'Name'}

    def test_from_json(self):
        category = Category.from_json('{"id": 12, "title": "Name"}')
        assert category.id == 12
        assert category.title == 'Name'


class TestPagination:
    def test_beginning(self):
        pagination = Pagination(items_count=200,
                                items_per_page=5,
                                current_page=1,
                                show_pages_count=5)

        assert pagination.total_pages_count == 40
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
        assert pagination.available_pages == [1, 2, 3]
        assert pagination.prev_page == 2
        assert pagination.next_page is None
