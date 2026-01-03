import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
import os
import matplotlib.pyplot as plt
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Import base LLM class safely
try:
    from pandasai.llm import LLM
except ImportError:
    from pandasai.llm.base import LLM

# --- CUSTOM ADAPTER ---
class GeminiAdapter(LLM):
    def __init__(self, api_key, model_name):
        self.chat_model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0
        )
    
    def call(self, instruction: str, value: str, suffix: str = "") -> str:
        prompt = f"{instruction}\n{value}\n{suffix}"
        response = self.chat_model.invoke(prompt)
        return response.content

    @property
    def type(self) -> str:
        return "google-gemini-adapter"

# --- PAGE CONFIG ---
st.set_page_config(page_title="Talk to your CSV", page_icon="🐼", layout="wide")
plt.switch_backend('Agg') 

st.title("Talk to your CSV 🐼")

# --- SIDEBAR & MODEL SELECTOR ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter your Google API Key", type="password")
    
    selected_model = "gemini-1.5-flash" # Default fallback
    
    # 2. Dynamic Model Fetching (The Fix for 404 Errors)
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Get only models that generate content
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Clean up model names (remove 'models/' prefix for display)
            model_options = [m.replace('models/', '') for m in models]
            
            st.success(f"✅ API Key Valid! Found {len(model_options)} models.")
            
            # Smart default selection
            default_index = 0
            if "gemini-1.5-flash" in model_options:
                default_index = model_options.index("gemini-1.5-flash")
            elif "gemini-1.5-flash-001" in model_options:
                default_index = model_options.index("gemini-1.5-flash-001")
                
            selected_model = st.selectbox("🤖 Select Model", model_options, index=default_index)
            
        except Exception as e:
            st.error(f"❌ API Key Error: {e}")

# --- MAIN APP ---
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=['csv'])

if 'df' not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Error reading file: {e}")

if st.session_state.df is not None:
    st.markdown("---")
    user_query = st.text_area("Enter your question:", height=100)
    
    if st.button("🚀 Ask"):
        if not api_key:
            st.error("⚠️ Please enter your API Key")
        else:
            try:
                with st.spinner(f"🤔 Thinking using {selected_model}..."):
                    
                    # 3. Pass the SELECTED model to the adapter
                    llm_adapter = GeminiAdapter(api_key=api_key, model_name=selected_model)
                    
                    smart_df = SmartDataframe(
                        st.session_state.df,
                        config={
                            "llm": llm_adapter,
                            "save_charts": True,
                            "save_charts_path": "exports/charts",
                            "verbose": True,
                            "open_charts": False
                        }
                    )
                    
                    response = smart_df.chat(user_query)
                    
                    st.markdown("---")
                    st.subheader("Results")
                    
                    if isinstance(response, str) and (response.endswith('.png') or response.endswith('.jpg')):
                        if os.path.exists(response):
                            st.image(response)
                        else:
                            st.write(response)
                    elif isinstance(response, pd.DataFrame):
                        st.dataframe(response)
                    else:
                        st.write(response)
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")