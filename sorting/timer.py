import time

class SortingTimer:
    """Modular timer for sorting algorithm visualizations"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False

    def start(self):
        """Start the timer"""
        self.start_time = time.time()
        self.is_running = True
        self.end_time = None

    def stop(self):
        """Stop the timer"""
        self.end_time = time.time()
        self.is_running = False

    def get_elapsed(self):
        """Get elapsed time in seconds"""
        if not self.is_running or self.start_time is None:
            return 0
        return time.time() - self.start_time

    def get_total_time(self):
        """Get total time taken (after stopping)"""
        if self.start_time is None or self.end_time is None:
            return 0
        return self.end_time - self.start_time

    def format_time(self, seconds):
        """Format seconds into readable format (mm:ss.ms)"""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"

    def reset(self):
        """Reset the timer"""
        self.start_time = None
        self.end_time = None
        self.is_running = False
