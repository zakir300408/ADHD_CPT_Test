"""
Core IMT/DMT Test logic module
Contains the main logic for administering the Immediate and Delayed Memory Task
"""
import random
import time
import numpy as np
from scipy.stats import norm
from datetime import datetime

class IMTDMTCore:
    """
    Core IMT/DMT Test logic, separated from GUI components
    
    The Immediate and Delayed Memory Task (IMT/DMT) is a continuous performance test that 
    measures response inhibition and attention by presenting a series of numbers where
    the participant must respond when a stimulus matches the previous stimulus (IMT) 
    or when it matches a stimulus shown several trials back (DMT).
    """
    def __init__(self):
        # Test parameters
        self.test_duration = 600  # 10 minutes in seconds
        self.stimulus_duration = 500  # milliseconds
        self.inter_stimulus_interval = 1500  # milliseconds
        self.dmt_delay = 3  # Number of stimuli between target and probe in DMT
        self.mode = "IMT"  # Default mode: IMT or DMT
        self.current_phase = "IMT"  # Current active phase
        
        # Stimulus parameters
        self.stimulus_length = 5  # Length of digit sequence
        self.current_stimulus = None
        self.stimulus_history = []
        
        # Test state
        self.test_running = False
        self.start_time = None
        self.response_times = []
        self.correct_responses = 0
        self.false_alarms = 0  # responses to non-targets
        self.misses = 0  # missed targets
        self.stimuli_shown = 0
        self.target_stimuli = 0
        self.non_target_stimuli = 0
        self.last_key_time = 0
        self.stimulus_time = 0
        self.participant_info = {}
        self.results = {
            "IMT": {},
            "DMT": {}
        }
        
    def start_test(self, mode="BOTH"):
        """
        Initialize test parameters and start the test
        
        Args:
            mode: Test mode - "IMT", "DMT", or "BOTH" (run IMT followed by DMT)
        """
        self.test_running = True
        self.start_time = time.time()
        self.mode = mode
        self.current_phase = "IMT" if mode in ["IMT", "BOTH"] else "DMT"
        
        # Reset metrics
        self.response_times = []
        self.correct_responses = 0
        self.false_alarms = 0
        self.misses = 0
        self.stimuli_shown = 0
        self.target_stimuli = 0
        self.non_target_stimuli = 0
        self.last_key_time = 0
        
        # Reset stimulus history
        self.stimulus_history = []
        self.phase_switch_time = None
        
        if self.mode == "BOTH":
            # If running both, switch to DMT halfway through
            self.phase_switch_time = time.time() + (self.test_duration / 2)
        
    def check_time_remaining(self):
        """Check remaining time in the test and handle phase switching"""
        if not self.test_running:
            return 0
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.test_duration - elapsed)
        
        # Check for phase switch if running both IMT and DMT
        if self.mode == "BOTH" and self.phase_switch_time and time.time() >= self.phase_switch_time:
            if self.current_phase == "IMT":
                # Calculate IMT results before switching
                self._calculate_phase_results("IMT")
                
                # Switch to DMT phase
                self.current_phase = "DMT"
                self.phase_switch_time = None
                
                # Reset metrics for DMT phase
                self.response_times = []
                self.correct_responses = 0
                self.false_alarms = 0
                self.misses = 0
                self.target_stimuli = 0
                self.non_target_stimuli = 0
                
                # Keep the stimulus history for DMT
                return remaining
        
        if remaining <= 0:
            self.end_test()
            
        return remaining
        
    def format_time_remaining(self, remaining):
        """Format remaining time as minutes:seconds"""
        minutes = int(remaining / 60)
        seconds = int(remaining % 60)
        return f"{minutes}:{seconds:02d}"
        
    def generate_stimulus(self):
        """Generate a stimulus (random number sequence)"""
        if not self.test_running:
            return None
            
        # Generate a random digit sequence
        if not self.stimulus_history or random.random() > 0.25:  # 25% chance of target
            # Generate new random stimulus
            new_stimulus = ''.join(str(random.randint(0, 9)) for _ in range(self.stimulus_length))
            self.non_target_stimuli += 1
        else:
            if self.current_phase == "IMT":
                # IMT target: same as the previous stimulus
                new_stimulus = self.stimulus_history[-1]
                self.target_stimuli += 1
            else:  # DMT
                # DMT target: same as n stimuli back (if available)
                if len(self.stimulus_history) > self.dmt_delay:
                    new_stimulus = self.stimulus_history[-(self.dmt_delay + 1)]
                    self.target_stimuli += 1
                else:
                    # Not enough history, generate new
                    new_stimulus = ''.join(str(random.randint(0, 9)) for _ in range(self.stimulus_length))
                    self.non_target_stimuli += 1
                    
        # Store the new stimulus and set as current
        self.stimulus_history.append(new_stimulus)
        self.current_stimulus = new_stimulus
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
        
        # Check if this is a correct response
        is_target = False
        
        if self.current_phase == "IMT" and len(self.stimulus_history) >= 2:
            # In IMT, target is when current matches the previous stimulus
            if self.stimulus_history[-1] == self.stimulus_history[-2]:
                is_target = True
                
        elif self.current_phase == "DMT" and len(self.stimulus_history) > self.dmt_delay + 1:
            # In DMT, target is when current matches the stimulus n trials back
            if self.stimulus_history[-1] == self.stimulus_history[-(self.dmt_delay + 2)]:
                is_target = True
                
        if is_target:
            # Correct response
            self.correct_responses += 1
            rt = (current_time - self.stimulus_time) * 1000  # convert to ms
            self.response_times.append(rt)
        else:
            # False alarm - response to a non-target
            self.false_alarms += 1
            
    def end_test(self):
        """End the test and calculate metrics"""
        if not self.test_running:
            return
            
        self.test_running = False
        
        # Calculate final results for the current phase
        self._calculate_phase_results(self.current_phase)
        
        # If we're in BOTH mode and only completed IMT, also add a placeholder for DMT
        if self.mode == "BOTH" and not self.results["DMT"]:
            self.results["DMT"] = {
                "total_stimuli": 0,
                "target_stimuli": 0,
                "non_target_stimuli": 0,
                "correct_responses": 0,
                "false_alarms": 0,
                "misses": 0,
                "mean_rt": 0,
                "rt_std": 0,
                "hit_rate": 0,
                "false_alarm_rate": 0,
                "d_prime": 0,
                "response_times": []
            }
        
        return self.results
        
    def _calculate_phase_results(self, phase):
        """
        Calculate results for the specified test phase
        
        Args:
            phase: The test phase to calculate results for ("IMT" or "DMT")
        """
        # Calculate misses (missed targets)
        self.misses = self.target_stimuli - self.correct_responses
        
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
            false_alarm_rate = self.false_alarms / self.non_target_stimuli
        else:
            false_alarm_rate = 0
            
        # Calculate d-prime
        d_prime = self.calculate_d_prime(hit_rate, false_alarm_rate)
        
        # Store results for this phase
        self.results[phase] = {
            "total_stimuli": self.stimuli_shown,
            "target_stimuli": self.target_stimuli,
            "non_target_stimuli": self.non_target_stimuli,
            "correct_responses": self.correct_responses,
            "false_alarms": self.false_alarms,
            "misses": self.misses,
            "mean_rt": mean_rt,
            "rt_std": rt_std,
            "hit_rate": hit_rate,
            "false_alarm_rate": false_alarm_rate,
            "d_prime": d_prime,
            "response_times": self.response_times.copy()  # Create a copy to avoid reference issues
        }
        
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
            # If false alarm rate is 1, adjust it down slightly
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
        
    def get_current_phase_label(self):
        """Get a descriptive label for the current test phase"""
        if self.current_phase == "IMT":
            return "Immediate Memory Task"
        else:
            return f"Delayed Memory Task (Delay: {self.dmt_delay})"