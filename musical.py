#!/usr/bin/python3.8

from tools import *
import subprocess
import time
import opensimplex
import threading

class State:
    def __init__(self, val):
        self.lock = threading.Lock()
        self.val = val
    
    def set(self, val):
        with self.lock:
            self.val = val
    
    def get(self):
        with self.lock:
            return self.val

class TimeField:
    def __init__(self, average=0, min=None, max=None, roughness=0.2, amplitude=0.05, seed=None):
        self.field = opensimplex.OpenSimplex()
        self.start_time = time.time()
        self.average = average
        self.min = min
        self.max = max
        self.roughness = roughness
        self.amplitude = amplitude
        if seed is None:
            self.seed  = 0
        else:
            self.seed = seed
    
    def evalulate(self):
        val = self.average + self.amplitude * self.field.noise2d(x=self.seed, y=self.roughness*(time.time()-self.start_time))
        if self.min is not None:
            val = max(self.min, val)
        if self.max is not None:
            val = min(self.max, val)
        return val

class Stream(threading.Thread):
    def __init__(self, stream_id, sequence, note_duration, note_delay, octave=0, volume=1, state=None, notes = list("CDEFGAB")):
        threading.Thread.__init__(self)
        self.stream_id = stream_id
        self.duration_field = TimeField(average=note_duration, min=0.05)
        self.delay_field = TimeField(average=note_delay, min=0)
        self.sequence = sequence
        self.octave = octave
        self.volume = volume
        self.state = state
        self.notes = notes
        self.stopped = False
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        while not self.stopped:
            x = self.sequence.x
            self.sequence = self.sequence.n()
            note = self.notes[x%len(self.notes)]
            if self.state is not None:
                self.state.set((x, note))
            cmd = f"play -qn -t alsa synth {self.duration_field.evalulate()} pluck {note} pitch {1200 * self.octave} vol {self.volume}"
            subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
            time.sleep(self.delay_field.evalulate())