#
# Commentary!
#
# Have a look through the code first and remember that it does exactly what
# your code does. To the end-user, there's no difference at all. Think of it
# like with math: it's true that 4+4 = 1+1+2+1+3 - so it is that both our
# implementations satisfactorily address the original question.
#
# In a real sense then, the difference between your code and my code is
# entirely cosmetic, but it's in that cosmetic difference that you start to see
# a different understanding of the original problem, and a different way of
# handling potential future changes the paying client might have.
#
# As a programmer you'll come across this alot: your code achieves what was
# asked but doesn't meet what they're expecting cosmetically.
#
# My lines of code is 10x yours, (and probably took 10x longer to write), so
# probably will cost the client at least 10x. However it should become clear
# that extending functionality will probably then take 1/10th the code, 1/10th
# as long to write and so cost 1/10th as much as extending yours. Not to mention
# that if I added Unit Tests, my code would probably crash 1/10th as much. At
# least the first time! Maybe 1/100th the time and cost to add a second change
# and so on ;-)
#
# Let's look at the wholly cosmetic changes that makes my code better than
# yours even though it does exactly the same thing.
#
# 1. I've divided the code into sections: constants, classes, set up, main loop
# and clean up. Another time I would put them into separate files which assists
# in allowing code re-use. In particular I've moved your classes above the code
# executed at start: related code should be together.
#
# 2. I've revisited how your classes work. A class creates an Object that
# implements a model of something in the real world. Your code models two
# things: the hardware of an ATM which can display output and accept input from
# a user stood in front of it; and a bank account which can show, accept and
# adjust balances. Higher-level code should not be concerned with the details of
# lower-level code. To that end then, we can consider if there's an object that
# encompasses both ATM hardware and Bank account and there is: the Bank itself.
# So I've created a third new class - Bank() - and hidden the complexity of the
# main loop within it.
#
# 3. I changed alot of the names. The most important consideration with naming
# is telling yourself in six months time what it is you were trying to achieve.
# initital.sface() is less descriptive. bank.bankAccount.setBalance(value) is
# more descriptive. After compilation or interpreting into bytecode, there is
# zero code difference in any language between using 'i' as a variable name or
# 'indexIntoBankAccounts'. In the 80s there might was value to saving disk
# space on short names but no more - so err on the side of long and
# descriptive!
#
# 4. Getters and Setters. An object should persist its own data. Consider the
# atmHardware() class which has a language it should use. Rather than
# constantly pass the language in as a parameter to every method we instead use
# a setter - setLanguage(). When we want to know the language, each method uses
# the getter - getLanguage(). Advantages:
# a. Because the Object persists the language, we don't need to pass it in and
# don't need to consider it at the top level of the code
# b. If we want to change the behaviour we only have a single place in the code
# that needs changing. So for the language we might want to check if the
# language we intend to change to is actually supported, we can add that check
# in the setter without needing to check anything anywhere else.
#

# ---------------------------------------------
# Section 1: constants
#
# A constant is a variable who's value does not change throughout the life of
# a run. Some constants are built in (True, False); messages sent to the user
# are usually constants, and there's often others. By defining the constants
# here someone can later improve things (such as my bad French) without needing
# access to the code itself. For instance, this can help limit the damage a
# mischievous translator could do.
#  A second reason is to reduce errors. For instance I used CONST_YES instead
# of "yes" in the code. That means I can't accidentally use "Yes" instead and
# so introduce a potential bug as "yes" != "Yes"
#
# Note that Python doesn't have constants so we use variables with uppercase
# names to indicate to ourselves we shouldn't be changing their contents.

#
# Language Constants
# English
CONST_EN = 'en'
MSG_EN_YOUR_BALANCE_WAS = "Your balance was "
MSG_EN_YOUR_BALANCE_IS = "Your balance is now "
# Note parenthesis used to keep lines under 80 chars long
MSG_EN_HOW_MUCH = (
    "Please enter how much you would like to deposit or withdraw ")
MSG_EN_WELCOME = "Welcome"
MSG_EN_INVALID_INPUT_TRY_AGAIN = "Invalid response, please try again"
MSG_EN_CONTINUE_YN = "Would you like to continue? yes/no "
# French
CONST_FR = 'fr'
MSG_FR_YOUR_BALANCE_WAS = "Votre solde était "
MSG_FR_YOUR_BALANCE_IS = "Votre solde est maintenant "
MSG_FR_HOW_MUCH = (
    "Veuillez saisir le montant que vous souhaitez déposer ou retirer ")
MSG_FR_WELCOME = "Bienvenue"
MSG_FR_INVALID_INPUT_TRY_AGAIN = "Réponse non valide, veuillez réessayer"
MSG_FR_CONTINUE_YN = "Voulez-vous continuer? Y (oui)/N (Non) "

#
# Other constants
CONST_WAS = "was"
CONST_IS = "is"
CONST_YES = "yes"
CONST_NO = "no"
CONST_OTHER = "other"
CONST_INITIAL_BALANCE = 100

# ---------------------------------------------
# Section 2: classes
#
# The class models some object in the real world. Your ATM code refers to two
# such objects: one is the ATM hardware with its screen and keyboard, and one
# is the account which is being adjusted for the user. We know they are
# different objects because its not normal for a bank account to assume you
# have a keyboard, and likewise wrong for a screen to assume you want to
# adjust money amounts through it.

# The ATM hardware assumes a screen to which it can send output, a keyboard
# from which it can receive input, and a language set up when its first
# used. The language right now is either French or English and assists in
# abstracting out the message being sent to the user from the content of
# that message. A later improvement might see Portuguese added, or a braille
# output added. In fact we could implement sending output to a printer
# instead of a screen, or have them ATM interact via email, etc.
class Bank():
    bankLanguage = ''
    bankAccount = ''
    atmMachine = ''

    def __init__(self, language):
        self.bankLanguage = language
        self.atmMachine = atmHardware(language)
        self.bankAccount = atmAccount()

    # Conduct a fake transaction
    def businessProcess001FakeATMTransaction(self):
        # show the balance
        bank.atmMachine.showBalanceToScreen(CONST_WAS,
                                            self.bankAccount.getBalance())
        bank.atmMachine.showNewLine()
        # get the amount to adjust from user and apply it
        wd = bank.atmMachine.obtainAmountFromKeyboard()
        self.bankAccount.applyTransaction(wd)
        # show the new balance
        bank.atmMachine.showNewLine()
        bank.atmMachine.showBalanceToScreen(CONST_IS,
                                            self.bankAccount.getBalance())
        bank.atmMachine.showNewLine()

    # Get a yes or no from the user: anything else? Ask again
    def businessProcess002CheckDoAgain(self):
        reply = CONST_OTHER
        while (reply == CONST_OTHER):
            reply = bank.atmMachine.showContinueYesOrNo()
            bank.atmMachine.showNewLine()
            if reply == CONST_YES:
                bank.atmMachine.printToScreen(bank.bankAccount.getBalance())
                reply = CONST_YES
            elif reply == CONST_NO:
                bank.atmMachine.printToScreen("test2")
            else:
                bank.atmMachine.showInvalidTryAgain()
                bank.atmMachine.showNewLine()
                bank.atmMachine.showNewLine()
                reply = CONST_OTHER
        return reply

# The ATM is an object of its own too. It doesn't really care about what the
# user means or expects to happen, it just cares about displaying messages to
# that user (Output) and receiving direction from that user (Input).
#
# I add 'language' to this object as by abstracting it out we can more easily
# make the ATM useful to foreign language speakers, perhaps improving sales
class atmHardware():
    language = ''

    # Initialising an ATM must include the language expected
    def __init__(self, lang):
        self.setLanguage(lang)

    def setLanguage(self, lang):
        self.language = lang

    def getLanguage(self):
        return self.language

    # Methods common to input and output
    def printToScreen(self, msg):
        print(msg)

    # -- Output methods --
    # By putting each kind of interaction into its own method we can leave room
    # for changes later: changes to language, changes to output method and so
    # forth. If the ATM had a screen output, and a Braille output, we might put
    # them in their own classes.
    def showBalanceToScreen(self, tense, balance):
        if self.getLanguage() == CONST_FR:
            if tense == CONST_WAS:
                msg = MSG_FR_YOUR_BALANCE_WAS + str(balance)
            else:
                msg = MSG_FR_YOUR_BALANCE_IS + str(balance)
        else:
            if tense == CONST_WAS:
                msg = MSG_EN_YOUR_BALANCE_WAS + str(balance)
            else:
                msg = MSG_EN_YOUR_BALANCE_IS + str(balance)
        self.printToScreen(msg)

    def showNewLine(self):
        msg = " "
        self.printToScreen(msg)

    def showWelcome(self):
        if self.getLanguage() == CONST_FR:
            msg = MSG_FR_WELCOME
        else:
            msg = MSG_EN_WELCOME
        self.printToScreen(msg)

    def showInvalidTryAgain(self):
        if self.getLanguage() == CONST_FR:
            msg = MSG_FR_INVALID_INPUT_TRY_AGAIN
        else:
            msg = MSG_EN_INVALID_INPUT_TRY_AGAIN
        self.printToScreen(msg)

    # -- Input methods --
    # Again I'm keeping code with similar tasks together. One thing important
    # with input is we want to make sure it's sanitised - we don't want user's
    # able to screw the code up. We barely santise code here.

    # No sanitising here: no decimals accepted because of int, which will
    # crash if we don't receive a number at all
    def obtainAmountFromKeyboard(self):
        if self.getLanguage() == CONST_FR:
            msg = MSG_FR_HOW_MUCH
        else:
            msg = MSG_EN_HOW_MUCH
        return int(input(msg))

    # Sanitising of a sort done here: we only accept the first character typed
    # in, we force that character to lower, and we return not that character
    # but a constant that we choose
    def showContinueYesOrNo(self):
        if self.getLanguage() == CONST_FR:
            msg = MSG_FR_CONTINUE_YN
        else:
            msg = MSG_EN_CONTINUE_YN
        response = input(msg)
        lcFirstLetter = response[0].lower()
        if lcFirstLetter == "y":
            return CONST_YES
        elif lcFirstLetter == "n":
            return CONST_NO
        return CONST_OTHER

# The ATM Account is an object of its own kind: it can report what the balance
# is, adjust itself relatively or absolutely, and can do so either manually
# where the account must interact with a user thought to be physically present
# or be prepared to work automatically - say in response to a standing order.
class atmAccount():
    def setBalance(self, balance):
        self.balance = balance

    def getBalance(self):
        return self.balance

    def adjustBalance(self, wd):
        self.setBalance(self.getBalance() - wd)

    def applyTransaction(self, wd):
        self.adjustBalance(wd)

# ---------------------------------------------
# Section 3: Set up
#
# Almost always we'll want to do some housekeeping work ahead of getting the
# real stuff done: loading data, preparing variables and so forth.

#
# Defaults
startBalance = CONST_INITIAL_BALANCE

#
# Start up
bank = Bank(CONST_EN)
bank.bankAccount.setBalance(startBalance)
bank.atmMachine.showNewLine()
bank.atmMachine.showNewLine()
bank.atmMachine.showWelcome()
bank.atmMachine.showNewLine()

# ---------------------------------------------
# Section 4: Main loop
#
# Execution will spend most of its time in the Main Loop, like in a game:
# Check if the user has moved | redraw screen | check for movement again.
#

reply = CONST_YES  # Python has no do loop, so fake it
while (reply == CONST_YES or reply == CONST_OTHER):
    #
    # Conduct a transaction
    currentBalance = bank.businessProcess001FakeATMTransaction()
    #
    # Check if we need to do another
    reply = bank.businessProcess002CheckDoAgain()

# ---------------------------------------------
# Section 5: Clean up
#
# If we claimed resources (files, memory etc) then we use this last
# opportunity to release them. The ATM code doesn't claim any so
# this section empty
