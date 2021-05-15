# Adding the PIN check (14 May '21)
#
# Review: the purpose was to adapt this code to behave like your original code.
# 1. We reviewed a video of your code's behaviour and chose to reimplement the
# PIN check
# 2. The PIN check happens at a specific place in your code's flow: after the
# welcome message and before the first transaction.
# More properly we'd ask: is there any function that a real ATM has that doesn't
# involve the PIN? And we'd answer yes: an ATM may scan a real bank card for
# identity before checking the PIN. Thus, we wouldn't choose to *always* check
# the PIN first, we would choose to mark off particular bits as code as not
# being accessible until the PIN is checked. That means other bits of code could
# be executed despite the PIN not being checked, which matches real behaviour.
# In the meantime, we've elided that by always requiring the PIN check to match
# your video.
# 3. With the check always happening in the one place, I started by adding code
# at that place - print("got here") - and testing that it showed up as expected
# during a run
# 4. Now that we know we're editing the right place in the code, and after a
# brief detour to put the classes and constants in their own file, we considered
# what kind of object checking the PIN involves and we decided on a class called
# Security(): it knows what the PIN should be, how many attempts should be
# allowed at guessing it, and knows how to test if the PIN is right.
# 5. So we implemented implemented the security class and the whole
# functionality of obtaining the guess and checking if it was correct. The "got
# here" debug line was replaced with a call creating the class and calling the
# check PIN method. We kept going with that method until its behaviour matched
# what we wanted.
# You can consider that this stage worked much like your own - developing the
# behaviour in a straight-forward linear fashion.
# 6. Once we were happy that my code matched the behaviour of your code
# completely, we turned to integrating my code into my style.
# 7. First we considered that 'checkPIN' shouldn't actually care about input and
# outputs, only checking. To that end we made Security class belong to the Bank
# class where we also created a new process businessProcess003CheckPin(). This
# allowed us to move the input and output code into the atmHardware class, where
# they belong.
# 8. We then moved the constants used to the constants file, except for
# correct_pin. As we know the correct PIN would vary according to the particular
# user, we left it as is.
# 9. Finally we matched up the new English constants with French constants and
# refactored the existing code to support them.
#
# Were we doing this properly we would:
# a. Add unit tests against Security(), Security.checkPin(),
# Bank.businessProcess003CheckPin(), atmHardware.showRemainingAttempts() and
# atmHardware.askForPiN().
# Some programmers argue that unit tests should be done *before* writing the
# code they test.
# b. Have each protected business process method check for the security status
# and call Security.checkPin() if required. This allows the ATM to have a
# process for checking the card first, or perhaps cycling through advertising
# onscreen, without needing a card to activate.
#
# Next time we should also start observing some of the Python style guide more
# closely! https://www.python.org/dev/peps/pep-0008
#
#
# Commentary! (12 May '21)
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
