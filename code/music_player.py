from textual.app import App
from textual.widgets import DirectoryTree, Placeholder, ScrollView, FileClick, Header, Footer
from textual.widget import Widget

from rich.syntax import Syntax
from rich.console import RenderableType
from rich.panel import Panel

import vlc

class MusicPlayer(App):

    global player

    player = vlc.MediaPlayer()

    async def on_load(self, event):
        await self.bind("q", "quit", "Quit") # quit keybind
        await self.bind("p", "pause_play()", "Pause/Play") # pause/play keybind
    
    # Action handler to pause music
    def action_pause_play(self):
        player.pause()

    async def on_mount(self) -> None:
        # Creating Widgets
        self.body = ScrollView() 
        self.directory = DirectoryTree("/home/andrxw/Downloads", "Music") # Actually shows the directory
        
        await self.view.dock(Header(), edge="top")
        self.title = "Music Player"
        await self.view.dock(Footer(), edge="bottom")

        await self.view.dock(ScrollView(self.directory), edge="left", size=48, name="Sidebar") # docks the directory and allows it to scroll

        await self.view.dock(self.body, edge="top")

    async def handle_file_click(self, message: FileClick) -> None:
        # Message sent by directory tree when clicked
        
        music_file: RenderableType

        music_file = message.path

        await self.body.update(music_file)
        
        player.set_mrl(music_file)

        if player.is_playing():
            player.pause()
        else:
            player.play()

MusicPlayer.run(log="textual.log")
