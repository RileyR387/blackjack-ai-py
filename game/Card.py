
def value(card):
    x = card[:2].strip()
    try:
        intVal = int(x)
        return intVal
    except Exception as e:
        if x == 'A':
            return 11
        else:
            return 10

