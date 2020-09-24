class Transaction():
    def __init__(self, amount, budget, date, descrip):
        self.amount = amount
        self.budget = budget
        self.date = date
        self.descrip = descrip.replace("\n", "")
    def toString(self):
        return """${:.2f}
{}
{}
{}""".format(self.amount, self.budget, self.date, self.descrip)
    def getCombo(self):
        return "{} - {} - {:.2f} - {}".format(self.date, self.budget, self.amount, self.descrip)