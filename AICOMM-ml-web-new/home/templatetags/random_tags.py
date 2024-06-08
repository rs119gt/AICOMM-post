import random
from django import template

register = template.Library()

@register.filter
def random_sequence(sequence):
    return random.sample(list(sequence), len(sequence))