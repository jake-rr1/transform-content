import os
from dotenv import load_dotenv
from openai import OpenAI

def gpt_response(frame_descriptions):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    load_dotenv(current_dir + '\\inputs.txt')
    
    content = os.getenv("CHATGPT_PROMPT")
    frame_descriptions = frame_descriptions

    description_inputs = []
    for idx, frame_desc in enumerate(frame_descriptions):
        description_inputs.append(f' [Description of Frame {idx + 1}: ' + frame_desc + ']')   
        
    content = content.replace('Descriptions of the frames:', 'Descriptions of the frames:' + ''.join(description_inputs))

    try:
        load_dotenv(current_dir + '\\.api')
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openai_api_key
        )
    except Exception as err:
        print(err)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo-16k-0613",
    )

    return chat_completion.choices[0].message.content