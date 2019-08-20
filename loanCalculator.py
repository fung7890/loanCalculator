# The borrower submits a loan request including the above loan amount and loan period 
# The investor will submit an offer with the above interest rate
# The borrower will accept the offer
# Check if the investor has sufficient balance in their account before they fund the loan
# The loan will be funded successfully and the loan status will be changed to `Funded` 
# The loan payment will be scheduled successfully on the system
# Once all the payments are successfully paid, the loan status will be `Completed`

# Payment calculations will be amortized, assuming monthly payments 


class User:
	def __init__(self, name, age, ID, balance): # User information
		self.name = name
		self.age = age
		self.ID = ID
		self.balance = balance
	
	def __str__(self):
		return 'User\'s name is: {self.name}, age: {self.age}, ID: {self.ID}'.format(self=self)

class Borrower(User):
	def __init__(self, name, age, ID, balance):
		User.__init__(self, name, age, ID, balance)

	def loan_request(self): # loan request with borrower's amount needed and payback period
		while True: # check if input is number
			amount = (input("BORROWER: Please enter the amount you wish to borrow in dollars (default is $5000.00 if you press ENTER without input): ") or "5000")
			if(check_if_num(amount, "dollars")): break

		while True:
			payback_period = (input("BORROWER: Please enter desired payback period in months (default is 6 months if you press ENTER without input): ") or "6")
			if(check_if_num(payback_period, "months")): break

		return(float(amount), float(payback_period))

	def accept_offer(self):
		accept = (input("BORROWER: Please enter YES if this interest rate is satisfactory or NO if it is not (default is YES if you press ENTER without input): ") or "YES")
		if accept.lower() == "yes":
			return True
		else:
			return False

class Investor(User):
	def __init__(self, name, age, ID, balance):
		User.__init__(self, name, age, ID, balance)

	def submit_offer(self): # interest rate offer submitted by investor based off borrower's amount and payback period
		while True:
			interest_rate = (input("INVESTOR: Please enter annual interest rate offer to this loan (default is 15% if you click ENTER without input): ") or "15")
			if(check_if_num(interest_rate, "interest rate percentage")): break

		return(float(interest_rate)/100)

class Loan:
	def __init__(self, borrower, investor, loanID):
		self.borrower = borrower
		self.investor = investor
		self.loanID = loanID
		self.loan_amount = 0
		self.loan_period = None
		self.interest_rate = 0
		self.lenmo_fee = 3
		self.loan_status = "UNFUNDED"
		self.borrower_offer_accepted = False
		self.loan_payment = 0

	def initialize_loan(self):

		# update summary
		print_summary(self)
		self.loan_amount, self.loan_period = self.borrower.loan_request() # get loan_amount and loan_period from borrower 
		print_summary(self)
		self.interest_rate = self.investor.submit_offer() # get interest rate offer from investor
		print_summary(self)
		self.borrower_offer_accepted = self.borrower.accept_offer()
		print_summary(self)

		if self.borrower_offer_accepted: # interest rate for loan has been accepted by borrower
			total_loan_amt = self.loan_amount + self.lenmo_fee
			if self.investor.balance >= total_loan_amt: # check if investor has sufficient balance for loan + fee
			
				# update users' balance 
				self.investor.balance -= total_loan_amt 
				self.borrower.balance += self.loan_amount 

				self.loan_status = "FUNDED" # update loan status
				print_summary(self)
			else:
				print("Investor has insufficient balance")
				input('Press ENTER to exit')
		else:
			print("Borrower has declined investor's offer")
			input('Press ENTER to exit')

		self.loan_payment = self.payment_calc(self.loan_amount, self.interest_rate, self.loan_period)
		print_summary(self)	

	# amortized payment calculations, assuming monthly payments 
	def payment_calc(self, loan_amount, interest_rate, num_payments):
		monthy_interest = interest_rate/12
		return loan_amount*((monthy_interest*(1+monthy_interest)**num_payments) / ((1+monthy_interest)**num_payments - 1))

	# borrower pays investor back with interest 
	def make_payments(self):

		if self.borrower.balance >= self.loan_payment: # check if borrower has enough to pay back
			self.loan_period -= 1
			
			# update users' balance 
			self.borrower.balance -= self.loan_payment
			self.investor.balance += self.loan_payment

			if self.loan_period == 0:
				self.loan_status = "COMPLETED"
				self.interest_rate = 0
				self.loan_amount = 0
				self.loan_payment = 0
		else:
			print("Borrower has insufficient funds to pay back loan payment for the month")	

# check if input is number
def check_if_num(check, message):
	if check.isdigit():
		return True
	else:
		print("Please enter a number in {}".format(message))
		return False

# print current summary of loan 
def print_summary(loan):
	print("\n" * 100) # clear screen
	template = ''' 
	___________________________
	########## Lenmo ##########					    
										
	 Loan ID: {}						
	 Loan Status: {}						
	___________________________
	 *BORROWER* 		    	  				
	 User ID: {}				   				
	 Name: {}
	 Balance (Private): ${:10.2f}
	___________________________      									
	 *INVESTOR* 
	 User ID: {} 	
	 Name: {}	
	 Balance (Private): ${:10.2f}
	___________________________
	 *LOAN INFORMATION*
	 Loan Amount: ${:10.2f}	       
	 Loan Period: {} Months

	 Interest Rate Offer: {}		  
	___________________________
	 *PAYMENT*
	 Payment: ${:10.2f}

		'''.format(loan.loanID, loan.loan_status,\
				   loan.borrower.ID, loan.borrower.name, loan.borrower.balance,\
				   loan.investor.ID, loan.investor.name, loan.investor.balance,\
				   loan.loan_amount, "N/A" if loan.loan_period == None else loan.loan_period, "N/A" if loan.interest_rate == 0 else str(int(loan.interest_rate*100))+"%",\
				   loan.loan_payment) 

	print(template)

def main():
	# emulate users
	borrow_usr = Borrower("Kenny", 26, "A652DE4K", 2000) 
	invest_usr = Investor("John", 35, "ASFKWI12", 10000)

	# emulate loan
	loan_1 = Loan(borrow_usr, invest_usr, "L48583")
	loan_1.initialize_loan()
	wait = input("Loan initialized, press ENTER to start payback")

	# emulate payback
	month = 0
	if loan_1.loan_status == "FUNDED":	
		while True:
			month += 1
			loan_1.make_payments()
			print_summary(loan_1)
			print("End of Month {}".format(month))

			if loan_1.loan_status == "COMPLETED":
				wait = input("Loan with interest has been paid back in full, please press ENTER to exit")
				break
			else:
				wait = input("Press ENTER for next month")

if __name__=="__main__":
	main()
