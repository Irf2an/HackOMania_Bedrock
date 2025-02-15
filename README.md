## **🍽️ Bedrock HackOMania 2025 Kitchen Copilot - AI-Powered Smart Cooking Assistant**  
🚀 **Generate recipes from ingredients you have! AI-powered cooking assistant using LangChain, Neo4j, and GPT-4 Turbo.**  

🔗 Try It Out! **[https://tinyurl.com/bedrock-hackomania](https://tinyurl.com/bedrock-hackomania)**  

---

### **🔧 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Irf2an/HackOMania_Bedrock
cd Kitchen-Copilot
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Backend**
```bash
python recipe_backend.py
```

### **4️⃣ Access the Web App**
Open your browser and visit:  
🔗 **[http://127.0.0.1:8071/](http://127.0.0.1:8071/)**  

---

## **🌟 Key Features**
### **1️⃣ AI-Powered Recipe Generation**
- **Uses LangChain & GPT-4 Turbo** for intelligent **ingredient-based recipe generation**.
- **Supports dietary filters** (Vegan, Keto, Gluten-Free, etc.).
- **Customize spice level, cooking time, difficulty, and recipe style**.

### **2️⃣ Smart Image Recognition - Only ~$0.01 per Image!**
- **AI-based ingredient detection** from fridge images.
- **Efficient, low-cost model** with caching to minimize API calls.

### **3️⃣ UX-Friendly Interface**
- **Intuitive UI matching Kitchen Copilot’s theme**.
- **Designed with Shneiderman’s 7 Golden Rules**:
  - **Loading icons** for real-time feedback.
  - **Image preview for uploaded pictures**.
  - **Delete confirmation for user actions**.

### **4️⃣ Secure Authentication**
- **Password hashing (PBKDF2-SHA256) & Flask secret session keys** for account security.

### **5️⃣ Favorites & Recipe Curation**
- **Save recipes for quick access**.
- **Dedicated "View Favorites" section** with an easy unfavorite option.

### **6️⃣ Neo4j Graph Database for Smart Recommendations**
- **Graph-based ingredient-recipe relationships** for **faster, optimized queries**.
- **Content-based filtering using cosine similarity** to recommend meals.

### **7️⃣ Ingredient Images for Better UX**
- **Each detected ingredient includes a high-quality image**.
- **Enhances user recognition and interaction**.

### **8️⃣ Customizable Preferences**
- **Select dietary preferences, spice level, cooking time, and more**.
- **Easily modify preferences at any time**.

### **9️⃣ Beautiful Recipe Display**
- **Each recipe includes an image, ingredients, and step-by-step instructions**.
- **Favorites are visually highlighted with a red heart ❤️**.

---

## **🛠️ Tech Stack**
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask, LangChain, Neo4j, OpenAI GPT-4 Turbo  
- **Database:** Neo4j Graph Database  
- **Security:** PBKDF2-SHA256, Flask Sessions  

---

## **👨‍💻 Contributors**
- **Xin Han** - [imevahans](https://github.com/imevahans)  
- **Bryan** - [ItsPeeko](https://github.com/ItsPeeko)  
- **Irfaan** - [Irf2an](https://github.com/Irf2an)  

---

## **🚀 Future Enhancements**
🔜 **AI Meal Planning & Weekly Recipe Suggestions**  
🔜 **Grocery Delivery Service Integration**  
🔜 **Mobile App (iOS & Android)**  
🔜 **Voice Assistant Support for Hands-Free Cooking**  