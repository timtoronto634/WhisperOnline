import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


import pyaudio
import wave


def main():
  chunk = 1024
  format_audio = pyaudio.paInt16
  channels = 1
  fs = 44100
  seconds = 5
  filename = "input.wav"

  audio = pyaudio.PyAudio()

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

  # Write audio file to disk in .wav format
  with wave.open(filename, 'wb') as wave_file:
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format_audio))
    wave_file.setframerate(fs)
    wave_file.writeframes(b''.join(frames))

  with open(filename, 'rb') as audio_file:
    response = openai.Audio.transcribe("whisper-1", audio_file)
    print(response.text)

if __name__ == "__main__":
  main()