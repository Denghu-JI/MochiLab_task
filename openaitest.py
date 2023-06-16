import openai

openai.api_key = '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'
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
  ]
)
print(response['choices'][0]['message']['content'])
