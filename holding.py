class editTransactions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Edit Transaction:", font=LARGEFONT)
        label.pack(pady=10,padx=10)
        
        self.combobox_value = tk.StringVar()
        self.combo = ttk.Combobox(self, height=10, width=50, textvariable=self.combobox_value)
        self.combo.pack()
        try:
            self.combo['values'] = tty.getTransactionsCombo()
        except:
            pass
        
        # - - - - - - - - - - - - - - - - -
        # Budget Type
        self.budgetType = tk.StringVar()
        self.budgetType.set("0")
        self.budgetFrame = tk.Frame(self, relief=tk.RIDGE)
        self.budgetFrame.pack(pady=5)
        
        self.budgetButton = ttk.Button(self.budgetFrame, text="Change Budget", command = self.showBudget)
        self.budgetButton.pack()
        
        # - - - - - - - - - - - - - - - - -
        # Amount
        self.amount = tk.StringVar()
        self.amount = ""
        
        self.amountFrame = tk.Frame(self, relief=tk.RIDGE)
        self.amountFrame.pack(pady=5)
        self.amountEntry = ttk.Entry(self.amountFrame)
        
        self.amountButton = ttk.Button(self.amountFrame, text="Change Amount", command = self.showAmount)
        self.amountButton.pack()

        # - - - - - - - - - - - - - - - - -
        # Date
        self.date = tk.StringVar()
        self.date = ""
        
        self.dateFrame = tk.Frame(self, relief=tk.RIDGE)
        self.dateFrame.pack(pady=5)
        
        self.dateButton = ttk.Button(self.dateFrame, text="Change Date", command=self.showDate)
        self.dateButton.pack()
        self.dateEntry = ttk.Entry(self.dateFrame)
        
        # - - - - - - - - - - - - - - - - -
        # Description:
        
        self.description = tk.StringVar()
        self.description = ""
        
        self.descriptionFrame = tk.Frame(self, relief=tk.RIDGE)
        self.descriptionFrame.pack(pady=5)
        
        self.description = tk.Text(self.descriptionFrame, height=10, width=20)
        self.description.configure(font=SMALLFONT)
        
        self.descriptionButton = ttk.Button(self.descriptionFrame, text="Change Description", command =self.showDescription)
        self.descriptionButton.pack()
        
        # - - - - - - - - - - - - - - - - - - 
        # Delete
        
        deleteFrame = tk.Frame(self, relief=tk.RIDGE)
        deleteFrame.pack(pady=5)
        
        deleteButton = ttk.Button(deleteFrame, text="Delete", command = lambda : self.deleteMethod(controller))
        deleteButton.pack()
        
        enterButton = ttk.Button(self, text="Enter", width=25, command = lambda : self.submitChanges(controller))
        enterButton.pack(pady=10)
        
        quitButton = ttk.Button(self, text="Cancel", width=25, command= lambda : self.reset(controller))
        quitButton.pack()
    
    def showBudget(self):
        self.budgetButton.destroy()
        budgetrow, budgetcolumn = 1, 1
        for i in tty.budgets:
            budget = ttk.Radiobutton(self.budgetFrame,text=tty.budgets.get(i).name,
                                     variable=self.budgetType,
                                     value=tty.budgets.get(i).name)
            budget.grid(row=budgetrow,column = budgetcolumn, sticky=tk.W + tk.N)
            #budget.pack()
            if budgetcolumn is 2:
                budgetcolumn = 1
                budgetrow += 1
            else:
                budgetcolumn +=1
        self.budgetType.set("{}".format(tty.comboboxReturn(self.combobox_value.get()).budget))
    
    def showAmount(self):
        self.amountButton.destroy()
        self.amountEntry.insert(0, "{:.2f}".format(tty.comboboxReturn(self.combobox_value.get()).amount))
        self.amountEntry.pack()
    
    def showDate(self):
        self.dateButton.destroy()
        self.dateEntry.insert(0, tty.comboboxReturn(self.combobox_value.get()).date)
        self.dateEntry.pack()
    
    def showDescription(self):
        self.descriptionButton.destroy()
        self.description.insert("1.0", tty.comboboxReturn(self.combobox_value.get()).descrip)
        self.description.pack()
        
    def reset(self, controller):
        controller.showFrameAndDestroy(TransactionsPage, editTransactions)
    
    def deleteMethod(self, controller):
        if messagebox.askyesno("Warning", "Delete {}?".format(self.combobox_value.get())):
            tty.removeTransaction(self.combobox_value.get())
            controller.updateAll()
            controller.showFrameAndDestroy(TransactionsPage, editTransactions)
        
    
    def update(self):
        try:
            self.combo['values'] = tty.getTransactionsCombo()
        except:
            pass
    
    def submitChanges(self, controller):
        date = self.dateEntry.get()
        amount = self.amountEntry.get()
        descrip = self.description.get("1.0", "end")
        budget = self.budgetType.get()
        data = self.combobox_value.get()
        tty.editTransaction(date, budget, amount, descrip, data)
        controller.updateAll()
        controller.showFrameAndDestroy(TransactionsPage, editTransactions)