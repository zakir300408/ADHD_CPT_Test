#!/usr/bin/env python
"""
ADHD Test Battery Application

A GUI-based application for administering cognitive tests for ADHD assessment:
1. Continuous Performance Task (CPT) - measures sustained attention and impulsivity
2. Immediate and Delayed Memory Task (IMT/DMT) - measures attention, memory, and impulsivity
3. Test of Variables of Attention (TOVA) - measures attention, inhibition, and response time variability
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ensure the cpt_test package is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cpt_test.gui.cpt_gui import CPTGUI
from cpt_test.gui.imt_dmt_gui import IMTDMTGUI
from cpt_test.gui.tova_gui import TOVAGUI

class ADHDTestBattery:
    """
    Main application for ADHD test battery
    Provides a menu to select between different assessment tests
    """
    def __init__(self, root):
        self.root = root
        self.root.title("ADHD Test Battery")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main user interface with test selection menu"""
        # Create main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame, 
            text="ADHD Assessment Test Battery", 
            font=("Arial", 24, "bold"), 
            bg="#f0f0f0"
        ).pack(pady=30)
        
        tk.Label(
            main_frame,
            text="Select a test to administer:",
            font=("Arial", 14),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        # Test selection buttons
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # CPT Button
        cpt_button = tk.Button(
            button_frame,
            text="Continuous Performance Task (CPT)",
            command=self.launch_cpt,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=15,
            width=40
        )
        cpt_button.pack(pady=10)
        
        # IMT/DMT Button
        imtdmt_button = tk.Button(
            button_frame,
            text="Immediate/Delayed Memory Task (IMT/DMT)",
            command=self.launch_imtdmt,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=15,
            width=40
        )
        imtdmt_button.pack(pady=10)
        
        # TOVA Button
        tova_button = tk.Button(
            button_frame,
            text="Test of Variables of Attention (TOVA)",
            command=self.launch_tova,
            font=("Arial", 12),
            bg="#FF5722",
            fg="white",
            padx=20,
            pady=15,
            width=40
        )
        tova_button.pack(pady=10)
        
        # Test descriptions
        desc_frame = tk.Frame(main_frame, bg="#f0f0f0")
        desc_frame.pack(pady=20, fill=tk.X)
        
        tk.Label(
            desc_frame,
            text="CPT: Measures sustained attention and impulsivity by responding to target stimuli.",
            font=("Arial", 10),
            bg="#f0f0f0",
            justify=tk.LEFT,
            wraplength=600
        ).pack(anchor=tk.W, pady=5)
        
        tk.Label(
            desc_frame,
            text="IMT/DMT: Measures attention, memory, and impulsivity by identifying matching sequences.",
            font=("Arial", 10),
            bg="#f0f0f0",
            justify=tk.LEFT,
            wraplength=600
        ).pack(anchor=tk.W, pady=5)
        
        tk.Label(
            desc_frame,
            text="TOVA: Measures attention, inhibition, and response time variability across varying target frequencies.",
            font=("Arial", 10),
            bg="#f0f0f0",
            justify=tk.LEFT,
            wraplength=600
        ).pack(anchor=tk.W, pady=5)
        
        # Exit button
        tk.Button(
            main_frame,
            text="Exit",
            command=self.root.destroy,
            font=("Arial", 12),
            bg="#F44336",
            fg="white",
            padx=20,
            pady=10
        ).pack(side=tk.BOTTOM, pady=20)
    
    def launch_cpt(self):
        """Launch the CPT test in a new window"""
        test_window = tk.Toplevel(self.root)
        test_window.geometry("800x600")
        CPTGUI(test_window)
    
    def launch_imtdmt(self):
        """Launch the IMT/DMT test in a new window"""
        test_window = tk.Toplevel(self.root)
        test_window.geometry("800x600")
        IMTDMTGUI(test_window)
        
    def launch_tova(self):
        """Launch the TOVA test in a new window"""
        test_window = tk.Toplevel(self.root)
        test_window.geometry("800x600")
        TOVAGUI(test_window)

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = ADHDTestBattery(root)
    root.mainloop()

if __name__ == "__main__":
    main()