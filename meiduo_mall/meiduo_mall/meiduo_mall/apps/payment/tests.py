from django.test import TestCase
import os
# Create your tests here.
path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys\应用私钥2048.txt")
print(path)

BASE_DIR=os.getcwd()
print(BASE_DIR)



