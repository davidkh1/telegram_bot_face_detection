## Telegram bot for face detection with OpenCV engine behind.

Recently Telegram has introduced a new feature, the bots.
I've created "Face Detection" bot that receives images from smartphone camera or photo library, and returns an image with detected faces.

![Alt text](screenshots/screenshot_iphone_faces.PNG?raw=true "Telegram Bot on iPhone")

## Instructions

1. Create a new bot using 'BotFather' on Telegram. Reference https://core.telegram.org/bots. BotFather supplies a token for your new bot.
2. Edit 'botToken' value in [online_face_detection_demo.py](online_face_detection_demo.py)
3. Run the bot backend in from command line (Ubuntu): `python online_face_detection_demo.py`
4. Open the bot from Telegram, and start sending pictures.
5. The running instance of the bot will fetch the pictures, detect faces and publish it back in the application window. The example of multi-face detection is above. 


