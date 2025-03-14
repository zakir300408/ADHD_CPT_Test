"""
Core TOVA Test logic module
Contains the main logic for administering the Test of Variables of Attention (TOVA)
"""
import random
import time
import numpy as np
from scipy.stats import norm
from datetime import datetime

class TOVACore:
    """
    Core TOVA Test logic, separated from GUI components
    
    The Test of Variables of Attention (TOVA) is a continuous performance test 
    that measures attention and impulsivity. It uses a simple visual stimulus
    with two conditions: target (requiring a response) and non-target (requiring inhibition).
    
    The test has two phases:
    1. Infrequent target phase (targets appear 22.5% of the time)
    2. Frequent target phase (targets appear 77.5% of the time)
    
    This implementation focuses on visual stimuli, presenting either a 
    square at the top of the screen (target) or at the bottom (non-target).
    """
    def __init__(self):
        # Test parameters
        self.test_duration = 1200  # 20 minutes in seconds (standard TOVA is ~21.6 minutes)
        self.stimulus_duration = 100  # milliseconds
        self.inter_stimulus_interval = 2000  # milliseconds (2 seconds)
        
        # Phase parameters
        self.infrequent_target_ratio = 0.225  # 22.5% targets in first half
        self.frequent_target_ratio = 0.775    # 77.5% targets in second half
        self.current_phase = "infrequent"     # Start with infrequent targets phase
        self.phase_switch_time = None
        
        # Stimulus state
        self.current_stimulus = None  # "target" or "non-target"
        
        # Test state
        self.test_running = False
        self.start_time = None
        self.response_times = []
        self.correct_responses = 0       # hits - correct response to target
        self.commission_errors = 0       # false alarms - response to non-target
        self.omission_errors = 0         # misses - no response to target
        self.anticipatory_responses = 0  # responses < 150ms (considered guesses)
        self.multiple_responses = 0      # multiple responses to single stimulus
        self.post_commission_errors = 0  # errors following a commission error
        
        self.stimuli_shown = 0
        self.target_stimuli = 0
        self.non_target_stimuli = 0
        self.last_key_time = 0
        self.stimulus_time = 0
        self.response_window_active = False
        self.current_response_count = 0  # count responses to current stimulus
        self.last_was_commission = False # track if last response was a commission error
        
        self.participant_info = {}
        self.results = {
            "infrequent_targets": {},
            "frequent_targets": {}
        }
        
    def start_test(self):
        """Initialize test parameters and start the test"""
        self.test_running = True
        self.start_time = time.time()
        
        # Reset metrics
        self.response_times = []
        self.correct_responses = 0
        self.commission_errors = 0
        self.omission_errors = 0
        self.anticipatory_responses = 0
        self.multiple_responses = 0
        self.post_commission_errors = 0
        
        self.stimuli_shown = 0
        self.target_stimuli = 0
        self.non_target_stimuli = 0
        self.last_key_time = 0
        self.current_phase = "infrequent"
        self.last_was_commission = False
        
        # Set phase switch time to halfway through the test
        self.phase_switch_time = time.time() + (self.test_duration / 2)
        
    def check_time_remaining(self):
        """Check remaining time in the test and handle phase switching"""
        if not self.test_running:
            return 0
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.test_duration - elapsed)
        
        # Check for phase switch
        if self.phase_switch_time and time.time() >= self.phase_switch_time:
            if self.current_phase == "infrequent":
                # Calculate results before switching
                self._calculate_phase_results("infrequent_targets")
                
                # Switch to frequent target phase
                self.current_phase = "frequent"
                self.phase_switch_time = None
                
                # Reset metrics for the new phase
                self.response_times = []
                self.correct_responses = 0
                self.commission_errors = 0
                self.omission_errors = 0
                self.anticipatory_responses = 0
                self.multiple_responses = 0
                self.post_commission_errors = 0
                
                self.target_stimuli = 0
                self.non_target_stimuli = 0
                self.stimuli_shown = 0
                
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
        """Generate a stimulus (target or non-target)"""
        if not self.test_running:
            return None
            
        # Reset response state for new stimulus
        self.response_window_active = True
        self.current_response_count = 0
        
        # Determine if this should be a target stimulus based on current phase
        target_ratio = self.infrequent_target_ratio if self.current_phase == "infrequent" else self.frequent_target_ratio
            
        if random.random() < target_ratio:
            self.current_stimulus = "target"
            self.target_stimuli += 1
        else:
            self.current_stimulus = "non-target"
            self.non_target_stimuli += 1
            
        self.stimuli_shown += 1
        self.stimulus_time = time.time()
        
        return self.current_stimulus
        
    def end_response_window(self):
        """End the response window for the current stimulus and process omissions"""
        if not self.test_running or not self.response_window_active:
            return
            
        self.response_window_active = False
        
        # If no response was made to a target, count as omission
        if self.current_stimulus == "target" and self.current_response_count == 0:
            self.omission_errors += 1
            
        # Reset commission error tracking for next stimulus
        self.last_was_commission = False
        
    def process_response(self):
        """Process a user response (spacebar press)"""
        if not self.test_running:
            return
            
        current_time = time.time()
        
        # Always track the last keypress time to prevent rapid responses
        if current_time - self.last_key_time < 0.2:
            return
            
        self.last_key_time = current_time
        
        # Allow response processing regardless of self.response_window_active status
        # This ensures responses are counted even if window activation is inconsistent
        rt = (current_time - self.stimulus_time) * 1000  # convert to ms
        
        # Count this response
        self.current_response_count += 1
        
        # If this is a multiple response (after first), count it separately
        if self.current_response_count > 1:
            self.multiple_responses += 1
            return
            
        # Check if this is an anticipatory response (< 150ms)
        if rt < 150:
            self.anticipatory_responses += 1
            return
        
        # Process regular responses
        if self.current_stimulus == "target":
            # Correct response to target
            self.correct_responses += 1
            self.response_times.append(rt)
        else:
            # Commission error - response to non-target
            self.commission_errors += 1
            
            # Check if this is an error following a commission error
            if self.last_was_commission:
                self.post_commission_errors += 1
                
            # Set flag for next stimulus
            self.last_was_commission = True
            
    def end_test(self):
        """End the test and calculate metrics"""
        if not self.test_running:
            return
            
        self.test_running = False
        
        # Calculate final results for the current phase
        self._calculate_phase_results(self.current_phase + "_targets")
        
        return self.results
        
    def _calculate_phase_results(self, phase_name):
        """
        Calculate results for the specified test phase
        
        Args:
            phase_name: The test phase to calculate results for 
                        ("infrequent_targets" or "frequent_targets")
        """
        # Basic metrics (already tracked during test)
        total_stimuli = self.stimuli_shown
        target_stimuli = self.target_stimuli
        non_target_stimuli = self.non_target_stimuli
        
        # Response time metrics
        if self.correct_responses > 0:
            mean_rt = sum(self.response_times) / len(self.response_times)
            if len(self.response_times) > 1:
                rt_std = np.std(self.response_times)
                rt_var = np.var(self.response_times)
            else:
                rt_std = 0
                rt_var = 0
        else:
            mean_rt = 0
            rt_std = 0
            rt_var = 0
        
        # Attention metrics
        if target_stimuli > 0:
            hit_rate = self.correct_responses / target_stimuli
            omission_rate = self.omission_errors / target_stimuli
        else:
            hit_rate = 0
            omission_rate = 0
            
        if non_target_stimuli > 0:
            false_alarm_rate = self.commission_errors / non_target_stimuli
        else:
            false_alarm_rate = 0
            
        # Calculate d-prime (sensitivity)
        d_prime = self.calculate_d_prime(hit_rate, false_alarm_rate)
        
        # Calculate ADHD scores
        # TOVA provides a number of derived indices, here we calculate
        # a simplified Attention Comparison Score (ACS)
        # Note: This is a simplified version for educational purposes only
        
        # Reaction time component -1 to 1 (normalized deviation from ~400ms ideal)
        if mean_rt > 0:
            rt_component = max(-1, min(1, (400 - mean_rt) / 200))
        else:
            rt_component = 0
            
        # Accuracy component -1 to 1 (based on d-prime)
        accuracy_component = max(-1, min(1, d_prime / 4))
        
        # Variability component -1 to 1 (inverse of RT variance, normalized)
        if rt_var > 0:
            variability_component = max(-1, min(1, 1 - (rt_var / 40000)))  # 200^2 = 40000
        else:
            variability_component = 0
            
        # Impulsivity component -1 to 1 (inverse of commission errors)
        if non_target_stimuli > 0:
            impulsivity_component = max(-1, min(1, 1 - (2 * false_alarm_rate)))
        else:
            impulsivity_component = 0
            
        # Final ACS score (normalized to 0-100 scale)
        acs_score = ((rt_component + accuracy_component + variability_component + impulsivity_component + 4) / 8) * 100
        
        # Store results for this phase
        self.results[phase_name] = {
            "total_stimuli": total_stimuli,
            "target_stimuli": target_stimuli,
            "non_target_stimuli": non_target_stimuli,
            "correct_responses": self.correct_responses,
            "commission_errors": self.commission_errors,
            "omission_errors": self.omission_errors,
            "anticipatory_responses": self.anticipatory_responses,
            "multiple_responses": self.multiple_responses,
            "post_commission_errors": self.post_commission_errors,
            "mean_rt": mean_rt,
            "rt_std": rt_std,
            "rt_var": rt_var,
            "hit_rate": hit_rate,
            "false_alarm_rate": false_alarm_rate,
            "omission_rate": omission_rate,
            "d_prime": d_prime,
            "acs_score": acs_score,
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
        if self.current_phase == "infrequent":
            return "Infrequent Targets (22.5%)"
        else:
            return "Frequent Targets (77.5%)"