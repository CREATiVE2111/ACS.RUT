x = []
with open('city.txt', encoding='utf-8') as file:
    x = file.readlines()
print(x)
for i in range(len(x)):
    x[i] = x[i].strip()
print(x)
for i in range(len(x)):
    x[i] = x[i].split(',')
for i in range(len(x)):
    x[i] = f'{x[i][0]} ({x[i][1][1:]})'
for i in range(len(x)):
    x[i] = f'<option>{x[i]}</option>'
print(len(x))
print(x)
s = ''
for i in x:
    s+=f'{str(i)}\n'

print(s)