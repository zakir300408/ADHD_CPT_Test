"""
GUI Module for IMT/DMT Test
Handles graphical user interface for the Immediate and Delayed Memory Task
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
from core.imt_dmt_test import IMTDMTCore
from reports.imt_dmt_report import IMTDMTReportGenerator

class IMTDMTGUI:
    """Main GUI Class for the IMT/DMT Test application"""
    
    def __init__(self, root):
        """Initialize the GUI with a Tkinter root window"""
        self.root = root
        self.root.title("Immediate and Delayed Memory Task (IMT/DMT)")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create IMT/DMT test core
        self.imt_dmt_core = IMTDMTCore()
        
        # Create frames
        self.create_frames()
        self.show_welcome_frame()
        
    def create_frames(self):
        """Create all GUI frames for the application"""
        # Welcome frame
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.welcome_frame, text="Immediate and Delayed Memory Task", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Label(self.welcome_frame, text="This test measures attention, memory, and impulsivity.", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        # Test mode selection
        mode_frame = tk.Frame(self.welcome_frame, bg="#f0f0f0")
        mode_frame.pack(pady=20)
        
        tk.Label(mode_frame, text="Select Test Mode:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=5)
        
        self.test_mode = tk.StringVar(value="BOTH")
        tk.Radiobutton(mode_frame, text="Immediate Memory Task (IMT) Only", variable=self.test_mode, value="IMT", bg="#f0f0f0", font=("Arial", 11)).pack(anchor="w", pady=2)
        tk.Radiobutton(mode_frame, text="Delayed Memory Task (DMT) Only", variable=self.test_mode, value="DMT", bg="#f0f0f0", font=("Arial", 11)).pack(anchor="w", pady=2)
        tk.Radiobutton(mode_frame, text="Both IMT and DMT", variable=self.test_mode, value="BOTH", bg="#f0f0f0", font=("Arial", 11)).pack(anchor="w", pady=2)
        
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
        
        self.instruction_text = tk.StringVar()
        self.instruction_label = tk.Label(self.instructions_frame, textvariable=self.instruction_text, font=("Arial", 12), justify="left", bg="#f0f0f0", wraplength=600)
        self.instruction_label.pack(pady=10)
        
        tk.Button(self.instructions_frame, text="Begin Test", command=self.start_test, font=("Arial", 12), bg="#4CAF50", fg="white", padx=15, pady=5).pack(pady=20)
        
        # Test frame
        self.test_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Phase indicator
        self.phase_label = tk.Label(self.test_frame, text="", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.phase_label.pack(pady=10)
        
        # Stimulus display
        self.stimulus_label = tk.Label(self.test_frame, text="", font=("Arial", 72, "bold"), bg="#f0f0f0")
        self.stimulus_label.pack(expand=True)
        
        # Timer
        self.time_label = tk.Label(self.test_frame, text="Time Remaining: 10:00", font=("Arial", 12), bg="#f0f0f0")
        self.time_label.pack(pady=20)
        
        # Results frame
        self.results_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.results_frame, text="Test Results", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        
        # Create tabs for IMT and DMT results
        self.results_tabs = ttk.Notebook(self.results_frame)
        self.results_tabs.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # IMT Results tab
        self.imt_tab = tk.Frame(self.results_tabs, bg="#f0f0f0")
        self.results_tabs.add(self.imt_tab, text="IMT Results")
        
        self.imt_results_text = tk.Text(self.imt_tab, height=10, width=60, font=("Arial", 12))
        self.imt_results_text.pack(pady=10)
        
        self.imt_plots_frame = tk.Frame(self.imt_tab, bg="#f0f0f0")
        self.imt_plots_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
        # DMT Results tab
        self.dmt_tab = tk.Frame(self.results_tabs, bg="#f0f0f0")
        self.results_tabs.add(self.dmt_tab, text="DMT Results")
        
        self.dmt_results_text = tk.Text(self.dmt_tab, height=10, width=60, font=("Arial", 12))
        self.dmt_results_text.pack(pady=10)
        
        self.dmt_plots_frame = tk.Frame(self.dmt_tab, bg="#f0f0f0")
        self.dmt_plots_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
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
            
        self.imt_dmt_core.participant_info = {
            "name": name,
            "age": int(age),
            "gender": gender,
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
        
        # Set appropriate instructions based on test mode
        mode = self.test_mode.get()
        
        if mode == "IMT":
            instructions = """
            Immediate Memory Task (IMT) Instructions:
            
            In this test, you will see 5-digit numbers appear on the screen one at a time.
            
            Press the SPACEBAR when you see a number that is IDENTICAL to the number that appeared immediately before it.
            
            Do not press any key for other numbers.
            
            Try to respond as quickly and accurately as possible.
            
            The test will last approximately 5 minutes.
            """
        elif mode == "DMT":
            instructions = f"""
            Delayed Memory Task (DMT) Instructions:
            
            In this test, you will see 5-digit numbers appear on the screen one at a time.
            
            Press the SPACEBAR when you see a number that is IDENTICAL to the number that appeared 
            {self.imt_dmt_core.dmt_delay} positions earlier in the sequence.
            
            Do not press any key for other numbers.
            
            Try to respond as quickly and accurately as possible.
            
            The test will last approximately 5 minutes.
            """
        else:  # BOTH
            instructions = """
            IMT/DMT Combined Test Instructions:
            
            This test has two parts:
            
            Part 1 - Immediate Memory Task (IMT):
            Press the SPACEBAR when you see a number that is IDENTICAL to the number that appeared immediately before it.
            
            Part 2 - Delayed Memory Task (DMT):
            Press the SPACEBAR when you see a number that is IDENTICAL to the number that appeared several positions earlier.
            
            A message will notify you when the test switches from IMT to DMT.
            
            Do not press any key for other numbers.
            
            Try to respond as quickly and accurately as possible.
            
            The complete test will last approximately 10 minutes.
            """
            
        self.instruction_text.set(instructions)
        
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.instructions_frame.pack(fill=tk.BOTH, expand=True)
        
    def start_test(self):
        """Start the IMT/DMT test"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start the core test with selected mode
        self.imt_dmt_core.start_test(mode=self.test_mode.get())
        
        # Update phase label
        self.update_phase_label()
        
        # Bind spacebar for responses
        self.root.bind("<space>", self.on_response)
        
        # Start test loop
        self.update_timer()
        self.present_stimulus()
        
    def update_phase_label(self):
        """Update the phase label to show current test phase"""
        self.phase_label.config(text=f"Current Phase: {self.imt_dmt_core.get_current_phase_label()}")
        
    def present_stimulus(self):
        """Clear current stimulus and schedule the next one"""
        if not self.imt_dmt_core.test_running:
            return
            
        # Clear the current stimulus
        self.stimulus_label.config(text="")
        
        # Schedule next stimulus after inter-stimulus interval
        self.root.after(self.imt_dmt_core.inter_stimulus_interval - self.imt_dmt_core.stimulus_duration, 
                        self.display_stimulus)
        
    def display_stimulus(self):
        """Display a stimulus (number sequence) on the screen"""
        if not self.imt_dmt_core.test_running:
            return
            
        # Generate new stimulus using the core logic
        stimulus = self.imt_dmt_core.generate_stimulus()
        if stimulus:
            self.stimulus_label.config(text=stimulus)
        
        # Update phase label in case it changed
        self.update_phase_label()
        
        # Clear the stimulus after stimulus duration
        self.root.after(self.imt_dmt_core.stimulus_duration, self.present_stimulus)
        
    def on_response(self, event):
        """Handle spacebar responses"""
        self.imt_dmt_core.process_response()
            
    def update_timer(self):
        """Update the timer display"""
        if not self.imt_dmt_core.test_running:
            return
            
        remaining = self.imt_dmt_core.check_time_remaining()
        time_str = self.imt_dmt_core.format_time_remaining(remaining)
        
        self.time_label.config(text=f"Time Remaining: {time_str}")
        
        if remaining <= 0:
            self.end_test()
        else:
            self.root.after(1000, self.update_timer)
            
    def end_test(self):
        """End the test and show results"""
        # End test and get results from core
        results = self.imt_dmt_core.end_test()
        
        # Unbind spacebar
        self.root.unbind("<space>")
        
        # Show results
        self.show_results()
        
    def show_results(self):
        """Display test results"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get results data
        participant = self.imt_dmt_core.participant_info
        results = self.imt_dmt_core.results
        
        # Show IMT results if available
        if results["IMT"]:
            self.display_phase_results("IMT", results["IMT"], self.imt_results_text, self.imt_plots_frame)
        
        # Show DMT results if available
        if results["DMT"]:
            self.display_phase_results("DMT", results["DMT"], self.dmt_results_text, self.dmt_plots_frame)
        
        # Select the appropriate tab to display first
        if self.imt_dmt_core.mode == "DMT":
            self.results_tabs.select(1)  # Show DMT tab
        else:
            self.results_tabs.select(0)  # Show IMT tab (default)
        
    def display_phase_results(self, phase, phase_results, text_widget, plots_frame):
        """Display results for a specific phase (IMT or DMT)"""
        participant = self.imt_dmt_core.participant_info
        
        # Clear text widget
        text_widget.delete(1.0, tk.END)
        
        # Add phase title and participant info
        text_widget.insert(tk.END, f"{phase} Results\n\n")
        text_widget.insert(tk.END, f"Participant: {participant['name']} ({participant['age']} years, {participant['gender']})\n")
        text_widget.insert(tk.END, f"Date: {participant['date']}\n\n")
        
        # Add performance metrics
        text_widget.insert(tk.END, f"Total Stimuli: {phase_results['total_stimuli']}\n")
        text_widget.insert(tk.END, f"Target Stimuli: {phase_results['target_stimuli']}\n")
        text_widget.insert(tk.END, f"Correct Responses: {phase_results['correct_responses']}\n")
        text_widget.insert(tk.END, f"False Alarms: {phase_results['false_alarms']}\n")
        text_widget.insert(tk.END, f"Misses: {phase_results['misses']}\n")
        text_widget.insert(tk.END, f"Mean Response Time: {phase_results['mean_rt']:.2f} ms\n")
        text_widget.insert(tk.END, f"Response Time SD: {phase_results['rt_std']:.2f} ms\n")
        text_widget.insert(tk.END, f"Hit Rate: {phase_results['hit_rate']:.2f}\n")
        text_widget.insert(tk.END, f"False Alarm Rate: {phase_results['false_alarm_rate']:.2f}\n")
        text_widget.insert(tk.END, f"d': {phase_results['d_prime']:.2f}\n")
        
        # Create plots
        self.create_phase_plots(phase, phase_results, plots_frame)
        
    def create_phase_plots(self, phase, phase_results, plots_frame):
        """Create plots for a specific phase (IMT or DMT)"""
        # Clear any existing plots
        for widget in plots_frame.winfo_children():
            widget.destroy()
            
        # Create plots only if we have data
        if not phase_results["response_times"]:
            tk.Label(plots_frame, text="No response data available for this phase", 
                   font=("Arial", 12), bg="#f0f0f0").pack(pady=20)
            return
            
        # Create a figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        
        # Plot 1: Response time histogram
        ax1.hist(phase_results["response_times"], bins=20, color='skyblue', edgecolor='black')
        ax1.set_title(f'{phase} Response Time Distribution')
        ax1.set_xlabel('Response Time (ms)')
        ax1.set_ylabel('Frequency')
        
        # Plot 2: Error types pie chart
        labels = ['Correct Responses', 'False Alarms', 'Misses']
        sizes = [phase_results["correct_responses"], 
                 phase_results["false_alarms"], 
                 phase_results["misses"]]
        colors = ['#4CAF50', '#F44336', '#2196F3']
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        ax2.set_title(f'{phase} Response Distribution')
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=plots_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def save_report(self):
        """Save test reports"""
        try:
            # Create report generator and save all reports
            from reports.imt_dmt_report import IMTDMTReportGenerator
            report_gen = IMTDMTReportGenerator(self.imt_dmt_core.results, self.imt_dmt_core.participant_info)
            report_files = report_gen.save_reports()
            
            # Show message with saved files
            messagebox.showinfo("Report Saved", 
                              f"Report saved as:\n{report_files['png']}\n{report_files['csv']}\n{report_files['html']}")
        except ImportError:
            # Fallback if the report module is not available
            messagebox.showerror("Error", "Report generator module not found. Please ensure the reports module is properly installed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
        
    def reset_test(self):
        """Reset the application for a new test"""
        self.imt_dmt_core = IMTDMTCore()  # Create new test core
        self.show_welcome_frame()