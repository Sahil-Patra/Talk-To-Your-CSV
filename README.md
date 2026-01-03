# 🐼 Talk to your CSV

A powerful Streamlit application that allows you to analyze your CSV data using natural language. Built with **PandasAI**, **LangChain**, and **Google Gemini**, this tool lets you ask questions, generate insights, and create visualizations instantly.

## 🚀 Features

- **Natural Language Querying:** Ask questions like "Show me the top 5 sales" or "Plot a bar chart of revenue by region".
- **Dynamic Model Selection:** Automatically detects available Google Gemini models (e.g., `gemini-1.5-flash`, `gemini-pro`) linked to your API key to prevent 404 errors.
- **Interactive Visualizations:** Generates and displays charts (Bar, Line, Scatter, Pie, etc.) directly in the app.
- **Data Privacy:** Your data is processed in memory and locally; the CSV itself is not trained upon, only the metadata/schema is sent to the LLM to generate code.

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **LLM Orchestration:** [PandasAI](https://github.com/gventuri/pandas-ai) & [LangChain](https://www.langchain.com/)
- **AI Model:** Google Gemini (via `google-generativeai`)
- **Data Manipulation:** Pandas

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/talk-to-your-csv.git
   cd talk-to-your-csv
   ```
2. **Create a virtual environment (Optional but recommended)**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

**How to Run**

1. Get your Google API Key from Google AI Studio.
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. The app will open in your browser at http://localhost:8501.

**Usage Guide**
1. Enter API Key: Paste your Google API Key in the sidebar.
2. Select Model: Wait for the app to validate your key and select a model from the dropdown (e.g., gemini-1.5-flash).
3. Upload CSV: Drag and drop your CSV file.
4. Ask Questions: Type questions like:
     . "What is the correlation between age and salary?"
     . "Plot a pie chart of department distribution"
     . "Summarize the dataframe"