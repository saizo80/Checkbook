import tkinter as tk
from tkinter import ttk
import checkbookFunctions, os

class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
          
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
        
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
        
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (MainPage, TransactionsPage, BudgetsPage, addTransaction): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # MainPage, TransactionsPage, BudgetsPage respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(MainPage) 
    
    # to display the current frame passed as a parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def updateAll(self):
        for f in self.frames:
            self.frames.get(f).update()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.label = ttk.Label(self, text ="Main Page", font = LARGEFONT) 
        self.label.configure(anchor="center")
        self.label.pack(fill=tk.X, pady=10)
        
        button1 = ttk.Button(self, text="Transactions", command = lambda : controller.show_frame(TransactionsPage))
        button1.pack(fill=tk.X, pady=10)
        
        button2 = ttk.Button(self, text="Budget Goals", command = lambda : controller.show_frame(BudgetsPage))
        button2.pack(fill=tk.X, pady=10)
        
        killButton = ttk.Button(self, text="Quit", command = tty.kill)
        killButton.pack(fill=tk.X, pady=10)
        
    def button3Click(self):
        tty.jam(self.label)
    def update(self):
        pass
        
class TransactionsPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        
        label = ttk.Label(self, text ="Transactions", font = LARGEFONT) 
        label.configure(anchor="center")
        label.pack(fill=tk.X, pady=10)
        
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALLFONT, undo=True, wrap='word')
        self.txt.pack(padx=2, pady=2)
        self.txt.insert(1.0, tty.getTransactions())

        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.pack()
        self.txt['yscrollcommand'] = scrollb.set
   
        button2 = ttk.Button(self, text ="Add Transaction", command = lambda : controller.show_frame(addTransaction)) 
        button2.pack(fill=tk.X, pady=10)
        
        returnButton = ttk.Button(self, text ="Return", command = lambda : controller.show_frame(MainPage)) 
        returnButton.pack(fill=tk.X, pady=10)
        
    def temp(self, controller):
        print(tty.transReport())
        self.updateAll(controller)
        
    def updateAll(self, controller):
        controller.updateAll()
        
    def update(self):
        self.txt.delete("1.0", "end")
        self.txt.insert(1.0, tty.getTransactions())

class addTransaction(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Add Transaction:", font = LARGEFONT)
        #label.grid(row=1, column=2)
        label.pack()

        # - - - - - - - - - - - - - - - 
        # Specify Budget Type:
        self.budgetType = tk.StringVar()
        self.budgetType.set("0")
        budgetFrame = ttk.LabelFrame(self, text="Budget Type", relief=tk.RIDGE, padding=6)
        #budgetFrame.grid(row=3, column=1, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        budgetFrame.pack()
        
        budgetrow = 1
        for i in tty.budgets:
            budget = ttk.Radiobutton(budgetFrame,text=tty.budgets.get(i).name,
                                     variable=self.budgetType,
                                     value=tty.budgets.get(i).name)
            #budget.grid(row=budgetrow,column=1, sticky=tk.W + tk.N)
            budget.pack()
            budgetrow += 1
        
        
        # - - - - - - - - - - - - - - -
        # Specify Amount:
        self.amount = tk.StringVar()
        self.amount = ""
        
        amountFrame = ttk.LabelFrame(self, text="Amount", relief=tk.RIDGE, padding=6)
        #amountFrame.grid(row=2, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        amountFrame.pack()
        
        self.amountEntry = ttk.Entry(amountFrame)
        #self.amountEntry.grid(row=1,column=1, sticky=tk.W+tk.N)
        self.amountEntry.pack()
        
        # - - - - - - - - - - - - -
        # Description:
        self.description = tk.StringVar()
        self.description = ""
        
        descriptionFrame = ttk.LabelFrame(self, text="Description", relief=tk.RIDGE, padding=6)
        #descriptionFrame.grid(row=3, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        descriptionFrame.pack()
        
        self.description = tk.Text(descriptionFrame, height=10, width=20)
        #self.description.grid(row=1,column=1, sticky=tk.W+tk.N)
        self.description.pack()
        
        # - - - - - - - - - - - - - 
        # Update and exit buttons
        enterButton = ttk.Button(self, text="Enter", width=25)
        #enterButton.grid(row=4,column=1)
        enterButton.pack()
        
        
        quitButton = ttk.Button(self, text ="Cancel", width=25, command = lambda : controller.show_frame(TransactionsPage))
        #quitButton.grid(row=6, column=1)
        quitButton.pack()
""" 
    def passInfo(self, parent, controller):
        if (self.tranType.get() == "Deposit"):
            self.budgetType.set("")
    
        amount1 = float(self.amountEntry.get())
        
        tty.addTransaction(self.tranType.get(), amount1,
                                self.budgetType.get(), transactionDate, 
                                self.description.get("1.0", "end"))
        
        
        controller.show_frame(transactionMenu)
"""
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
class BudgetsPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        
        label = ttk.Label(self, text ="Budget Goals", font = LARGEFONT) 
        label.configure(anchor="center")
        label.pack(fill=tk.X, pady=10)
   
        button2 = ttk.Button(self, text ="Report", command = self.temp)  
        button2.pack(fill=tk.X, pady=10)
        
        returnButton = ttk.Button(self, text ="Return", command = lambda : controller.show_frame(MainPage)) 
        returnButton.pack(fill=tk.X, pady=10)
    def temp(self):
        print (tty.bugReport())
    def update(self):
        pass
   
def center(win):
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()
    
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y)) 

if __name__ == "__main__":
    LARGEFONT = ("Arial", 35)
    SMALLFONT = ("Arial", 13)
    tty = checkbookFunctions.Functions()
    
    app = tkinterApp() 
    
    app.geometry("400x550")
    #app.maxsize(500, 500)
    
    app.title("CheckBook")
    
    center(app)
    
    os.system("clear")
    
    app.mainloop()        