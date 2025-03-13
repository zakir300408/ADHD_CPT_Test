"""
Core CPT Test logic module
Contains the main logic for administering a Continuous Performance Task
"""
import random
import time
import numpy as np
from datetime import datetime
from scipy.stats import norm

class CPTCore:
    """
    Core CPT Test logic, separated from GUI components
    """
    def __init__(self):
        # Test parameters
        self.test_duration = 300  # 5 minutes in seconds
        self.stimulus_duration = 250  # milliseconds
        self.inter_stimulus_interval = 1500  # milliseconds
        self.target_ratio = 0.2  # 20% of stimuli are targets
        self.target_letter = "X"
        
        # Test state
        self.current_stimulus = None
        self.test_running = False
        self.start_time = None
        self.response_times = []
        self.correct_responses = 0
        self.commission_errors = 0  # responses to non-targets
        self.omission_errors = 0  # missed targets
        self.stimuli_shown = 0
        self.target_stimuli = 0
        self.non_target_stimuli = 0
        self.last_key_time = 0
        self.stimulus_time = 0
        self.participant_info = {}
        self.results = {}
        
    def start_test(self):
        """Initialize test parameters and start the test"""
        self.test_running = True
        self.start_time = time.time()
        self.response_times = []
        self.correct_responses = 0
        self.commission_errors = 0
        self.omission_errors = 0
        self.stimuli_shown = 0
        self.target_stimuli = 0
        self.non_target_stimuli = 0
        self.last_key_time = 0
        
    def check_time_remaining(self):
        """Check remaining time in the test"""
        if not self.test_running:
            return 0
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.test_duration - elapsed)
        
        if remaining <= 0:
            self.end_test()
            
        return remaining
        
    def format_time_remaining(self, remaining):
        """Format remaining time as minutes:seconds"""
        minutes = int(remaining / 60)
        seconds = int(remaining % 60)
        return f"{minutes}:{seconds:02d}"
        
    def generate_stimulus(self):
        """Generate a stimulus (target or non-target letter)"""
        if not self.test_running:
            return None
            
        # Determine if this should be a target stimulus (X) or non-target
        if random.random() < self.target_ratio:
            self.current_stimulus = self.target_letter
            self.target_stimuli += 1
        else:
            # Choose a random letter that's not X
            letters = [chr(i) for i in range(65, 91) if chr(i) != self.target_letter]
            self.current_stimulus = random.choice(letters)
            self.non_target_stimuli += 1
            
        self.stimuli_shown += 1
        self.stimulus_time = time.time()
        return self.current_stimulus
        
    def process_response(self):
        """Process a user response (spacebar press)"""
        if not self.test_running:
            return
            
        current_time = time.time()
        
        # Prevent multiple rapid keypresses by requiring a minimal delay
        if current_time - self.last_key_time < 0.2:
            return
            
        self.last_key_time = current_time
        
        # If current stimulus is target, it's a correct response
        if self.current_stimulus == self.target_letter:
            self.correct_responses += 1
            rt = (current_time - self.stimulus_time) * 1000  # convert to ms
            self.response_times.append(rt)
        else:
            # If current stimulus is not the target, it's a commission error
            self.commission_errors += 1
            
    def end_test(self):
        """End the test and calculate metrics"""
        self.test_running = False
        
        # Calculate omission errors (missed targets)
        self.omission_errors = self.target_stimuli - self.correct_responses
        
        # Calculate metrics
        if self.correct_responses > 0:
            mean_rt = sum(self.response_times) / len(self.response_times)
            if len(self.response_times) > 1:
                rt_std = np.std(self.response_times)
            else:
                rt_std = 0
        else:
            mean_rt = 0
            rt_std = 0
        
        if self.target_stimuli > 0:
            hit_rate = self.correct_responses / self.target_stimuli
        else:
            hit_rate = 0
            
        if self.non_target_stimuli > 0:
            false_alarm_rate = self.commission_errors / self.non_target_stimuli
        else:
            false_alarm_rate = 0
            
        # Calculate d-prime
        d_prime = self.calculate_d_prime(hit_rate, false_alarm_rate)
        
        # Store results
        self.results = {
            "total_stimuli": self.stimuli_shown,
            "target_stimuli": self.target_stimuli,
            "non_target_stimuli": self.non_target_stimuli,
            "correct_responses": self.correct_responses,
            "commission_errors": self.commission_errors,
            "omission_errors": self.omission_errors,
            "mean_rt": mean_rt,
            "rt_std": rt_std,
            "hit_rate": hit_rate,
            "false_alarm_rate": false_alarm_rate,
            "d_prime": d_prime,
            "response_times": self.response_times
        }
        
        return self.results
        
    def calculate_d_prime(self, hit_rate, false_alarm_rate):
        """
        Calculate d' (d-prime) with proper handling of extreme values.
        Uses a standard correction for perfect scores: replacing rates of 0 with 1/(2N)
        and rates of 1 with 1-1/(2N), where N is the number of trials.
        """
        # Apply corrections for extreme values
        if hit_rate == 1.0:
            # If hit rate is perfect, adjust it down slightly
            hit_rate = 1.0 - (1.0 / (2 * self.target_stimuli)) if self.target_stimuli > 0 else 0.99
        elif hit_rate == 0.0:
            # If hit rate is zero, adjust it up slightly
            hit_rate = 1.0 / (2 * self.target_stimuli) if self.target_stimuli > 0 else 0.01
            
        if false_alarm_rate == 1.0:
            # If false alarm rate is 1 (all non-targets got a response), adjust it down slightly
            false_alarm_rate = 1.0 - (1.0 / (2 * self.non_target_stimuli)) if self.non_target_stimuli > 0 else 0.99
        elif false_alarm_rate == 0.0:
            # If false alarm rate is zero, adjust it up slightly
            false_alarm_rate = 1.0 / (2 * self.non_target_stimuli) if self.non_target_stimuli > 0 else 0.01
            
        # Calculate d-prime
        try:
            d_prime = norm.ppf(hit_rate) - norm.ppf(false_alarm_rate)
        except:
            # Fallback in case the calculation still fails
            d_prime = 4.65 if hit_rate > false_alarm_rate else 0
            
        return d_prime