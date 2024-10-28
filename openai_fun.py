import os
import requests


def get_answer(question) -> str:
  # Configuration
  API_KEY = os.getenv("OPENAI_API_KEY")
  headers = {
      "Content-Type": "application/json",
      "api-key": API_KEY,
  }

  # Payload for the request
  payload = {
    "messages": [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": "情報を見つけるのに役立つ AI アシスタントです。"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": question,
          }
        ]
      }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
  }

  ENDPOINT = "https://masa1028.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

  # Send request
  try:
      response = requests.post(ENDPOINT, headers=headers, json=payload)
      response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
      answer = response.json()["choices"][0]["message"]["content"]
  except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}")

  # Handle the response as needed (e.g., print or process)
  print(response.json())
  return answer