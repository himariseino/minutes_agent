import os
import yaml
import time
import datetime
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from pydub import AudioSegment
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class SpeechToText():
    def __init__(self):
        with open("config/config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.voice_path = config["VOICE_PATH"]
        self.model_name = config["VOICE_MODEL_NAME"]
        self.speech_to_text_client = OpenAI()
        self.MAX_SIZE = 25 * 1024 * 1024
        self.output_path = config["OUTPUT_PATH"]

    def split_audio(self, voice_path):
        audio = AudioSegment.from_file(voice_path)
        # チャンクの幅時間を設定
        chunk_length_ms = int(len(audio) * (self.MAX_SIZE / os.path.getsize(voice_path)))
        chunks = []
        start = 0
        duration_ms = len(audio)
        # 1秒ごとに増やしながら25MB未満になるように分割
        while start < duration_ms:
            end = start + 10000  # まず10秒単位で
            while end <= duration_ms:
                chunk = audio[start:end]
                chunk_path = f'{voice_path}_chunk_{start}.wav'
                chunk.export(chunk_path, format="wav")
                if os.path.getsize(chunk_path) > self.MAX_SIZE:
                    os.remove(chunk_path)
                    if end - start <= 1000:
                        # 1秒でも超える場合は強制終了
                        raise ValueError("Cannot split audio into small enough chunks.")
                    end -= 1000  # 1秒短くして再トライ
                else:
                    break
            else:
                # 最後の部分
                chunk = audio[start:duration_ms]
                chunk_path = f'{voice_path}_chunk_{start}.wav'
                chunk.export(chunk_path, format="wav")
                if os.path.getsize(chunk_path) > self.MAX_SIZE:
                    raise ValueError("Last chunk is still too large.")
                end = duration_ms
            chunks.append(chunk_path)
            start = end
        return chunks

    def transcribe_chunk(self, chunk_path):
        with open(chunk_path, 'rb') as audio_file:
            return self.speech_to_text_client.audio.transcriptions.create(
                model=self.model_name,
                file=audio_file,
                response_format="text",
            )

    def transcribe_audio_to_text(self) -> str:
        """
        Transcribe audio file to text using Whisper model.

        Args:
            audio_file_path (str): Path to the audio file.
            model_name (str): Name of the Whisper model to use. Default is "base".

        Returns:
            str: Transcribed text from the audio file.
        """

        # 音声ファイルが存在しない場合にエラーを返す
        if not os.path.exists(self.voice_path):
            raise FileNotFoundError(f"Audio file not found: {self.voice_path}")

        if os.path.getsize(self.voice_path) > self.MAX_SIZE:
            chunk_paths = self.split_audio(self.voice_path)
        else:
            chunk_paths = [self.voice_path]

        text_list = []
        start = time.perf_counter()

        # 並列でAPIリクエスト
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.transcribe_chunk, chunk_path): chunk_path
                for chunk_path in chunk_paths
                if os.path.getsize(chunk_path) >= 1024  # 1KB未満はスキップ
            }
            for future in tqdm(as_completed(futures), total=len(futures), desc="Transcribing chunks"):
                chunk_path = futures[future]
                try:
                    transcription = future.result()
                    text_list.append(transcription)
                except Exception as e:
                    print(f"Error in chunk {chunk_path}: {e}")
                finally:
                    if chunk_path != self.voice_path:
                        os.remove(chunk_path)  # 一時ファイル削除

        texts = "\n".join(text_list)

        end = time.perf_counter()
        print(f'テキスト生成にかかった時間: {((end-start)/60):.2f}分')

        if os.path.isdir(self.output_path):
            pass
        else:
            os.makedirs(self.output_path)

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        transcription_path = os.path.join(self.output_path, f'output_{now}.txt')
        transcription_path = os.path.join(self.output_path, 'output.txt')
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(texts)

        return texts

if __name__ == "__main__":

    try:
        transcribe = SpeechToText()
        text = transcribe.transcribe_audio_to_text()
        print("Transcribed Text:", text)
    except Exception as e:
        print("Error:", e)
