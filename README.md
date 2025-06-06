.
├── agent.py          # Agent implementation with LLM and tool integration
├── app.py            # Streamlit user interface
├── requirements.txt  # Package dependencies
└── .env              # API keys (create this file locally)

# langchain-agent

1. Clone the repository
Clone the repository to your local machine using the following command:

git clone https://github.com/dhanwin2222/langchain-agent.git

2. Navigate to the project folder
Move into the project directory:

cd langchain-agent

3. Create and activate a virtual environment
Create a virtual environment to isolate your project dependencies:

python3 -m venv venv

Activate the virtual environment:

On Mac/Linux:

source venv/bin/activate

On Windows:

venv\Scripts\activate

4. Install project dependencies
Install all the necessary dependencies listed in the requirements.txt:

pip install -r requirements.txt

5. Set up your API keys
Create a .env file in the root directory of the project (next to app.py and requirements.txt).

Add your Groq API key to the .env file like this:

GROQ_API_KEY=your_actual_api_key_here

I have also put the API key in the project documentation; however, there is a possibility it may have been exhausted by the time of access

6.Run the application
Once the dependencies are installed, and the API key is set up, run the application using:

streamlit run app.py









