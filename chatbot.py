import os
import json
import boto3
from dotenv import load_dotenv


class CollegeAdvisor:
    def __init__(self):
        load_dotenv(encoding="utf-8")
        
        # Configure AWS client
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv('AWS_DEFAULT_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
        self.history = []
        
        self.system_prompt = """You are an AI college advisor that helps students with university admissions and course selection. Provide personalized guidance based on academic interests, career goals, and application materials. Be supportive and informative while maintaining professionalism."""

    def chat(self):
        print("🎓 College Admission Assistant (Type 'exit' to quit)\n")
        while True:
            try:
                user_input = input("Student: ")
                if user_input.lower() in ['exit', 'quit']:
                    print("\n🌟 Good luck with your applications!")
                    break
                
                response = self.get_response(user_input)
                print(f"\nAdvisor: {self.format_response(response)}\n")
                
            except KeyboardInterrupt:
                print("\nSession ended.")
                break

    def get_response(self, prompt):
        # Add user message to history
        self.history.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })
        
        # Build API request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": self.system_prompt,
            "messages": self.history[-5:]  # Maintain conversation context
        }
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body))
            
            response_data = json.loads(response['body'].read())
            ai_response = response_data['content'][0]['text']
            
            # Add assistant response to history
            self.history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": ai_response}]
            })
            
            return ai_response
            
        except Exception as e:
            return f"Error: {str(e)}"

    def format_response(self, text):
        # Improved formatting for lists and emphasis
        return (text
                .replace("- ", "• ")
                .replace("", "")
                .replace("Step ", "\nStep ")
                .replace("  ", " ")
                .strip())

if __name__ == "__main__":
    try:
        advisor = CollegeAdvisor()
        print("✅ System ready!")
        advisor.chat()
    except Exception as e:
        print(f"❌ Startup failed: {str(e)}")