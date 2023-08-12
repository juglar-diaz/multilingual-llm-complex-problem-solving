from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
load_dotenv()


from tenacity import (
    retry,
    stop_after_attempt,
    wait_chain,
    wait_fixed
) 

@retry(wait=wait_chain(*[wait_fixed(3) for i in range(3)] +
                      [wait_fixed(5) for i in range(2)] +
                       [wait_fixed(10)]))
def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client(target_language='es')

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target, source_language='en', format_='text')

    #print("Text: {}".format(result["input"]))
    #print("Translation: {}".format(result["translatedText"]))
    #print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result


def translate_file(file_name, folder_name, lang_cod):
    file = open(f"{folder_name}{file_name}")
    output_file  = open(f"{folder_name}{file_name[:-4]}_{lang_cod}.txt", "w")
    for line in file:
        translated_line = translate_text(target=lang_cod, text=line.strip())['translatedText']
        #print(translated_line+'\n')
        output_file.write(translated_line+"\n")
    file.close()
    output_file.close()