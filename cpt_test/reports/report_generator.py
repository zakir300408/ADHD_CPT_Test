"""
Reporting module for CPT Test
Handles generating and saving reports in various formats
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class ReportGenerator:
    """
    Generates reports from CPT test results in various formats
    (CSV, PNG plots, HTML)
    """
    def __init__(self, results, participant_info):
        """
        Initialize with test results and participant info
        """
        self.results = results
        self.participant_info = participant_info
        self.reports_dir = "e:/adhd/reports"
        
    def create_base_filename(self):
        """Generate a unique filename based on participant name and timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self.participant_info["name"].replace(" ", "_")
        return f"{self.reports_dir}/CPT_Report_{safe_name}_{timestamp}"
    
    def save_reports(self):
        """Save reports in all formats (CSV, PNG, HTML)"""
        # Create reports directory if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Generate base filename
        filename = self.create_base_filename()
        
        # Save plots to PNG file
        self.save_plots(filename)
        
        # Save results to CSV
        self.save_csv_results(filename)
        
        # Save response times to a separate CSV
        self.save_response_times(filename)
        
        # Create an HTML report
        self.create_html_report(filename)
        
        return {
            "png": f"{filename}.png",
            "csv": f"{filename}.csv",
            "response_times": f"{filename}_response_times.csv",
            "html": f"{filename}.html"
        }
        
    def generate_plots(self):
        """Generate plots for the report"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        
        # Plot 1: Response time histogram
        if self.results["response_times"]:
            ax1.hist(self.results["response_times"], bins=20, color='skyblue', edgecolor='black')
            ax1.set_title('Response Time Distribution')
            ax1.set_xlabel('Response Time (ms)')
            ax1.set_ylabel('Frequency')
        else:
            ax1.text(0.5, 0.5, "No response time data", ha='center')
        
        # Plot 2: Error types pie chart
        labels = ['Correct Responses', 'Commission Errors', 'Omission Errors']
        sizes = [self.results["correct_responses"], 
                 self.results["commission_errors"], 
                 self.results["omission_errors"]]
        colors = ['#4CAF50', '#F44336', '#2196F3']
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        ax2.set_title('Response Distribution')
        
        # Adjust layout
        plt.tight_layout()
        
        return fig
        
    def save_plots(self, filename_base):
        """Save plots to PNG file"""
        fig = self.generate_plots()
        fig.savefig(f"{filename_base}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        
    def save_csv_results(self, filename_base):
        """Save test results to CSV file"""
        results_df = pd.DataFrame({
            "Name": [self.participant_info["name"]],
            "Age": [self.participant_info["age"]],
            "Gender": [self.participant_info["gender"]],
            "Date": [self.participant_info["date"]],
            "Total_Stimuli": [self.results["total_stimuli"]],
            "Target_Stimuli": [self.results["target_stimuli"]],
            "Correct_Responses": [self.results["correct_responses"]],
            "Commission_Errors": [self.results["commission_errors"]],
            "Omission_Errors": [self.results["omission_errors"]],
            "Mean_RT": [self.results["mean_rt"]],
            "RT_STD": [self.results["rt_std"]],
            "Hit_Rate": [self.results["hit_rate"]],
            "False_Alarm_Rate": [self.results["false_alarm_rate"]],
            "D_Prime": [self.results["d_prime"]]
        })
        results_df.to_csv(f"{filename_base}.csv", index=False)
        
    def save_response_times(self, filename_base):
        """Save response times to a separate CSV file"""
        rt_df = pd.DataFrame({"response_times_ms": self.results["response_times"]})
        rt_df.to_csv(f"{filename_base}_response_times.csv", index=False)
        
    def create_html_report(self, filename_base):
        """Create an HTML report with test results and plots"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CPT Test Results - {self.participant_info["name"]}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                .report-header {{ margin-bottom: 20px; }}
                .results-table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                .results-table th, .results-table td {{ border: 1px solid #ddd; padding: 8px; }}
                .results-table th {{ padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #4CAF50; color: white; }}
                .plots {{ margin-top: 30px; }}
                .plot-img {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <div class="report-header">
                <h1>CPT Test Results</h1>
                <p><strong>Participant:</strong> {self.participant_info["name"]} ({self.participant_info["age"]} years, {self.participant_info["gender"]})</p>
                <p><strong>Date:</strong> {self.participant_info["date"]}</p>
            </div>
            
            <h2>Summary Results</h2>
            <table class="results-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Stimuli</td>
                    <td>{self.results["total_stimuli"]}</td>
                </tr>
                <tr>
                    <td>Target Stimuli (X)</td>
                    <td>{self.results["target_stimuli"]}</td>
                </tr>
                <tr>
                    <td>Correct Responses</td>
                    <td>{self.results["correct_responses"]}</td>
                </tr>
                <tr>
                    <td>Commission Errors</td>
                    <td>{self.results["commission_errors"]}</td>
                </tr>
                <tr>
                    <td>Omission Errors</td>
                    <td>{self.results["omission_errors"]}</td>
                </tr>
                <tr>
                    <td>Mean Response Time</td>
                    <td>{self.results["mean_rt"]:.2f} ms</td>
                </tr>
                <tr>
                    <td>Response Time SD</td>
                    <td>{self.results["rt_std"]:.2f} ms</td>
                </tr>
                <tr>
                    <td>Hit Rate</td>
                    <td>{self.results["hit_rate"]:.2f}</td>
                </tr>
                <tr>
                    <td>False Alarm Rate</td>
                    <td>{self.results["false_alarm_rate"]:.2f}</td>
                </tr>
                <tr>
                    <td>d'</td>
                    <td>{self.results["d_prime"]:.2f}</td>
                </tr>
            </table>
            
            <div class="plots">
                <h2>Visualization</h2>
                <img class="plot-img" src="{os.path.basename(filename_base)}.png" alt="Results plots">
            </div>
            
            <div class="interpretation">
                <h2>Interpretation</h2>
                <p>The Continuous Performance Task (CPT) is a measure of sustained attention and inhibitory control.</p>
                <ul>
                    <li><strong>Hit Rate:</strong> Proportion of correctly identified targets. Higher values indicate better sustained attention.</li>
                    <li><strong>False Alarm Rate:</strong> Proportion of incorrect responses to non-targets. Lower values indicate better inhibitory control.</li>
                    <li><strong>d':</strong> A measure of sensitivity that accounts for both hit rate and false alarm rate. Higher values indicate better ability to discriminate targets from non-targets.</li>
                    <li><strong>Response Time:</strong> Speed of correct responses. Consistent response times generally indicate sustained attention.</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        with open(f"{filename_base}.html", "w") as f:
            f.write(html_content)