from models import BaseModel
import time
import attrs

class GeminiModel(BaseModel):
    def __init__(self, api_key):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.client = genai

    def generate(self, prompt, greedy_generation, model_id="gemini-2.5-pro", max_attempts=3):
        for i in range(max_attempts):
            try:
                responses = self._make_api_call(prompt, model_id, greedy_generation)
                return responses
            except Exception as e:
                print(f"Error making API call: {e}.\n\n Retrying...")
                time.sleep(1.5 ** i)

    def _build_gemini_and_system_messages(self, prompt):
        # First pass: collect system content and build gemini_messages
        gemini_messages = []
        system_message = ""

        for msg in prompt:
            if msg.get("role") == "user":
                gemini_messages.append({"role": "user", "parts": [msg["content"]]})
            elif msg.get("role") == "assistant":
                gemini_messages.append({"role": "model", "parts": [msg["content"]]})
            elif msg.get("role") == "system":
                system_message += msg["content"] + "\n\n"
        
        return gemini_messages, system_message
    
    def _handle_system_content_and_user_role(self, gemini_messages, system_message):
        if system_message:
            user_message_found = False
            if gemini_messages:
                # Find the first message with user role and prepend system content
                for msg in gemini_messages:
                    if msg["role"] == "user":
                        msg["parts"][0] = system_message + msg["parts"][0]
                        user_message_found = True
                        break
            
            # If no user message was found (either no messages or no user role), create one
            if not user_message_found:
                gemini_messages.append({"role": "user", "parts": [system_message]})
        
        return gemini_messages


    def _make_api_call(self, prompt, model_id, greedy_generation):
        import google.generativeai as genai

        # Convert OpenAI-style messages to Gemini format
        if not isinstance(prompt, list) or not len(prompt) > 0:
            model = self.client.GenerativeModel(model_id)
            response = model.generate_content(prompt)
            return response.text 
        # Handle chat format
        gemini_messages, system_message = self._build_gemini_and_system_messages(prompt)        
        # Handle system content
        gemini_messages = self._handle_system_content_and_user_role(gemini_messages, system_message)
        
        # Use the chat model
        model = self.client.GenerativeModel(model_id)
        chat = model.start_chat(history=[])
        # Send the first user message (which now contains system + user content)
        if gemini_messages:
            response = chat.send_message(gemini_messages[0]["parts"][0])
            return response.text