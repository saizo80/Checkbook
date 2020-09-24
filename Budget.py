class Budget():
    def __init__(self, name, cap, current):
        self.name = name
        self.cap = cap
        self.current = current
    
    def toString(self):
        return """{}
Cap: ${:.2f}
Current : ${:.2f}
Remaining: ${:.2f}""".format(self.name, self.cap, self.current, self.cap + self.current)