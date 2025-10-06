import openai
import googlemaps
from flask import Flask, request, jsonify


app = Flask(__name__)


gmaps = googlemaps.Client(key='AIzaSyBRm2TmOGjRE5vrpLF9oY5LtPYhruRxUk0')


openai.api_key = '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'


potholes_data = {
    "New York": [{"location": "5th Ave", "severity": "High", "reported_on": "2025-09-25"}],
    "Los Angeles": [{"location": "Hollywood Blvd", "severity": "Medium", "reported_on": "2025-09-20"}],
    # Add more cities and potholes as needed
}


def get_potholes_info(location):
    if location in potholes_data:
        return potholes_data[location]
    else:
        return None


def generate_chatbot_response(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"User: {user_input}\nChatbot:",
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/chat', methods=['POST'])
def chat():
  
    user_input = request.json.get('message')


    if 'pothole' in user_input.lower():
        location = user_input.split("in")[-1].strip()  # Extract location from the user input

      
        potholes = get_potholes_info(location)
        
        if potholes:
          
            pothole_details = "\n".join(
                [f"Location: {pothole['location']}, Severity: {pothole['severity']}, Reported On: {pothole['reported_on']}" for pothole in potholes]
            )
            response = f"Here are the potholes reported in {location}:\n{pothole_details}"
        else:
          
            response = f"No potholes have been reported in {location}. Would you like to report one?"

    else:
       
        response = generate_chatbot_response(user_input)
    
    return jsonify({'response': response})

@app.route('/')
def index():
    return "AI Pothole Chatbot is running. Send a POST request to /chat."

if __name__ == '__main__':
    app.run(debug=True)
