import os
import base64
import pickle
dict = {'1': {'count': 10, 'selected': True}, '2': {'count': 20, 'selected': False}}
ret=pickle.dumps(dict)
print(ret)
b=base64.b64encode(ret)
print(b)
b=b.decode()
print(b)
print('*'*20)
b=b.encode()
print(b)
ret=base64.b64decode(b)
print(ret)
dict=pickle.loads(ret)
print(dict)

path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys\应用私钥2048.txt")
print(path)

