from agents import Agent, Runner, function_tool
import asyncio
from dotenv import load_dotenv
load_dotenv()
import yaml
import logging

from modules.speech_to_text import SpeechToText
from modules.summary import SummaryMinutes


with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)
model_name = config["SUMMARIZE_MODEL_NAME"]

# ログの基本設定
logging.basicConfig(
    filename="log/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@function_tool
def voice_to_text():
    """
    音声から文字起こしをします。
    ここで作成された文字起こしが、後に議事録を作成する際に使用されます。
    """
    logging.info("文字起こしの生成を開始します...")
    speech_to_text = SpeechToText()
    result = speech_to_text.transcribe_audio_to_text()
    logging.info("文字起こしが完了しました")
    return result

@function_tool
def summary():
    """
    この関数はSummaryMinutesという外部モジュールを呼び出して使用します。
    SummaryMinutesは文字起こしされたゼミナールの様子を議事録としてまとめて、
    ネクストアクションがわかるようにしてくれるクラスです。
    """
    logging.info("議事録の生成を開始します...")
    summary = SummaryMinutes()
    result = summary.summary()
    logging.info("議事録の生成が完了しました")
    return result

async def main():
    agent = Agent(
        name="Minutes agent",
        instructions="Summarize seminar class transcription from folder",
        model=model_name,
        tools=[voice_to_text, summary]
    )

    print("チャットを開始します。'exit'で終了します。")
    while True:
        user_input = input("あなた: ")
        if user_input.lower() in ["exit", "quit"]:
            print("チャットを終了します。")
            break
        result = await Runner.run(agent, user_input)
        print("エージェント:", result.final_output)

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except Exception as e:
        logging.error("予期せぬエラーが発生しました", exc_info=True)
        print("Error:", e)
