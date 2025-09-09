# Hand Gesture Ping Pong Game 🎮✋  

This project is an interactive **Ping Pong game controlled by hand gestures** using **OpenCV**, **CvZone**, and **MediaPipe**. The webcam detects your hands, and virtual bats appear on the left and right sides of the screen to hit the ball.  

---

## 🚀 Features  
- Play **Ping Pong** using just your **hands** (no keyboard/mouse needed).  
- **Real-time hand tracking** using `cvzone.HandTrackingModule`.  
- Dynamic ball movement with bouncing physics.  
- **Score tracking** for both players.  
- Game Over screen when the ball crosses the left or right boundary.  
- Press **R** to restart the game after it ends.  

---

## 📂 Project Structure  
```
.
├── pro (1).py              # Main game script
├── Resources/              # Image assets
│   ├── Background.png
│   ├── Ball.png
│   ├── bat1.png
│   ├── bat2.png
│   └── gameOver.png
```

---

## 🛠️ Installation  

1. Clone this repository or download the project.  
   ```bash
   git clone https://github.com/your-username/hand-gesture-pingpong.git
   cd hand-gesture-pingpong
   ```

2. Install dependencies:  
   ```bash
   pip install opencv-python cvzone numpy
   ```

3. Ensure you have a **webcam** connected.  

---

## ▶️ Usage  

Run the game with:  
```bash
python "pro (1).py"
```

- **Left hand** → Controls the left bat  
- **Right hand** → Controls the right bat  
- **Ball** → Bounces off bats and walls  
- **Game Over** → If the ball goes beyond left/right boundaries  
- **Press "R"** → Restart the game  

---

## 🎯 Controls  
- Move your **hands up and down** → Move the bats.  
- Keep the ball in play as long as possible to score points.  

---

## 📸 Screenshots (example)  
*(You can add screenshots of your gameplay here)*  

---

## 📌 Requirements  
- Python 3.7+  
- OpenCV  
- CvZone  
- NumPy  

---

## 🏆 Future Improvements  
- Add sound effects for ball hit & game over.  
- Single-player mode with AI opponent.  
- Better UI with menus and difficulty levels.  

---

## 👨‍💻 Author  
Developed by **Mohd Aazam**  
