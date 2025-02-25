# Technical Project - Full Stack Developer in AI
---

#### Live URL: [https://victorious-beach-00bf7640f.4.azurestaticapps.net/](https://victorious-beach-00bf7640f.4.azurestaticapps.net/) 
**Note:** It might take a few moments for the server to start up. Thank you for your patience!

#### <u>Submission Date</u>: February 2, 2025, 9:00 PM EST
#### <u>Submission Date (v1.1)</u>: February 25, 2025, 6:00 PM EST
=======

<!--ts-->
  - [Scenarios](#scenarios)
    - [scenario 1 ](#scenario-1)
    - [scenario 2 ](#scenario-2)
  - [Project](#project)
    - [Objective](#objective)
    - [Tech Stack](#tech-stack)
    - [Setup & Configuration](#setup-config)
  - [References](#references)
  <!-- - [References](#references) -->
<!--te-->

---



## Scenarios<a id="scenarios"></a>

### AI-based Proof-of-Concept Coordination<a id="scenario-1"></a>

To address negative user feedback and improve our AI sytems productivity, we need to identify the root causes. The performance of the AI system can be broken down into five main areas:

1. **Accuracy**: Check if the AI system provides correct and reliable information.
2. **Verbosity**: Evaluate if the response is too short or too long, and if it affects understanding.
3. **Hallucination**: Look for instances where the AI generates hallucinations or made-up information.
4. **Adherence to Instructions**: Ensure the AI follows the instructions given in the prompt and stays on task.
5. **Writing Quality**: Review the grammar, clarity, and structure of the response. Also, check if the AI uses inappropriate, aggressive, or absuive language or phrases.

Based on the issues identified in each key area, we can focus on specific enhancements:

- **Prompt Engineering**: If issues are found in areas like accuracy, hallucination, or instruction following, we may need to refine the prompts to guide the AI better.
- **Database Quality**: If the problem lies in accuracy or hallucination, improving the quality and diversity of the available dataset can provide more reliable information.
- **Model Training**: If issues are found with instruction tracking or writing quality, we can focus on fine-tuning the model with specific training data to address those weaknesses.
- **Stress Testing**: Pushing AI systems to their limits to detect potential bottlenecks for further enhancements.  


### Future of Food and Farming (2030) <a id="scenario-2"></a>

Balancing productivity and sustainability is a major challenge for farmers. By 2030, factors like climate change, resource scarcity, pollution, loss of biodiversity, and population growth will make food systems even more fragile.  

#### The Role of Agri-Tech  

AI and emerging technologies will enhance agriculture through:  
- **Precision Agriculture**: Reducing waste, optimizing soil nutrition, and using moisture sensors  
- **Automation**: Monitoring irrigation, fertilizer use, and weather patterns  
- **Supply Chain Management**: Improving food distribution and reducing environmental impact  

#### Generative AI in Agriculture  

Generative AI can revolutionize farming by creating **adaptive, data-driven ecosystems** that optimize every stage of food production. For example:  
- **Drones (computer vision)** monitor crop health and detect diseases in real time.  
- **Digital sensors** analyze soil composition, weather conditions, and fertilizer efficiency.  
- **AI-generated simulations** process this data to predict optimal planting strategies, resource usage, and climate resilience techniques.  
- **AI-driven supply chain optimization** predicts demand, reduces food waste, and streamlines distribution for faster and more sustainable food delivery.  

By continuously learning from real-world data, AI can **simulate future scenarios**, helping farmers adapt to climate shifts, prevent crop failures, and maximize yields, while reducing environmental impact.


## Project<a id="project"></a>
### Objective <a id="objective"></a>

The objective of this project is to develop a web application with a minimal dashboard and UI that allows users to submit feedback, analyze sentiment, and generate personalized responses in both text and audio by utilizing the GPT-4 large language model (LLM), Azure Cognitive Services, and optimized prompts. The text-to-speech feature uses Azure Speech and SSML to provide an emotional and engaging experience.

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
    cd backend
    python -m venv venv
    ```
   macOS/Linux: ```source venv/bin/activate```
   
   Windows: ```venv\Scripts\activate```
   
    ```python
   pip install -r requirements.txt`

5. **Place the `.env` file** in the root directory:  
   -- If you don't have access to the `.env` file, you need to set up **Azure Cognitive Services** (Language, Speech), **OpenAI API key**, and other credentials based on the `.env.example` file.  

6. **Run the backend**:
    ```bash
    python3 backend/manage.py runserver

1. **Run the frontend**: Open a new terminal
   ```bash
   cd frontend
   npm start

## References<a id="references"></a>

1. [BASF Agriculture](https://agriculture.basf.com/ca/en)  
2. [XCube Labs - The Future of AgriTech](https://www.xcubelabs.com/blog/understanding-agritech-the-future-of-agriculture-technology/)  
3. [EU Food 2030 Initiative](https://research-and-innovation.ec.europa.eu/research-area/environment/bioeconomy/food-systems/food-2030_en)  
4. [Azure Sentiment Analysis](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview?tabs=prebuilt)  
5. [Azure Speech Synthesis](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup)  
6. [Azure Text-to-Speech Language Support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts#text-to-speech?azure-portal=true)  
