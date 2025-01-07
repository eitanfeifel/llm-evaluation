from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Tuple, Any, List
import google.generativeai as genai
from huggingface_hub import HfApi
from dotenv import load_dotenv
from openai import OpenAI  
from groq import Groq  
import anthropic
import asyncio
import torch
import time
import os

load_dotenv()

class ModelLoader:
    def __init__(self):
        self.loaded_models: Dict[str, Tuple[Any, Any]] = {}
        self.api_models: Dict[str, Any] = {}
        self.available_models: Dict[str, List[str]] = {
            'openai': ['gpt-4o', 'gpt-4o-mini'],
            'gemini': ['gemini-1.5-flash'],
            'groq': ['mixtral-8x7b-32768', 'llama3-70b-8192'],
            'claude': ['claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022']
        }

    async def initialize_models(self):
        try:
            # OpenAI setup 
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                openai_client = OpenAI(api_key=openai_key) 
                self.api_models['openai'] = openai_client  
                print("✓ OpenAI client initialized")
            else:
                print("✗ OpenAI API key not found")

            # Gemini setup 
            gemini_key = os.getenv('GOOGLE_API_KEY')
            if gemini_key:
                genai.configure(api_key=gemini_key)
                self.api_models['gemini'] = genai
                print("✓ Gemini client initialized")
            else:
                print("✗ Gemini API key not found")

            # Groq setup
            groq_key = os.getenv('GROQ_API_KEY')
            if groq_key:
                groq_client = Groq(api_key=groq_key)
                self.api_models['groq'] = groq_client
                print("✓ Groq client initialized")
            else:
                print("✗ Groq API key not found")
            
            #claude setup
            anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            if anthropic_key:
                anthropic_client = anthropic.Anthropic(api_key = anthropic_key)
                self.api_models['claude'] = anthropic_client
                print("✓ Claude client initialized")
            else:
                print("✗ Claude API key not found")

            

        except Exception as e:
            print(f"Error initializing API clients: {str(e)}")

        

    def openai(self, model_name: str, prompt_text: str, task: str):
        if 'openai' in self.api_models and model_name in self.available_models['openai']:
            openai_client = self.api_models['openai']  # Access the OpenAI client
            completion = openai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": f"You are a helpful assistant answer questions regarding: {task}."},
                          {"role": "user", "content": prompt_text}]
            )
            return completion.choices[0].message.content
        else:
            print(f"✗ OpenAI model {model_name} not available or initialized.")
            return None

    def gemini(self, model_name: str, prompt_text: str, task: str):
        if 'gemini' in self.api_models:
            model = genai.GenerativeModel(model_name)
            task_prompt = f"Respond to the following prompt based on the domain: {task}. Prompt: {prompt_text}  "
            response = model.generate_content(task_prompt, stream=True)
            response_text = ""
            for chunk in response:
                response_text += chunk.text
            return response_text
        else:
            print(f"✗ Gemini model {model_name} not available or initialized.")
            return None

    def groq(self, model_name: str, prompt_text: str, task: str):
        if 'groq' in self.api_models:
            groq_client = self.api_models['groq']
            chat_response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": f"You are a helpful assistant, answering questions within the domain of {task}"}, {"role": "user", "content": prompt_text}],
                model=model_name
            )
            return chat_response.choices[0].message.content
        else:
            print(f"✗ Groq model {model_name} not available or initialized.")
            return None
        
    def claude(self, model_name: str, prompt_text: str, task: str):
        if 'claude' in self.api_models:
            anthropic_client = self.api_models['claude']
            message = anthropic_client.messages.create(
                model=model_name,
                max_tokens=1000, 
                messages=[{
                    "role": "user",
                    "content": f"You are a helpful assistant, answering questions in the domain of: {task}"
                    }, {
                    "role": "user",
                    "content": [{"type": "text","text": prompt_text}]
                }]
            )
            return message.content[0].text
        else:
            print(f"✗ Claude model {model_name} not available or initialized.")
            return None


    
    