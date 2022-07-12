from textual.app import App
from textual.widgets import DirectoryTree, Placeholder, ScrollView, FileClick, Header, Footer
from textual.widget import Widget
from textual.reactive import Reactive

from rich.syntax import Syntax
from rich.console import RenderableType
from rich.panel import Panel
from rich.align import Align

import os.path

import vlc

# TODO: Refactor DirectorySelector into its own file
#       Implement functionality
class DirectorySelector(Widget):

    mouse_over=Reactive(False)

    def render(self) -> Panel:
        return Panel(Align.center("Select Music Directory", vertical="middle"), style=("on dark_red" if self.mouse_over else ""), width=48)

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

class MusicPlayer(App):

    global player

    player = vlc.MediaPlayer() # media player provided by VLC to control music

    async def on_load(self, event):
        await self.bind("q", "quit", "Quit") # quit keybind
        await self.bind("p", "pause_play()", "Pause/Play") # pause/play keybind
    
    # Action handler to pause music
    def action_pause_play(self):
        player.pause()

    async def on_mount(self) -> None:
        # Creating Widgets
        self.body = ScrollView(Align.center("Nothing Playing", vertical="middle"))

        # TODO: UN-hard code directory
        self.directory = DirectoryTree("/home/andrxw/Downloads", "Music") # shows the directory
        
        await self.view.dock(Header(), edge="top") # Docks the header
        self.title = "Music Player" # Sets title on top of header

        await self.view.dock(Footer(), edge="bottom") # Docks Footer

        # await self.view.dock(Placeholder(), edge="bottom", size=10)

        await self.view.dock(DirectorySelector(), edge="bottom", size=10)

        await self.view.dock(ScrollView(self.directory), edge="left", size=48, name="Sidebar") # docks the directory and allows it to scroll
 
        await self.view.dock(self.body, edge="top") # docks body which will display the currently playing music

    async def handle_file_click(self, message: FileClick) -> None:
        # Message sent by directory tree when clicked
        
        music_file: RenderableType

        music_file = message.path # sets music_file to the file clicked
        
        # TODO: Update to show status of the song as well (paused/playing)
        await self.body.update(Align.center(os.path.basename(music_file), vertical="middle")) # updates body to show currently playing
        
        player.set_mrl(music_file) # sets the player to the selected music file
        
        # checks if the player is playing before playing the music
        # NOTE: this doesn't work properly and will need to be fixed
        if player.is_playing():
            player.pause()
        else:
            player.play()

MusicPlayer.run(log="textual.log")
