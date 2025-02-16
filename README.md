# **🍽️ Bedrock HackOMania 2025 Kitchen Copilot - AI-Powered Smart Cooking Assistant**  
🚀 **Generate recipes from ingredients you have! AI-powered cooking assistant using LangChain, Neo4j, and GPT-4 Turbo.**  

🔗 Try It Out! **[https://tinyurl.com/bedrock-hackomania](https://tinyurl.com/bedrock-hackomania)**  

---

## **🔧 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Irf2an/HackOMania_Bedrock
cd HackOMania_Bedrock
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
Create a **`.env` file** inside the project folder and add the following:  

```
# 🔑 OpenAI API Key for GPT-4 & Image Generation
OPENAI_API_KEY=

# 🔗 Neo4j Database Credentials (AuraDB Cloud / Local Instance)
AURA_CONNECTION_URI=
AURA_USERNAME=
AURA_PASSWORD=

# 🔒 Flask Secret Key for Secure Sessions
FLASK_SECRET_KEY=
```
- **Replace the placeholders** with **your actual API keys and credentials**.
- **Flask Secret Key** is needed for **secure user authentication**.

### **4️⃣ Run the Backend**
```bash
python recipe_backend.py
```

### **5️⃣ Access the Web App**
Open your browser and visit:  
🔗 **[http://127.0.0.1:8071/](http://127.0.0.1:8071/)**  

---

## **🌟 Key Features**
### **1️⃣ AI-Powered Recipe Generation**
- **Uses LangChain & GPT-4 Turbo** for intelligent **ingredient-based recipe generation**.
- **Supports dietary filters** (Vegan, Keto, Gluten-Free, etc.).
- **Customize spice level, cooking time, difficulty, and recipe style**.
- **Multi-Agent Workflow with LangGraph:**  Employs LangGraph to orchestrate a multi-agent system for recipe generation. This pipeline includes:
    - **Ingredient Generator:**  Analyzes images to identify and extract potential ingredients.
    - **Ingredient Filter:** Refines the generated ingredient list, ensuring relevance and culinary appropriateness.
    - **Recipe Generator:**  Leverages the filtered ingredients to create delicious and customized recipes.
    - **Recipe Filter:** Further refines and filters generated recipes based on user preferences.

### **2️⃣ Smart Image Recognition - Only ~$0.01 per Image!**
- **AI-based ingredient detection** from fridge images.
- **Efficient, low-cost model** with caching to minimize API calls.

### **3️⃣ Intelligent Image Caching for Faster Loading**
- **Ingredient and recipe images are cached** to avoid repeated API calls.
- **Reduces loading times significantly** for a seamless experience.
- **Stored locally & refreshed periodically** for up-to-date images.

### **4️⃣ UX-Friendly Interface**
- **Intuitive UI matching Kitchen Copilot’s theme**.
- **Designed with Shneiderman’s 7 Golden Rules**:
  - **Loading icons** for real-time feedback.
  - **Image preview for uploaded pictures**.
  - **Delete confirmation for user actions**.

### **5️⃣ Secure Authentication**
- **Password hashing (PBKDF2-SHA256) & Flask secret session keys** for account security.

### **6️⃣ Favorites & Recipe Curation**
- **Save recipes for quick access**.
- **Dedicated "View Favorites" section** with an easy unfavorite option.

### **7️⃣ Neo4j Graph Database for Smart Recommendations**
- **Graph-based ingredient-recipe relationships** for **faster, optimized queries**.
- **Content-based filtering using cosine similarity** to recommend meals.

### **8️⃣ Ingredient Images for Better UX**
- **Each detected ingredient includes a high-quality image**.
- **Enhances user recognition and interaction**.

### **9️⃣ Customizable Preferences**
- **Select dietary preferences, spice level, cooking time, and more**.
- **Easily modify preferences at any time**.

### **🔟 Beautiful Recipe Display**
- **Each recipe includes an image, ingredients, and step-by-step instructions**.
- **Favorites are visually highlighted with a red heart ❤️**.

---

## **🛠️ Tech Stack**
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask, LangChain, Neo4j, OpenAI GPT-4 Turbo  
- **Database:** Neo4j Graph Database  
- **Security:** PBKDF2-SHA256, Flask Sessions  

---

## **🚀 Future Enhancements**
🔜 **Voice Assistant Support for Hands-Free Cooking**  
- **Alexa & Google Assistant integration** for step-by-step cooking guidance.  
- Voice-based **recipe search & ingredient logging**.

🔹 **Add a "Cooking Mode"**  
- **Full-screen, step-by-step guided cooking mode** for a seamless experience.  
- **Hands-free navigation via voice commands**.

🔹 **Enhance Community Features**  
- **Allow users to share their own recipes** and discover others.  
- **Like, comment, and discuss recipes within the community**.

🔹 **Voice-Enabled Recipe Search**  
- **Use speech recognition** to **search for recipes hands-free**.
- Compatible with **smart speakers and voice assistants**.

---

## **👨‍💻 Contributors**
- **Xin Han** - [imevahans](https://github.com/imevahans)  
- **Bryan** - [ItsPeeko](https://github.com/ItsPeeko)  
- **Irfaan** - [Irf2an](https://github.com/Irf2an)  
