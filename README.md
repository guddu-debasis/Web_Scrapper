# 🧠 AI Insight - Intelligent RAG Summarizer

![AI Insight UI](https://via.placeholder.com/800x400?text=AI+Insight+Dashboard)
*(Replace with actual screenshot)*

**AI Insight** is a modern, high-performance web application that generates intelligent, structured summaries of web content using **Retrieval-Augmented Generation (RAG)**. Built with **FastAPI**, **LangChain**, and **Llama 3** (via Groq), it allows users to digest complex articles, documentation, or news in seconds.

## ✨ Features

*   **🚀 Fast & Intelligent Summarization**: Uses Llama 3.1-8b via Groq for lightning-fast inference.
*   **🔍 RAG Engine**: Retrieval-Augmented Generation ensures summaries are grounded in the actual page content (no hallucinations).
*   **🔐 Secure Authentication**: Full Signup/Login system with **Argon2** hashing and JWT (JSON Web Tokens).
*   **🌐 Generic Web Scraper**: Capable of summarizing Wikipedia, Blogs, News Sites, and Documentation (HTML support).
*   **🎨 Premium UI**: Glassmorphism design system using Tailwind CSS, featuring dark mode, transparent cards, and markdown rendering.
*   **🗄️ History Tracking**: Automatically saves summaries to MongoDB for future reference.

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI
*   **AI/LLM**: LangChain, Groq API (Llama 3), HuggingFace Embeddings
*   **Database**: MongoDB (Atlas Cloud or Local)
*   **Frontend**: HTML5, Tailwind CSS, JavaScript (Vanilla), Marked.js
*   **Security**: PyJWT, Argon2-cffi, Passlib

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   MongoDB Instance (Local or Atlas)
*   Groq API Key

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai-summarizer.git
    cd ai-summarizer
    ```

2.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/summerizer_app
    DB_NAME=summerizer_app
    SECRET_KEY=your_super_secret_key_here
    ALGORITHM=HS256
    GROQ_API_KEY=gsk_your_groq_key_here
    ```

5.  **Run the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Access the App**:
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## 📂 Project Structure

```
PROJECT_SUmmerizer/
├── app/
│   ├── config/         # Database configuration
│   ├── controller/     # Auth and Logic controllers
│   ├── models/         # Pydantic models
│   ├── routes/         # API Routes
│   ├── services/       # AI & Scraping Logic (RAG Chain)
│   ├── utils/          # Hashing & Security utils
│   └── main.py         # Entry point
├── static/
│   └── index.html      # Frontend UI
├── .env                # Secrets (Ignored in Git)
├── .gitignore
├── Procfile            # Deployment config
├── requirements.txt    # Python dependencies
└── README.md
```

## ☁️ Deployment

This project is configured for easy deployment on **Render**, **Railway**, or **Heroku**.
See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

---
*Created with ❤️ by AI Insight Team.*
