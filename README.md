# Azure Cognitive Services Feedback Form (AI-900 Project)
---

#### Live URL: [https://victorious-beach-00bf7640f.4.azurestaticapps.net/](https://victorious-beach-00bf7640f.4.azurestaticapps.net/) 
**Note:** It might take a few moments for the server to start up. Thank you for your patience!

---

<!--ts-->
  - [Project](#project)
    - [Objective](#objective)
    - [Tech Stack](#tech-stack)
    - [Setup & Configuration](#setup-config)
<!--te-->

---


## Project<a id="project"></a>
### Objective <a id="objective"></a>

The objective of this project is to develop a web application featuring a streamlined dashboard and user interface that enables users to submit feedback, analyze sentiment, and generate personalized responses in both text and audio formats. This functionality leverages the GPT-4 large language model (LLM), Azure Cognitive Services, and optimized prompts. The text-to-speech feature utilizes Azure Speech and SSML to deliver a dynamic and emotionally engaging experience.
### Tech Stack <a id="tech-stack"></a>

- **Backend**: Azure, Django, Unit Testing
- **Frontend**: React, Axios
- **Azure Services**: Azure App Service, Azure Static Web App, Azure AI Services (Language, Speech)  
- **DevOps & Tools**: CI/CD, GitHub Actions, Git, GitHub  
- **AI**: LLM (GPT-4), Prompt Engineering, Sentiment Analysis

### Setup & Configuration <a id="setup-config"></a>

1. **Clone the repository**:  
   Run this in the root directory:
   ```bash
   git clone https://github.com/soroush-04/azure-ai-sentiment.git

3. **Install required dependencies**:
    ```bash
    python -m venv venv
    cd backend
    ```
   macOS/Linux: ```source venv/bin/activate```
   
   Windows: ```venv\Scripts\activate```
   
    ```python
   pip install -r requirements.txt`

4. **Place the `.env` file** in the root directory:  
   -- If you don't have access to the `.env` file, you need to set up **Azure Cognitive Services** (Language, Speech), **OpenAI API key**, and other credentials based on the `.env.example` file.  

5. **Run the backend**:
    ```bash
    python3 backend/manage.py runserver

6. **Run the frontend**: Open a new terminal
   ```bash
   cd frontend
   npm start
