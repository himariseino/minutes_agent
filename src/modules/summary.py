import os
import yaml
import time
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from pydub import AudioSegment
from tqdm import tqdm

class SummaryMinutes():
    def __init__(self):
        """
        クラスの初期化を行う関数。
        """
        with open("config/config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.model_name = config["SUMMARIZE_MODEL_NAME"]
        self.output_path = config["OUTPUT_PATH"]
        self.system_prompt = config["system"]["prompt"]
        self.user_prompt = config["user"]["prompt"]
        self.summary_text_client = OpenAI()

    def summary(self):
        text_path = os.path.join(self.output_path, 'output.txt')
        with open(text_path, 'r') as texts:
            transcription_texts = texts.read()

        message = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": self.user_prompt.format(user_input=transcription_texts)
            }
        ]

        start = time.perf_counter()
        summary = self.summary_text_client.responses.create(
            model=self.model_name,
            input=message
        )
        end = time.perf_counter()
        print(f'テキスト生成にかかった時間: {((end-start)/60):.2f}分')
        return summary.output[0].content[0].text

if __name__ == "__main__":

    try:
        summary = SummaryMinutes()
        text = summary.summary()
        print("Summarised Text:", text)
    except Exception as e:
        print("Error:", e)
