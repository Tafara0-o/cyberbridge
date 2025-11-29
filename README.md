# CyberBridge

> An AI-powered security awareness and training platform prototype built with Flask and Gemini AI.

**Repository:** [Tafara0-o/cyberbridge](https://github.com/Tafara0-o/cyberbridge)

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [How to Use the App](#how-to-use-the-app)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Prerequisites

**Required:**

- Python 3.10 or higher
- Git
- A web browser (Chrome, Edge, Firefox, etc.)

**Optional (recommended):**

- VS Code with Python extension

---

## Installation

### 1. Clone the Repository

Open a terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
git clone https://github.com/Tafara0-o/cyberbridge.git
cd cyberbridge
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If that fails, try:

```bash
pip install flask google-generativeai python-dotenv
```

---

## Configuration

### Get Your Gemini API Key

Each teammate needs their own API key:

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Navigate to the [API key page](https://aistudio.google.com/app/apikey)
4. Click "Create API key" (or use an existing one)
5. Copy the generated key (it starts with `AIza...`)

### Create Your `.env` File

In the project root (same folder as `app.py`), create a file named `.env` and add:

```
GEMINI_API_KEY=your_api_key_here
```

> **Important:** Never commit your `.env` file to Git. It should already be in `.gitignore`.

---

## Running the App

Every time you want to run the app:

1. Open terminal and navigate to the project folder:

   ```bash
   cd cyberbridge
   ```

2. Activate the virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **Mac / Linux:**
   ```bash
   source venv/bin/activate
   ```

3. Start the Flask app:

   ```bash
   python app.py
   ```

4. Open your browser and navigate to:

   ```
   http://localhost:5000/
   ```

---

## How to Use the App

### Risk Profile

1. On the homepage, select:
   - Business type (e.g., Professional Services)
   - Industry (e.g., IT/Tech)
   - Company size
2. Click "Analyze Risk"
3. View your personalized risk assessment

### Dashboard

After completing your risk profile, you'll see:

- Risk score and breakdown
- Recommended training modules
- Charts and alerts

### Training Modules

1. Click "Start New Module"
2. Choose a module (e.g., "Phishing Awareness")
3. Complete the training content:
   - Title and introduction
   - Key concepts
   - Real-world examples
   - Best practices
4. Take the quiz
5. Return to dashboard to see updated stats

---

## Troubleshooting

### "Gemini API Error"

- There may be an issue with your Gemini key or quota
- Check the terminal output for Gemini error messages
- Verify your key is valid in [Google AI Studio](https://aistudio.google.com)

### "Port Already in Use"

- Another process is using port 5000
- Stop the other process, or change the port in `app.py`:

  ```python
  app.run(port=5001)
  ```

---

## Contributing

1. Pull the latest changes before starting work:

   ```bash
   git pull origin main
   ```

2. Create a new branch for your changes (optional but recommended):

   ```bash
   git checkout -b feature/your-name-description
   ```

3. Test locally with `python app.py` before committing

4. Commit small, focused changes with clear messages

---

## License

This project is for educational purposes as part of a capstone project.
