import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from utils.Predefined import FUNCTIONS, ERRORS
from methods.mathMethods import *
from methods.externalTask import *

class IntegralApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Несобственные интегралы 2 рода")
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.func_label = QLabel("Выберите функцию:")
        self.func_combo = QComboBox()
        self.func_combo.addItems(FUNCTIONS.keys())

        self.method_label = QLabel("Метод интегрирования:")
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Левые прямоугольники",
            "Правые прямоугольники",
            "Средние прямоугольники",
            "Трапеции",
            "Симпсона"
        ])

        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Верхний предел (b)")

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Нижний предел (a)")

        self.eps_input = QLineEdit()
        self.eps_input.setPlaceholderText("Точность (ε)")

        self.calc_button = QPushButton("Вычислить")
        self.calc_button.clicked.connect(self.calculate)

        self.result_label = QLabel("Результат:")
        self.result_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.func_label)
        layout.addWidget(self.func_combo)
        layout.addWidget(self.method_label)
        layout.addWidget(self.method_combo)
        layout.addWidget(self.a_input)
        layout.addWidget(self.b_input)
        layout.addWidget(self.eps_input)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        try:
            func_name = self.func_combo.currentText()
            method_name = self.method_combo.currentText()
            try:
                a = float(self.a_input.text().replace(',', '.'))
                b = float(self.b_input.text().replace(',', '.'))
                eps = float(self.eps_input.text().replace(',', '.'))
            except:
                raise ValueError(1)
            if a > b:
                raise ValueError(2)
            f = FUNCTIONS[func_name]

            method_map = {
                "Левые прямоугольники": (left_rectangles, 2),
                "Правые прямоугольники": (right_rectangles, 2),
                "Средние прямоугольники": (mid_rectangles, 2),
                "Трапеции": (trapezoidal, 2),
                "Симпсона": (simpson, 4)
            }

            method, order = method_map[method_name]

            discontinuities = find_discontinuities(f, a, b)
            if discontinuities:
                eps_shift = 1e-5
                converges = True
                for d in discontinuities:
                    left = try_to_compute(f, d - eps_shift)
                    right = try_to_compute(f, d + eps_shift)
                    if (a == d and right is None) or (b == d and left is None) or (
                            a < d < b and (left is None or right is None)):
                        converges = False
                        break
                if not converges:
                    raise ValueError(3)
                else:
                    discontinuities = [a] + [x for x in discontinuities if a < x < b] + [b]
                    result = 0
                    for i in range(len(discontinuities) - 1):
                        r, n = runge_method(method, f,
                                            discontinuities[i] + eps_shift,
                                            discontinuities[i + 1] - eps_shift,
                                            eps)
                        result += r
                    self.result_label.setText(f"Значение интеграла: {result:.6f} (учтены разрывы)")
                    return
            result, n = runge_method(method, f, a, b, eps)
            self.result_label.setText(f"Значение интеграла: {result:.6f}, количество разбиений = {n}")

        except ValueError as ve:
            self.result_label.setText(ERRORS[ve.args[0]])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegralApp()
    window.show()
    sys.exit(app.exec_())
