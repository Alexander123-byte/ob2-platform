from django import template

register = template.Library()


@register.filter
def format_phone(phone_number):
    """Форматирует номер телефона в вид +7(000)-000-00-00"""
    if not phone_number:
        return phone_number

    if phone_number and phone_number.startswith('+7(') and '-' in phone_number:
        return phone_number

    digits = ''.join(filter(str.isdigit, str(phone_number)))

    if len(digits) == 11 and digits.startswith('7'):
        return f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]
        return f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 10:
        return f"+7({digits[0:3]})-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

    return phone_number
