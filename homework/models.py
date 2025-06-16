class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        if self.quantity >= quantity:
            return True
        else:
            return False
        # raise NotImplementedError

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError
        # raise NotImplementedError

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count > 0:
            if product in self.products:
                self.products[product] += buy_count
            else:
                self.products[product] = buy_count
        else:
            raise ValueError
        # raise NotImplementedError

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:
            if remove_count is not None and remove_count < self.products[product]:
                self.products[product] = self.products[product] - remove_count
            else:
                del self.products[product]
        else:
            raise ValueError
        # raise NotImplementedError

    def clear(self):
        self.products.clear()
        # raise NotImplementedError

    def get_total_price(self) -> float:
        total_price = 0.0
        for key_prod, count_prod in self.products.items():
            total_price += key_prod.price * count_prod
        return total_price
        # raise NotImplementedError

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        original_cart = {product: product.quantity for product in self.products}
        try:
            for key_prod, count_prod in self.products.items():
                if key_prod.check_quantity(count_prod):
                    key_prod.quantity -= count_prod
                else:
                    raise ValueError(f"Недостаточно товара '{key_prod.name}'")
            self.products.clear()
        except Exception as e:
            for key_prod, count_prod in original_cart.items():
                key_prod.quantity = count_prod
            raise ValueError
        # raise NotImplementedError
