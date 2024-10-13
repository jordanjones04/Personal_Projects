from gtts import gTTS
import os

def text_to_audio(japanese_text, output_file, output_path):
    tts = gTTS(text=japanese_text, lang='ja')
    output_full_path = os.path.join(output_path, f"{output_file}.mp3")
    tts.save(output_full_path)
    print(f"Audio file saved as {output_full_path}")

words = ['さまざまな職業',
'自分に自信を持つ',
'相手の反応',
'とても面白い',
'寝不足になる',
'40代の主婦',
'（数学）が苦手だ',
'最近',
'髪をピンク色に染める',
'全然違う',
'ラジオ番組',
'困っている人を助ける',
'（生活）が変化する',
'努力し続ける',
'将来',
'卒業式',
'（SNS）が嫌いだ',
'（K-POP）に夢中だ']

# Example usage
for i in range(len(words)): 
    japanese_text = words[i]
    output_file = str(i+1)
    output_path = "/Users/jordanjones/Documents/Swarthmore College/Spring 2024/Japanese/Audio Files/４の単語"  # Replace with your desired location
    text_to_audio(japanese_text, output_file, output_path)

