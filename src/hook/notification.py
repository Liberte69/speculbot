def trade(func):
    """Decorator for a particular trade decision

    Args:
        stock (str): Name of the stock being traded
        decision (str): Decision made on the trade
    """
    def wrapper(stock, decision, **args):
        "@TRADE\n" + func()
        func()
    return wrapper

def issue(func):
    """Decorator for issue messages needing to be sent to Discord server

    Args:
        message (str): Issue message to be sent
    """
    def wrapper(message):
        "@ISSUE\n" + func()
        func()
    return wrapper

def help(func):
    """Decorator for issue messages needing to be sent to Discord server

    Args:
        message (str): Issue message to be sent
    """
    def wrapper(): # TODO Varargs pour les arguments et les usages
        "@HELP\n" + func()
    return wrapper

@help
def usageAdd():
    return "$add <algo> -n <name>"

@help
def usageRemove():
    return "$remove <name>"
