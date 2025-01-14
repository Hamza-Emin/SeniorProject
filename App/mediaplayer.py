import sys
import vlc  # VLC Python bindings
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog


class VLCPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VLC Media Player Example")
        self.setGeometry(100, 100, 800, 600)

        # Create VLC instance and media player
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        # Set up UI layout
        layout = QVBoxLayout()

        # Button to open video file
        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

        # Button to play the video
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        layout.addWidget(self.play_button)

        # Button to pause the video
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_video)
        layout.addWidget(self.pause_button)

        # Button to stop the video
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)
        layout.addWidget(self.stop_button)

        # Video rendering widget
        self.video_widget = QWidget(self)
        self.video_widget.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_widget)

        self.setLayout(layout)

        # Set the VLC media player to use the video widget for rendering
        win_id = int(self.video_widget.winId())
        self.media_player.set_hwnd(win_id)  # Use `set_nsobject(win_id)` on macOS

    def open_file(self):
        """Open a file dialog to choose a video file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Videos (*.mp4 *.avi *.mkv *.mov)")
        if file_path:
            media = self.vlc_instance.media_new(file_path)
            self.media_player.set_media(media)

    def play_video(self):
        """Play the video."""
        self.media_player.play()

    def pause_video(self):
        """Pause the video."""
        self.media_player.pause()

    def stop_video(self):
        """Stop the video."""
        self.media_player.stop()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VLCPlayer()
    player.show()
    sys.exit(app.exec_())
