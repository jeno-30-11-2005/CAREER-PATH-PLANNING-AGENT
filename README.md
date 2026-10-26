# Intelligent Career Path Planning System

**BE Artificial Intelligence and Data Science Mini-Project**  
A simple, complete, and explainable career guidance application built with **Python & Streamlit**.

---

## 🎯 Project Purpose
Many engineering students struggle to decide which career path fits their skills and interests. This application helps students:
1. Input their academic profile, skills, and interests.
2. Receive transparent, rule-based career recommendations.
3. Understand their **Skill Gap** (skills they already possess vs. skills they need to learn).
4. Follow a structured **4-step career roadmap** with timelines and milestones.

---

## 🛠️ Technology Stack
- **Language:** Python 3.11
- **User Interface:** Streamlit (clean, modern, single-page dashboard)
- **Logic:** Transparent rule-based weighted matching (no black-box AI, no external APIs, no database required)

---

## 📁 Project Structure (Only 4 Core Files)

```
CAREER PATH PLANNING AGENT/
│
├── app.py              # Main Streamlit web application (UI & navigation)
├── career_data.py      # Career knowledge base & roadmaps (Python dictionary)
├── logic.py            # Scoring formula & skill-gap functions
├── test_system.py      # Automated verification test script (5 test cases)
├── requirements.txt    # Streamlit dependency
├── viva_guide.md       # Viva questions & project report outline
└── README.md           # Setup and execution guide
```

---

## ⚡ How to Run the Project (Windows PowerShell)

### Step 1: Open PowerShell
Make sure you are in the project folder:
```powershell
cd "c:\Users\student\Desktop\CAREER PATH PLANNING AGENT"
```

### Step 2: Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(You will see `(venv)` appear on the left side of your prompt).*

### Step 3: Run the Streamlit Application
```powershell
streamlit run app.py
```
*Expected Output:*
```
Local URL: http://localhost:8501
Network URL: http://...:8501
```
Streamlit will automatically open your web browser at **`http://localhost:8501`**!

---

## 🧪 How to Run Automated Tests

To verify that all recommendation math and skill-gap calculations work properly:
```powershell
python test_system.py
```
*Expected Result:*
```
ALL 5 TESTS PASSED SUCCESSFULLY! (100% Verified)
```

---

## 💡 Quick Demo Tips for Your College Viva
1. In the sidebar, click **"Load Sample Student Profile (AI/ML)"** to instantly populate realistic student data.
2. Explain the 4 main sections to your examiner:
   - **Section 1 (Student Profile):** Academic details and multiselect skill inputs.
   - **Section 2 (Recommendations):** Displays ranked cards with compatibility percentages.
   - **Section 3 (Skill Gap):** Green box shows skills already possessed; orange box shows skills to learn.
   - **Section 4 (Roadmap):** Step-by-step 4-phase learning milestones (Foundations $\rightarrow$ Core $\rightarrow$ Projects $\rightarrow$ Portfolio).
3. Review **`viva_guide.md`** for common examiner questions and exact answers!
