# 🚀 ISS Tracker & Pong Game for Pico Display 2.8"

![ISS Tracker](https://github.com/holmesha/ISS_tracker/blob/main/IMG_6613.jpg)

This project combines **real-time ISS tracking** with a **classic Pong game**, running on the **Pimoroni Pico Display Pack 2.8"**.  

Track the **International Space Station's position** on a **world map** and switch to **Pong** for a quick game—all controlled using the buttons on the display!  

-I used the new Pimoroni Micropython Firmware for the Pico 2w [HERE](https://github.com/pimoroni/pimoroni-pico-rp2350/releases)

---

## 🖥️ Features

### ISS Tracker:
- **Real-Time Tracking:** Displays the ISS position using live data from the **Where the ISS At? API**.  
- **World Map Display:** Shows the ISS position over a **map background** with **grid lines** and a **path history**.  
- **Dynamic Controls:**
  - Toggle **grid overlay** and **ISS path lines**.  
- **Coordinates Display:** Shows **latitude** and **longitude** in real-time.  
- **Path Memory:** Tracks and connects up to **50 past positions**.  

### Pong Game:
- **Classic Pong Gameplay:** Paddle movement, scoring, and AI opponent.  
- **Adjustable Speeds:** Customize paddle and ball speeds for faster gameplay.  
- **Dynamic Ball Bounces:** Angled bounces based on where the ball hits the paddle.  
- **Triple-Y Exit:** Press **Y three times quickly** to **return to the ISS Tracker**.  

---

## 🎮 Controls

### ISS Tracker Controls:
- **Button A:** Toggle **grid overlay**.  
- **Button B:** Toggle **ISS path line**.  
- **Button X:** Launch **Pong game**.  
- **Button Y:** **Placeholder** for future functionality.  

### Pong Game Controls:
- **Left Button (A):** Move paddle **left**.  
- **Right Button (B):** Move paddle **right**.  
- **Triple-Y Press (Y):** **Exit Pong** and return to **ISS Tracker**.  

---

## 🛠️ Hardware Requirements

- **Raspberry Pi Pico 2W** (with Wi-Fi support).  
- **Pimoroni Pico Display Pack 2.8"** with **4 buttons**.  
- **Micro-USB Cable** for programming and power.

---

## 📂 File Structure

```plaintext
/
├── lib/
│   ├── pong.py         # Pong game module
│   └── secrets.py      # Wi-Fi credentials (not included in repo)
├── worldmap.png        # Background world map for ISS Tracker
├── main.py             # Main ISS Tracker program
└── README.md           # Project documentation
```
---

## 🚀 Usage

1. **Power On:** Connect the **Pico W** to power via USB.  
2. **Connect to Wi-Fi:** The device will automatically connect and fetch ISS data.  
3. **Track ISS Position:**
   - Watch the **red dot** move across the **world map** in real time.  
   - Toggle the **grid** and **path** using buttons.  
4. **Play Pong:**
   - Press **X** to launch the **Pong game**.  
   - Use **left** and **right** buttons to **move the paddle** and **score points**.  
   - Press **Y three times** quickly to **exit Pong** and return to the ISS Tracker.  

---

## 🔧 Configuration

### Adjust Speeds:
Modify these variables in **`pong.py`**:  
```python
paddle_speed = 5    # Paddle speed
ball_speed = 3      # Ball speed
```
### Path Memory Length:
Adjust path length in main.py:
```python
if len(iss_path) > 50:  # Limit to 50 points
    iss_path.pop(0)
```
## 📝 Installation Instructions

1. **Download and Prepare Files**

   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/iss_tracker.git

2. Install Pimoroni MicroPython Firmware

- Download the Pimoroni Pico W MicroPython firmware from:  
  [Pimoroni Firmware Releases](https://github.com/pimoroni/pimoroni-pico-rp2350/releases)
- Flash the firmware onto your Pico 2W:
  1. Hold the **BOOTSEL** button on the Pico 2W.
  2. Connect it to your computer via USB.
  3. Release the **BOOTSEL** button once it mounts as a drive.
  4. Drag and drop the downloaded `.uf2` file onto the drive.

3. Set Up Wi-Fi Credentials

- Create a file named `secrets.py` inside the `lib/` folder:
```python
secrets = {
    "ssid": "your-wifi-name",
    "password": "your-wifi-password"
}
```
- Replace "your-wifi-name" and "your-wifi-password" with your network details.

4. Upload Map Image

- Copy `worldmap.png` to the root directory of the Pico. If you cloned the repository, it should already be there.
- Ensure the image is:
  - 320×240 pixels in size.
  - Saved as a PNG file.

5. Run the Program

- Open Thonny IDE.
- Select the **MicroPython (Raspberry Pi Pico)** interpreter.
- Open `main.py` and click **Run**. *note: if you call this file main.py, it should just load by itself.*

---

# 🚀 Usage

- **Power On**: Connect the Pico W to power via USB.
- **Connect to Wi-Fi**: The device will automatically connect and fetch ISS data.

### Track ISS Position
- Watch the red dot move across the world map in real time.
- Toggle the grid and path using buttons.

### Play Pong
- Press **X** to launch the Pong game.
- Use **left** (A) and **right** (B) buttons to move the paddle and score points.
- Press **Y** three times quickly to exit Pong and return to the ISS Tracker.

---

# 🧑‍💻 Contributing

Pull requests are welcome!

1. **Fork** the repo.
2. **Create** a feature branch:
  ```bash
  git checkout -b feature/your-feature
  ```
3. **Commit** changes:
  ```bash
  git commit -m "Add new feature"
  ```
4. **Push** to your branch:
  ```bash
  git push origin feature/your-feature
  ```
5. **Open** a pull request

---

# 📜 License

This project is licensed under the **MIT License**.  
