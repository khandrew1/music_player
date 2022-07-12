from textual.app import App
from textual.widgets import DirectoryTree, Placeholder, ScrollView, FileClick, Header, Footer
from textual.widget import Widget

from rich.syntax import Syntax
from rich.console import RenderableType
from rich.panel import Panel

import vlc

class MusicPlayer(App):

    global player

    player = vlc.MediaPlayer() # media player provided by VLC to play music

    async def on_load(self, event):
        await self.bind("q", "quit", "Quit") # quit keybind
        await self.bind("p", "pause_play()", "Pause/Play") # pause/play keybind
    
    # Action handler to pause music
    def action_pause_play(self):
        player.pause()

    async def on_mount(self) -> None:
        # Creating Widgets
        self.body = ScrollView("Nothing Playing")

        # TODO: UN-hard code directory
        self.directory = DirectoryTree("/home/andrxw/Downloads", "Music") # shows the directory
        
        await self.view.dock(Header(), edge="top") # Docks the header
        self.title = "Music Player" # Sets title on top of header

        await self.view.dock(Footer(), edge="bottom") # Docks Footer

        await self.view.dock(ScrollView(self.directory), edge="left", size=48, name="Sidebar") # docks the directory and allows it to scroll

        await self.view.dock(self.body, edge="top") # docks body which will display the currently playing music

    async def handle_file_click(self, message: FileClick) -> None:
        # Message sent by directory tree when clicked
        
        music_file: RenderableType

        music_file = message.path # sets music_file to the file clicked
        
        # TODO: Only show base name of the file
        #       Update to show status of the song as well (paused/playing)
        await self.body.update(music_file) # updates body to show currently playing
        
        player.set_mrl(music_file) # sets the player to the selected music file
        
        # checks if the player is playing before playing the music
        # NOTE: this doesn't work properly and will need to be fixed
        if player.is_playing():
            player.pause()
        else:
            player.play()

MusicPlayer.run(log="textual.log")
