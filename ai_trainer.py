import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

def create_training_prompt(topic, user_profile):
    """Create a prompt for Gemini to generate training content"""
    
    return f"""
You are an expert cybersecurity trainer creating a short training module.

Create a training module in JSON format with this structure:

{{
  "title": "string - module title",
  "introduction": "string - 2-3 sentences explaining why this matters for their role",
  "key_concepts": [
    {{"concept": "string - concept name", "explanation": "string - clear explanation"}},
    {{"concept": "string", "explanation": "string"}}
  ],
  "real_world_examples": [
    "string - realistic example"
  ],
  "best_practices": [
    "string - actionable best practice"
  ],
  "quiz": [
    {{"question": "string - quiz question", "options": ["option A", "option B", "option C"], "correct": "option A"}}
  ]
}}

Topic: {topic}
User Role: {user_profile['role']}
Industry: {user_profile['industry']}
Technical Level: beginner

Requirements:
- Make it relevant to their {user_profile['industry']} industry
- Use real examples from their role ({user_profile['role']})
- Keep it practical and actionable
- Include 3-4 key concepts
- Include 2-3 real world examples
- Include 4-5 best practices
- Include 3-5 quiz questions with clear correct answers
- Use professional but accessible language

IMPORTANT: Return ONLY the JSON. No extra text, no markdown, no explanations. Just the JSON object.
"""

def generate_training_module(topic, user_profile):
    """
    Generate AI training content using Gemini
    
    Args:
        topic: Training topic (e.g., "Phishing Awareness")
        user_profile: Dict with 'role', 'industry', 'tech_level'
    
    Returns:
        Dict with training content or None if error
    """
    
    prompt = create_training_prompt(topic, user_profile)
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        print(f"🤖 Generating AI content for: {topic}")
        print(f"   Role: {user_profile['role']}")
        print(f"   Industry: {user_profile['industry']}")
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "")
        
        # Try to parse JSON
        content = json.loads(text)
        
        print(f"✅ Generated successfully: {content.get('title', topic)}")
        return content
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"   Raw response: {text[:200]}...")
        return None
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return None

def get_fallback_content(topic):
    """Fallback content if AI generation fails"""
    
    fallbacks = {
        "Phishing Awareness": {
            "title": "Phishing Awareness",
            "introduction": "Phishing attacks are the #1 way hackers target businesses. Learn to spot suspicious emails and protect your organization.",
            "key_concepts": [
                {"concept": "What is Phishing?", "explanation": "Phishing is when attackers send fake emails pretending to be trusted sources to steal information."},
                {"concept": "Recognizing Red Flags", "explanation": "Look for urgent language, requests for passwords, suspicious links, and mismatched email addresses."},
                {"concept": "What to Do", "explanation": "Never click links in suspicious emails. Report to IT. Call the company directly if unsure."}
            ],
            "real_world_examples": [
                "Email from 'paypa1.com' asking to verify your account",
                "Message from 'CEO' asking for urgent wire transfer",
                "Link to Google login that looks slightly off"
            ],
            "best_practices": [
                "Hover over links to see actual URL before clicking",
                "Never enter credentials from email links",
                "Report suspicious emails to IT immediately",
                "Verify requests by calling directly"
            ],
            "quiz": [
                {
                    "question": "You receive an email from your bank asking to click a link to update payment info. What should you do?",
                    "options": ["Click the link immediately", "Call your bank directly at their known number", "Forward to colleagues"],
                    "correct": "Call your bank directly at their known number"
                },
                {
                    "question": "What's a red flag in a suspicious email?",
                    "options": ["Generic greeting", "Request for sensitive info", "All of the above"],
                    "correct": "All of the above"
                }
            ]
        },
        "Password Security": {
            "title": "Password Security",
            "introduction": "Weak passwords are a major security risk. Learn to create strong passwords and protect your accounts.",
            "key_concepts": [
                {"concept": "Strong vs Weak Passwords", "explanation": "Strong passwords have 12+ characters, mix upper/lower case, numbers, and symbols."},
                {"concept": "Password Reuse Risk", "explanation": "Never use the same password across multiple sites. If one site is breached, all accounts are at risk."}
            ],
            "real_world_examples": [
                "Weak: 'password123' - Easy to guess",
                "Strong: 'BlueSky$42!Elephant' - Mix of characters"
            ],
            "best_practices": [
                "Use 12+ character passwords with mixed character types",
                "Never reuse passwords across different sites",
                "Enable Multi-Factor Authentication (MFA) everywhere",
                "Use a password manager to store complex passwords"
            ],
            "quiz": [
                {
                    "question": "Which password is strongest?",
                    "options": ["password123", "P@ssw0rd!", "BlueSky$42!Elephant"],
                    "correct": "BlueSky$42!Elephant"
                }
            ]
        },
        "Ransomware Prevention": {
            "title": "Ransomware Prevention",
            "introduction": "Ransomware locks your files and demands payment. Learn prevention strategies to protect your organization.",
            "key_concepts": [
                {"concept": "What is Ransomware?", "explanation": "Malware that encrypts files and demands payment for decryption keys."},
                {"concept": "How It Spreads", "explanation": "Often through phishing emails, suspicious downloads, or unpatched software."}
            ],
            "real_world_examples": [
                "Email with infected attachment claiming to be invoice",
                "Fake Windows security warning asking to download"
            ],
            "best_practices": [
                "Keep all software updated and patched",
                "Don't download files from untrusted sources",
                "Maintain regular encrypted backups",
                "Report unusual activity immediately"
            ],
            "quiz": [
                {
                    "question": "What's the best response if you suspect ransomware?",
                    "options": ["Pay the ransom", "Contact IT immediately", "Ignore it"],
                    "correct": "Contact IT immediately"
                }
            ]
        },
        "Data Protection Basics": {
            "title": "Data Protection Basics",
            "introduction": "Protecting sensitive data is everyone's responsibility. Learn best practices for handling business and customer information.",
            "key_concepts": [
                {"concept": "Data Classification", "explanation": "Classify data as public, internal, confidential, or restricted to handle appropriately."},
                {"concept": "Access Control", "explanation": "Only authorized personnel should access sensitive data, following 'need to know' principle."}
            ],
            "real_world_examples": [
                "Customer credit card data must be encrypted",
                "Employee personal files require access controls"
            ],
            "best_practices": [
                "Only share data with authorized people",
                "Use secure file sharing (not personal email)",
                "Lock your computer when away",
                "Dispose of sensitive documents securely"
            ],
            "quiz": [
                {
                    "question": "What should you do with sensitive customer data?",
                    "options": ["Email it to colleagues", "Use secure file sharing", "Store on personal cloud"],
                    "correct": "Use secure file sharing"
                }
            ]
        }
    }
    
    return fallbacks.get(topic, {
        "title": topic,
        "introduction": f"Training on {topic}",
        "key_concepts": [],
        "real_world_examples": [],
        "best_practices": [],
        "quiz": []
    })
