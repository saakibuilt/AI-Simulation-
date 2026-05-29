import json
import os
import threading
from flask import has_request_context

_thread_local = threading.local()

_locales_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'locales')
_default_locale = 'en'

with open(os.path.join(_locales_dir, 'en.json'), 'r', encoding='utf-8') as f:
    _translations = {
        _default_locale: json.load(f)
    }


def set_locale(locale: str):
    
    _thread_local.locale = _default_locale


def get_locale() -> str:
    if has_request_context():
        return _default_locale
    return getattr(_thread_local, 'locale', _default_locale)


def t(key: str, **kwargs) -> str:
    locale = get_locale()
    messages = _translations.get(locale, _translations[_default_locale])

    value = messages
    for part in key.split('.'):
        if isinstance(value, dict):
            value = value.get(part)
        else:
            value = None
            break

    if value is None:
        value = _translations[_default_locale]
        for part in key.split('.'):
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break

    if value is None:
        return key

    if kwargs:
        for k, v in kwargs.items():
            value = value.replace(f'{{{k}}}', str(v))

    return value


def get_language_instruction() -> str:
    return 'Please respond in English.'
