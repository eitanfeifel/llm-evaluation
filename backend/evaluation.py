import asyncio
from load_models import ModelLoader

def format_output(provider, model_name, output):
    return f"\n[{provider.upper()} - {model_name}]\n{output}\n"

async def evaluate():
    loader = ModelLoader()

    print("\nInitializing API clients and loading models...")
    await loader.initialize_api_clients()

    # Display available models for each provider
    for provider, client in loader.api_models.items():
        print(f"\n✓ {provider.capitalize()} API client initialized.")
        print(f"  Available models: {', '.join(loader.available_models[provider])}")

    while True:
        # Prompt the user for input
        user_input = input("\nEnter your prompt (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting... Goodbye!")
            break

        # Process the prompt for each provider
        for provider, models in loader.available_models.items():
            for model_name in models:
                print(f"\nGenerating output for {provider.capitalize()} model: {model_name}...")

                try:
                    if provider == 'openai':
                        output = loader.openai(model_name, user_input)
                    elif provider == 'gemini':
                        output = loader.gemini(model_name, user_input)
                    elif provider == 'groq':
                        output = loader.groq(model_name, user_input)
                    else:
                        output = "Provider not recognized."

                    print(format_output(provider, model_name, output))

                except Exception as e:
                    print(f"Error generating output for {provider.capitalize()} model {model_name}: {str(e)}")


if __name__ == "__main__":
    asyncio.run(evaluate())
