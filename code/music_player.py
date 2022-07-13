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

# TODO: Refactor NowPlaying into its own file as well
class NowPlaying(Widget):

    mf = "Nothing Playing"

    def render(self) -> Panel:
        return Panel(Align.center(self.mf, vertical="middle"), title="Now Playing")

    def update(self, mf):
       self.mf = mf
       self.refresh()

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
        # Creating Grid

        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(size=48, name="left", min_size=20)
        grid.add_column(size=30, name="center") 
        grid.add_column(fraction=1, name="right")

        grid.add_row(size=3, name="top", min_size=2)
        grid.add_row(fraction=1, name="middle")
        grid.add_row(size=10, name="button")
        grid.add_row(size=1, name="bottom") 


        grid.add_areas(
                area1="left-start|right-end,top",
                area2="left-start|right-end,bottom",
                area3="left,middle",
                area4="left,button",
                area5="left-end|right-end,middle",
                area6="left-end|right-end,button",
        )


        # Creating Widgets
        self.body = NowPlaying()

        # TODO: UN-hard code directory
        self.directory = DirectoryTree("/home/andrxw/Downloads", "Music") # shows the directory
        
        grid.place(
                area1=Header(),
                area2=Footer(),
                area3=ScrollView(self.directory),
                area4=DirectorySelector(), 
                area5=self.body,
                area6=Placeholder(),
        )

        self.title="Music Player"

    async def handle_file_click(self, message: FileClick) -> None:
        # Message sent by directory tree when clicked
        
        music_file: RenderableType

        music_file = message.path # sets music_file to the file clicked
        
        # TODO: Update to show status of the song as well (paused/playing)
        self.body.update(os.path.basename(music_file)) # updates body to show currently playing
        
        player.set_mrl(music_file) # sets the player to the selected music file
        
        # checks if the player is playing before playing the music
        # NOTE: this doesn't work properly and will need to be fixed
        if player.is_playing():
            player.pause()
        else:
            player.play()

MusicPlayer.run(log="textual.log")
