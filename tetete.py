# # import socket
# #
# # socket = socket.socket()
# # socket.bind(('', 5000))
# # socket.listen(3)
# # data, addr = socket.accept()
# # while True:
# #     print(addr)
# #     bdata = data.recv(1024)
# #     if not bdata:
# #         break
# #     print(bdata)
# #     # data.send(data)
# #
# # # socket.close()
# # # socket.connect((),'http://ya.ru')
# # from datetime import datetime
# #
# #
# # print(datetime.now())
import requests
#
# resp = requests.post('https://api.sclera.xyz/task/add', data={'date': '2017-11-25 22:38:05.399357', 'description': 'Вротой таск', 'image': 'https://www.sclera.xyz/book_covers_step_13.png', "token": "KgOXelsyC6ZEq6LJh_iLGtoj"})
resp = requests.post('https://api.sclera.xyz/login', data={'login': 'boris', 'password': '1000'})
# resp = requests.post('https://api.sclera.xyz/task/my', data={"token": "KgOXelsyC6ZEq6LJh_iLGtoj"})
print(resp.text)
# resp = requests.post('https://api.sclera.xyz/task/add', data={'login': 'solo', 'password': '123'})
# print(resp.text)
# from terminaltables import AsciiTable
#
# table_data = [
#     ['Heading1', 'Heading2'],
#     ['row1 column1', 'row1 column2'],
#     ['row2 column1', 'row2 column2'],
#     ['row3 column1', 'row3 column2']
# ]
# table = AsciiTable(table_data).table
# print(table)