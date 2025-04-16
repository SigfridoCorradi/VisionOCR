# Optical character recognition using LLM optimized for visual recognition (like `llama3.2-vision`)

This project allows using the Llama 3.2-Vision model (or similar), an instruction-tuned model optimized for visual recognition, in order to act as an optical character recognition (OCR) and output transcribed text (in two possible modes: flat text and Markdown) from an image.

## Ollama

The python code relies on the `Ollama Python Library` to interact with [Ollama](https://ollama.com/) (a tool designed for running open-source large language models - LLMs - directly on local hardware), so first you have to install [Ollama](https://ollama.com/download) and then download the model, e.g.: [llama3.2-vision](https://ollama.com/library/llama3.2-vision:11b) (available with 11b parameters and 90b parameters - depending on local memory availability):

`ollama pull llama3.2-vision:11b`

to verify that the model has been downloaded correctly:

`ollama list`

in case you want to delete the downloaded model to switch to another one (and free up memory):

`ollama rm llama3.2-vision:11b`

You must then start the Ollama server before running the Python code:

`ollama serve`

## Code structure

The code is structured as class **VisionOCR**. Note the 4 class constants:

* DEFAULT_OLLAMA_HOST: indicates the url (with port - like `http://127.0.0.1:11434`) to which Ollama responds, here valued with a default that may generally be fine unless configured differently for Ollama;
* DEFAULT_MODEL: represents the model to be used with Ollama (like `llama3.2-vision:11b`);
* DEFAULT_TEXT_PROMPT and MARKDOWN_TEXT_PROMPT: these are the prompts that are associated with the image to be parsed, to tell the LLM model how it should act (whether to generate flat text or Markdown).

In the code we can see how the text of the two constants DEFAULT_TEXT_PROMPT and MARKDOWN_TEXT_PROMPT is used to compose the message to be sent to the model:
```
messages = [
    {
        'role': 'user',
        'content': system_prompt,
        'images': [base64_image]
    }
]
```

The class constructor prepares the connection to Ollama and in case trigger an error message.
```
ocr_vision = VisionOCR(
    ollama_host=custom_OLLAMA_HOST_ADDR,
    model=custom_MODEL_NAME
)
```

The `perform_vision_ocr` method allows inference to be performed by Ollama on the model:
```
plain_text_result = ocr_vision.perform_vision_ocr(
    image_path=custom_IMAGE_FILE_PATH,
    temperature= 0.3
)
```
> [!NOTE]
> Let us pay attention to the value of `temperature` parameter

In the example given in `__main__` two queries are performed for flat text and Markdown, given an image `test.jpg`.
