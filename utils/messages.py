from django.utils.translation import gettext

from uniq import settings


# auth_ messages
CONFIRM_EMAIL = gettext('Пожалуйста подтвердите ваш Email, чтобы завершить регистрацию')
ACCOUNT_EXIST = gettext('Пользователь с таким Email уже существует')
SUCCESS_REGISTER = gettext('Вы успешно зарегистрировались')
PASSWORD_CHANGED = gettext('Пароль изменен')
USER_DETAILS_CHANGED = gettext('Данные пользователя изменены')
RESET_LINK_SENT = gettext('Ссылка на восстановление пароля отправлена на ваш Email')
#######################################################
ACTIVATE_SUBJECT = gettext('Активация аккаунта')
RESET_SUBJECT = gettext('Восстановление пароля')

# US_CONFIRM_EMAIL = "Please verify your Email to finish registration"
# US_ACCOUNT_EXIST = "User with this Email already exist"
# US_SUCCESS_REGISTER = "You successfully registered"
# US_PASSWORD_CHANGED = "Password changed"
# US_USER_DETAILS_CHANGED = "User details changed"
# US_RESET_LINK_SENT = "Activation link has been sent to your Email"

#
# US_ACTIVATE_SUBJECT = 'Activate account'
# US_RESET_SUBJECT = 'Reset password'


# auth_ errors
PASSWORDS_NOT_SAME = gettext('Passwords don\'t match')
WRONG_PASSWORD = gettext('Wrong password')
EMAIL_DOESNT_EXIST = gettext('Email does not exist')
INVALID_RESET_LINK = gettext('Invalid reset password link')
ALREADY_EXIST = gettext('Email already exist')
INVALID_ACTIVATION_LINK = gettext('Invalid activation link')
NO_CREDENTIALS = gettext('Enter credentials')
WRONG_EMAIL_OR_PASSWORD = gettext('Wrong email or password')
EARLY_ATTEMPT = gettext('Resent password link was sent recently. Wait {0} minutes'.format(settings.WAITING_TIME_ATTEMPTS_MIN)) # noqa


