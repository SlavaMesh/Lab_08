from django import template

register = template.Library()


@register.filter()
def censored(value: str):

    CENSORED_WORDS = {
        'спорт': 'с****',
        'Спорт': 'C****',
        'мода': 'м***',
        'Мода': 'М***',
        'кино': 'к***',
        'Кино': 'К***',
        'политика': 'п*******',
        'Политика': 'П*******',
    }

    if isinstance(value, str):
        for word in CENSORED_WORDS.keys():
            value = value.replace(word, CENSORED_WORDS[word])
    else:
        raise ValueError

    return value

