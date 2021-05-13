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
# Section 3: Set up
#
# Almost always we'll want to do some housekeeping work ahead of getting the
# real stuff done: loading data, preparing variables and so forth.

#
# Imports
from classes import *
from constants import *

#
# Defaults

#
# Start up
bank = Bank(CONST_EN)
bank.bankAccount.setBalance(CONST_INITIAL_BALANCE)
# Show welcome and check PIN
bank.atmMachine.showNewLine()
bank.atmMachine.showNewLine()
bank.atmMachine.showWelcome()
bank.atmMachine.showNewLine()
bank.businessProcess003CheckPin()

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
