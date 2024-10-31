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
    total_area = request.form['total_area']
    lease_area = request.form['lease_area']
    anchor_area = request.form['anchor_area']
    rate_first_period = request.form['rate_first_period']
    rate_second_period = request.form['rate_second_period']
    rate_third_period = request.form['rate_third_period']
    rate_fourth_period = request.form['rate_fourth_period']
    market_area = request.form['market_area']
    market_rate = request.form['market_rate']
    operating_expenses = request.form['operating_expenses']
    actual_expenses = request.form['actual_expenses']
    underloading = request.form['underloading']
    capitalization_coefficient = request.form['capitalization_coefficient']
    discount_rate = request.form['discount_rate']

    # Создаем список значений для таблицы
    results = [

        {"number": 1,
         "name": "Арендопригодная площадь:",
         "unit": "кв. м",
         "value1": lease_area,
         "value2": lease_area,
         "value3": lease_area,
         "value4": lease_area
         },

        {"number": 2,
         "name": "Арендная ставка по действующему договору аренды:",
         "unit": "руб/кв.м. в год",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 3,
         "name": "Рыночная арендная ставка:",
         "unit": "руб/кв.м. в год",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 4,
         "name": "Возмещаемые операционные расходы",
         "unit": "руб/кв.м. (на 1 кв.м. аренднопригодной площади здания)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 5,
         "name": "Арендная ставка с учетом возмещаемых операционных расходов",
         "unit": "руб./кв.м.(для якорных арендаторов)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 6,
         "name": "Арендная ставка с учетом возмещаемых операционных расходов",
         "unit": "руб./кв.м.(рыночная)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 7,
         "name": "ПВД",
         "unit": "руб.(якорные арендаторы)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 8,
         "name": "ПВД",
         "unit": "руб. (рыночные ставки)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 9,
         "name": "Недозагрузка",
         "unit": "% (для площадей сдаваемых по рыночным ставкам)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 10,
         "name": "ДВД",
         "unit": "руб. (по рыночным ставкам)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 11,
         "name": "ДВД",
         "unit": "руб. (якорные арендаторы)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 12,
         "name": "ДВД",
         "unit": "руб. (всего)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 13,
         "name": "Операционные расходы",
         "unit": "руб./кв.м. в год (на кв.м. общей площади здания)",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 14,
         "name": "Операционные расходы",
         "unit": "руб. в год",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 15,
         "name": "ЧОД",
         "unit": "руб.",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 16,
         "name": "Ставка терминальной капитализации ",
         "unit": "%",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 17,
         "name": "Терминальная стоимость",
         "unit": "руб.",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 18,
         "name": "Ставка дисконтирования",
         "unit": "%. ",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
        },

        {"number": 19,
         "name": "Фактор дисконтирования",
         "unit": "",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 20,
         "name": "Текущая стоимость денежного потока ",
         "unit": " руб.",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""},

        {"number": 21,
         "name": "Рыночная стоимость ",
         "unit" : " руб.",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""
         },

        {"number": 22, "name": "Рыночная стоимость ",
         "unit": " руб. (округленно) ",
         "value1": "",
         "value2": "",
         "value3": "",
         "value4": ""},
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