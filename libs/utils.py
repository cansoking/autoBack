# from PIL import Image, ImageDraw, ImageFont
# import random
#
#
# def generate_math_questions(width=500, height=800, font_size=25, line_height=40, num_per_row=3, num_min=1, num_max=100,
#                             operators=['+', '-', '×', '÷']):
#     """
#     生成随机的数学口算题，并将它们绘制在一张图片上。
#
#     参数：
#     width：图片的宽度，单位为像素。
#     height：图片的高度，单位为像素。
#     font_size：口算题的字体大小，单位为像素。
#     line_height：每行口算题的行高，单位为像素。
#     num_per_row：每行口算题的数量。
#     num_min：口算题中数字的最小值，默认为 1。
#     num_max：口算题中数字的最大值，默认为 100。
#     operators：口算题中可以包含的运算符，默认为加减乘除四则运算均可。
#
#     返回：
#     生成的口算题图片对象。
#     """
#
#     # 创建一个空白的白色图片
#     image = Image.new('RGB', (width, height), 'white')
#
#     # 获取绘图对象
#     draw = ImageDraw.Draw(image)
#
#     # 设置字体
#     font = ImageFont.truetype('arial.ttf', font_size)
#
#     # 定义生成题目的函数
#     def generate_question():
#         num1 = random.randint(num_min, num_max)
#         num2 = random.randint(num_min, num_max)
#         operator = random.choice(operators)
#         if operator == '+':
#             answer = num1 + num2
#         elif operator == '-':
#             answer = num1 - num2
#         elif operator == '×':
#             answer = num1 * num2
#         else:
#             answer = num1 // num2
#         question = f'{num1} {operator} {num2} = '
#         return question, answer
#
#     # 计算每行可以容纳多少题目
#     max_rows = height // line_height  # 最多能放多少行
#
#     # 生成题目
#     for row in range(max_rows):
#         for col in range(num_per_row):
#             x = col * (width // num_per_row) + 20
#             y = row * line_height + 10
#             question, answer = generate_question()
#             draw.text((x, y), question, fill='black', font=font)
#
#     return image
#
#
# # image = generate_math_questions(width=500, height=800, font_size=25, line_height=40, num_per_row=3, num_min=1,
# #                                 num_max=100, operators=['+', '-', '×', '÷'])
# # image.save('math_questions3.png')
from PIL import Image, ImageDraw, ImageFont
import random


def generate_math_questions(width=500, height=800, font_size=25, line_height=40, num_per_row=3, num_min=1, num_max=100,
                            operators=['+', '-', '×', '÷']):
    """
    生成随机的数学口算题，并将它们绘制在一张图片上。

    参数：
    width：图片的宽度，单位为像素。
    height：图片的高度，单位为像素。
    font_size：口算题的字体大小，单位为像素。
    line_height：每行口算题的行高，单位为像素。
    num_per_row：每行口算题的数量。
    num_min：口算题中数字的最小值，默认为 1。
    num_max：口算题中数字的最大值，默认为 100。
    operators：口算题中可以包含的运算符，默认为加减乘除四则运算均可。

    返回：
    生成的口算题图片对象。
    """

    # 创建一个空白的白色图片
    image = Image.new('RGB', (width, height), 'white')

    # 获取绘图对象
    draw = ImageDraw.Draw(image)

    # 设置字体
    font = ImageFont.truetype('arial.ttf', font_size)

    # 定义生成题目的函数
    def generate_question():
        while True:
            num1 = random.randint(num_min, num_max)
            num2 = random.randint(num_min, num_max)
            operator = random.choice(operators)
            if operator == '+':
                answer = num1 + num2
            elif operator == '-':
                # 避免出现负数
                if num1 < num2:
                    num1, num2 = num2, num1
                answer = num1 - num2
            elif operator == '×':
                # 避免得数超过 1000
                if num1 * num2 > 1000:
                    continue
                answer = num1 * num2
            else:
                # 避免出现小数和除数为 0 的情况
                if num2 == 0 or num1 % num2 != 0 or num1 // num2 > 1000:
                    continue
                answer = num1 // num2
            question = f'{num1} {operator} {num2} = '
            return question, answer

    # 计算每行可以容纳多少题目
    max_rows = height // line_height  # 最多能放多少行

    # 生成题目
    for row in range(max_rows):
        for col in range(num_per_row):
            x = col * (width // num_per_row) + 20
            y = row * line_height + 10
            question, answer = generate_question()
            draw.text((x, y), question, fill='black', font=font)

    return image
