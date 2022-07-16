from textual import events
from textual.app import App
from textual.widgets import DirectoryTree, Placeholder, ScrollView, FileClick, Header, Footer
from textual.widget import Widget
from textual.reactive import Reactive
from textual.binding import Bindings

from rich.syntax import Syntax
from rich.console import RenderableType
from rich.panel import Panel
from rich.align import Align

import os.path

import vlc

# TODO: Refactor DirectorySelector into its own file
class DirectorySelector(Widget):

    mouse_over=Reactive(False)

    md = "Select Music Directory"
    
    title = "."
    
    select_directory_title = ""
    
    has_focus = False

    status = False

    def render(self) -> Panel:
        return Panel(Align.center(self.md, vertical="middle"), style=("red" if self.mouse_over else ""), width=48, title=self.select_directory_title)

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

    def on_click(self) -> None:
        self.md = ""
        self.select_directory_title = "Enter Directory: "
        self.has_focus = True
        self.refresh()

    async def on_focus(self):
        self.has_focus = True

    def get_md(self):
        return self.title

    def on_key(self, event: events.Key) -> None:
        if self.has_focus == True:
            if event.key == "ctrl+h":
                self.md = self.md[:-1]
                self.refresh()
            elif event.key == "escape":
                self.md = "Select Music Directory"
                self.select_directory_title = ""
                self.has_focus = False
                self.refresh()
            elif event.key == "enter":
                self.title = self.md
                self.md = "Select Music Directory"
                self.select_directory_title = ""
                self.has_focus = False
                self.refresh()  
            else:
                self.md += event.key
                self.refresh()


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
        await self.bind("ctrl+c", "quit", "Quit") # quit keybind
        await self.bind("ctrl+p", "pause_play()", "Pause/Play") # pause/play keybind
    
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

        self.directory_selector = DirectorySelector()
        
        self.music_directory = self.directory_selector.get_md()

        self.directory = ScrollView(DirectoryTree(self.music_directory, "Music")) # shows the directory
        
        grid.place(
                area1=Header(),
                area2=Footer(),
                area3=self.directory,
                area4=self.directory_selector, 
                area5=self.body,
                area6=Placeholder(),
        )

        self.title="Music Player"

    async def on_key(self, event) -> None:
        if event.key == "enter":
            self.music_directory = self.directory_selector.get_md()
            await self.directory.update(DirectoryTree(self.music_directory, "Music"))

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
