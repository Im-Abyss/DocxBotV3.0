from mistralai import Mistral

from config import AI_TOKEN


async def main(content):

    '''
    Это базовая функция, при которой
    пользователь отправляет сообщение
    боту, а бот отвечает с помощью ИИ
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

async def check_error(content):

    '''
    Эта функция специнально для проверки
    ошибок в документе, но она ещё
    не доработана
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