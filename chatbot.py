import random
import re
from datetime import datetime
from typing import Dict, List, Any

class FixedHealthDataChatbot:
    def __init__(self):
        self.setup_knowledge_base()
        self.user_profiles = {}
        self.conversation_history = []
        
    def setup_knowledge_base(self):
        """Local dataset and knowledge base"""
        self.health_data_faq = {
            "greeting": [
                "👋 Hello Sonia! I'm your HealthData AI assistant. Ready to explore secure health data sharing?",
                "🤖 Hi Sonia! I can help you contribute to medical research while earning income safely.",
                "💊 Welcome Sonia! I specialize in health data marketplaces. Ask me about earnings, security, or how to get started."
            ],
            "how_it_works": [
                "Our platform uses blockchain for consent and AI for anonymization. Three simple steps:\n1. You set data preferences\n2. AI anonymizes your data\n3. Researchers purchase it\n4. You get paid in cryptocurrency",
                "Process: Blockchain records your consent → AI removes personal identifiers → Researchers buy anonymized data → You receive crypto payments automatically."
            ],
            "earnings": [
                "💰 **Sleep Data Earnings**: $60-100 depending on detail level\n• Basic sleep patterns: $60\n• Detailed sleep stages: $80\n• Long-term sleep analysis: $100+",
                "💰 Typical sleep data earnings: $60-150. More detailed data (sleep stages, heart rate, O2 levels) earns more."
            ],
            "security": [
                "🔒 **Sleep Data Security**: Advanced AI anonymization removes personal identifiers while preserving research value.",
                "🔒 Your sleep data is protected by:\n• Differential privacy\n• k-Anonymity algorithms\n• Blockchain consent records\n• Encrypted storage"
            ],
            "data_types": {
                "sleep": "🛌 Sleep data includes: sleep duration, quality, stages (REM/deep/light), disruptions, and patterns over time.",
                "medical": "🏥 Medical records: diagnosis history, treatments, medications, lab results, doctor visits.",
                "genetic": "🧬 Genetic data: DNA markers, ancestry information, health predispositions, trait data.",
                "fitness": "🏃 Fitness data: activity levels, heart rate, steps, workouts, recovery metrics."
            },
            "getting_started": [
                "🚀 Let's start with your sleep data! I'll help you set up secure sharing and estimate your earnings."
            ]
        }
        
        self.data_valuation = {
            "sleep": {"base": 60, "detailed": 100, "longitudinal": 150},
            "medical": {"base": 100, "chronic": 200, "routine": 50},
            "genetic": {"base": 200, "rare": 500, "common": 150},
            "fitness": {"base": 80, "continuous": 150, "spot": 30}
        }

    def classify_intent(self, message: str) -> str:
        """Better intent classification"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            return "greeting"
        elif any(word in message_lower for word in ['how', 'work', 'process', 'mechanism']):
            return "how_it_works"
        elif any(word in message_lower for word in ['earn', 'money', 'payment', 'income', 'worth', 'value']):
            return "earnings"
        elif any(word in message_lower for word in ['safe', 'secure', 'privacy', 'protect', 'anonymous']):
            return "security"
        elif any(word in message_lower for word in ['sleep', 'medical', 'genetic', 'fitness', 'data type']):
            return "data_types"
        elif any(word in message_lower for word in ['yes', 'sure', 'ok', 'okay', 'let\'s', 'start', 'begin', 'guide']):
            return "get_started"
        elif any(word in message_lower for word in ['no', 'not', "don't"]):
            return "negative"
        else:
            return "general_inquiry"

    def generate_response(self, message: str, user_id: str = "sonia") -> str:
        """Fixed response generation with proper conversation flow"""
        intent = self.classify_intent(message)
        
        # Update user profile with current intent
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "current_topic": None,
                "data_interests": [],
                "conversation_step": 0
            }
        
        profile = self.user_profiles[user_id]
        
        # Handle conversation flow
        if intent == "get_started" or (intent == "greeting" and "start" in message.lower()):
            profile["conversation_step"] = 1
            return self.get_started_response()
            
        elif intent == "data_types" and "sleep" in message.lower():
            profile["data_interests"] = ["sleep"]
            profile["conversation_step"] = 2
            return self.handle_sleep_data_interest()
            
        elif intent == "earnings" or (intent == "get_started" and profile["data_interests"]):
            profile["conversation_step"] = 3
            return self.provide_earnings_estimation(profile["data_interests"])
            
        elif intent == "security":
            profile["conversation_step"] = 4
            return self.provide_security_info(profile["data_interests"])
            
        elif intent == "how_it_works":
            return random.choice(self.health_data_faq["how_it_works"])
            
        elif intent == "negative":
            return "No problem! What would you like to know about instead? Earnings, security, or how it works?"
            
        else:
            # Follow context from previous steps
            if profile["conversation_step"] == 1:
                return "What type of health data do you have? (sleep, medical, genetic, fitness)"
            elif profile["conversation_step"] == 2:
                return "Would you like to know about earnings potential for your sleep data, or how we keep it secure?"
            elif profile["conversation_step"] >= 3:
                return "Is there anything else you'd like to know about sleep data sharing? Or shall we proceed to setup?"
            else:
                return random.choice(self.health_data_faq["greeting"]) + "\n\nI can help you with:\n• Data valuation 💰\n• Security explanations 🔒\n• Getting started 🚀"

    def get_started_response(self) -> str:
        """Start the conversation flow"""
        return """🚀 Excellent! Let's get you set up step by step:

First, what type of health data would you like to share?
• 🛌 Sleep data
• 🏥 Medical records  
• 🧬 Genetic/DNA data
• 🏃 Fitness tracker data

Just tell me which type you have!"""

    def handle_sleep_data_interest(self) -> str:
        """Handle sleep data specifically"""
        return """🛌 Great choice! Sleep data is very valuable for research on:
• Sleep disorders
• Mental health studies
• Chronic disease research
• Performance optimization

Would you like to know:
1. 💰 How much you can earn with sleep data?
2. 🔒 How we keep your sleep data secure?
3. 🚀 How to get started right away?

Just say 'earnings', 'security', or 'get started'!"""

    def provide_earnings_estimation(self, data_types: List[str]) -> str:
        """Provide detailed earnings information"""
        if "sleep" in data_types:
            return f""" **Sleep Data Earnings Breakdown:**

• Basic sleep duration: ${self.data_valuation['sleep']['base']}
• Detailed sleep stages: ${self.data_valuation['sleep']['detailed']} 
• Long-term patterns (3+ months): ${self.data_valuation['sleep']['longitudinal']}+

📈 **Passive Income Potential**: $80-150 monthly for continuous sleep monitoring data

Your sleep data helps research on insomnia, sleep apnea, and mental health!"""

    def provide_security_info(self, data_types: List[str]) -> str:
        """Provide security information"""
        if "sleep" in data_types:
            return """ **Sleep Data Security Features:**

• AI Anonymization: Personal identifiers removed while preserving sleep patterns
• Differential Privacy: Mathematical guarantee that your identity is protected
• Blockchain Consent: You control exactly what researchers can access
• Encrypted Storage: Military-grade encryption for all stored data
• k-Anonymity: Your data is grouped with 50+ others for extra protection

Your sleep habits and patterns are completely anonymous to researchers!"""

def interactive_chat():
    """Run the fixed interactive chat"""
    bot = FixedHealthDataChatbot()
    user_id = "sonia"
    
    print("\n" + "=" * 60)
    print(" HealthData AI Assistant Activated!")
    print(" Ask about: Earnings • Security • How it works • Getting started")
    print(" Type 'quit' to exit")
    print("=" * 60)
    
    # Initial greeting
    print(f" {bot.generate_response('hello', user_id)}")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(" Thank you Sonia! Your health data can make a difference. Stay healthy! ")
                break
                
            if user_input:
                response = bot.generate_response(user_input, user_id)
                print(f" Bot: {response}")
            else:
                print(" Please type your question about health data sharing!")
                
        except KeyboardInterrupt:
            print("\n Session ended. Thank you Sonia!")
            break
        except Exception as e:
            print(f" I encountered an error. Let's continue! What else would you like to know?")

# Test function to verify it works
def test_fixed_bot():
    """Test the fixed bot with Sonia's conversation"""
    bot = FixedHealthDataChatbot()
    user_id = "sonia"
    
    test_conversation = [
        "ok lets start",
        "sleep data", 
        "earnings",
        "security",
        "how does it work",
        "get started"
    ]
    
    print("Testing Fixed Bot with Sonia's conversation...")
    print("=" * 50)
    
    for message in test_conversation:
        print(f" Sonia: {message}")
        response = bot.generate_response(message, user_id)
        print(f" Bot: {response}")
        print("-" * 50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_fixed_bot()
    else:
        interactive_chat()
