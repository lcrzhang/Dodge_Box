import os
import pygame

class SoundManager:
    """Simple sound manager using pygame.mixer.
    Place background music and sfx in a 'sounds' folder next to this file.
    - Music files (ogg/mp3) are played via pygame.mixer.music
    - SFX files (wav/ogg) are preloaded and played by name (filename without ext)
    """

    def __init__(self, sounds_dir=None):
        self._available = False
        try:
            pygame.mixer.init()
            self._available = True
        except Exception:
            self._available = False

        self.sounds = {}
        if sounds_dir is None:
            sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
        self.sounds_dir = sounds_dir
        self._load_sfx_folder(self.sounds_dir)

    def _load_sfx_folder(self, folder):
        if not self._available or not os.path.isdir(folder):
            return
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            if not os.path.isfile(path):
                continue
            name, ext = os.path.splitext(fname)
            if ext.lower() in (".wav", ".ogg", ".flac"):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except Exception:
                    # skip files that fail to load
                    pass

    def play_sfx(self, name, loops=0, maxtime=0, fade_ms=0):
        if not self._available:
            return
        snd = self.sounds.get(name)
        if snd:
            try:
                snd.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
            except Exception:
                pass

    def play_music(self, music_path, loops=-1, start=0.0, volume=0.5):
        if not self._available:
            return
        # allow relative path from project root or absolute
        if not os.path.isabs(music_path):
            music_path = os.path.join(os.path.dirname(__file__), music_path)
        if not os.path.isfile(music_path):
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=loops, start=start)
        except Exception:
            pass

    def stop_music(self):
        if not self._available:
            return
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def set_music_volume(self, volume):
        if not self._available:
            return
        try:
            pygame.mixer.music.set_volume(float(volume))
        except Exception:
            pass