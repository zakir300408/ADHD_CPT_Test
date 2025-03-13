"""
IMT/DMT Report Generator
Handles generating and saving reports for the IMT/DMT test
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class IMTDMTReportGenerator:
    """
    Generates reports from IMT/DMT test results in various formats
    (CSV, PNG plots, HTML)
    """
    def __init__(self, results, participant_info):
        """
        Initialize with test results and participant info
        
        Args:
            results: Dictionary containing IMT and DMT phase results
            participant_info: Dictionary containing participant information
        """
        self.results = results
        self.participant_info = participant_info
        self.reports_dir = "e:/adhd/reports"
        
    def create_base_filename(self):
        """Generate a unique filename based on participant name and timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self.participant_info["name"].replace(" ", "_")
        return f"{self.reports_dir}/IMTDMT_Report_{safe_name}_{timestamp}"
    
    def save_reports(self):
        """Save reports in all formats (CSV, PNG, HTML)"""
        # Create reports directory if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Generate base filename
        filename = self.create_base_filename()
        
        # Save plots to PNG file
        self.save_plots(filename)
        
        # Save results to CSV
        csv_file = self.save_csv_results(filename)
        
        # Save response times to separate CSV files
        rt_files = self.save_response_times(filename)
        
        # Create an HTML report
        self.create_html_report(filename)
        
        files = {
            "png": f"{filename}.png",
            "csv": csv_file,
            "response_times": rt_files,
            "html": f"{filename}.html"
        }
        
        return files
        
    def generate_plots(self):
        """Generate plots for the report, with IMT and DMT results side by side"""
        has_imt = bool(self.results["IMT"])
        has_dmt = bool(self.results["DMT"])
        
        # Determine layout based on available data
        if has_imt and has_dmt:
            # If we have both, create 2x2 grid of plots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=100)
            
            # Top row: IMT plots
            self._plot_response_time(ax1, "IMT", self.results["IMT"])
            self._plot_pie_chart(ax2, "IMT", self.results["IMT"])
            
            # Bottom row: DMT plots
            self._plot_response_time(ax3, "DMT", self.results["DMT"])
            self._plot_pie_chart(ax4, "DMT", self.results["DMT"])
            
        elif has_imt:
            # Only IMT data available
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=100)
            self._plot_response_time(ax1, "IMT", self.results["IMT"])
            self._plot_pie_chart(ax2, "IMT", self.results["IMT"])
            
        elif has_dmt:
            # Only DMT data available
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=100)
            self._plot_response_time(ax1, "DMT", self.results["DMT"])
            self._plot_pie_chart(ax2, "DMT", self.results["DMT"])
            
        else:
            # No data available
            fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=100)
            ax.text(0.5, 0.5, "No test data available", ha='center', va='center', fontsize=14)
            ax.axis('off')
        
        fig.suptitle(f"IMT/DMT Test Results - {self.participant_info['name']}", fontsize=16)
        plt.tight_layout()
        
        return fig
    
    def _plot_response_time(self, ax, phase_name, phase_data):
        """Helper method to plot response time distribution"""
        if not phase_data or not phase_data.get("response_times"):
            ax.text(0.5, 0.5, f"No {phase_name} response time data", ha='center')
            ax.set_title(f'{phase_name} Response Time Distribution')
            return
        
        ax.hist(phase_data["response_times"], bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f'{phase_name} Response Time Distribution')
        ax.set_xlabel('Response Time (ms)')
        ax.set_ylabel('Frequency')
        
    def _plot_pie_chart(self, ax, phase_name, phase_data):
        """Helper method to plot response distribution pie chart"""
        if not phase_data or not phase_data.get("correct_responses", 0) + \
                          phase_data.get("false_alarms", 0) + \
                          phase_data.get("misses", 0) == 0:
            ax.text(0.5, 0.5, f"No {phase_name} response data", ha='center')
            ax.set_title(f'{phase_name} Response Distribution')
            return
        
        labels = ['Correct Responses', 'False Alarms', 'Misses']
        sizes = [phase_data.get("correct_responses", 0), 
                 phase_data.get("false_alarms", 0), 
                 phase_data.get("misses", 0)]
        colors = ['#4CAF50', '#F44336', '#2196F3']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title(f'{phase_name} Response Distribution')
        
    def save_plots(self, filename_base):
        """Save plots to PNG file"""
        fig = self.generate_plots()
        fig.savefig(f"{filename_base}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        
    def save_csv_results(self, filename_base):
        """Save test results to CSV file"""
        # Create a DataFrame with both IMT and DMT results
        imt_results = self.results["IMT"] if self.results["IMT"] else {}
        dmt_results = self.results["DMT"] if self.results["DMT"] else {}
        
        # Create DataFrames for each phase
        data = {
            "Name": self.participant_info["name"],
            "Age": self.participant_info["age"],
            "Gender": self.participant_info["gender"],
            "Date": self.participant_info["date"],
            "Test_Type": "IMT/DMT"
        }
        
        # Add IMT and DMT columns with phase prefix
        for phase_name, phase_data in [("IMT", imt_results), ("DMT", dmt_results)]:
            if phase_data:
                for key, value in phase_data.items():
                    if key != "response_times":  # Skip response_times array
                        data[f"{phase_name}_{key}"] = value
            
        # Save to CSV
        df = pd.DataFrame([data])
        csv_filename = f"{filename_base}.csv"
        df.to_csv(csv_filename, index=False)
        
        return csv_filename
        
    def save_response_times(self, filename_base):
        """Save response times to separate CSV files for each phase"""
        rt_files = []
        
        # Save IMT response times if available
        if self.results["IMT"] and self.results["IMT"].get("response_times"):
            rt_imt_file = f"{filename_base}_imt_response_times.csv"
            rt_df = pd.DataFrame({"imt_response_times_ms": self.results["IMT"]["response_times"]})
            rt_df.to_csv(rt_imt_file, index=False)
            rt_files.append(rt_imt_file)
            
        # Save DMT response times if available
        if self.results["DMT"] and self.results["DMT"].get("response_times"):
            rt_dmt_file = f"{filename_base}_dmt_response_times.csv"
            rt_df = pd.DataFrame({"dmt_response_times_ms": self.results["DMT"]["response_times"]})
            rt_df.to_csv(rt_dmt_file, index=False)
            rt_files.append(rt_dmt_file)
            
        return rt_files
        
    def create_html_report(self, filename_base):
        """Create an HTML report with test results and plots"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>IMT/DMT Test Results - {self.participant_info["name"]}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2 {{ color: #333; }}
                .report-header {{ margin-bottom: 20px; }}
                .results-table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                .results-table th, .results-table td {{ border: 1px solid #ddd; padding: 8px; }}
                .results-table th {{ padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #4CAF50; color: white; }}
                .plots {{ margin-top: 30px; }}
                .plot-img {{ max-width: 100%; height: auto; }}
                .phase-section {{ margin-top: 40px; }}
            </style>
        </head>
        <body>
            <div class="report-header">
                <h1>Immediate and Delayed Memory Task (IMT/DMT) Results</h1>
                <p><strong>Participant:</strong> {self.participant_info["name"]} ({self.participant_info["age"]} years, {self.participant_info["gender"]})</p>
                <p><strong>Date:</strong> {self.participant_info["date"]}</p>
            </div>
            
            <div class="plots">
                <h2>Results Visualization</h2>
                <img class="plot-img" src="{os.path.basename(filename_base)}.png" alt="Results plots">
            </div>
        """
        
        # Add IMT results if available
        if self.results["IMT"]:
            imt_data = self.results["IMT"]
            html_content += self._generate_phase_html("IMT", imt_data)
            
        # Add DMT results if available
        if self.results["DMT"]:
            dmt_data = self.results["DMT"]
            html_content += self._generate_phase_html("DMT", dmt_data)
            
        # Add interpretation section
        html_content += """
            <div class="interpretation">
                <h2>Interpretation</h2>
                <p>The Immediate and Delayed Memory Task (IMT/DMT) is a measure of attention, memory, and impulsivity.</p>
                <ul>
                    <li><strong>Hit Rate:</strong> Proportion of correctly identified targets. Higher values indicate better sustained attention and working memory.</li>
                    <li><strong>False Alarm Rate:</strong> Proportion of incorrect responses to non-targets. Lower values indicate better inhibitory control.</li>
                    <li><strong>d':</strong> A measure of sensitivity that accounts for both hit rate and false alarm rate. Higher values indicate better ability to discriminate targets from non-targets.</li>
                    <li><strong>Response Time:</strong> Speed of correct responses. Faster response times generally indicate better processing speed.</li>
                </ul>
                <p>The DMT phase is typically more challenging than the IMT phase as it requires maintaining information in working memory for a longer period.</p>
            </div>
        </body>
        </html>
        """
        
        with open(f"{filename_base}.html", "w") as f:
            f.write(html_content)
            
    def _generate_phase_html(self, phase_name, phase_data):
        """Generate HTML content for a specific test phase"""
        html = f"""
        <div class="phase-section">
            <h2>{phase_name} Results</h2>
            <table class="results-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Stimuli</td>
                    <td>{phase_data["total_stimuli"]}</td>
                </tr>
                <tr>
                    <td>Target Stimuli</td>
                    <td>{phase_data["target_stimuli"]}</td>
                </tr>
                <tr>
                    <td>Correct Responses</td>
                    <td>{phase_data["correct_responses"]}</td>
                </tr>
                <tr>
                    <td>False Alarms</td>
                    <td>{phase_data["false_alarms"]}</td>
                </tr>
                <tr>
                    <td>Misses</td>
                    <td>{phase_data["misses"]}</td>
                </tr>
                <tr>
                    <td>Mean Response Time</td>
                    <td>{phase_data["mean_rt"]:.2f} ms</td>
                </tr>
                <tr>
                    <td>Response Time SD</td>
                    <td>{phase_data["rt_std"]:.2f} ms</td>
                </tr>
                <tr>
                    <td>Hit Rate</td>
                    <td>{phase_data["hit_rate"]:.2f}</td>
                </tr>
                <tr>
                    <td>False Alarm Rate</td>
                    <td>{phase_data["false_alarm_rate"]:.2f}</td>
                </tr>
                <tr>
                    <td>d'</td>
                    <td>{phase_data["d_prime"]:.2f}</td>
                </tr>
            </table>
        </div>
        """
        return html