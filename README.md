# ai-agent-email-ollama
An AI-powered email assistant built using Ollama and the Llama 3.2:3B model — running locally on your system.
This project allows you to summarize and interact with your emails through a Streamlit interface. 

> ⚠️ **Disclaimer:**  
> This project is still in **prototype** stage.  
> Currently, the AI agent can only fetch and summarize a maximum of **25 emails** due to token limitations in the `Llama 3.2:3b` model.


<img width="1920" height="1080" alt="API" src="https://github.com/user-attachments/assets/817a7871-2cb3-415d-b2cf-51433e8ebb3a" />

## 🚀Features

📨 Summarize your Gmail inbox automatically

🔒 100% local processing (privacy-friendly)

⚙️ Streamlit-based interactive UI

## How to download

```
git clone https://github.com/syahriza-ctrl/ai-agent-email-ollama.git
```


- First you must have credentials.json! You can get from Google Cloud
- Download Ollama and get Llama3.2:3b (You can change the model instead!)

make 
```pip install -r requirements.txt ```

## Usage

```
streamlit run strmlit.py
```


