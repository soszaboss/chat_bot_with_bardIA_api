import os
from openai import OpenAI

KEY = "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"
client = OpenAI(api_key=KEY)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won thz 2014 world cup?"},
  ]
)
print(response)#.choices[0].message.content)

