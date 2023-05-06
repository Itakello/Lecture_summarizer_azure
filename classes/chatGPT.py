import json
import os
import time
from dataclasses import dataclass

import openai

from .chunk import Chunk
from .recordings import Language


@dataclass
class ChatGPTUtils():
    
    def __post_init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        
    def call_openai_api(self, content:str, prompt:str, retries:int = 0) -> str:
        MAX_RETRIES = 5
        if retries > MAX_RETRIES:
            raise Exception("Reached maximum number of retries.")
        try:
            retries += 1
            response = self._invoke_prompt(content, prompt)
            parsed_res = json.loads(response)
        except json.decoder.JSONDecodeError as je:
            print(je)
            time.sleep(10)
            je_content, je_propmpt = self._create_content_and_prompt_json_error(response, je)
            response = self._invoke_prompt(je_content, je_propmpt)
            parsed_res = json.loads(response)
        except Exception as e:
            print(e)
            time.sleep(10)
            self.call_openai_api(content, prompt, retries)
        return parsed_res
    
    def get_additional_info(self, transcription:str, language:Language) -> Chunk:
        content, prompt = self._create_content_and_prompt(transcription, language)
        parsed_res = self.call_openai_api(content, prompt)
        chunk = self._create_chunk(transcription, parsed_res)
        return chunk
    
    def _create_chunk(self, transcription: str, parsed_res:dict) -> Chunk:
        return Chunk(parsed_res['title'], transcription, parsed_res['summary'], parsed_res['main_points'], parsed_res['follow_up'])
    
    def _invoke_prompt(self, content:str, prompt:str) -> str:
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages = [
                        {"role": "system", "content":content},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )       
        return response.choices[0]['message']['content']
    
    def _create_content_and_prompt(self, transcription:str, language:Language) -> tuple[str, str]:
        if language == Language.ENGLISH:
            prompt = f'Analyze the transcript of a lesson provided below, which could contain errors especially at the start and end of the text, then provide the following:\nKey "title:" - add a title.\n\nKey "main_points" - add an array of the main points. Limit each item to 100 words, and limit the list to 10 items.\nKey "follow_up:" - add an array of follow-up questions. Limit each item to 100 words, and limit the list to 5 items.\nKey "summary" - create a really detailed summary of at least 250 words.\n\nEnsure that the final element of any array within the JSON object is not followed by a comma.\nTranscript:\n{transcription}'
            content = 'You are an assistant that only speaks JSON. Do not write normal text.\nExample formatting:\n{\n"title": "Notion Buttons",\n"main_points": [\n"item 1",\n"item 2",\n"item 3"\n],\n"follow_up": [\n"item 1",\n"item 2",\n"item 3"\n],,\n"summary": "A detailed description of buttons for Notion"}'
        elif language == Language.ITALIAN:
            prompt = f'Analizza la trascrizione sottostante di una lezione, la quale potrebbe contenere errori specialmente all\' inizio e fine del testo, e produci i seguenti:\nChiave "title:" - aggiungi un titolo.\n\nChiave "main_points" - aggiungi un array di punti principali. Limita ogni elemento a 100 parole, e limita il numero di elementi a 10.\nChiave "follow_up:" - aggiungi un array di domande aggiuntive. Limita ogni elemento a 100 parole, e limita il numero di elementi a 5.\nChiave "summary" - crea un riassunto molto dettagliato di almeno 250 parole.\n\nAssicurati che l\' elemento final di ogni array all\' interno dell\' oggett JSON non sia seguito da un virgola.\Trascrizione:\n{transcription}'
            content = 'Tu sei un assistente che parla solamente in JSON. Non scrivere testo normale.\nEsempio di formattazione:\n{\n"title": "I bottoni della giacca",\n"main_points": [\n"elemento 1",\n"elemento 2",\n"elemento 3"\n],\n"follow_up": [\n"elemento 1",\n"elemento 2",\n"elemento 3"\n],\n"summary": "Una descrizione dettagliata dei bottoni della giacca"}'
        else:
            raise NotImplementedError("Language not supported")
        return content, prompt
    
    def _create_content_and_prompt_json_error(self, json:str, error:str) -> tuple[str, str]:
        prompt = f'You have an error in the JSON formatting. Please fix it and print it out.\nError: {error}\nJSON: {json}'
        content = 'You are an assistant that only speaks JSON. Do not write normal text.\nExample formatting:\n{\n"title": "Notion Buttons",\n"main_points": [\n"item 1",\n"item 2",\n"item 3"\n],\n"follow_up": [\n"item 1",\n"item 2",\n"item 3"\n],\n"summary": "A detailed description of buttons for Notion"}'
        return content, prompt