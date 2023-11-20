from flask import Flask, render_template, request, send_file, Response
import psycopg2
import word
import EmailF
import random #TEST!!!
app = Flask(__name__)

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="1234",
                        port="5432")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS people
                    (id INT GENERATED ALWAYS AS IDENTITY,
                    FCs TEXT NOT NULL,
                    dateS TEXT NOT NULL,
                    dateE TEXT NOT NULL,
                    passport TEXT NOT NULL,
                    address TEXT NOT NULL,
                    citizenship TEXT NOT NULL,
                    post TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    uFCs TEXT NOT NULL,
                    uphone TEXT NOT NULL,
                    umail TEXT NOT NULL,
                    uinstitute TEXT NOT NULL,
                    status TEXT NOT NULL,
                    file TEXT NOT NULL);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS car
                    (id INT GENERATED ALWAYS AS IDENTITY,
                    FCs TEXT NOT NULL,
                    date TEXT NOT NULL,
                    car_brand TEXT NOT NULL,
                    SRM TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    uFCs TEXT NOT NULL,
                    uphone TEXT NOT NULL,
                    umail TEXT NOT NULL,
                    uinstitute TEXT NOT NULL,
                    status TEXT NOT NULL,
                    file TEXT NOT NULL);''')
conn.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/autopass')
def autopass():
    return render_template('autopass.html')

@app.route('/peoplepass')
def peoplepass():
    return render_template('peoplepass.html')

@app.route('/process_form_people', methods=['POST'])
def process_form_people():
    input_values_people = []
    input_values_people.append(request.form['FCs'])
    input_values_people.append('.'.join(request.form['dateS'].split("-")[::-1]))
    input_values_people.append('.'.join(request.form['dateE'].split("-")[::-1]))
    input_values_people.append(request.form['passport'])
    input_values_people.append(request.form['address'])
    input_values_people.append(request.form['citizenship'])
    input_values_people.append(request.form['post'])
    input_values_people.append(request.form['purpose'].strip())
    input_values_people.append(request.form['uFCs'])
    input_values_people.append(request.form['uphone'])
    input_values_people.append(request.form['umail'])
    input_values_people.append(request.form['uinstitute'])

    count = get_count('people')
    word.word_pep_gen(input_values_people, count)
    sqlp(input_values_people, f"reqp{count}.docx")
    EmailF.send_message(input_values_people[0],input_values_people[1],input_values_people[2],input_values_people[7])

    return 'Данные приняты. Значение поля ввода: {}'.format(input_values_people)

@app.route('/process_form_car', methods=['POST'])
def process_form_car():
    input_values_car = []
    input_values_car.append(request.form['FCs'])
    input_values_car.append('.'.join(request.form['date'].split("-")[::-1]))
    input_values_car.append(request.form['car_brand'])
    input_values_car.append(request.form['SRM'])
    input_values_car.append(request.form['address'])
    input_values_car.append(request.form['phone'])
    input_values_car.append(request.form['purpose'].strip())
    input_values_car.append(request.form['uFCs'])
    input_values_car.append(request.form['uphone'])
    input_values_car.append(request.form['umail'])
    input_values_car.append(request.form['uinstitute'])

    count = get_count('car')
    word.word_car_gen(input_values_car, count)
    sqlc(input_values_car, f"reqc{count}.docx")

    return 'Данные приняты. Значение поля ввода: {}'.format(input_values_car)

@app.route('/pdata')
def pdata():
    data = get_data("people")
    return render_template('security_table_p.html', data=data)

@app.route('/process_form_people_search', methods=['POST'])
def process_form_people_search():
    ifcs = request.form['search']
    print(ifcs)
    cursor.execute(f"SELECT * FROM people WHERE fcs = '{ifcs}' ORDER BY id DESC;")
    data = cursor.fetchall()
    conn.commit()
    return render_template('security_table_p.html', data=data)

    return 'Данные приняты. Значение поля ввода: {}'.format(input_values_people)

@app.route('/cdata')
def cdata():
    data = get_data("car")
    return render_template('security_table_c.html', data=data)

@app.route('/download_word_fileP/<file_id>')
def download_word_fileP(file_id):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT file FROM people WHERE file = %s", (file_id,))
        row = cursor.fetchone()
        if row:
            file_path = row[0]
            with open(file_path, 'rb') as file: file_data = file.read()
            return Response(file_data, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            headers={"Content-Disposition": f"attachment; filename={file_path}"})
        else: return "File not found"
    except psycopg2.Error as e:
        return f"Error fetching file: {e}"
    finally: conn.commit()

@app.route('/download_word_fileC/<file_id>')
def download_word_fileC(file_id):
    cursor = conn.cursor()
    print(file_id)
    try:
        cursor.execute(f"SELECT file FROM car WHERE file = %s", (file_id,))
        row = cursor.fetchone()
        if row:
            file_path = row[0]
            print(file_path)
            with open(file_path, 'rb') as file: file_data = file.read()
            return Response(file_data, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            headers={"Content-Disposition": f"attachment; filename={file_path}"})
        else: return "File not found"
    except psycopg2.Error as e:
        return f"Error fetching file: {e}"
    finally: conn.commit()

def sqlp(input_values_people, file_path):
    status = "unknown"
    try:
        cursor.execute(
            f"INSERT INTO people (FCs, dateS, dateE, passport, address, citizenship, post, purpose,\
             uFCs, uphone, umail, uinstitute, status, file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (input_values_people[0], input_values_people[1], input_values_people[2], input_values_people[3],
             input_values_people[4], input_values_people[5], input_values_people[6], input_values_people[7],
             input_values_people[8], input_values_people[9], input_values_people[10], input_values_people[11],
             status, file_path))
        # Сохранение изменений и закрытие соединения
        conn.commit()
        print("Record created successfully")
    except psycopg2.Error as e:
        print(f"Error inserting record: {e}")
    finally:
        conn.commit()

def sqlc(input_values_people, file_path, table_name):
    status = "unknown"
    try:
        cursor.execute(
            f"INSERT INTO car (FCs, date, car_brand, SRM, address, phone, purpose, uFCs, uphone, umail,\
            uinstitute, status, file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (input_values_people[0], input_values_people[1], input_values_people[2], input_values_people[3],
             input_values_people[4], input_values_people[5], input_values_people[6], input_values_people[7],
             input_values_people[8], input_values_people[9], input_values_people[10], status, file_path)
        )
        # Сохранение изменений и закрытие соединения
        conn.commit()
        print("Record created successfully")
    except psycopg2.Error as e:
        print(f"Error inserting record: {e}")
    finally:
        conn.commit()

def get_data(table_name):
    cursor.execute(f'SELECT * FROM {table_name} ORDER BY id DESC;')
    data = cursor.fetchall()
    conn.commit()
    return data

def get_count(table_name):
    cursor.execute(f'SELECT COUNT(*) FROM {table_name} ORDER BY id DESC;')
    count = (cursor.fetchall())[0][0]
    conn.commit()
    return count

# @app.route('/pdatas')
# def pdatas():
#     data = get_data_search("people")
#     return render_template('security_table_p.html', data=data)


if __name__ == '__main__':
    # key = input()
    # if key == '1':
    #     for i in range(0, 10):
    #         put = []
    #         put.append(str(random.choice(["Громов", "Ермаков", "Кузнецов", "Крылов", "Михайлова", "Харитонова"]) + ' ' +
    #                        random.choice(["Давид", "Сергей", "Виктор", "Макар", "Ева", "Вероника"]) + ' ' +
    #                        random.choice(["Кириллович", "Георгиевич", "Тимурович", "Маркович", "Степановна", "Георгиевна"])
    #                        ))
    #         put.append(str(random.choice(["23.11.2023", "06.12.2023", "27.11.2023", "20.11.2023", "08.12.2023", \
    #                                       "28.11.2023", "22.11.2023", "07.12.2023", "05.12.2023", "30.11.2023"])))
    #         put.append(str(random.choice(["18.12.2023", "11.12.2023", "13.12.2023", "22.12.2023", "21.12.2023", \
    #                                       "20.12.2023", "14.12.2023", "15.12.2023", "12.12.2023", "19.12.2023"])))
    #         put.append(str(random.choice(["4720 895208", "4185 644317", "4997 921352", "4088 951657", "4472 682946", \
    #                                       "4979 905549", "4963 933688", "4559 442237", "4428 453189", "4867 986106"])))
    #         put.append(str(random.choice(["улица Образцова, 9 с10", "Новосущёвская улица, 22 с9"])))
    #         put.append(str(random.choice(["Гражданство России", "Гражданство Белоруссии"])))
    #         put.append(str(random.choice(["Менеджер", "Специалист в области ИИ", "Ведущий программист Сбер"])))
    #         put.append(str(random.choice(
    #             ["посещением проектной деятельности в качестве эксперта", "проведением лекции по экономике",
    #              "приглашением в качестве эксперта"])))
    #         put.append("Василев Алексей Иванович")
    #         put.append("+9672427362")
    #         put.append("v.alex_test@mail.ru")
    #         put.append('"Высшая инженерная школа" (АВИШ)')
    #         sqlp(put, "testpath")
    app.run(host='0.0.0.0', port=2111, debug=True)