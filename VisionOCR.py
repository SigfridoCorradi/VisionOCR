import base64
import ollama
import os

class VisionOCR:
    DEFAULT_OLLAMA_HOST: str = "http://127.0.0.1:11434"
    DEFAULT_MODEL: str = "llama3.2-vision:11b"
    DEFAULT_TEXT_PROMPT: str = """Act as an OCR assistant. Analyze the provided image and:
1. Recognize all visible text in the image as accurately as possible.
2. Maintain the original structure and formatting of the text as best as possible.
3. If any words or phrases are unclear, indicate this with [unclear] in your transcription.
Provide only the transcription without any additional comments."""
    MARKDOWN_TEXT_PROMPT: str = """Act as an expert OCR assistant specializing in document structure. Analyze the provided image and:
1. Recognize all visible text in the image as accurately as possible.
2. Structure the recognized text using appropriate Markdown formatting (e.g., headings (#, ##), lists (*, -), bold (**text**), italics (*text*), code blocks (```), etc.) to reflect the visual layout and hierarchy of the original image.
3. If any words or phrases are unclear, indicate this with `[unclear]` (using backticks for code style) in your transcription.
4. Ensure the output is valid Markdown.
Provide *only* the Markdown transcription without any introductory sentences, explanations, or closing remarks."""

    def __init__(self,
                 ollama_host: str = DEFAULT_OLLAMA_HOST,
                 model: str = DEFAULT_MODEL,
                 default_text_prompt: str = DEFAULT_TEXT_PROMPT):
        self.model = model
        self.default_text_prompt = default_text_prompt
        try:
            self.client = ollama.Client(host=ollama_host)
            print(f"Connection to Ollama at: {ollama_host}...")
            self.client.list()
            self._host = ollama_host
            print(f"Successfully connected! Model: '{self.model}'")
        except Exception as e:
            print(f"\n[ERROR] Could not connect to: '{ollama_host}'.")
            raise ConnectionError(f"[ERROR] Could not connect to: {ollama_host}") from e

    @staticmethod
    def _encode_image_to_base64(image_path: str):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"\n[ERROR] Image not found: '{image_path}'")
            return None
        except Exception as e:
            print(f"\n[ERROR] Unable to encode image: '{image_path}'")
            return None

    def perform_vision_ocr(self,
                    image_path: str,
                    temperature: 0.9,
                    system_prompt_override = None
                    ):
        system_prompt = system_prompt_override if system_prompt_override is not None else self.default_text_prompt

        base64_image = self._encode_image_to_base64(image_path)
        if not base64_image:
            return None

        messages = [
            {
                'role': 'user',
                'content': system_prompt,
                'images': [base64_image]
            }
        ]
        options = {'temperature': temperature}

        try:
            #Sending request to Ollama model '{self.model}'
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=False,
                options=options
            )

            message = response.get('message', {})
            content = message.get('content')

            if content and isinstance(content, str):
                processed_content = content.strip()
                return processed_content
            else:
                print("\n[ERROR] Response 'content' is missing. Received ", response)
                return None
        except ollama.ResponseError as e:
            print(f"\n[ERROR] Ollama API Error: status {e.status_code}")
            return None
        except Exception as e:
            print(f"\n[ERROR] An unexpected error: {e}")
            return None

if __name__ == "__main__":
    custom_IMAGE_FILE_PATH = "test.jpg"
    custom_OLLAMA_HOST_ADDR = VisionOCR.DEFAULT_OLLAMA_HOST
    custom_MODEL_NAME = VisionOCR.DEFAULT_MODEL

    if not os.path.exists(custom_IMAGE_FILE_PATH):
         print(f"\n[FATAL ERROR] Image not found: '{custom_IMAGE_FILE_PATH}'")
         exit(1)

    try:
        ocr_vision = VisionOCR(
            ollama_host=custom_OLLAMA_HOST_ADDR,
            model=custom_MODEL_NAME
        )

        #Performing OCR (Default Plain Text Prompt)
        plain_text_result = ocr_vision.perform_vision_ocr(
            image_path=custom_IMAGE_FILE_PATH,
            temperature= 0.3
        )
        if plain_text_result:
            print(plain_text_result)
        else:
            print("\n[ERROR] Text OCR process failed.")

        #Performing OCR (Markdown Prompt Override)
        markdown_result = ocr_vision.perform_vision_ocr(
            image_path=custom_IMAGE_FILE_PATH,
            temperature= 0.3,
            system_prompt_override=VisionOCR.MARKDOWN_TEXT_PROMPT
        )
        if markdown_result:
            print(markdown_result)
        else:
            print("\n[ERROR] Text OCR process failed.")

    except ConnectionError as e:
        print(f"\n[FATAL ERROR] Ollama connection issue.")
        exit(1)

    except Exception as e:
        print(f"\n[FATAL ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()
        exit(1)