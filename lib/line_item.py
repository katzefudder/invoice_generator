class Line_item:
    description = ''
    price = 0.00
    total_price = 0.00
    total_price_netto = 0.00
    amount = 0
    tax = 0
    total_tax = 0.0

    def __init__(self, description, price:float, amount:int, tax:int):
        if (price < 0):
            raise Exception('price cannot be negative')
        if (amount < 0):
            raise Exception('amount cannot be negative')

        self.description = description
        self.price = price
        self.amount = amount
        self.tax = tax

        self.total_price_netto = price * amount
        self.total_tax = self.total_price_netto * (tax / 100)
        self.total_price = self.total_price_netto + self.total_tax

    def get_description(self):
        return self.description

    def get_total_tax(self):
        return self.total_tax

    def get_total_price(self):
        return self.total_price

    def get_total_price_netto(self):
        return self.total_price_netto

    def get_amount(self):
        return self.amount