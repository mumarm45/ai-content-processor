from gtts import gTTS
import pygame
import tempfile
import os
import time

def main():
    story = """The Amazing World of Lovebirds
    Have you ever wondered why some birds are called "lovebirds"? Let me introduce you to these delightful little parrots!
    Lovebirds are small, colorful birds native to Africa and Madagascar. They're only about 5-7 inches long—roughly the size of your hand! These cheerful birds come in beautiful colors like green, peach, yellow, and blue, making them look like flying rainbows.
    So why the romantic name? Lovebirds are famous for forming incredibly strong bonds with their partners. Once they choose a mate, they often stay together for life! You'll frequently see bonded pairs sitting close together, grooming each other's feathers, and gently touching beaks—which looks a lot like kissing. It's absolutely adorable!
    Here's something fascinating: lovebirds are highly social creatures. In the wild, they live in small flocks and chatter constantly with cheerful chirps and whistles. They're also quite intelligent and playful, enjoying toys and learning simple tricks.
    Despite their small size, lovebirds have big personalities! They're energetic, curious, and surprisingly brave. They love to explore, climb, and even hang upside down just for fun. These little acrobats need plenty of mental stimulation to stay happy.
    What We Learned:
    Lovebirds are small, colorful parrots from Africa known for their strong pair bonds and affectionate behavior. They're social, intelligent, and full of personality—making them fascinating birds whether in the wild or as beloved pets. Their loyalty to their partners truly earns them their heartwarming name!
   """  # Your story here
    
    print("Hello from story-teller!")
    print("Generating audio...")

    # Generate speech
    tts = gTTS(story)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_file = fp.name
        tts.save(temp_file)
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    print("Playing audio...")
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()
    
    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Clean up
    pygame.mixer.quit()
    os.unlink(temp_file)
    print("Done!")

if __name__ == "__main__":
    main()