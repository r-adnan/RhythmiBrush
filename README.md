# RhythmiBrush: Paint with Music 🎨🎵

**Paint with music. Our tool adjusts brush strokes based on your song. Color shifts with melody, size with energy. A blend of art and sound.**
## How It Works

- **Draw**: Put up just your pointer finger to draw on the screen.
- **Erase**: Put up your pointer and your middle finger to erase.
- **Adjust Brush Size**: Turn up your sound for a thicker brush size.
- **Exit**: Press 'q' to stop the program.

## Prerequisites

- **Python** [Download Python](https://www.python.org/downloads/)
- **API Keys**: Obtain API keys from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) (or relevant service).
- **Hardware**: Ensure you have a working camera.

## Setup
1. Navigate to the RhythmiBrush directory.
2. Make sure you have all the prerequisites installed.
3. Navigate to the src directory, and create a file named api_keys.py containing 3 lines:
```bash
clientID = "[YOUR CLIENT ID]"
clientSecret = "[YOUR CLIENT SECRET]"
clientURI = "[SOME URI REDIRECT LINK]" # because we are using spotipy api, it should look something like http://localhost/7777 or any 4 digit port number
```
4. After that, go back to the main directory, and run .\RhythmiBrush.bat for Windows and ./RhythmiBrush.sh for Linux/MacOS
5. It should automatically configure the python environment for you, and install the dependencies within, for any issues please refer to the [TroubleShooting](#troubleshooting) section

## Running the Project

### For Windows:

Run the following in the command prompt:
```bash
.\RhythmiBrush.bat
```
And enter your audio input device when prompted.

### For Linux or MacOS:
Run the following in the command prompt:
```bash
chmod +x run_project.sh
./RhythmiBrush.sh
```
And enter your audio input device when prompted.

## TroubleShooting
If you encounter any issues while setting up or running the application, please refer to the common problems and their solutions listed below.

### Known Issues

1. **Brush size not varying**
    - **Symptom:** Caused by issues with recording sound from audio device, maybe the wrong device is selected for listening.
    - **Solution:** You could navigate to the Painter.py code itself and hardcode the current recording loopback microphone you are using, although this may be difficult. Working on a more proper fix.
