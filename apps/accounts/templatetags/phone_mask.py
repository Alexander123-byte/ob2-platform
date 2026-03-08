from django import template

register = template.Library()


@register.filter
def format_phone(phone_number):
    """Форматирует номер телефона в вид +7(000)-000-00-00"""
    if phone_number and len(phone_number) >= 11:
        # Убираем все не-цифры
        digits = ''.join(filter(str.isdigit, phone_number))
        if len(digits) == 11 and digits.startswith('7'):
            return f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        elif len(digits) == 11 and digits.startswith('8'):
            digits = '7' + digits[1:]
            return f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return phone_number
