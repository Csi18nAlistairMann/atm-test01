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
MSG_EN_INCORRECT_REMAINING_1 = "Incorrect, "
MSG_EN_INCORRECT_REMAINING_2 = " remaining attempts"
MSG_EN_ENTER_PIN = "Please enter your PIN "
# French
CONST_FR = 'fr'
MSG_FR_YOUR_BALANCE_WAS = "Votre solde était "
MSG_FR_YOUR_BALANCE_IS = "Votre solde est maintenant "
MSG_FR_HOW_MUCH = (
    "Veuillez saisir le montant que vous souhaitez déposer ou retirer ")
MSG_FR_WELCOME = "Bienvenue"
MSG_FR_INVALID_INPUT_TRY_AGAIN = "Réponse non valide, veuillez réessayer"
MSG_FR_CONTINUE_YN = "Voulez-vous continuer? Y (oui)/N (Non) "
MSG_FR_INCORRECT_REMAINING_1 = "Incorrect, "
MSG_FR_INCORRECT_REMAINING_2 = " tentatives restantes"
MSG_FR_ENTER_PIN = "Veuillez saisir votre code PIN "

#
# Bank constants
CONST_MAX_PIN_ATTEMPTS = 3
CONST_INITIAL_BALANCE = 100

#
# Other constants
CONST_WAS = "was"
CONST_IS = "is"
CONST_YES = "yes"
CONST_NO = "no"
CONST_OTHER = "other"
CONST_OK = 'ok'
CONST_NOK = 'nok'
