"""
GUI Module for CPT Test
Handles graphical user interface for the ADHD CPT Test
"""
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
import time

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.cpt_test import CPTCore
from reports.report_generator import ReportGenerator

class CPTGUI:
    """Main GUI Class for the CPT Test application"""
    
    def __init__(self, root):
        """Initialize the GUI with a Tkinter root window"""
        self.root = root
        self.root.title("ADHD Continuous Performance Task (CPT)")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create CPT test core
        self.cpt_core = CPTCore()
        
        # Create frames
        self.create_frames()
        self.show_welcome_frame()
        
    def create_frames(self):
        """Create all GUI frames for the application"""
        # Welcome frame
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.welcome_frame, text="ADHD Continuous Performance Task", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Label(self.welcome_frame, text="This test measures attention and impulsivity.", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        tk.Button(self.welcome_frame, text="Start", command=self.show_info_frame, font=("Arial", 14), bg="#4CAF50", fg="white", padx=20, pady=10).pack(pady=20)
        
        # Participant info frame
        self.info_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.info_frame, text="Participant Information", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
        
        info_fields = tk.Frame(self.info_frame, bg="#f0f0f0")
        info_fields.pack(pady=10)
        
        tk.Label(info_fields, text="Name:", bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky="e")
        tk.Label(info_fields, text="Age:", bg="#f0f0f0").grid(row=1, column=0, pady=5, sticky="e")
        tk.Label(info_fields, text="Gender:", bg="#f0f0f0").grid(row=2, column=0, pady=5, sticky="e")
        
        self.name_entry = tk.Entry(info_fields, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        
        self.age_entry = tk.Entry(info_fields, width=30)
        self.age_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        
        self.gender_var = tk.StringVar()
        gender_options = ttk.Combobox(info_fields, textvariable=self.gender_var, width=27)
        gender_options['values'] = ('Male', 'Female', 'Other')
        gender_options.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        
        tk.Button(self.info_frame, text="Start Test", command=self.show_instructions_frame, font=("Arial", 12), bg="#4CAF50", fg="white", padx=15, pady=5).pack(pady=20)
        
        # Instructions frame
        self.instructions_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.instructions_frame, text="Test Instructions", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
        instruction_text = """
        In this test, you will see letters appear on the screen one at a time.
        
        Press the SPACEBAR only when you see the letter 'X'.
        
        Do not press any key for other letters.
        
        Try to respond as quickly and accurately as possible.
        
        The test will last approximately 5 minutes.
        """
        tk.Label(self.instructions_frame, text=instruction_text, font=("Arial", 12), justify="left", bg="#f0f0f0").pack(pady=10)
        tk.Button(self.instructions_frame, text="Begin Test", command=self.start_test, font=("Arial", 12), bg="#4CAF50", fg="white", padx=15, pady=5).pack(pady=20)
        
        # Test frame
        self.test_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.stimulus_label = tk.Label(self.test_frame, text="", font=("Arial", 72, "bold"), bg="#f0f0f0")
        self.stimulus_label.pack(expand=True)
        self.time_label = tk.Label(self.test_frame, text="Time Remaining: 5:00", font=("Arial", 12), bg="#f0f0f0")
        self.time_label.pack(pady=20)
        
        # Results frame
        self.results_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.results_frame, text="Test Results", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        self.results_text = tk.Text(self.results_frame, height=10, width=60, font=("Arial", 12))
        self.results_text.pack(pady=10)
        
        # Create a frame for the plots
        self.plots_frame = tk.Frame(self.results_frame, bg="#f0f0f0")
        self.plots_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
        # Buttons for results frame
        buttons_frame = tk.Frame(self.results_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=10)
        tk.Button(buttons_frame, text="Save Report", command=self.save_report, font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(buttons_frame, text="New Test", command=self.reset_test, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

    def show_welcome_frame(self):
        """Show the welcome frame"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_info_frame(self):
        """Show the participant info frame"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_instructions_frame(self):
        """Validate participant info and show instructions"""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if not age or not age.isdigit():
            messagebox.showerror("Error", "Please enter a valid age.")
            return
        if not gender:
            messagebox.showerror("Error", "Please select your gender.")
            return
            
        self.cpt_core.participant_info = {
            "name": name,
            "age": int(age),
            "gender": gender,
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
        
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.instructions_frame.pack(fill=tk.BOTH, expand=True)
        
    def start_test(self):
        """Start the CPT test"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start the core test
        self.cpt_core.start_test()
        
        # Bind spacebar for responses
        self.root.bind("<space>", self.on_response)
        
        # Start test loop
        self.update_timer()
        self.present_stimulus()
        
    def present_stimulus(self):
        """Clear current stimulus and schedule the next one"""
        if not self.cpt_core.test_running:
            return
            
        # Clear the current stimulus
        self.stimulus_label.config(text="")
        
        # Schedule next stimulus after inter-stimulus interval
        self.root.after(self.cpt_core.inter_stimulus_interval - self.cpt_core.stimulus_duration, 
                       self.display_stimulus)
        
    def display_stimulus(self):
        """Display a stimulus (letter) on the screen"""
        if not self.cpt_core.test_running:
            return
            
        # Generate new stimulus using the core logic
        stimulus = self.cpt_core.generate_stimulus()
        if stimulus:
            self.stimulus_label.config(text=stimulus)
        
        # Clear the stimulus after stimulus duration
        self.root.after(self.cpt_core.stimulus_duration, self.present_stimulus)
        
    def on_response(self, event):
        """Handle spacebar responses"""
        self.cpt_core.process_response()
            
    def update_timer(self):
        """Update the timer display"""
        if not self.cpt_core.test_running:
            return
            
        remaining = self.cpt_core.check_time_remaining()
        time_str = self.cpt_core.format_time_remaining(remaining)
        
        self.time_label.config(text=f"Time Remaining: {time_str}")
        
        if remaining <= 0:
            self.end_test()
        else:
            self.root.after(1000, self.update_timer)
            
    def end_test(self):
        """End the test and show results"""
        # End test and get results from core
        results = self.cpt_core.end_test()
        
        # Unbind spacebar
        self.root.unbind("<space>")
        
        # Show results
        self.show_results()
        
    def show_results(self):
        """Display test results"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display summary results in text widget
        self.results_text.delete(1.0, tk.END)
        participant = self.cpt_core.participant_info
        results = self.cpt_core.results
        
        self.results_text.insert(tk.END, f"Participant: {participant['name']} ({participant['age']} years, {participant['gender']})\n")
        self.results_text.insert(tk.END, f"Date: {participant['date']}\n\n")
        self.results_text.insert(tk.END, f"Total Stimuli: {results['total_stimuli']}\n")
        self.results_text.insert(tk.END, f"Target Stimuli (X): {results['target_stimuli']}\n")
        self.results_text.insert(tk.END, f"Correct Responses: {results['correct_responses']}\n")
        self.results_text.insert(tk.END, f"Commission Errors: {results['commission_errors']}\n")
        self.results_text.insert(tk.END, f"Omission Errors: {results['omission_errors']}\n")
        self.results_text.insert(tk.END, f"Mean Response Time: {results['mean_rt']:.2f} ms\n")
        self.results_text.insert(tk.END, f"Response Time SD: {results['rt_std']:.2f} ms\n")
        self.results_text.insert(tk.END, f"Hit Rate: {results['hit_rate']:.2f}\n")
        self.results_text.insert(tk.END, f"False Alarm Rate: {results['false_alarm_rate']:.2f}\n")
        self.results_text.insert(tk.END, f"d': {results['d_prime']:.2f}\n")
        
        # Create plots
        self.create_plots()
        
    def create_plots(self):
        """Create plots for result visualization"""
        # Clear any existing plots
        for widget in self.plots_frame.winfo_children():
            widget.destroy()
            
        # Create a report generator and use it to get the figure
        report_gen = ReportGenerator(self.cpt_core.results, self.cpt_core.participant_info)
        fig = report_gen.generate_plots()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def save_report(self):
        """Save test reports"""
        # Create report generator and save all reports
        report_gen = ReportGenerator(self.cpt_core.results, self.cpt_core.participant_info)
        report_files = report_gen.save_reports()
        
        # Show message with saved files
        messagebox.showinfo("Report Saved", 
                          f"Report saved as:\n{report_files['png']}\n{report_files['csv']}\n{report_files['html']}")
        
    def reset_test(self):
        """Reset the application for a new test"""
        self.cpt_core = CPTCore()  # Create new test core
        self.show_welcome_frame()