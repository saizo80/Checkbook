class Budget():
    def __init__(self, name, cap, current):
        self.name = name
        self.cap = cap
        self.current = current
    
    def toString(self):
        return """{}
Cap: ${}
Current : ${}
Remaining: ${}""".format(self.name, self.cap, self.current, self.cap-self.current)