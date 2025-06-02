import tkinter as tk
from tkinter import ttk
import webbrowser
from tkinterhtml import HtmlFrame

class SpotifyPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Embed Example")
        self.root.geometry("800x500")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Spotify.TButton", 
                            background="#191414", 
                            foreground="white", 
                            padding=10, 
                            borderwidth=0)
        self.style.map("Spotify.TButton",
                      background=[('active', '#1Db954')])
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame for episodes
        self.episodes_frame = ttk.Frame(self.main_frame, width=300)
        self.episodes_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Frame for player info
        self.player_frame = ttk.Frame(self.main_frame)
        self.player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create episode buttons
        self.create_episode_buttons()
        
        # Create player info area
        self.create_player_info()
        
        # Make responsive
        self.root.bind("<Configure>", self.on_resize)
        
    def create_episode_buttons(self):
        episodes = [
            ("My Path to Spotify: Women in Engineering", "7makk4oTQel546B0PZlDM5"),
            ("What is Backstage?", "43cbJh4ccRD7lzM2730YK3"),
            ("Introducing Nerd Out@Spotify", "6I3ZzCxRhRkNqnQNo8AZPV")
        ]
        
        for title, episode_id in episodes:
            btn = ttk.Button(
                self.episodes_frame, 
                text=title, 
                style="Spotify.TButton",
                command=lambda id=episode_id, t=title: self.load_episode(id, t)
            )
            btn.pack(fill=tk.X, pady=5)
    
    def create_player_info(self):
        self.current_episode_label = ttk.Label(
            self.player_frame, 
            text="Select an episode to play", 
            font=('Arial', 12),
            wraplength=400
        )
        self.current_episode_label.pack(pady=20)
        
        self.open_browser_btn = ttk.Button(
            self.player_frame,
            text="Open in Browser",
            command=self.open_in_browser,
            state=tk.DISABLED
        )
        self.open_browser_btn.pack(pady=10)
        
        # HTML frame for basic display
        self.html_frame = HtmlFrame(self.player_frame)
        self.html_frame.pack_forget()  # Hide by default
        
    def load_episode(self, episode_id, title):
        self.current_episode = episode_id
        self.current_title = title
        self.current_episode_label.config(text=f"Selected: {title}")
        self.open_browser_btn.config(state=tk.NORMAL)
        
        # Show HTML info
        html_content = f"""
        <h3>{title}</h3>
        <p>This episode is ready to play. Click "Open in Browser" to listen.</p>
        <p><small>Episode ID: {episode_id}</small></p>
        """
        self.html_frame.set_content(html_content)
        self.html_frame.pack(fill=tk.BOTH, expand=True)  # Show the frame
    
    def open_in_browser(self):
        if self.current_episode:
            url = f"https://open.spotify.com/episode/{self.current_episode}"
            webbrowser.open(url)
    
    def on_resize(self, event):
        # Make responsive
        if event.width < 600:
            self.episodes_frame.pack_forget()
            self.episodes_frame.pack(fill=tk.X, pady=(0, 10))
            self.player_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.episodes_frame.pack_forget()
            self.player_frame.pack_forget()
            self.episodes_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
            self.player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpotifyPlayerApp(root)
    root.mainloop()