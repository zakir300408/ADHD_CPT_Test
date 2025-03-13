"""
TOVA Report Generator
Handles generating and saving reports for the TOVA test
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class TOVAReportGenerator:
    """
    Generates reports from TOVA test results in various formats
    (CSV, PNG plots, HTML)
    """
    def __init__(self, results, participant_info):
        """
        Initialize with test results and participant info
        
        Args:
            results: Dictionary containing infrequent_targets and frequent_targets phases
            participant_info: Dictionary containing participant information
        """
        self.results = results
        self.participant_info = participant_info
        self.reports_dir = "e:/adhd/reports"
        
    def create_base_filename(self):
        """Generate a unique filename based on participant name and timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self.participant_info["name"].replace(" ", "_")
        return f"{self.reports_dir}/TOVA_Report_{safe_name}_{timestamp}"
    
    def save_reports(self):
        """Save reports in all formats (CSV, PNG, HTML)"""
        # Create reports directory if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Generate base filename
        filename = self.create_base_filename()
        
        # Save various report files
        png_file = self.save_plots(filename)
        csv_file = self.save_csv_results(filename)
        rt_files = self.save_response_times(filename)
        html_file = self.create_html_report(filename)
        
        files = {
            "png": png_file,
            "csv": csv_file,
            "response_times": rt_files,
            "html": html_file
        }
        
        return files
        
    def generate_plots(self):
        """Generate plots for the report, comparing infrequent and frequent target phases"""
        # Check what data is available
        has_infreq = bool(self.results.get("infrequent_targets"))
        has_freq = bool(self.results.get("frequent_targets"))
        
        # Create a figure with multiple subplots
        if has_infreq and has_freq:
            # Full test data - create comprehensive comparison plots
            fig = plt.figure(figsize=(12, 10), dpi=100)
            
            # RT Histogram - Top Left
            ax1 = plt.subplot2grid((2, 2), (0, 0))
            
            # Combine response time data for histogram
            infreq_rt = self.results["infrequent_targets"].get("response_times", [])
            freq_rt = self.results["frequent_targets"].get("response_times", [])
            
            if infreq_rt:
                ax1.hist(infreq_rt, bins=15, alpha=0.6, label="Infrequent Targets", color='#2196F3')
            if freq_rt:
                ax1.hist(freq_rt, bins=15, alpha=0.6, label="Frequent Targets", color='#8BC34A')
                
            ax1.set_title("Response Time Distribution")
            ax1.set_xlabel("Response Time (ms)")
            ax1.set_ylabel("Frequency")
            ax1.legend()
            
            # Error Rates - Top Right
            ax2 = plt.subplot2grid((2, 2), (0, 1))
            
            infreq_data = self.results["infrequent_targets"]
            freq_data = self.results["frequent_targets"]
            
            labels = ['Commission\nErrors', 'Omission\nErrors']
            infreq_values = [infreq_data.get("false_alarm_rate", 0), infreq_data.get("omission_rate", 0)]
            freq_values = [freq_data.get("false_alarm_rate", 0), freq_data.get("omission_rate", 0)]
            
            x = np.arange(len(labels))
            width = 0.35
            
            ax2.bar(x - width/2, infreq_values, width, label='Infrequent Targets', color='#2196F3')
            ax2.bar(x + width/2, freq_values, width, label='Frequent Targets', color='#8BC34A')
            
            ax2.set_ylabel('Rate')
            ax2.set_title('Error Rates Comparison')
            ax2.set_xticks(x)
            ax2.set_xticklabels(labels)
            ax2.legend()
            
            # Performance Metrics - Bottom Left
            ax3 = plt.subplot2grid((2, 2), (1, 0))
            
            metrics = ['Hit Rate', 'd\'', 'ACS/100']
            infreq_metrics = [infreq_data.get("hit_rate", 0), 
                            infreq_data.get("d_prime", 0)/4, 
                            infreq_data.get("acs_score", 0)/100]
            freq_metrics = [freq_data.get("hit_rate", 0), 
                          freq_data.get("d_prime", 0)/4, 
                          freq_data.get("acs_score", 0)/100]
            
            x = np.arange(len(metrics))
            
            ax3.bar(x - width/2, infreq_metrics, width, label='Infrequent Targets', color='#2196F3')
            ax3.bar(x + width/2, freq_metrics, width, label='Frequent Targets', color='#8BC34A')
            
            ax3.set_ylabel('Score')
            ax3.set_title('Performance Metrics')
            ax3.set_xticks(x)
            ax3.set_xticklabels(metrics)
            ax3.set_ylim(0, 1.2)
            ax3.legend()
            
            # RT Comparison - Bottom Right
            ax4 = plt.subplot2grid((2, 2), (1, 1))
            
            rt_labels = ['Mean RT', 'RT Variability']
            infreq_rt_data = [infreq_data.get("mean_rt", 0), infreq_data.get("rt_std", 0)]
            freq_rt_data = [freq_data.get("mean_rt", 0), freq_data.get("rt_std", 0)]
            
            x = np.arange(len(rt_labels))
            
            ax4.bar(x - width/2, infreq_rt_data, width, label='Infrequent Targets', color='#2196F3')
            ax4.bar(x + width/2, freq_rt_data, width, label='Frequent Targets', color='#8BC34A')
            
            ax4.set_ylabel('Milliseconds')
            ax4.set_title('Response Time Metrics')
            ax4.set_xticks(x)
            ax4.set_xticklabels(rt_labels)
            ax4.legend()
            
        elif has_infreq:
            # Only infrequent targets data
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=100)
            
            # RT Histogram
            infreq_rt = self.results["infrequent_targets"].get("response_times", [])
            if infreq_rt:
                ax1.hist(infreq_rt, bins=15, alpha=0.6, color='#2196F3')
                ax1.set_title("Response Time Distribution")
                ax1.set_xlabel("Response Time (ms)")
                ax1.set_ylabel("Frequency")
            
            # Performance pie chart
            infreq_data = self.results["infrequent_targets"]
            labels = ['Correct Responses', 'Commission Errors', 'Omission Errors']
            sizes = [
                infreq_data.get("correct_responses", 0),
                infreq_data.get("commission_errors", 0),
                infreq_data.get("omission_errors", 0)
            ]
            colors = ['#4CAF50', '#F44336', '#2196F3']
            
            if sum(sizes) > 0:
                ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax2.axis('equal')
                ax2.set_title('Infrequent Targets - Response Distribution')
            
        elif has_freq:
            # Only frequent targets data
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=100)
            
            # RT Histogram
            freq_rt = self.results["frequent_targets"].get("response_times", [])
            if freq_rt:
                ax1.hist(freq_rt, bins=15, alpha=0.6, color='#8BC34A')
                ax1.set_title("Response Time Distribution")
                ax1.set_xlabel("Response Time (ms)")
                ax1.set_ylabel("Frequency")
            
            # Performance pie chart
            freq_data = self.results["frequent_targets"]
            labels = ['Correct Responses', 'Commission Errors', 'Omission Errors']
            sizes = [
                freq_data.get("correct_responses", 0),
                freq_data.get("commission_errors", 0),
                freq_data.get("omission_errors", 0)
            ]
            colors = ['#4CAF50', '#F44336', '#2196F3']
            
            if sum(sizes) > 0:
                ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax2.axis('equal')
                ax2.set_title('Frequent Targets - Response Distribution')
        else:
            # No data available
            fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=100)
            ax.text(0.5, 0.5, "No test data available", ha='center', va='center', fontsize=14)
            ax.axis('off')
            
        fig.suptitle(f"TOVA Test Results - {self.participant_info['name']}", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave room for suptitle
        
        return fig
        
    def save_plots(self, filename_base):
        """Save plots to PNG file"""
        fig = self.generate_plots()
        png_filename = f"{filename_base}.png"
        fig.savefig(png_filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return png_filename
        
    def save_csv_results(self, filename_base):
        """Save test results to CSV file"""
        # Create a DataFrame with both phases
        infreq = self.results.get("infrequent_targets", {})
        freq = self.results.get("frequent_targets", {})
        
        # Create data dictionary
        data = {
            "Name": self.participant_info["name"],
            "Age": self.participant_info["age"],
            "Gender": self.participant_info["gender"],
            "Date": self.participant_info["date"],
            "Test_Type": "TOVA"
        }
        
        # Add data for both phases
        for phase_name, phase_data in [("InfrequentTargets", infreq), ("FrequentTargets", freq)]:
            if phase_data:
                for key, value in phase_data.items():
                    if key != "response_times":  # Skip response_times array
                        data[f"{phase_name}_{key}"] = value
        
        # Calculate overall metrics if both phases are available
        if infreq and freq:
            # Overall ACS score
            data["Overall_ACS_Score"] = (infreq.get("acs_score", 0) + freq.get("acs_score", 0)) / 2
            
            # RT improvement
            if infreq.get("mean_rt", 0) > 0 and freq.get("mean_rt", 0) > 0:
                rt_improvement = infreq["mean_rt"] - freq["mean_rt"]
                rt_improvement_pct = (rt_improvement / infreq["mean_rt"]) * 100 if infreq["mean_rt"] > 0 else 0
                
                data["RT_Improvement_ms"] = rt_improvement
                data["RT_Improvement_percent"] = rt_improvement_pct
            
        # Save to CSV
        df = pd.DataFrame([data])
        csv_filename = f"{filename_base}.csv"
        df.to_csv(csv_filename, index=False)
        
        return csv_filename
        
    def save_response_times(self, filename_base):
        """Save response times to separate CSV files for each phase"""
        rt_files = []
        
        # Save infrequent targets response times if available
        if (self.results.get("infrequent_targets") 
                and self.results["infrequent_targets"].get("response_times")):
            rt_infreq_file = f"{filename_base}_infrequent_rt.csv"
            rt_df = pd.DataFrame({
                "infrequent_target_response_times_ms": 
                    self.results["infrequent_targets"]["response_times"]
            })
            rt_df.to_csv(rt_infreq_file, index=False)
            rt_files.append(rt_infreq_file)
            
        # Save frequent targets response times if available
        if (self.results.get("frequent_targets") 
                and self.results["frequent_targets"].get("response_times")):
            rt_freq_file = f"{filename_base}_frequent_rt.csv"
            rt_df = pd.DataFrame({
                "frequent_target_response_times_ms": 
                    self.results["frequent_targets"]["response_times"]
            })
            rt_df.to_csv(rt_freq_file, index=False)
            rt_files.append(rt_freq_file)
            
        return rt_files
        
    def create_html_report(self, filename_base):
        """Create an HTML report with test results and plots"""
        html_file = f"{filename_base}.html"
        
        has_infreq = bool(self.results.get("infrequent_targets"))
        has_freq = bool(self.results.get("frequent_targets"))
        
        # Calculate overall metrics if both phases are available
        overall_html = ""
        if has_infreq and has_freq:
            infreq = self.results["infrequent_targets"]
            freq = self.results["frequent_targets"]
            
            # Calculate overall ACS score
            overall_acs = (infreq.get("acs_score", 0) + freq.get("acs_score", 0)) / 2
            
            # ADHD likelihood based on ACS (simplified educational version)
            if overall_acs < 40:
                adhd_likelihood = "High"
                likelihood_color = "#F44336"
            elif overall_acs < 60:
                adhd_likelihood = "Moderate"
                likelihood_color = "#FF9800"
            else:
                adhd_likelihood = "Low"
                likelihood_color = "#4CAF50"
            
            # RT improvement
            if infreq.get("mean_rt", 0) > 0 and freq.get("mean_rt", 0) > 0:
                rt_improvement = infreq["mean_rt"] - freq["mean_rt"]
                rt_improvement_pct = (rt_improvement / infreq["mean_rt"]) * 100 if infreq["mean_rt"] > 0 else 0
            else:
                rt_improvement = 0
                rt_improvement_pct = 0
            
            overall_html = f"""
            <div class="summary-section">
                <h2>Overall Assessment</h2>
                <table class="results-table summary-table">
                    <tr>
                        <th>Overall Attention Comparison Score</th>
                        <td>{overall_acs:.1f}/100</td>
                    </tr>
                    <tr>
                        <th>ADHD Indicator Likelihood</th>
                        <td><span style="color:{likelihood_color}; font-weight:bold;">{adhd_likelihood}</span></td>
                    </tr>
                    <tr>
                        <th>RT Improvement</th>
                        <td>{rt_improvement:.1f} ms ({rt_improvement_pct:.1f}%)</td>
                    </tr>
                </table>
            </div>
            """
        
        # Generate HTML content for each available phase
        phases_html = ""
        if has_infreq:
            phases_html += self._generate_phase_html("infrequent_targets", 
                                                  "Infrequent Targets (First Half)",
                                                  self.results["infrequent_targets"])
        
        if has_freq:
            phases_html += self._generate_phase_html("frequent_targets",
                                                  "Frequent Targets (Second Half)",
                                                  self.results["frequent_targets"])
            
        # Create the complete HTML document
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TOVA Test Results - {self.participant_info["name"]}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 40px;
                }}
                h1, h2 {{
                    color: #205493;
                }}
                .report-header {{
                    margin-bottom: 30px;
                    border-bottom: 2px solid #ddd;
                    padding-bottom: 10px;
                }}
                .participant-info {{
                    margin-bottom: 20px;
                }}
                .summary-section {{
                    margin-top: 30px;
                    margin-bottom: 30px;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-radius: 5px;
                }}
                .summary-table {{
                    width: 50%;
                    margin: 0 auto;
                }}
                .results-table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                    margin-bottom: 30px;
                }}
                .results-table th, .results-table td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                .results-table th {{
                    background-color: #205493;
                    color: white;
                }}
                .results-table tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .phase-section {{
                    margin-top: 40px;
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                }}
                .plots {{
                    margin-top: 30px;
                    text-align: center;
                }}
                .plot-img {{
                    max-width: 100%;
                    height: auto;
                    margin-top: 20px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                .interpretation {{
                    margin-top: 40px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-left: 5px solid #205493;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #666;
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="report-header">
                <h1>TOVA Test Results</h1>
                <div class="participant-info">
                    <p><strong>Participant:</strong> {self.participant_info["name"]} ({self.participant_info["age"]} years, {self.participant_info["gender"]})</p>
                    <p><strong>Test Date:</strong> {self.participant_info["date"]}</p>
                </div>
            </div>
            
            <div class="plots">
                <h2>Test Results Visualization</h2>
                <img class="plot-img" src="{os.path.basename(filename_base)}.png" alt="TOVA Test Results Plots">
            </div>
            
            {overall_html}
            
            {phases_html}
            
            <div class="interpretation">
                <h2>Interpretation Guide</h2>
                <p>The Test of Variables of Attention (TOVA) is a continuous performance test that measures attention and impulse control. It consists of two phases:</p>
                <ul>
                    <li><strong>Infrequent Targets:</strong> The first half of the test, where targets appear rarely (22.5% of the time). This primarily measures sustained attention.</li>
                    <li><strong>Frequent Targets:</strong> The second half of the test, where targets appear frequently (77.5% of the time). This primarily measures inhibitory control and impulsivity.</li>
                </ul>
                
                <p><strong>Key Metrics:</strong></p>
                <ul>
                    <li><strong>Omission Errors:</strong> Failing to respond to targets, indicating inattention.</li>
                    <li><strong>Commission Errors:</strong> Incorrectly responding to non-targets, indicating impulsivity.</li>
                    <li><strong>Response Time:</strong> Speed of response to targets, which may be slower in ADHD.</li>
                    <li><strong>Response Time Variability:</strong> Inconsistency in response times, often higher in ADHD.</li>
                    <li><strong>d':</strong> A measure of discriminability between targets and non-targets.</li>
                    <li><strong>ACS (Attention Comparison Score):</strong> A composite score ranging from 0-100, with lower scores indicating greater attention difficulties.</li>
                </ul>
                
                <p><strong>Note:</strong> This implementation of the TOVA is for educational and demonstration purposes only and should not be used for clinical diagnosis.</p>
            </div>
            
            <div class="footer">
                <p>Report generated on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}</p>
                <p>ADHD Test Battery</p>
            </div>
        </body>
        </html>
        """
        
        # Write the HTML file
        with open(html_file, "w") as f:
            f.write(html_content)
            
        return html_file
    
    def _generate_phase_html(self, phase_id, phase_name, phase_data):
        """Generate HTML section for a specific test phase"""
        if not phase_data:
            return ""
            
        # Format metrics for display
        metrics_html = ""
        
        # Basic metrics
        metrics = [
            ("Total Stimuli", phase_data.get("total_stimuli", 0)),
            ("Target Stimuli", phase_data.get("target_stimuli", 0)),
            ("Non-Target Stimuli", phase_data.get("non_target_stimuli", 0)),
            ("Correct Responses", phase_data.get("correct_responses", 0)),
            ("Commission Errors", phase_data.get("commission_errors", 0)),
            ("Omission Errors", phase_data.get("omission_errors", 0)),
            ("Anticipatory Responses", phase_data.get("anticipatory_responses", 0)),
            ("Multiple Responses", phase_data.get("multiple_responses", 0)),
        ]
        
        for label, value in metrics:
            metrics_html += f"""
            <tr>
                <th>{label}</th>
                <td>{value}</td>
            </tr>
            """
            
        # Performance metrics with formatting
        perf_metrics = [
            ("Mean Response Time", f"{phase_data.get('mean_rt', 0):.1f} ms"),
            ("Response Time Variability (SD)", f"{phase_data.get('rt_std', 0):.1f} ms"),
            ("Hit Rate", f"{phase_data.get('hit_rate', 0):.3f}"),
            ("False Alarm Rate", f"{phase_data.get('false_alarm_rate', 0):.3f}"),
            ("Omission Rate", f"{phase_data.get('omission_rate', 0):.3f}"),
            ("d'", f"{phase_data.get('d_prime', 0):.2f}"),
            ("Attention Comparison Score (ACS)", f"{phase_data.get('acs_score', 0):.1f}/100"),
        ]
        
        for label, value in perf_metrics:
            metrics_html += f"""
            <tr>
                <th>{label}</th>
                <td>{value}</td>
            </tr>
            """
            
        # Create the phase HTML section
        html = f"""
        <div class="phase-section">
            <h2>{phase_name}</h2>
            <table class="results-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                {metrics_html}
            </table>
        </div>
        """
        
        return html