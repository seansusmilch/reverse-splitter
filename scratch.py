import os 
from ollama import Client

client = Client(host='http://goku:11434')
res = client.pull('llama3.1')
print(res)

response = client.generate(model='llama3.1', prompt='Why is the sky blue?', max_tokens=20)
print(response)