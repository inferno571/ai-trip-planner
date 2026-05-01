# Local Setup Commands

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment (Windows)
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Run the Backend (in Terminal 1)
uvicorn main:app --reload

# 5. Run the Frontend (in Terminal 2)
streamlit run streamlit_app.py
```
