from flask import Flask, render_template, request, redirect, url_for, make_response, session
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


app = Flask(__name__)

# Регистрация шрифта DejaVu Sans
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
app.secret_key = 'your_secret_key'  # Установите секретный ключ

@app.route('/')
def index():
    # Перенаправляем на страницу с формой
    return redirect(url_for('form'))

@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    # Получаем данные из формы
    total_area = float(request.form['total_area']) #1. Общая площадь здания (кв. м.):
    lease_area = float(request.form['lease_area']) #2. Аренднопригодная площадь (кв. м.):
    anchor_area = float(request.form['anchor_area']) #3. Площадь якорных арендаторов (%):
    rate_first_period = float(request.form['rate_first_period']) # 4. Ставка на первый период (руб.):
    rate_second_period = float(request.form['rate_second_period']) #5. Ставка на второй период (руб.):
    rate_third_period = float(request.form['rate_third_period']) #6. Ставка на третий период (руб.):
    rate_fourth_period = float(request.form['rate_fourth_period']) #7. Ставка на четвертый период (руб.):
    market_area = float(request.form['market_area']) #8. Площадь рыночных арендаторов (%):
    market_rate = float(request.form['market_rate']) #9. Ставка рыночных арендаторов (руб.):
    operating_expenses = float(request.form['operating_expenses']) #10. Операционные расходы арендатора (руб на 1 кв. м.):
    actual_expenses = float(request.form['actual_expenses']) #11. Фактические расходы собственника (руб на 1 кв. м.):
    underloading = float(request.form['underloading']) #12. Недозагрузка (%):
    capitalization_coefficient = float(request.form['capitalization_coefficient']) #13. Коэффициент капитализации для реверсии (%):
    discount_rate = float(request.form['discount_rate']) #14. Ставка дисконтирования (%):

    # Перменные для конфигурации

    value_1_1 = lease_area
    value_1_2 = lease_area
    value_1_3 = lease_area
    value_1_4 = lease_area

    value_2_1 = rate_first_period
    value_2_2 = rate_second_period
    value_2_3 = rate_third_period
    value_2_4 = rate_fourth_period

    value_3_1 = market_rate
    value_3_2 = market_rate
    value_3_3 = market_rate
    value_3_4 = market_rate

    value_4_1 = operating_expenses
    value_4_2 = operating_expenses
    value_4_3 = operating_expenses
    value_4_4 = operating_expenses

    value_5_1 = value_2_1 + value_4_1
    value_5_2 = value_2_2 + value_4_2
    value_5_3 = value_2_3 + value_4_3
    value_5_4 = value_2_4 + value_4_4

    value_6_1 = value_3_1 + value_4_1
    value_6_2 = value_3_1 + value_4_1
    value_6_3 = value_3_1 + value_4_1
    value_6_4 = value_3_1 + value_4_1

    value_7_1 = value_5_1 * (value_1_1 * anchor_area / 100)
    value_7_2 = value_5_2 * (value_1_1 * anchor_area / 100)
    value_7_3 = value_5_3 * (value_1_1 * anchor_area / 100)
    value_7_4 = value_5_4 * (value_1_1 * anchor_area / 100)

    value_8_1 = value_6_1 * (value_1_1 * market_area / 100)
    value_8_2 = value_6_2 * (value_1_1 * market_area / 100)
    value_8_3 = value_6_3 * (value_1_1 * market_area / 100)
    value_8_4 = value_6_4 * (value_1_1 * market_area / 100)

    value_9_1 = underloading
    value_9_2 = underloading
    value_9_3 = underloading
    value_9_4 = underloading

    value_10_1 = value_8_1 * ((100 - value_9_1) / 100)
    value_10_2 = value_8_1 * ((100 - value_9_1) / 100)
    value_10_3 = value_8_1 * ((100 - value_9_1) / 100)
    value_10_4 = value_8_1 * ((100 - value_9_1) / 100)

    value_11_1 = value_7_1
    value_11_2 = value_7_2
    value_11_3 = value_7_3
    value_11_4 = value_7_4

    value_12_1 = value_10_1 + value_11_1
    value_12_2 = value_10_1 + value_11_2
    value_12_3 = value_10_1 + value_11_3
    value_12_4 = value_10_1 + value_11_4

    value_13_1 = actual_expenses
    value_13_2 = actual_expenses
    value_13_3 = actual_expenses
    value_13_4 = actual_expenses

    value_14_1 = value_13_1 *  total_area
    value_14_2 = value_13_1 *  total_area
    value_14_3 = value_13_1 *  total_area
    value_14_4 = value_13_1 *  total_area

    value_15_1 = value_12_1 -  value_14_1
    value_15_2 = value_12_2 -  value_14_1
    value_15_3 = value_12_3 -  value_14_1
    value_15_4 = value_12_4 -  value_14_1

    value_16_1 = capitalization_coefficient
    value_16_2 = capitalization_coefficient
    value_16_3 = capitalization_coefficient
    value_16_4 = capitalization_coefficient

    value_17_1 = value_15_4/ value_16_1
    value_17_2 = value_15_4/ value_16_1
    value_17_3 = value_15_4/ value_16_1
    value_17_4 = value_15_4/ value_16_1

    value_18_1 = 0
    value_18_2 = 0
    value_18_3 = 0
    value_18_4 = 0

    value_19_1 = 0
    value_19_2 = 0
    value_19_3 = 0
    value_19_4 = 0

    value_20_1 = 0
    value_20_2 = 0
    value_20_3 = 0
    value_20_4 = 0

    value_21_1 = 0
    value_21_2 = 0
    value_21_3 = 0
    value_21_4 = 0

    value_22_1 = 0
    value_22_2 = 0
    value_22_3 = 0
    value_22_4 = 0


    # Создаем список значений для таблицы
    results = [

        {"number": 1,
         "name": "Арендопригодная площадь:",
         "unit": "кв. м",
         "value1": value_1_1,
         "value2": value_1_2,
         "value3": value_1_3,
         "value4": value_1_4
         },

        {"number": 2,
         "name": "Арендная ставка по действующему договору аренды:",
         "unit": "руб/кв.м. в год",
         "value1": value_2_1,
         "value2": value_2_2,
         "value3": value_2_3,
         "value4": value_2_4
         },

        {"number": 3,
         "name": "Рыночная арендная ставка:",
         "unit": "руб/кв.м. в год",
         "value1": value_3_1,
         "value2": value_3_2,
         "value3": value_3_3,
         "value4": value_3_4
         },

        {"number": 4,
         "name": "Возмещаемые операционные расходы",
         "unit": "руб/кв.м. (на 1 кв.м. аренднопригодной площади здания)",
         "value1": value_4_1,
         "value2": value_4_2,
         "value3": value_4_3,
         "value4": value_4_4
         },

        {"number": 5,
         "name": "Арендная ставка с учетом возмещаемых операционных расходов",
         "unit": "руб./кв.м.(для якорных арендаторов)",
         "value1": value_5_1,
         "value2": value_5_2,
         "value3": value_5_3,
         "value4": value_5_4
         },

        {"number": 6,
         "name": "Арендная ставка с учетом возмещаемых операционных расходов",
         "unit": "руб./кв.м.(рыночная)",
         "value1": value_6_1,
         "value2": value_6_2,
         "value3": value_6_3,
         "value4": value_6_4
         },

        {"number": 7,
         "name": "ПВД",
         "unit": "руб.(якорные арендаторы)",
         "value1": value_7_1,
         "value2": value_7_2,
         "value3": value_7_3,
         "value4": value_7_4
         },

        {"number": 8,
         "name": "ПВД",
         "unit": "руб. (рыночные ставки)",
         "value1": value_8_1,
         "value2": value_8_2,
         "value3": value_8_3,
         "value4": value_8_4
         },

        {"number": 9,
         "name": "Недозагрузка",
         "unit": "% (для площадей сдаваемых по рыночным ставкам)",
         "value1": value_9_1,
         "value2": value_9_2,
         "value3": value_9_3,
         "value4": value_9_4
         },

        {"number": 10,
         "name": "ДВД",
         "unit": "руб. (по рыночным ставкам)",
         "value1": value_10_1,
         "value2": value_10_2,
         "value3": value_10_3,
         "value4": value_10_4
         },

        {"number": 11,
         "name": "ДВД",
         "unit": "руб. (якорные арендаторы)",
         "value1": value_11_1,
         "value2": value_11_2,
         "value3": value_11_3,
         "value4": value_11_4
         },

        {"number": 12,
         "name": "ДВД",
         "unit": "руб. (всего)",
         "value1": value_12_1,
         "value2": value_12_2,
         "value3": value_12_3,
         "value4": value_12_4
         },

        {"number": 13,
         "name": "Операционные расходы",
         "unit": "руб./кв.м. в год (на кв.м. общей площади здания)",
         "value1": value_13_1,
         "value2": value_13_2,
         "value3": value_13_3,
         "value4": value_13_4
         },

        {"number": 14,
         "name": "Операционные расходы",
         "unit": "руб. в год",
         "value1": value_14_1,
         "value2": value_14_2,
         "value3": value_14_3,
         "value4": value_14_4
         },

        {"number": 15,
         "name": "ЧОД",
         "unit": "руб.",
         "value1": value_15_1,
         "value2": value_15_2,
         "value3": value_15_3,
         "value4": value_15_4
         },

        {"number": 16,
         "name": "Ставка терминальной капитализации ",
         "unit": "%",
         "value1": value_16_1,
         "value2": value_16_2,
         "value3": value_16_3,
         "value4": value_16_4
         },

        {"number": 17,
         "name": "Терминальная стоимость",
         "unit": "руб.",
         "value1": value_17_1,
         "value2": value_17_2,
         "value3": value_17_3,
         "value4": value_17_4
         },

        {"number": 18,
         "name": "Ставка дисконтирования",
         "unit": "%. ",
         "value1": value_18_1,
         "value2": value_18_2,
         "value3": value_18_3,
         "value4": value_18_4
        },

        {"number": 19,
         "name": "Фактор дисконтирования",
         "unit": "",
         "value1": value_19_1,
         "value2": value_19_2,
         "value3": value_19_3,
         "value4": value_19_4
         },

        {"number": 20,
         "name": "Текущая стоимость денежного потока ",
         "unit": " руб.",
         "value1": value_20_1,
         "value2": value_20_2,
         "value3": value_20_3,
         "value4": value_20_4
         },

        {"number": 21,
         "name": "Рыночная стоимость ",
         "unit" : " руб.",
         "value1": value_21_1,
         "value2": value_21_2,
         "value3": value_21_3,
         "value4": value_21_4
         },

        {"number": 22, "name": "Рыночная стоимость ",
         "unit": " руб. (округленно) ",
         "value1": value_22_1,
         "value2": value_22_2,
         "value3": value_22_3,
         "value4": value_22_4
         },
    ]


    session['results'] = results
    return render_template('results.html', results=results)


def draw_multiline_text(canvas, text, x, y, max_width, font_size):
    canvas.setFont("DejaVuSans", font_size)
    lines = []

    # Разделяем текст на строки по 30 символов
    while len(text) > 0:
        line = text[:30]  # Берем первые 30 символов
        text = text[30:]  # Убираем их из текста
        lines.append(line)

    # Рисуем каждую строку
    for line in lines:
        canvas.drawString(x, y, line)
        y -= font_size + 2  # Уменьшаем y для следующей строки

    return y  # Возвращаем новую позицию y


@app.route('/export_pdf')
def export_pdf():
    # Получаем данные из сессии
    results = session.get('results', [])

    # Создаем PDF в памяти с альбомной ориентацией
    output = BytesIO()
    p = canvas.Canvas(output, pagesize=landscape(letter))  # Альбомная ориентация
    width, height = landscape(letter)

    # Заголовок
    p.setFont("DejaVuSans", 14)  # Уменьшенный размер шрифта
    p.drawString(100, height - 50, "Результаты расчетов")

    # Позиция для таблицы
    y_position = height - 100

    # Заголовки таблицы
    p.setFont("DejaVuSans", 12)
    p.drawString(30, y_position, "№")  # Изменено на "№"
    p.drawString(100, y_position, "Название ")  # Уменьшен отступ
    p.drawString(300, y_position, "Значение 1")
    p.drawString(400, y_position, "Значение 2")
    p.drawString(500, y_position, "Значение 3")
    p.drawString(600, y_position, "Значение 4")

    # Печатаем данные таблицы
    y_position -= 20
    p.setFont("DejaVuSans", 10)  # Уменьшенный размер шрифта для данных

    for result in results:
        p.drawString(30, y_position, str(result["number"]))  # Столбец с номерами
        y_position = draw_multiline_text(p, f"{result['name']} ({result['unit']})", 100, y_position, 300,
                                         10)  # Уменьшен отступ для названий

        p.drawString(300, y_position, str(result["value1"]))
        p.drawString(400, y_position, str(result["value2"]))
        p.drawString(500, y_position, str(result["value3"]))
        p.drawString(600, y_position, str(result["value4"]))
        y_position -= 20

        if y_position < 50:  # Если достигли нижней границы страницы
            p.showPage()
            p.setFont("DejaVuSans", 12)
            p.drawString(30, height - 50, "№")  # Заголовок для новой страницы
            p.drawString(100, height - 50, "Название ")
            p.drawString(300, height - 50, "Значение 1")
            p.drawString(400, height - 50, "Значение 2")
            p.drawString(500, height - 50, "Значение 3")
            p.drawString(600, height - 50, "Значение 4")
            y_position = height - 70

    # Завершаем PDF документ
    p.showPage()
    p.save()

    # Возвращаем PDF как ответ
    output.seek(0)
    response = make_response(output.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=results.pdf'

    return response


if __name__ == '__main__':
    app.run(debug=True)