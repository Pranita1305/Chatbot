
# import os
# import cohere
# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv
from datetime import datetime

# load_dotenv()


# app=Flask(__name__)
# api_key=os.getenv('COHERE_API_KEY')
# llm=cohere.ClientV2(api_key)

def get_greeting():
    import pdb; pdb.set_trace()
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning! How can I assist you today?"
    elif 12 <= hour < 18:
        return "Good Afternoon! How can I help you?"
    else:
        return "Good Evening! What can I do for you?"
    
    
# hour=get_greeting()
# print(hour)


# @app.route("/")
# def home():
#     greeting=get_greeting()
#     return render_template("index.html",greeting=greeting)

import os
import cohere
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

api_key = os.getenv('COHERE_API_KEY')
llm = cohere.Client(api_key)

@app.route("/")
def home():
    return render_template("index.html", greeting=get_greeting())

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    if not prompt:
        return jsonify({"response": "Please type something."})

    try:
        response = llm.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return jsonify({"response": response.generations[0].text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

# instruction,input,context,format->prompt engineering
#vector db
#langchain framework,langchain.chat_models/prompts



    
