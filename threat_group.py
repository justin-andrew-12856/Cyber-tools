import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from pyattck import Attck
import threading

class ThreatAnalyzerApp:
    """
    A GUI application to analyze threat groups using the pyattck library.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Threat Group Analyzer")
        self.root.geometry("800x600")

        # --- Top Frame for Input ---
        input_frame = tk.Frame(root, pady=10)
        input_frame.pack(fill=tk.X)

        self.label = tk.Label(input_frame, text="Enter Threat Group Name:")
        self.label.pack(side=tk.LEFT, padx=(10, 5))

        self.entry = tk.Entry(input_frame, width=40)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.entry.bind("<Return>", self.start_analysis_thread) # Allow pressing Enter

        self.analyze_button = tk.Button(input_frame, text="Analyze", command=self.start_analysis_thread)
        self.analyze_button.pack(side=tk.LEFT, padx=5)

        # --- Middle Frame for Output ---
        output_frame = tk.Frame(root)
        output_frame.pack(expand=True, fill=tk.BOTH, padx=10)

        self.text_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # --- Bottom Frame for Export ---
        export_frame = tk.Frame(root, pady=10)
        export_frame.pack(fill=tk.X)
        
        self.export_button = tk.Button(export_frame, text="Export to Text File", command=self.export_report)
        self.export_button.pack()

    def get_analysis_report(self, group_name):
        """
        Fetches and formats the analysis report for a given threat group.
        This function is designed to be run in a separate thread.
        """
        try:
            attack = Attck()
            report_lines = []
            group_found = False

            for actor in attack.enterprise.actors:
                if actor.name.lower() == group_name.lower():
                    group_found = True
                    report_lines.append("-" * 60)
                    report_lines.append(f"Analysis for Threat Group: {actor.name}")
                    report_lines.append("-" * 60)

                    if actor.malwares:
                        report_lines.append("\n[+] Malware Used:")
                        for malware in actor.malwares:
                            report_lines.append(f"\n  - Malware: {malware.name}")
                            if malware.techniques:
                                report_lines.append("    Associated Techniques:")
                                for tech in malware.techniques:
                                    report_lines.append(f"      - {tech.id}: {tech.name}")
                            else:
                                report_lines.append("    No associated techniques found.")
                    else:
                        report_lines.append("\n[-] No malware listed for this group.")

                    if actor.tools:
                        report_lines.append("\n[+] Tools Used:")
                        for tool in actor.tools:
                            report_lines.append(f"\n  - Tool: {tool.name}")
                            if tool.techniques:
                                report_lines.append("    Associated Techniques:")
                                for tech in tool.techniques:
                                    report_lines.append(f"      - {tech.id}: {tech.name}")
                            else:
                                report_lines.append("    No associated techniques found.")
                    else:
                        report_lines.append("\n[-] No tools listed for this group.")
                    break
            
            if not group_found:
                report = f"\n[!] Error: Threat group '{group_name}' not found."
            else:
                report = "\n".join(report_lines)
            
            # Schedule the UI update to run in the main thread
            self.root.after(0, self.update_text_area, report)

        except Exception as e:
            self.root.after(0, self.update_text_area, f"An error occurred: {e}")

    def start_analysis_thread(self, event=None):
        """
        Starts the analysis in a new thread to keep the GUI responsive.
        """
        group_name = self.entry.get()
        if not group_name:
            messagebox.showwarning("Input Error", "Please enter a threat group name.")
            return

        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.INSERT, f"Fetching data for '{group_name}', please wait...\nThis may take a moment.")
        
        # Disable buttons during analysis
        self.analyze_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.DISABLED)

        # Run the data fetching in a separate thread
        thread = threading.Thread(target=self.get_analysis_report, args=(group_name,))
        thread.daemon = True
        thread.start()

    def update_text_area(self, report):
        """
        Updates the text area with the report and re-enables buttons.
        This method is called from the main GUI thread.
        """
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, report)
        
        # Re-enable buttons
        self.analyze_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.NORMAL)

    def export_report(self):
        """
        Saves the content of the text area to a text file.
        """
        report_content = self.text_area.get("1.0", tk.END).strip()
        if not report_content or "Fetching data" in report_content:
            messagebox.showwarning("Export Error", "There is no report to export.")
            return

        # Open a save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Report As"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(report_content)
                messagebox.showinfo("Success", f"Report successfully saved to\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ThreatAnalyzerApp(root)
    root.mainloop()
