import random
# test.py и test2.py предназначены для теста обмена сообщениями между скриптом-граббером и скиптом бота. На
# примере test.py текстовый файл, первой строчкой которого является номер-состояние. Эта строчка меняется при каждом
# изменении файла и присваивается случайно. В свою очередь test2.py записывает изначальный номер-состояние, а затем,
# переодически проверяя файл на изменение номера-состояния, ждёт сообщений, а как найдёт - выкладывает и чистит файл


while True:

    data = input()

    file = open("data.txt", 'r')
    last_messages = file.readlines()
    print(last_messages)
    file.close()

    file = open("data.txt", 'w')
    file.write(f"{random.randint(0, 10 ** 6)}\n")
    file.writelines(last_messages[1::])
    file.write(f"\n{data}")
    file.close()