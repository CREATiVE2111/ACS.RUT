from docxtpl import DocxTemplate

def word_pep_gen(input_values_people, count):
    fcs, dateS, dateE, passport, address, citizenship, post, purpose, ufcs, uphone, umail, uinstitute = input_values_people
    doc = DocxTemplate("Шаблон_пеший.docx")
    context = { "фио": fcs,
                "дата_1": dateS,
                "дата_2": dateE,
                "паспорт": passport,
                "адрес": address,
                "гражданство": citizenship,
                "должность": post,
                "цель": purpose
               }
    doc.render(context)
    doc.save(f"reqp{count}.docx")

def word_car_gen(input_values_people, count):
    fcs, phone, car_brand, SRM, date, addres, purpose, ufcs, uphone, umail, uinstitute = input_values_people
    doc = DocxTemplate("Шаблон_авто.docx")
    context = { "фио": fcs,
                "дата": date,
                "марка": car_brand,
                "госрегзнак": SRM,
                "адрес": addres,
                "телефон": phone,
                "цель": purpose
               }
    doc.render(context)
    doc.save(f"reqc{count}.docx")