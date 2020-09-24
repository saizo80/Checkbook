class Transaction():
    def __init__(self, amount, budget, date, descrip):
        self.amount = amount
        self.budget = budget
        self.date = date
        self.descrip = descrip
    def toString(self):
        return """${}
{}
{}
{}""".format(self.amount, self.budget, self.date, self.descrip)