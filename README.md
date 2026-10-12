
# CodeAlpha Language Translation Tool

## Overview
A Python-based language translation web application built with Streamlit. Users can enter text, select source and target languages, translate text, copy the result, and listen to the translated text.

## Features
- Multiple language options
- Source language selection and limited automatic source-language fallback
- Online text translation using the MyMemory Translation API
- Copy translation to clipboard
- Text-to-speech using the browser Web Speech API
- Input validation and error handling
- Reverse translation support

## Technologies Used
- Python
- Streamlit
- Requests
- MyMemory Translation API
- JavaScript Web Speech API and Clipboard API

## Installation

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Install the dependencies:

   pip install -r requirements.txt

4. Run the application:

   streamlit run app.py

## Usage
1. Enter the text to translate.
2. Select the source and target languages.
3. Click Translate.
4. Copy or listen to the translated result.

## Limitations
- An internet connection is required.
- Translation depends on the availability and limits of the external service.
- Automatic source-language detection tries a limited set of languages.
- Clipboard and speech features depend on browser support.

## Screenshots

### English to Hindi Translation
![Translation Success]("C:\Users\aayus\OneDrive\เอกสาร\CodeAlpha_LanguageTranslationTool\screenshots\translation_success.png.png")

### Copy Translation
![Copy Translation]("C:\Users\aayus\OneDrive\เอกสาร\CodeAlpha_LanguageTranslationTool\screenshots\copyclipboard&voice success.png.png")
## Internship Project
Task 1 — Language Translation Tool
CodeAlpha Artificial Intelligence Internship

## Author
Ayush Kumar Singh
