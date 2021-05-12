print (" ")
print (" ")
print ("Welcome")
print (" ")
balance = 100


class initital:
    def interface (balance):
        print ("Your balance is", balance)
        print (" ")
        wd = int(input ("Please enter how much you would like to deposit or withdraw "))
        balance -= wd
        print (" ")
        print ("Your balance is now", balance)
        print (" ")
        return balance


    def sface (balance):
        cont = input("Would you like to continue? yes/no ")
        print (" ")
        if cont == "yes" or cont == "Yes" or cont == "YES":
            print(balance)
        elif cont == "no" or cont == "No" or cont == "NO":
            print ("test2")
        else:
            print("Invalid response, please try again")
            print (" ")
            print (" ")
            initital.sface(balance)

balance = initital.interface(balance)
initital.sface(balance
