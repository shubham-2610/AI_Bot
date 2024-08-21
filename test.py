import tempfile
import pyttsx3
import os
import webbrowser
import datetime
import inspect
import speech_recognition as sr
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.2)

engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Your AI"

        
def process_pdf(uploaded_file):
    with open(uploaded_file, "rb") as f:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(f.read())
            temp_file_path = temp_file.name

    pdf_loader = PyPDFLoader(temp_file_path)
    pages = pdf_loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    context = "\n\n".join(str(p.page_content) for p in pages)
    texts = text_splitter.split_text(context)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 1})
    
    return vector_index

def personal_bot():
    say("Hello there, welcome to your personal bot")
    print("Listening....")
    query = takeCommand()
    sites = [["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
            ["twitter", "https://www.twitter.com"],
            ["facebook", "https://www.facebook.com"],
            ["LinkedIn", "https://www.linkedin.com"],
            ["reddit", "https://www.reddit.com"],
            ["github", "https://www.github.com"],
            ["stackoverflow", "https://stackoverflow.com"],
            ["amazon web service", "https://aws.amazon.com/"],
            ["netflix", "https://www.netflix.com"],
            ["instagram", "https://www.instagram.com"],
            ["medium", "https://www.medium.com"],
            ["quora", "https://www.quora.com"]]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])

    if f"time" in query:
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"Sir time is {hour} and {min} minutes")

    if f"close" in query:
        say("Do you want to switch bot?")
        print("Listening....")
        query = takeCommand()
        if "yes".lower() in query.lower():
            current_frame = inspect.currentframe()
            # Get the caller's frame
            caller_frame = current_frame.f_back
            # Get the method name
            method_name = caller_frame.f_code.co_name
            if method_name == "rag_bot":
                say("switched to RAG bot")
                rag_bot()
        else:
            say(f"Thank You for using Your AI")
            exit()

def rag_bot():
    say("Hello there! You are using RAG Bot")
    while True:
        print("Listening....")
        query = takeCommand()
        if"PDF" in query:
            say("Enter the path to the file you want to upload: ")
            uploaded_file = input("Upload: ")
            say("Your file is uploaded successfully")
            vector_index = process_pdf(uploaded_file)
            say("Please ask your question")
            question = takeCommand()
            qa_chain = RetrievalQA.from_chain_type(
                    llm,
                    retriever=vector_index,
                    return_source_documents=True
                )
            result = qa_chain({"query": question})
            print(result["result"])
            output_dir = 'output'
            os.makedirs(output_dir, exist_ok=True)
            content = result["result"]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{timestamp}.txt"
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as file:
                file.write(content)
            say("i have saved your response in output folder, please check")

        if f"close".lower() in query.lower():
            say(f"Thank You for using Your AI")
            say("Do you want to switch bot?")
            print("Listening....")
            query = takeCommand()
            if "yes".lower() in query.lower():
                say("switched to personal bot")
                personal_bot()
            else:
                say(f"Thank You for using Your AI")
                exit()

if __name__ == '__main__':
    print("Welcome to your RAGbot")
    say("Hello, How can I help you today?")
    print("press 1. to use PDF bot")
    print("press 2. to use personal bot")
    user_input = int(input())
    if user_input == 1:
        rag_bot()
    elif user_input == 2:
        personal_bot()
    else:
        say("I didn't get you, you can try again later")
        
            

