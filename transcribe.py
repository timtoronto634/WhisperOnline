import openai
import os
import time
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")


import pyaudio
import wave

def chat(text):
  resp = openai.Completion.create(
    model="text-davinci-003",
    prompt=text,
    max_tokens=2048,
    temperature=0.2
  )

  print("ChatGPT Response:")
  if resp.choices:
    for choice in resp.choices:
        if choice.text:
            print(choice.text.strip())

  print("---")
  print(f"total_tokens used: {resp.usage.total_tokens}")
  return

def transcribe():
  chunk = 1024
  format_audio = pyaudio.paInt16
  channels = 1
  fs = 44100
  seconds = 5
  dir_name = "data"
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)
  filename = f"{dir_name}/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"

  audio = pyaudio.PyAudio()

  print("you can now speak")
  stream = audio.open(
      format=format_audio,
      channels=channels,
      rate=fs,
      input=True,
      frames_per_buffer=chunk
  )

  frames = []

  for i in range(0, int(fs/chunk*seconds)):
      data = stream.read(chunk)
      frames.append(data)

  stream.stop_stream()
  stream.close()
  audio.terminate()
  print("finished recording")

  # Write audio file to disk in .wav format
  with wave.open(filename, 'wb') as wave_file:
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format_audio))
    wave_file.setframerate(fs)
    wave_file.writeframes(b''.join(frames))

  text = ""
  with open(filename, 'rb') as audio_file:
    response = openai.Audio.transcribe("whisper-1", audio_file)
    print(response.text)
    text = response.text
  return text


def main():
  for _ in range(5):
    text = transcribe()
    chat(text)
    time.sleep(5)


if __name__ == "__main__":
  main()