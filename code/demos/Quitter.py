from textual.app import App

class Quitter(App):
    async def on_load(self, event):
        await self.bind("q", "quit")

Quitter.run()
