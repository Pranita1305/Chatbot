import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Langchain imports
from langchain_cohere import ChatCohere # For chat models, which is what Cohere's command-r-plus is
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

app = Flask(__name__)

cohere_api_key = os.getenv('COHERE_API_KEY')

llm = ChatCohere(cohere_api_key=cohere_api_key, model="command-r-plus", temperature=0.7)
output_parser = StrOutputParser()

def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning! What would you like to talk about today?"
    elif 12 <= hour < 18:
        return "Good Afternoon! What are you curious about today?"
    else:
        return "Good Evening! What topic are you interested in exploring?"

def get_trending_topics():
    
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful AI assistant. Your goal is to list trending topics."),
        HumanMessagePromptTemplate.from_template("List 3 trending topics that people are talking about right now. Just give the list with one topic per line, starting with a bullet point.")
    ])
    
    chain = prompt_template | llm | output_parser

    try:
        response = chain.invoke({})
        return [topic.strip("• ").strip() for topic in response.strip().split("\n") if topic.strip()]
    except Exception as e:
        print(f"Error fetching trending topics: {e}")
        return ["AI advancements", "Space exploration", "Climate change initiatives"]

def get_related_topics(user_topic):
    
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful AI assistant. Your goal is to suggest related topics."),
        HumanMessagePromptTemplate.from_template("Given the topic '{topic}', suggest 3 to 5 related or sub-topics that someone might be interested in. List them with one topic per line, starting with a bullet point.")
    ])
    
    chain = prompt_template | llm | output_parser

    try:
        response = chain.invoke({"topic": user_topic})
        return [topic.strip("• ").strip() for topic in response.strip().split("\n") if topic.strip()]
    except Exception as e:
        print(f"Error fetching related topics for '{user_topic}': {e}")
        return [f"More about {user_topic}", "Future of " + user_topic.lower(), "Impact of " + user_topic.lower()]

@app.route("/")
def home():
    greeting = get_greeting()
    topics = get_trending_topics()
    return render_template("index.html", greeting=greeting, topics=topics)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("prompt", "")
    raw_chat_history = request.json.get("history", [])

    if not user_input:
        return jsonify({"response": "Please type something!"})

    
    messages = []
    for i, msg in enumerate(raw_chat_history):
        if i % 2 == 0: 
            messages.append(HumanMessage(content=msg))
        else: 
            messages.append(AIMessage(content=msg))
    
    messages.append(HumanMessage(content=user_input)) 

    
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful and friendly chatbot."),
        MessagesPlaceholder(variable_name="chat_history"), 
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    
    chain = prompt_template | llm | output_parser

    try:
        
        reply = chain.invoke({"chat_history": messages, "input": user_input})
        return jsonify({"response": reply})
    except Exception as e:
        print(f"Error during chat: {e}")
        return jsonify({"response": "Error: Could not process your request at the moment. Please try again later."})

@app.route("/suggest_topics", methods=["POST"])
def suggest_topics():
    user_topic = request.json.get("topic", "")
    if not user_topic:
        return jsonify({"suggestions": [], "error": "No topic provided for suggestions."})
    suggestions = get_related_topics(user_topic)
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)

