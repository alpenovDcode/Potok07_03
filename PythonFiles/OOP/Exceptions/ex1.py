# # Типы исключений (Выполнение, до выполнения)
#
# import math
#
#
# class NegativeNumberError(Exception):
#     """Исключение для обработки отрицательных чисел."""
#     pass
#
# def get_square_root(value):
#     if value < 0:
#         raise NegativeNumberError("Квадратный корень из отрицательного числа не определен.")
#         # Искусственно вызываем другое исключение для демонстрации
#     if value == 13:
#         raise RuntimeError("Непредвиденная ошибка для числа 13")
#     return math.sqrt(value)
#
#
# def main():
#     try:
#         user_input = input("Введите число для вычисления квадратного корня: ")
#         value = float(user_input)
#         result = get_square_root(value)
#     except ValueError:
#         print("Ошибка: введено некорректное значение. Пожалуйста, введите числовое значение.")
#     except NegativeNumberError as e:
#         print(f"Ошибка: {e}")
#     except Exception as e:
#         print(f"Неизвестная ошибка: {e}")
#     else:
#         print(f"Квадратный корень из {value} равен {result}")
#     finally:
#         print("Программа завершена.")
#
#
# if __name__ == "__main__":
#     main()