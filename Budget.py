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

    def report(self):
        return ("{}:\nLimit: ${:.2f}\nCurrent: ${:.2f}\nPercentage: "
            "{:.2f}%\nRemaining: ${:.2f}".format(self.name, self.cap, 
             self.current, (abs(self.current/self.cap*100)), 
             self.cap + self.current))