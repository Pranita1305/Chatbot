import openai 
import os
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")  
print(api_key)

import pdb; pdb.set_trace()

# client = OpenAI(api_key=api_key)
openai.api_key=os.getenv("OPENAI_API_KEY")


try:
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "user", "content": "what is python?"}])
        # max_tokens=20
    
    print("OpenAI key is working. Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print("Error: Could not connect to OpenAI.")
    print(e)
    
#C:\Users\prani\OneDrive\Documents\GenAi_Int>python -m venv venv

#C:\Users\prani\OneDrive\Documents\GenAi_Int>venv\Scripts\activate

# cohere_api_key = "'Ad6apiCprmtiNxKNZhZF0PW2XDR65uhDbZ73MkHh'"

# llm = cohere.ClientV2('Ad6apiCprmtiNxKNZhZF0PW2XDR65uhDbZ73MkHh')
# //llm method exploration
# response = llm.chat(
#             model="command-a-03-2025",
#             messages=[{"role": "user", "content": text}],
#         )

# === OpenAI CLI Commands and Debugging Summary ===

# 🔧 ENVIRONMENT SETUP
# --------------------
# venv\Scripts\activate
#     → Activates your Python virtual environment.

# 🐍 RUNNING PYTHON SCRIPT
# ------------------------
# python main.py
#     → Executes your main Python script.

# 📦 PACKAGE MANAGEMENT
# ---------------------
# pip freeze
#     → Lists all installed packages in the virtual environment.

# pip uninstall openai
#     → Uninstalls the OpenAI package (here, version 1.93.0 was removed).

# pip install openai==0.28
#     → Installs a specific (older/legacy) version of the OpenAI Python SDK.

# 🐞 PYTHON DEBUGGER (PDB)
# ------------------------
# Entered after hitting an error inside main.py

# Common PDB commands used:
#     - c                      → Continue execution
#     - response = ...        → Manually call OpenAI API
#     - import openai         → Re-import the module inside debugger
#     - openai.api_key = ...  → Set the API key manually inside PDB

# 📛 ERRORS ENCOUNTERED
# ---------------------
# 1. QUOTA ERROR (HTTP 429):
#     You exceeded your current quota, please check your plan and billing details.

# 2. VERSION CONFLICT ERROR:
#     Tried using `openai.ChatCompletion` in SDK version >=1.0.0 which is deprecated.
#     Solved by downgrading to openai==0.28.

# 3. AUTHENTICATION ERROR:
#     No API key provided. You must set it either by:
#         - Setting `openai.api_key = <your-key>`
#         - Or using a .env file with `OPENAI_API_KEY=...`

# 4. ATTRIBUTE TYPO:
#     Used `openai.ChatCompletions.create` → Incorrect (extra ‘s’)
#     Correct one: `openai.ChatCompletion.create`

# ✅ FINAL WORKING CODE (For openai==0.28)
# ---------------------------------------
# main.py:
# --------
# import openai
# import os
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "What is Python?"}]
# )

# print(response["choices"][0]["message"]["content"])


# 📎 NOTES
# --------
# - You downgraded OpenAI SDK to 0.28 for legacy compatibility.
# - Consider checking your OpenAI billing: https://platform.openai.com/account/billing
# - Also make sure your .env file is configured correctly and located in the root of the project.