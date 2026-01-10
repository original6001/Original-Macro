# Original Macro

The "Original Macro" application is a powerful macro designed to automate mouse clicks and record complex keyboard/mouse sequences with high precision. It is built to provide a smooth, lag-free experience for all your automation needs.

## Features

This application includes several features to enhance your workflow:

### 1. Autoclicker
*   **Adjustable Speeds:** Choose between 10, 15, 20, or 100 CPS (Clicks Per Second).
*   **Custom Activation:** Record a specific key to start the autoclicker whenever it's executed.
*   **Quick Stop:** Press the `c` key to stop clicking immediately.

### 2. Custom Macro Recorder
*   **Full Capture:** Record both mouse movements/clicks and keyboard inputs simultaneously.
*   **Perfect Sync:** Playback is perfectly timed, ensuring keyboard and mouse actions stay in sync exactly as they were performed.
*   **DPI Aware:** Coordinate accuracy is maintained across different screen resolutions and scaling settings.
*   **Easy Controls:** Start recording with a button and stop it by pressing the `/` (slash) key.
*   **Custom Activation:** Record a specific key to start the macro playback whenever it's executed.
*   **Save to File:** Save macros to a `.ini` file for later playback. Has capabilities to load, save and clear.

### 3. Advanced Macro Builder
*   **Manual Creation:** Build a macro step-by-step by adding specific keybinds and delays.
*   **Visual Sequence:** View your current macro sequence directly in the application.
*   **Management:** Save, load, and clear advanced macros using dedicated slots.
*   **Quick Correction:** Use the "Backspace" button to remove the last action from your sequence.

### 4. Advanced Features
*   **High-Precision Mode:** The app utilizes the Windows timer with 1 ms precision during macro recording for maximum accuracy.
*   **Global Hotkeys:**
    *   `Esc`: Completely exits the application.
    *   `c`: Stops the autoclicker or the current macro playback.
    *   `/`: Stops macro recording.

## How to use it

1.  **Run the application:** Execute `python main.py`.
2.  **Using the Autoclicker:**
    *   Select the desired CPS.
    *   Click "Autoclicker" to start a 3-second countdown.
    *   Alternatively, click "Record" next to "Start on:", press a key, and then click "Start on:" to wait for that keypress.
3.  **Recording Macros:**
    *   Click "Record Macro".
    *   Perform the actions you wish to save.
    *   Press `/` to finish recording.
    *   Play back the macro by clicking "Playback Macro" or by binding it to a "Start on:" key.

4.  **Using the Advanced Macro Builder:**
    *   Go to the "Advanced Macro" tab.
    *   Click "Record" next to "Add Keybind:", press a key, and then click "Add Keybind:" to add it to the sequence.
    *   Enter a delay in seconds and click "Add Delay (s):" to insert a pause.
    *   Use "Backspace" to remove the last entry.
    *   Click "Run Macro" to execute the sequence.
    *   Save and Load your custom sequences using the slots provided.

## Requirements

This tool is built using Python and the following libraries:
*   `keyboard`
*   `mouse`
*   `pydirectinput`
*   `configparser`
*   `custontkinter`

Install the dependencies by running the `install_dependencies.bat` file or manually using:
```bash
pip install keyboard mouse pydirectinput customtkinter
```

## License

This project is licensed under the GNU General Public License v3.0, see the [LICENSE](LICENSE) file for details.

## Contact Me
There are two ways that you can contact me:
*   Discord: 'ultamanium'
*   GitHub Issues: https://github.com/original6001/Original-Macro/issues 
