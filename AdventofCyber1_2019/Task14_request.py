import requests
import json

newpath = "" 
answerarray = []
basepath = "http://10.10.169.100:3000/"


while newpath != "end":
  
   response = requests.get(basepath + newpath) 
   jsondata = response.json()
   # print(type(jsondata))
   newpath = jsondata['next']
   if newpath == "end" : 
      print("we done")
      break
   answerarray.append(jsondata['value'])
   print("------------doing some things-----------------")
   
   
   
answer = ''.join(answerarray)
print("------------Answer is here-----------------")
print(answer)
