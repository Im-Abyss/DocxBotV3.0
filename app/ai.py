from mistralai import Mistral

from config import AI_TOKEN


async def check_error(content):

    '''
    Эта функция ИИ ассистента, но
    она пока ещё не доработана
    '''

    api_key = AI_TOKEN
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    response = await client.chat.complete_async(
        model=model,
        messages=[
             {
                  "role": "user",
                  "content": content,
              },
        ],
    )
    
    return response.choices[0].message.content