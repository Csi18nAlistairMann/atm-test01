from constants import *

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
class Security():
    correct_pin = '1234'
    max_attempts = CONST_MAX_PIN_ATTEMPTS

    def checkPin(self, pin):
        if pin == self.correct_pin:
            return CONST_OK
        return CONST_NOK


class Bank():
    bankLanguage = ''
    bankAccount = ''
    atmMachine = ''
    security = ''

    def __init__(self, language):
        self.bankLanguage = language
        self.atmMachine = atmHardware(language)
        self.bankAccount = atmAccount()
        self.security = Security()

    # Conduct a fake transaction
    def businessProcess001FakeATMTransaction(self):
        # show the balance
        self.atmMachine.showBalanceToScreen(CONST_WAS,
                                            self.bankAccount.getBalance())
        self.atmMachine.showNewLine()
        # get the amount to adjust from user and apply it
        wd = self.atmMachine.obtainAmountFromKeyboard()
        self.bankAccount.applyTransaction(wd)
        # show the new balance
        self.atmMachine.showNewLine()
        self.atmMachine.showBalanceToScreen(CONST_IS,
                                            self.bankAccount.getBalance())
        self.atmMachine.showNewLine()

    # Get a yes or no from the user: anything else? Ask again
    def businessProcess002CheckDoAgain(self):
        reply = CONST_OTHER
        while (reply == CONST_OTHER):
            reply = self.atmMachine.showContinueYesOrNo()
            self.atmMachine.showNewLine()
            if reply == CONST_YES:
                self.atmMachine.printToScreen(self.bankAccount.getBalance())
                reply = CONST_YES
            elif reply == CONST_NO:
                self.atmMachine.printToScreen("test2")
            else:
                self.atmMachine.showInvalidTryAgain()
                self.atmMachine.showNewLine()
                self.atmMachine.showNewLine()
                reply = CONST_OTHER
        return reply

    def businessProcess003CheckPin(self):
        attempts = 0
        pin = ''
        while (attempts < self.security.max_attempts and
               pin != self.security.correct_pin):
            if pin != '':
                self.atmMachine.showRemainingAttempts(
                    self.security.max_attempts - attempts)
            attempts += 1
            pin = self.atmMachine.askForPin()
            response = self.security.checkPin(pin)
            if (attempts == self.security.max_attempts and
               response == CONST_NOK):
                exit()

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

    def showRemainingAttempts(self, number):
        if self.getLanguage() == CONST_FR:
            msg = (MSG_FR_INCORRECT_REMAINING_1 + str(number) +
                  MSG_FR_INCORRECT_REMAINING_2)
        else:
            msg = (MSG_EN_INCORRECT_REMAINING_1 + str(number) +
                  MSG_EN_INCORRECT_REMAINING_2)
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

    def askForPin(self):
        if self.getLanguage() == CONST_FR:
            return input(MSG_FR_ENTER_PIN)
        else:
            return input(MSG_EN_ENTER_PIN)

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
