"""
GUI Module for TOVA Test
Handles graphical user interface for the Test of Variables of Attention (TOVA)
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
from core.tova_test import TOVACore

class TOVAGUI:
    """Main GUI Class for the TOVA Test application"""
    
    def __init__(self, root):
        """Initialize the GUI with a Tkinter root window"""
        self.root = root
        self.root.title("Test of Variables of Attention (TOVA)")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create TOVA test core
        self.tova_core = TOVACore()
        
        # Create frames
        self.create_frames()
        self.show_welcome_frame()
        
    def create_frames(self):
        """Create all GUI frames for the application"""
        # Welcome frame
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.welcome_frame, text="Test of Variables of Attention (TOVA)", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Label(self.welcome_frame, text="This test measures attention, inhibition, and response time variability.", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        # TOVA length options
        time_frame = tk.Frame(self.welcome_frame, bg="#f0f0f0")
        time_frame.pack(pady=20)
        
        tk.Label(time_frame, text="Test Duration:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10)
        
        self.duration_var = tk.StringVar(value="Standard")
        duration_options = ttk.Combobox(time_frame, textvariable=self.duration_var, width=15)
        duration_options['values'] = ('Short (10 min)', 'Standard (20 min)')
        duration_options.grid(row=0, column=1, padx=10)
        
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
        tk.Label(self.instructions_frame, text="TOVA Instructions", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
        
        # Image example frame
        example_frame = tk.Frame(self.instructions_frame, bg="#f0f0f0")
        example_frame.pack(pady=15)
        
        # Target example (square at top)
        target_frame = tk.Frame(example_frame, bg="#f0f0f0", width=120, height=180, bd=1, relief=tk.RAISED)
        target_frame.pack(side=tk.LEFT, padx=20)
        target_frame.pack_propagate(False)
        
        tk.Label(target_frame, text="TARGET", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)
        
        # Create canvas for square
        target_canvas = tk.Canvas(target_frame, width=100, height=100, bg="white", highlightthickness=0)
        target_canvas.pack(pady=5)
        target_canvas.create_rectangle(25, 5, 75, 55, fill="black")  # Square at top
        
        tk.Label(target_frame, text="RESPOND", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        
        # Non-target example (square at bottom)
        nontarget_frame = tk.Frame(example_frame, bg="#f0f0f0", width=120, height=180, bd=1, relief=tk.RAISED)
        nontarget_frame.pack(side=tk.LEFT, padx=20)
        nontarget_frame.pack_propagate(False)
        
        tk.Label(nontarget_frame, text="NON-TARGET", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)
        
        # Create canvas for square
        nontarget_canvas = tk.Canvas(nontarget_frame, width=100, height=100, bg="white", highlightthickness=0)
        nontarget_canvas.pack(pady=5)
        nontarget_canvas.create_rectangle(25, 45, 75, 95, fill="black")  # Square at bottom
        
        tk.Label(nontarget_frame, text="DO NOT RESPOND", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        
        instructions_text = """
        In this test, you will see a black square appear either at the top or 
        the bottom of a white box in the center of the screen.

        Press the SPACEBAR when the square appears at the TOP of the box.
        Do NOT press any key when the square appears at the BOTTOM.

        Try to respond as quickly and accurately as possible.
        The test has two parts:
        1. First half: The target (top square) appears infrequently (22.5%)
        2. Second half: The target (top square) appears frequently (77.5%)
        
        The full test will take approximately 20 minutes to complete.
        """
        tk.Label(self.instructions_frame, text=instructions_text, font=("Arial", 12), justify="left", bg="#f0f0f0", wraplength=600).pack(pady=10)
        tk.Button(self.instructions_frame, text="Begin Test", command=self.start_test, font=("Arial", 12), bg="#4CAF50", fg="white", padx=15, pady=5).pack(pady=20)
        
        # Test frame
        self.test_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Phase indicator
        self.phase_label = tk.Label(self.test_frame, text="", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.phase_label.pack(pady=10)
        
        # Stimulus display
        self.stimulus_canvas = tk.Canvas(self.test_frame, width=160, height=160, bg="#ffffff", highlightthickness=2, highlightbackground="#000000")
        self.stimulus_canvas.pack(expand=True)
        
        # Timer
        self.time_label = tk.Label(self.test_frame, text="Time Remaining: 20:00", font=("Arial", 12), bg="#f0f0f0")
        self.time_label.pack(pady=20)
        
        # Results frame
        self.results_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.results_frame, text="TOVA Results", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        
        # Create tabs for the two phases
        self.results_tabs = ttk.Notebook(self.results_frame)
        self.results_tabs.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Infrequent targets tab
        self.infrequent_tab = tk.Frame(self.results_tabs, bg="#f0f0f0")
        self.results_tabs.add(self.infrequent_tab, text="Infrequent Targets (First Half)")
        
        self.infrequent_results_text = tk.Text(self.infrequent_tab, height=10, width=60, font=("Arial", 11))
        self.infrequent_results_text.pack(pady=5)
        
        self.infrequent_plots_frame = tk.Frame(self.infrequent_tab, bg="#f0f0f0")
        self.infrequent_plots_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Frequent targets tab
        self.frequent_tab = tk.Frame(self.results_tabs, bg="#f0f0f0")
        self.results_tabs.add(self.frequent_tab, text="Frequent Targets (Second Half)")
        
        self.frequent_results_text = tk.Text(self.frequent_tab, height=10, width=60, font=("Arial", 11))
        self.frequent_results_text.pack(pady=5)
        
        self.frequent_plots_frame = tk.Frame(self.frequent_tab, bg="#f0f0f0")
        self.frequent_plots_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Summary tab
        self.summary_tab = tk.Frame(self.results_tabs, bg="#f0f0f0")
        self.results_tabs.add(self.summary_tab, text="Overall Summary")
        
        self.summary_results = tk.Text(self.summary_tab, height=5, width=60, font=("Arial", 12))
        self.summary_results.pack(pady=5)
        
        self.summary_plots_frame = tk.Frame(self.summary_tab, bg="#f0f0f0")
        self.summary_plots_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
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
        # Set test duration based on selection
        if self.duration_var.get() == "Short (10 min)":
            self.tova_core.test_duration = 600  # 10 minutes
        else:
            self.tova_core.test_duration = 1200  # 20 minutes
            
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
            
        self.tova_core.participant_info = {
            "name": name,
            "age": int(age),
            "gender": gender,
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
        
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.instructions_frame.pack(fill=tk.BOTH, expand=True)
        
    def start_test(self):
        """Start the TOVA test"""
        for frame in [self.welcome_frame, self.info_frame, self.instructions_frame, self.test_frame, self.results_frame]:
            frame.pack_forget()
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start the core test
        self.tova_core.start_test()
        
        # Update phase label
        self.update_phase_label()
        
        # Bind spacebar for responses
        self.root.bind("<space>", self.on_response)
        
        # Start test loop
        self.update_timer()
        self.present_stimulus()
        
    def update_phase_label(self):
        """Update the phase label to show current test phase"""
        self.phase_label.config(text=f"Current Phase: {self.tova_core.get_current_phase_label()}")
        
    def present_stimulus(self):
        """Clear current stimulus and schedule the next one"""
        if not self.tova_core.test_running:
            return
            
        # Clear the stimulus
        self.stimulus_canvas.delete("all")
        
        # End the response window for the previous stimulus
        self.tova_core.end_response_window()
        
        # Schedule next stimulus after inter-stimulus interval
        self.root.after(self.tova_core.inter_stimulus_interval, self.display_stimulus)
        
    def display_stimulus(self):
        """Display a TOVA stimulus (square at top or bottom)"""
        if not self.tova_core.test_running:
            return
            
        # Generate new stimulus using the core logic
        stimulus_type = self.tova_core.generate_stimulus()
        
        if stimulus_type:
            # Clear canvas first
            self.stimulus_canvas.delete("all")
            
            # Draw stimulus based on type
            if stimulus_type == "target":
                # Target: Square at top
                self.stimulus_canvas.create_rectangle(50, 10, 110, 70, fill="black")
            else:
                # Non-target: Square at bottom
                self.stimulus_canvas.create_rectangle(50, 90, 110, 150, fill="black")
        
        # Update phase label in case it changed
        self.update_phase_label()
        
        # Schedule removal of stimulus after duration
        self.root.after(self.tova_core.stimulus_duration, self.present_stimulus)
        
    def on_response(self, event):
        """Handle spacebar responses"""
        self.tova_core.process_response()
            
    def update_timer(self):
        """Update the timer display"""
        if not self.tova_core.test_running:
            return
            
        remaining = self.tova_core.check_time_remaining()
        time_str = self.tova_core.format_time_remaining(remaining)
        
        self.time_label.config(text=f"Time Remaining: {time_str}")
        
        if remaining <= 0:
            self.end_test()
        else:
            self.root.after(1000, self.update_timer)
            
    def end_test(self):
        """End the test and show results"""
        # End test and get results from core
        results = self.tova_core.end_test()
        
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
        participant = self.tova_core.participant_info
        results = self.tova_core.results
        
        # Show results for infrequent targets phase
        if results.get("infrequent_targets"):
            self.display_phase_results("infrequent_targets", results["infrequent_targets"], 
                                     self.infrequent_results_text, self.infrequent_plots_frame)
        
        # Show results for frequent targets phase
        if results.get("frequent_targets"):
            self.display_phase_results("frequent_targets", results["frequent_targets"], 
                                     self.frequent_results_text, self.frequent_plots_frame)
        
        # Display overall summary
        self.display_overall_summary(results)
        
    def display_phase_results(self, phase_name, phase_data, text_widget, plots_frame):
        """Display results for a specific phase"""
        participant = self.tova_core.participant_info
        
        # Format phase name for display
        display_name = "Infrequent Targets (First Half)" if phase_name == "infrequent_targets" else "Frequent Targets (Second Half)"
        
        # Clear text widget
        text_widget.delete(1.0, tk.END)
        
        # Add phase title and participant info
        text_widget.insert(tk.END, f"{display_name}\n\n")
        text_widget.insert(tk.END, f"Participant: {participant['name']} ({participant['age']} years, {participant['gender']})\n")
        text_widget.insert(tk.END, f"Date: {participant['date']}\n\n")
        
        # Add performance metrics
        text_widget.insert(tk.END, f"Total Stimuli: {phase_data['total_stimuli']}\n")
        text_widget.insert(tk.END, f"Target Stimuli: {phase_data['target_stimuli']}\n")
        text_widget.insert(tk.END, f"Correct Responses: {phase_data['correct_responses']}\n")
        text_widget.insert(tk.END, f"Commission Errors: {phase_data['commission_errors']}\n")
        text_widget.insert(tk.END, f"Omission Errors: {phase_data['omission_errors']}\n")
        text_widget.insert(tk.END, f"Mean RT: {phase_data['mean_rt']:.2f} ms\n")
        text_widget.insert(tk.END, f"RT Variability (SD): {phase_data['rt_std']:.2f} ms\n")
        text_widget.insert(tk.END, f"Anticipatory Responses: {phase_data['anticipatory_responses']}\n")
        text_widget.insert(tk.END, f"Multiple Responses: {phase_data['multiple_responses']}\n")
        text_widget.insert(tk.END, f"Hit Rate: {phase_data['hit_rate']:.2f}\n")
        text_widget.insert(tk.END, f"False Alarm Rate: {phase_data['false_alarm_rate']:.2f}\n")
        text_widget.insert(tk.END, f"d': {phase_data['d_prime']:.2f}\n")
        text_widget.insert(tk.END, f"Attention Comparison Score: {phase_data['acs_score']:.1f}\n")
        
        # Create plots
        self.create_phase_plots(phase_name, phase_data, plots_frame)
        
    def create_phase_plots(self, phase_name, phase_data, plots_frame):
        """Create plots for a specific phase"""
        # Clear any existing plots
        for widget in plots_frame.winfo_children():
            widget.destroy()
            
        # Create plots only if we have data
        if not phase_data["response_times"]:
            tk.Label(plots_frame, text="No response data available for this phase", 
                   font=("Arial", 12), bg="#f0f0f0").pack(pady=20)
            return
            
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        
        # Plot 1: Response time histogram
        ax1.hist(phase_data["response_times"], bins=15, color='skyblue', edgecolor='black')
        ax1.set_title('Response Time Distribution')
        ax1.set_xlabel('Response Time (ms)')
        ax1.set_ylabel('Frequency')
        
        # Plot 2: Error types pie chart
        labels = ['Correct Responses', 'Commission Errors', 'Omission Errors']
        sizes = [phase_data["correct_responses"], 
                 phase_data["commission_errors"], 
                 phase_data["omission_errors"]]
        colors = ['#4CAF50', '#F44336', '#2196F3']
        
        # Only create pie chart if we have data
        if sum(sizes) > 0:
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')
            ax2.set_title('Response Distribution')
        else:
            ax2.text(0.5, 0.5, "No response data", ha='center')
            ax2.axis('off')
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=plots_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def display_overall_summary(self, results):
        """Display overall summary of test results"""
        # Clear text widget
        self.summary_results.delete(1.0, tk.END)
        
        # Check if we have both phases
        has_infrequent = bool(results.get("infrequent_targets"))
        has_frequent = bool(results.get("frequent_targets"))
        
        if not has_infrequent and not has_frequent:
            self.summary_results.insert(tk.END, "No test data available")
            return
            
        # Calculate overall scores if both phases are available
        if has_infrequent and has_frequent:
            infrq = results["infrequent_targets"]
            freq = results["frequent_targets"]
            
            # Calculate overall ACS score
            overall_acs = (infrq["acs_score"] + freq["acs_score"]) / 2
            
            # Calculate ADHD likelihood based on ACS
            # (This is a simplified educational version, not for clinical use)
            if overall_acs < 40:
                adhd_likelihood = "High"
            elif overall_acs < 60:
                adhd_likelihood = "Moderate"
            else:
                adhd_likelihood = "Low"
                
            # Response time difference between phases (RT improvement)
            if infrq["mean_rt"] > 0 and freq["mean_rt"] > 0:
                rt_improvement = infrq["mean_rt"] - freq["mean_rt"]
                rt_improvement_pct = (rt_improvement / infrq["mean_rt"]) * 100
            else:
                rt_improvement = 0
                rt_improvement_pct = 0
                
            # Display summary
            self.summary_results.insert(tk.END, f"Overall Attention Comparison Score: {overall_acs:.1f}/100\n")
            self.summary_results.insert(tk.END, f"ADHD Indicator Likelihood: {adhd_likelihood}\n")
            self.summary_results.insert(tk.END, f"RT Improvement: {rt_improvement:.1f} ms ({rt_improvement_pct:.1f}%)\n")
            
            # Create summary plots
            self.create_summary_plots(results)
        else:
            # Only one phase available
            phase_name = "infrequent_targets" if has_infrequent else "frequent_targets"
            phase_data = results[phase_name]
            
            self.summary_results.insert(tk.END, f"Partial Test Results (only one phase completed)\n")
            self.summary_results.insert(tk.END, f"Attention Comparison Score: {phase_data['acs_score']:.1f}/100\n")
            
            # Create single phase summary
            for widget in self.summary_plots_frame.winfo_children():
                widget.destroy()
            
            tk.Label(self.summary_plots_frame, 
                   text="Complete both test phases for comprehensive analysis", 
                   font=("Arial", 12), bg="#f0f0f0").pack(pady=20)
            
    def create_summary_plots(self, results):
        """Create summary plots comparing both phases"""
        # Clear any existing plots
        for widget in self.summary_plots_frame.winfo_children():
            widget.destroy()
            
        # Extract data from both phases
        infrq = results["infrequent_targets"]
        freq = results["frequent_targets"]
        
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        
        # Plot 1: RT comparison
        labels = ['Infrequent\nTargets', 'Frequent\nTargets']
        rt_means = [infrq["mean_rt"], freq["mean_rt"]]
        rt_std = [infrq["rt_std"], freq["rt_std"]]
        
        x = range(len(labels))
        ax1.bar(x, rt_means, yerr=rt_std, capsize=10, color=['#2196F3', '#8BC34A'])
        ax1.set_ylabel('Response Time (ms)')
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)
        ax1.set_title('Response Time Comparison')
        
        # Plot 2: Performance Metrics Comparison
        metrics = ['Hit Rate', 'False Alarm Rate', 'd\'', 'ACS/100']
        infrq_values = [infrq["hit_rate"], infrq["false_alarm_rate"], infrq["d_prime"]/4, infrq["acs_score"]/100]
        freq_values = [freq["hit_rate"], freq["false_alarm_rate"], freq["d_prime"]/4, freq["acs_score"]/100]
        
        x = range(len(metrics))
        width = 0.35
        ax2.bar([i - width/2 for i in x], infrq_values, width, label='Infrequent Targets', color='#2196F3')
        ax2.bar([i + width/2 for i in x], freq_values, width, label='Frequent Targets', color='#8BC34A')
        
        ax2.set_ylabel('Score')
        ax2.set_xticks(x)
        ax2.set_xticklabels(metrics)
        ax2.set_title('Performance Metrics Comparison')
        ax2.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.summary_plots_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def save_report(self):
        """Save test reports"""
        try:
            # Import report generator here
            from reports.tova_report import TOVAReportGenerator
            
            # Create report generator and save reports
            report_gen = TOVAReportGenerator(self.tova_core.results, self.tova_core.participant_info)
            report_files = report_gen.save_reports()
            
            # Show message with saved files
            messagebox.showinfo("Report Saved", 
                              f"Report saved as:\n{report_files['png']}\n{report_files['csv']}\n{report_files['html']}")
        except ImportError:
            # Fallback if the report module is not available
            messagebox.showerror("Error", "Report generator module not found. Please implement the TOVA report module.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
        
    def reset_test(self):
        """Reset the application for a new test"""
        self.tova_core = TOVACore()  # Create new test core
        self.show_welcome_frame()