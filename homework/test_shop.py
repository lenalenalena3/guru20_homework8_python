"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_new():
    return Product("book_new", 1.1, "This is a book", 50)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        count_less = 999  # меньше чем есть в наличии
        count_equals = 1000  # равно значению, которое есть в наличие
        count_more = 1001  # больше чем есть в наличии
        assert product.check_quantity(count_less), (
            f"Не выполняется проверка: запрошено меньше, чем доступно"
            f"\nДля продукта '{product.name}': доступно {product.quantity}, запрошено {count_less} "
        )
        assert product.check_quantity(count_equals), (
            f"Не выполняется проверка: запрошено меньше, чем доступно"
            f"\nДля продукта '{product.name}': доступно {product.quantity}, запрошено {count_equals} "
        )
        assert not product.check_quantity(count_more), (
            f"Не выполняется проверка: запрошено больше, чем доступно"
            f"\nДля продукта '{product.name}': доступно {product.quantity}, запрошено {count_more}")

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(950)
        assert product.quantity == 50  # проверка, когда продукта хватает
        product.buy(50)
        assert product.quantity == 0  # проверка, когда продукта хватает

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        count = product.quantity
        with pytest.raises(ValueError) as exception:
            product.buy(1050)
        # проверка, что возникает ошибка и количество продукта не изменилось
        assert exception.typename == 'ValueError' and product.quantity == count


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, product):  # проверка: добавления продукта в корзину без указания количества
        # создание данных для проверки
        cart_test = Cart()
        # добавление продукта в корзину
        cart_test.add_product(product)
        # проверка, что продукт добавлен и его количество =1
        assert product in cart_test.products and cart_test.products[
            product] == 1

    def test_add_product_some(self, product):  # проверка: Если продукт уже есть в корзине, то увеличиваем количество
        # создание данных для проверки
        cart_test = Cart()
        cart_test.add_product(product, 3)
        # добавление продукта в корзину
        cart_test.add_product(product, 2)
        # проверка, что для продукта увеличилось количество до 5
        assert product in cart_test.products and cart_test.products[
            product] == 5

    def test_add_product_error(self, product):  # проверка: появление ошибки при добавлении в корзину с количеством < 1
        # создание данных для проверки
        cart_test = Cart()
        # добавление продукта в корзину
        with pytest.raises(ValueError) as exception:
            cart_test.add_product(product, 0)
        # проверка, что продукт не был добавлен
        assert product not in cart_test.products

    # ****************************************

    def test_remove_product_not_count(self, product,
                                      product_new):  # проверка: Если remove_count не передан, то удаляется вся позиция
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        cart_test.products[product_new] = 7
        # удаление продукта без указания количества
        cart_test.remove_product(product)
        # проверка, что удален только продукт product
        assert product not in cart_test.products and product_new in cart_test.products

    def test_remove_product_some(self, product,
                                 product_new):  # проверка: Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        cart_test.products[product_new] = 7
        # удаление продукта с указанием количества, большего чем есть
        cart_test.remove_product(product, 50)
        # проверка, что удален только продукт product, количество продукта product_new не изменилось
        assert product not in cart_test.products and product_new in cart_test.products and cart_test.products[
            product_new] == 7

    def test_remove_product(self, product, product_new):  # проверка: удаление продукта из корзины
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        cart_test.products[product_new] = 7
        # удаление продукта с указанием количества, меньшего чем есть
        cart_test.remove_product(product, 3)
        # проверка, что уменьшено количество продукта product
        assert product in cart_test.products and cart_test.products[
            product] == 2

    def test_remove_product_error(self, product,
                                  product_new):  # проверка: появление ошибки при удалении отсутствующего продукта
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        # удаление продукта, которого нет в корзине
        with pytest.raises(ValueError) as exception:
            cart_test.remove_product(product_new)
        # проверка, что возникает ошибка и содержание корзины не изменилось
        assert exception.typename == 'ValueError' and product in cart_test.products and product_new not in cart_test.products

    # ****************************************

    def test_clear(self):  # проверка: очистка пустой корзины
        # создание данных для проверки
        cart_test = Cart()
        # очищение корзины
        cart_test.products.clear()
        # проверка, что корзина пустая
        assert not cart_test.products, "Словарь должен быть пустым"

    def test_clear_full(self, product, product_new):  # проверка: очистка полной корзины
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        cart_test.products[product_new] = 7
        # очищение корзины
        cart_test.products.clear()
        # проверка, что корзина пустая
        assert not cart_test.products, "Словарь должен быть пустым"

    # ****************************************

    def test_get_total_price(self, product, product_new):  # проверка: подсчет общей стоимости корзины
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        cart_test.products[product_new] = 7
        # проверка, что общая стоимость корректна
        assert cart_test.get_total_price() == 507.7

    # ****************************************

    def test_buy(self, product, product_new):  # проверка: успешная покупка
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 1000
        cart_test.products[product_new] = 7
        # покупка
        cart_test.buy()
        # проверка остатков продуктов на складе после покупки
        assert product.quantity == 0 and product_new.quantity == 43, (
            f"Остатки на складе не соответствуют значениям после покупки")

    def test_buy_error(self, product, product_new):  # проверка: не успешная покупка
        # создание данных для проверки
        cart_test = Cart()
        cart_test.products[product] = 5
        cart_test.products[product_new] = 55
        # покупка
        with pytest.raises(ValueError) as exception:
            cart_test.buy()
        # проверка, что возникает ошибка и что остатки продуктов на складе не изменились
        assert exception.typename == 'ValueError' and product.quantity == 1000 and product_new.quantity == 50
