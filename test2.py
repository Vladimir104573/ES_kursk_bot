import time
# test.py и test2.py предназначены для теста обмена сообщениями между скриптом-граббером и скиптом бота. На
# примере test.py текстовый файл, первой строчкой которого является номер-состояние. Эта строчка меняется при каждом
# изменении файла и присваивается случайно. В свою очередь test2.py записывает изначальный номер-состояние, а затем,
# переодически проверяя файл на изменение номера-состояния, ждёт сообщений, а как найдёт - выкладывает и чистит файл


file = open('data.txt', "r")
code = file.readline()
print(code)
file.close()

while True:
    time.sleep(10)
    file = open("data.txt", "r")
    new_code = file.readline()
    if code != new_code:
        for i in file.readlines():
            if i != '\n':
                print(i)
        code = new_code
    file.close()

    file = open("data.txt", "w")
    file.write(code)
    file.close()