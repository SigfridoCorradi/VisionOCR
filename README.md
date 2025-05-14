# Optical character recognition using LLM optimized for visual recognition (like `llama3.2-vision`)

This project provides a Python tool to perform Optical Character Recognition (OCR) on images using a local or remote Ollama instance hosting a vision-capable Large Language Model (LLM), such as Llama 3.2-Vision (or similar).

Traditional OCR software often relies on predefined fonts and layouts, which can struggle with complex images, varied styling, or specific document structures. By leveraging the advanced visual understanding capabilities of modern vision LLMs, this tool offers a more flexible and potentially more accurate approach to transcribing text from images, including the ability to interpret structural elements and output in formats like Markdown.

The tool supports two primary output modes:
1.  **Plain Text:** A straightforward transcription of detected text, attempting to preserve basic structure.
2.  **Markdown:** A transcription structured using Markdown syntax to reflect the visual layout and hierarchy of the original image.

## Ollama

The python code relies on the `Ollama Python Library` to interact with [Ollama](https://ollama.com/) (a tool designed for running open-source large language models - LLMs - directly on local hardware), so first you have to install [Ollama](https://ollama.com/download) and then download the model, e.g.: [llama3.2-vision](https://ollama.com/library/llama3.2-vision:11b) (available with 11b parameters and 90b parameters - depending on local memory availability):

`ollama pull llama3.2-vision:11b`

to verify that the model has been downloaded correctly:

`ollama list`

in case you want to delete the downloaded model to switch to another one (and free up memory):

`ollama rm llama3.2-vision:11b`

You must then start the Ollama server before running the Python code:

`ollama serve`

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/SigfridoCorradi/VisionOCR
    cd VisionOCR
    ```

2. **Create a virtual environment** (optional but **strongly** recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The `VisionOCR.py` file can be run directly for a quick test using the `__main__` block, or the `VisionOCR` class can be imported and used in your own Python scripts.

### Using the Example Script (`__main__`)

The example block demonstrates how to use the `VisionOCR` class with default settings and an override.

1.  **Place an Image:** Make sure you have an image file (e.g., `test.jpg`) in the same directory as `VisionOCR.py`, or update the `custom_IMAGE_FILE_PATH` variable in the script to point to your image.
2.  **Configure (Optional):** Modify the `custom_IMAGE_FILE_PATH`, `custom_OLLAMA_HOST_ADDR`, or `custom_MODEL_NAME` variables in the `__main__` block if needed.
3.  **Run the Script:** Execute the script from your terminal:
    ```bash
    python VisionOCR.py
    ```

The script will attempt to connect to Ollama, perform OCR on the specified image using both the default plain text prompt and the Markdown prompt, and print the results to the console.

### Using the `VisionOCR` Class in Your Own Code

You can import the `VisionOCR` class and use its methods in your projects:

```python
from VisionOCR import VisionOCR

# Configuration
ollama_host = "http://127.0.0.1:11434"
model_name = "llama3.2-vision:11b"
image_file = "path/to/your/image.jpg"
temperature_setting = 0.3 #Adjust temperature (lower is more deterministic, higher more creative)

try:
    # Initialize the OCR tool
    ocr_tool = VisionOCR(ollama_host=ollama_host, model=model_name)

    #Perform Plain Text OCR
    print("\nPlain Text OCR Result:")
    plain_text = ocr_tool.perform_vision_ocr(
        image_path=image_file,
        temperature=temperature_setting,
        # Using the default prompt
    )
    if plain_text:
        print(plain_text)
    else:
        print("[ERROR] Plain text OCR failed.")

    #Perform Markdown OCR
    print("\nMarkdown OCR Result:")
    markdown_text = ocr_tool.perform_vision_ocr(
        image_path=image_file,
        temperature=temperature_setting,
        system_prompt_override=VisionOCR.MARKDOWN_TEXT_PROMPT #Using the Markdown prompt
    )
    if markdown_text:
        print(markdown_text)
    else:
        print("[ERROR] Markdown OCR failed.")

except ConnectionError as e:
    print(f"[FATAL ERROR] Could not connect to Ollama: {e}")
except FileNotFoundError as e:
    print(f"[FATAL ERROR] Image file not found: {e}")
except Exception as e:
    print(f"[FATAL ERROR] An unexpected error occurred: {e}")

```

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

## Prompts

The tool includes two predefined prompts optimized for different output formats:

*   `VisionOCR.DEFAULT_TEXT_PROMPT`: Designed for extracting plain text while preserving basic structure.
*   `VisionOCR.MARKDOWN_TEXT_PROMPT`: Designed for extracting text and structuring it using Markdown syntax based on the visual layout.

You can also create your own custom prompt string and pass it using `system_prompt_override`.
