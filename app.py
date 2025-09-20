# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import subprocess
import json
import tempfile
import os

# --- Configuration ---
# The code will try to get the API key from Streamlit's secrets management.
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except (KeyError, FileNotFoundError):
    st.error("API Key not found! Please create a .streamlit/secrets.toml file with your GOOGLE_API_KEY.")
    st.stop()


# --- Core Logic Functions ---

# The new function takes 'language' as an argument
def analyze_security(code_string, language):
    report = ""
    # Still create a temp file, but the suffix might change
    suffix_map = {
        "Python": ".py",
        "Java": ".java",
        "C": ".c",
        "C++": ".cpp"
    }
    suffix = suffix_map.get(language, ".tmp")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as temp_file:
        temp_file.write(code_string)
        temp_filepath = temp_file.name

    try:
        if language == "Python":
            command = ['bandit', '-f', 'json', temp_filepath]
            # (Your existing Bandit parsing logic goes here)

        elif language == "C" or language == "C++":
            # NOTE: Cppcheck outputs XML. You'll need an XML parser.
            command = ['cppcheck', '--enable=all', '--xml', temp_filepath]
            # (You'll need to write new logic to run this command and parse the XML report)
            
        elif language == "Java":
            # NOTE: PMD also has different output formats.
            # This is an example command; you'll need to check the PMD docs.
            command = [
                'pmd', 'check', '-d', temp_filepath, 
                '-R', 'rulesets/java/quickstart.xml', '-f', 'text'
            ]
            # (You'll need to write new logic to run this and parse the text report)
        
        # --- This part needs to be rewritten to handle different command outputs ---
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        report = result.stderr if language == "C++" else result.stdout # Example
        if not report:
             report = f"No security issues found by {language} scanner."

    finally:
        os.remove(temp_filepath)
        
    return report

# The new function also takes 'language'
def get_ai_suggestions(code_string, security_report, language):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # The prompt now uses the 'language' variable
    prompt = f"""
    You are an expert code reviewer for the **{language}** programming language.
    Your task is to analyze the following code for performance and security.
    
    Instructions:
    1.  **Time Complexity Analysis:** Determine the Big O notation.
    2.  **Code Optimization:** Rewrite the code to be more efficient in **{language}**.
    3.  **Security Review:** Based on the security report, explain the vulnerabilities.
    4.  **Format your response** with the headings: `### Time Complexity Analysis`, `### Optimized Code`, `### Security Review`.

    **Security Report:**
    ```
    {security_report}
    ```

    **Code to Analyze:**
    ``` {language.lower()}
    {code_string}
    ```
    """
    
    # (The rest of the function stays the same)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with the AI model: {e}"    


# --- Streamlit UI ---

st.set_page_config(layout="wide")
st.title("🤖 AI Code Optimizer")
language = st.selectbox(
    "Select the programming language:",
    ("Python", "C", "C++", "Java")
)

st.write(f"Paste your {language} code below to get suggestions...")

placeholder_code = """
# Enter you code here
"""

user_code = st.text_area("Your Python Code:", height=300, value=placeholder_code)

# This is the complete UI logic
if st.button(f"🚀 Analyze {language} Code"):
    if not user_code.strip():
        st.warning("Please paste some code to analyze.")
    else:
        with st.spinner("Analyzing..."):
            security_report = analyze_security(user_code, language)
            ai_response = get_ai_suggestions(user_code, security_report, language)
        
        st.success("Analysis complete!")
        st.markdown("---")
        st.header("Analysis Results")
        
        # Try to parse the AI's response to show the side-by-side view
        try:
            parts = ai_response.split("### Optimized Code")
            analysis_text_part1 = parts[0]
            
            code_and_rest = parts[1].split("### Security Review")
            optimized_code_snippet = code_and_rest[0].strip().replace("```python", "").replace("```", "").replace(language.lower(), "")
            analysis_text_part2 = "### Security Review" + code_and_rest[1]
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Your Original Code")
                st.code(user_code, language=language.lower())
            with col2:
                st.subheader("AI's Suggested Code")
                st.code(optimized_code_snippet, language=language.lower())
            
            st.subheader("💡 AI Insights")
            st.markdown(analysis_text_part1 + analysis_text_part2)

        except IndexError:
            # If the AI's response format is unexpected, just display the whole thing
            st.subheader("💡 AI Insights")
            st.markdown(ai_response)