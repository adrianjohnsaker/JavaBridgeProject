pip install pyjnius

from jnius import autoclass

# Load Kotlin AI class dynamically
try:
    AmeliaAI = autoclass('com.yourpackage.AmeliaAI')  # Change to actual package name
    amelia = AmeliaAI()
    print("✅ Amelia AI loaded successfully")
except Exception as e:
    print(f"❌ Error loading Amelia AI: {e}")

# Example function to communicate with Kotlin AI
def query_amelia(input_text):
    try:
        return amelia.respond(input_text)
    except Exception as e:
        print(f"Error in Amelia AI response: {e}")
        return None
