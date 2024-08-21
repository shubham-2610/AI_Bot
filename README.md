

# Personal AI Bot with PDF Retrieval

This project is a Python-based AI assistant that includes two main functionalities:

1. **Personal Bot**: Interacts with the user to perform tasks like opening websites, telling the time, and switching between bots.
2. **RAG Bot**: Processes PDF documents and answers questions based on the content using a Retrieval-Augmented Generation (RAG) approach.

## Features

- **Speech Recognition**: Uses `speech_recognition` to understand user commands via voice input.
- **Text-to-Speech**: Uses `pyttsx3` to provide voice feedback to the user.
- **Website Navigation**: Opens popular websites based on voice commands.
- **Time Reporting**: Announces the current time when asked.
- **PDF Processing**: Reads and processes PDF files, allowing the user to ask questions based on the content of the PDF.
- **Answer Saving**: Saves the answer to the question in a text file within the `output` directory.

## Dependencies

The following Python packages are required to run this project:

- `pyttsx3`: For text-to-speech conversion.
- `speech_recognition`: For recognizing voice commands.
- `google-generativeai`: For interacting with Google's Gemini model.
- `langchain`: For managing the question-answering chain.
- `webbrowser`: For opening websites.
- `datetime`: For handling date and time functions.
- `tempfile`: For handling temporary file storage.
- `os`: For interacting with the operating system.
- `inspect`: For inspecting the current frame and calling methods.

Install the dependencies using pip:

```bash
pip install pyttsx3 speechrecognition google-generativeai langchain
```

## Getting Started

1. **Set Up Google API Key**:
   - Ensure you have a Google API key and set it as an environment variable with the name `GEMINI_API_KEY`.

2. **Run the Bot**:
   - Execute the `rag_bot.py` script and choose either the Personal Bot or RAG Bot functionalities.

```bash
python rag_bot.py
```

3. **Select Functionality**:
   - Press `1` to use the PDF processing bot (RAG Bot).
   - Press `2` to use the Personal Bot.

## Usage

### Personal Bot

- **Open Websites**: Say "Open [website name]" (e.g., "Open YouTube") to open the respective website.
- **Get Time**: Say "time" to get the current time.
- **Switch Bot**: Say "close" to switch to the RAG Bot.

### RAG Bot

- **Process PDF**: Say "PDF" and provide the path to your PDF file. You can then ask questions based on the content.
- **Save Answers**: The bot saves the answers to your questions in the `output` directory with a timestamp.

## Customization

- **Modify Sites**: You can modify the list of sites in the `sites` array within the `personal_bot()` function.
- **Adjust LLM Settings**: You can tweak the parameters of the `ChatGoogleGenerativeAI` model to adjust its behavior.

## Acknowledgments

- This project utilizes the `LangChain` library for orchestrating the LLMs and retrieval mechanisms.
- Speech recognition and text-to-speech functionalities are powered by `speech_recognition` and `pyttsx3`.
