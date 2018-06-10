from threading import Timer
from functools import partial

class Interval(object):
    """https://gist.github.com/bbengfort/a7d46013f39cf367daa5"""

    def __init__(self, interval, function, args=[], kwargs={}):
        """Runs the function at a specified interval with given arguments."""

        self.interval = interval
        self.function = partial(function, *args, **kwargs)
        self.running  = False 
        self._timer   = None 

    def __call__(self):
        """Handler function for calling the partial and continuting."""

        self.running = False  
        self.start()           
        self.function()       

    def start(self):
        """Starts the interval and lets it run."""

        if self.running:
            # Don't start if we're running! 
            return 
            
        # Create the timer object, start and set state. 
        self._timer = Timer(self.interval, self)
        self._timer.start() 
        self.running = True

    def stop(self):
        """Cancel the interval (no more function calls)."""
        
        if self._timer:
            self._timer.cancel() 
        self.running = False 
        self._timer  = None
