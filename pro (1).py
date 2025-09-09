import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height

# Importing all images
imgBackground = cv2.imread("C:/Users/LENOVO/OneDrive/Desktop/git/Game/Resources/Background.png")
imgBall = cv2.imread("C:/Users/LENOVO/OneDrive/Desktop/git/Game/Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("C:/Users/LENOVO/OneDrive/Desktop/git/Game/Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("C:/Users/LENOVO/OneDrive/Desktop/git/Game/Resources/bat2.png", cv2.IMREAD_UNCHANGED)
imgGameOver = cv2.imread("C:/Users/LENOVO/OneDrive/Desktop/git/Game/Resources/gameOver.png")

# Check if images are loaded correctly
def check_img(img, name):
    if img is None:
        print(f"❌ Error: {name} not found. Check the path.")
        exit()

check_img(imgBackground, "Background.png")
check_img(imgBall, "Ball.png")
check_img(imgBat1, "bat1.png")
check_img(imgBat2, "bat2.png")
check_img(imgGameOver, "gameOver.png")

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX, speedY = 10, 10
gameOver = False
finalOver = False
score = [0, 0]
roundWins = [0, 0]  # [Left, Right]
winningScore = 5    # points to win a round
bestOf = 3          # best of 3 rounds
winner = None
finalWinner = None

while True:
    success, img = cap.read()
    if not success:
        print("❌ Failed to grab frame from camera")
        break

    # Flip image (mirror effect)
    img = cv2.flip(img, 1)

    # Find hands
    hands, img = detector.findHands(img, flipType=False)

    # Overlay background
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Checking for hands and bat-ball collision
    if not gameOver and not finalOver and hands:
        for hand in hands:
            x, y, w, h = hand["bbox"]
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                bat_x, bat_y = 59, y1
                if (bat_x < ballPos[0] < bat_x + w1) and (bat_y < ballPos[1] < bat_y + h1):
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                bat_x, bat_y = 1195, y1
                if (bat_x - w1 < ballPos[0] < bat_x) and (bat_y < ballPos[1] < bat_y + h1):
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    # Move ball and check boundaries
    if not gameOver and not finalOver:
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        # Scores during game
        cv2.putText(img, f"Left: {score[0]}", (100, 650), cv2.FONT_HERSHEY_COMPLEX, 2,
                    (255, 255, 255), 5, cv2.LINE_AA)
        cv2.putText(img, f"Right: {score[1]}", (900, 650), cv2.FONT_HERSHEY_COMPLEX, 2,
                    (255, 255, 255), 5, cv2.LINE_AA)

        # Check if ball missed (point lost)
        if ballPos[0] < 40:
            winner = "Right Player"
            roundWins[1] += 1
            gameOver = True
        elif ballPos[0] > 1200:
            winner = "Left Player"
            roundWins[0] += 1
            gameOver = True

        # Check score win condition
        if score[0] >= winningScore:
            winner = "Left Player"
            roundWins[0] += 1
            gameOver = True
        elif score[1] >= winningScore:
            winner = "Right Player"
            roundWins[1] += 1
            gameOver = True

        # Draw scoreboard banner (always visible)
        cv2.rectangle(img, (400, 10), (880, 60), (50, 50, 50), -1)  # dark background
        cv2.putText(img, f"Round Wins  Left [{roundWins[0]}]  |  Right [{roundWins[1]}]",
                    (410, 50), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 255), 3)

    elif gameOver and not finalOver:
        # Show Game Over Screen with Winner + Round Wins
        img = imgGameOver.copy()

        cv2.putText(img, f"{winner} Wins Round!", (250, 300),
                    cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 255, 0), 5)

        cv2.putText(img, f"Round Wins", (480, 420),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)

        cv2.putText(img, f"Left: {roundWins[0]}", (300, 500),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 4)
        cv2.putText(img, f"Right: {roundWins[1]}", (800, 500),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 4)

        cv2.putText(img, "Press R to Restart Round", (350, 600),
                    cv2.FONT_HERSHEY_COMPLEX, 1.5, (200, 0, 200), 4)

        # Final match winner check
        if roundWins[0] == 2:
            finalWinner = "Left Player"
            finalOver = True
        elif roundWins[1] == 2:
            finalWinner = "Right Player"
            finalOver = True

    elif finalOver:
        # Final Winner Screen
        img = imgGameOver.copy()
        cv2.putText(img, f"{finalWinner} Wins the Match!", (200, 360),
                    cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 255, 255), 5)
        cv2.putText(img, f"Final Score  Left {roundWins[0]} - Right {roundWins[1]}", (250, 500),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)
        cv2.putText(img, "Press ESC to Quit", (400, 620),
                    cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 200, 200), 4)

    # Show window
    cv2.imshow("Pong Game", img)
    key = cv2.waitKey(1)

    # Restart round
    if key == ord('r') or key == ord('R'):
        ballPos = [100, 100]
        speedX, speedY = 10, 10
        gameOver = False
        score = [0, 0]
        winner = None

    # Quit game
    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
