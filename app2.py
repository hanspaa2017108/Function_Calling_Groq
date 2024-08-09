'''
import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={OPENWEATHER_API_KEY}&q={location}"

    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['main']
        temperature_k = data['main']['temp']
        
        if unit == "celsius":
            temperature = temperature_k - 273.15  # Convert Kelvin to Celsius
            temp_unit = "°C"
        else:
            temperature = (temperature_k - 273.15) * 9/5 + 32  # Convert Kelvin to Fahrenheit
            temp_unit = "°F"
        
        weather_info = (
            f"The current weather in {location} is {weather} with a temperature of "
            f"{round(temperature, 2)}{temp_unit}."
        )
        return weather_info
    else:
        return f"Sorry, I couldn't fetch the weather data for {location}."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },   
    }
]

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": "What is the weather like in ghorakpur?",
        }
    ],
    temperature=0,
    max_tokens=300,
    tools=tools,
    tool_choice="auto"
)
groq_response = response.choices[0].message
print(groq_response)
args = json.loads(groq_response.tool_calls[0].function.arguments)
print(args)

print("output")
print(get_current_weather(**args))

'''


import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={OPENWEATHER_API_KEY}&q={location}"

    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['main']
        temperature_k = data['main']['temp']
        
        if unit == "celsius":
            temperature = temperature_k - 273.15  # Convert Kelvin to Celsius
            temp_unit = "°C"
        else:
            temperature = (temperature_k - 273.15) * 9/5 + 32  # Convert Kelvin to Fahrenheit
            temp_unit = "°F"
        
        weather_info = (
            f"The current weather in {location} is {weather} with a temperature of "
            f"{round(temperature, 2)}{temp_unit}."
        )
        return weather_info
    else:
        return f"Sorry, I couldn't fetch the weather data for {location}."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },   
    }
]

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": "What is the weather like in Beijing?",
        }
    ],
    temperature=0,
    max_tokens=300,
    tools=tools,
    tool_choice="auto"
)

groq_response = response.choices[0].message
args = json.loads(groq_response.tool_calls[0].function.arguments)

# Print only the weather information
print(get_current_weather(**args))
