# LangChain + Groq Starter

This project is a simple Python starter for using LangChain with Groq's ChatGroq integration.

## Setup

1. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Copy the example environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Add your Groq API key in `.env`.
4. Run the app:
   ```powershell
   python app.py
   ```

## Example

The app sends a prompt to Groq using `ChatGroq` and prints the response.
