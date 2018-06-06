"""
This module contains all models for the application
"""

from typing import List, Union
from math import ceil

PAGES_COUNT_IN_PAGINATION = 10


class Category:
    """
    Simple category model
    """
    def __init__(self, obj_id: int, title: str):
        self.obj_id = obj_id
        self.title = title


class AllCategories:
    """
    Model for collection of all categories
    """
    def __init__(self, categories: List[Category]):
        self.categories = categories
        self.category_ids = [category.obj_id for category in categories]


class Offer:
    """
    Model for a product offer
    """
    def __init__(self, offer_id: int, shop_name: str, price: float, url: str):
        self.id = offer_id
        self.shop_name = shop_name
        self.price = price
        self.url = url


class Product:
    """
    Model for a product
    """
    def __init__(self, product_id: int,
                 category_id: int,
                 title: str,
                 description: str,
                 image_urls: List[str],
                 offers: List[Offer]):

        self.id = product_id
        self.category_id = category_id
        self.title = title
        self.description = description
        self.image_urls = image_urls
        self.offers = offers

    @property
    def min_price(self) -> float:
        """
        Return minimum of product offer prices
        :return: minimal price
        """
        return min([offer.price for offer in self.offers])

    @property
    def max_price(self) -> float:
        """
        Return maximum product offer prices
        :return: maximal price
        """
        return max([offer.price for offer in self.offers])

    @property
    def sorted_offers(self) -> List[Offer]:
        """
        Return offers sorted by price, from minimal to maximal
        :return: List of sorted :class:`Offer` objects
        """
        return sorted(self.offers, key=lambda offer: offer.price)


class Pagination:
    """
    Class which provides data for pagination component, calculates and provides:
    - total pages of items
    - page numbers to show on a HTML page
    - whether prev, next page are available from the current page
    - page number validation
    """
    def __init__(self, items_count: int,
                 items_per_page: int,
                 current_page: int,
                 show_pages_count: int=PAGES_COUNT_IN_PAGINATION):

        self.show_pages_count = show_pages_count
        self.total_pages_count = ceil(items_count / items_per_page)
        self.current_page = self.validate_page_number(current_page)

    @property
    def prev_page(self) -> Union[int, None]:
        """
        Calculates previous page number
        :return: previous page number or `None`
        """
        page = self.current_page - 1
        if page < 1:
            return None
        else:
            return page

    @property
    def next_page(self) -> Union[int, None]:
        """
        Calculates next page number
        :return: next page number or `None`
        """
        page = self.current_page + 1
        if page > self.total_pages_count:
            return None
        else:
            return page

    @property
    def available_pages(self) -> List[int]:
        """
        Calculates available page number to be shown on the page
        :return: List of page number to be shown
        """

        start_page = self.current_page - (self.show_pages_count // 2)
        if start_page < 1:
            start_page = 1

        end_page = start_page + self.show_pages_count - 1
        if end_page > self.total_pages_count:
            end_page = self.total_pages_count
            start_page = end_page - self.show_pages_count + 1

        prepare_pages = list(range(start_page, end_page+1))
        return [page for page in prepare_pages if page > 0]

    def validate_page_number(self, page_number: int) -> int:
        """
        Returns always valid page number
        :return: the same number if valid or 1 if invalid
        """
        if 1 <= page_number <= self.total_pages_count:
            return page_number
        else:
            return 1
