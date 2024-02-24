import os
from openai import OpenAI

# KEY = os.environ.get('OPENAI_API_KEY')
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