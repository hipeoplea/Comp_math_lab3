import math

FUNCTIONS = {
    "sin(x)": math.sin,
    "cos(x)": math.cos,
    "x^2": lambda x: x ** 2,
    "exp(x)": math.exp,
    "1 / (1 + x^2)": lambda x: 1 / (1 + x ** 2),
    "1 / sqrt(x)": lambda x: 1 / math.sqrt(x),
    "1 / x": lambda x: 1 / x,
    "ln(x)": lambda x: math.log(x)
}

ERRORS = {
    1: "Все поля должны быть заполнены числами",
    2: "Нижний предел больше верхнего",
    3: "Интеграл расходится",
    4: "Достигнут предел разбиения, интеграл, возможно, расходится"
}