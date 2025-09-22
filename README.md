# 🤖 AI Code Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![made-with-streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red.svg)](https://streamlit.io/)

An intelligent tool that analyzes your code for security vulnerabilities and performance bottlenecks, providing AI-powered suggestions for optimization.

---

## 🚀 Live Demo

You can access the live, deployed version of the application here:

**[https://ai-code-optimizer-service-155656706851.us-central1.run.app](https://ai-code-optimizer-service-155656706851.us-central1.run.app)**

---


*(A screenshot of the application analyzing a C++ code snippet)*

## ✨ Features

* **Multi-Language Support:** Analyzes **Python**, **Java**, **C**, and **C++** code.
* **AI-Powered Optimization:** Leverages Google's Gemini LLM to suggest more efficient and Pythonic/idiomatic code.
* **Time Complexity Analysis:** Provides the Big O notation for your code to help you understand its performance characteristics.
* **Security Vulnerability Scanning:** Integrates industry-standard static analysis tools to find common security flaws:
    * **Python:** `Bandit`
    * **C/C++:** `Cppcheck`
    * **Java:** `PMD`
* **Side-by-Side Comparison:** Displays your original code next to the AI's optimized suggestion for easy review.

---

## 🛠️ Tech Stack

This project is built with a modern, cloud-native technology stack:

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend:** [Python 3.11](https://www.python.org/)
* **AI Model:** [Google Gemini API](https://ai.google.dev/)
* **Containerization:** [Docker](https://www.docker.com/)
* **Deployment:** [Google Cloud Run](https://cloud.google.com/run)
* **Static Analysis:** `Bandit`, `Cppcheck`, `PMD`

---

## ⚙️ How It Works

The application follows a simple yet powerful workflow:

1.  The user selects a programming language and submits a code snippet through the **Streamlit** frontend.
2.  The Python backend receives the code and runs the appropriate static analysis tool based on the language.
3.  The original code and the security report from the tool are packaged into a detailed prompt.
4.  This prompt is sent to the **Google Gemini API**.
5.  Gemini returns a detailed analysis including an optimized code version, time complexity, and security explanations.
6.  The results are parsed and displayed back to the user in a clean, side-by-side interface.

---

## 🔧 Running a Local Instance

To run this project on your local machine, you'll need Git and Docker Desktop installed.

**1. Clone the repository:**
bash
git clone [https://github.com/Muralikarthic/AI_Code_Optimizer-.git](https://github.com/Muralikarthic/AI_Code_Optimizer-.git)
cd AI_Code_Optimizer-

2. Prepare the PMD file:
Due to the unreliability of download links, this project copies the PMD tool from a local file.

Download pmd-dist-7.17.0-bin.zip from the .

Place the downloaded .zip file inside the main project directory.

3. Build the Docker image:
This command builds the container with all dependencies (Python, Java, Cppcheck, PMD, etc.).

4. Run the Docker container:
This command starts the application. Remember to replace "YOUR_SECRET_API_KEY" with your actual Gemini API key.

5. Access the application:
Open your web browser and navigate to http://localhost:8501.


