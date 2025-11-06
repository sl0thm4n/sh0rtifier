"""
sh0rtifier - GUI Interface

Simple cross-platform GUI using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from typing import Optional

from core import (
    convert_to_shorts,
    get_video_info,
    ConversionOptions,
    ValidationError,
    ProcessingError,
    VideoInfo
)


class ShortsConverterGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("sh0rtifier")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # State
        self.input_file: Optional[Path] = None
        self.output_folder: Optional[Path] = None
        self.video_info: Optional[VideoInfo] = None
        self.is_processing = False
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup UI components"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="sh0rtifier",
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Convert 16:9 videos to 9:16 Shorts (max 60s)",
            font=("Arial", 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # === File Selection Section ===
        file_section = ttk.LabelFrame(main_frame, text="Step 1: Select Video", padding="15")
        file_section.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.file_path_var = tk.StringVar(value="No file selected")
        file_path_label = ttk.Label(file_section, textvariable=self.file_path_var, wraplength=500)
        file_path_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.video_info_var = tk.StringVar(value="")
        video_info_label = ttk.Label(file_section, textvariable=self.video_info_var, foreground="gray")
        video_info_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        select_file_btn = ttk.Button(
            file_section,
            text="📁 Browse Video File",
            command=self.select_input_file,
            width=30
        )
        select_file_btn.grid(row=2, column=0, pady=(0, 0))
        
        # === Output Folder Section ===
        output_section = ttk.LabelFrame(main_frame, text="Step 2: Select Output Folder", padding="15")
        output_section.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.output_path_var = tk.StringVar(value="Same as input file")
        output_path_label = ttk.Label(output_section, textvariable=self.output_path_var, wraplength=500)
        output_path_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        select_output_btn = ttk.Button(
            output_section,
            text="📁 Browse Output Folder",
            command=self.select_output_folder,
            width=30
        )
        select_output_btn.grid(row=1, column=0)
        
        # === Options Section ===
        self.options_frame = ttk.LabelFrame(main_frame, text="Step 3: Conversion Options", padding="15")
        self.options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # This will be populated dynamically based on video duration
        self.options_widgets = {}
        self.create_default_options_ui()
        
        # === Progress Section ===
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=600
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, pady=(5, 0))
        
        # === Convert Button ===
        self.convert_btn = ttk.Button(
            main_frame,
            text="🎬 Convert to Shorts",
            command=self.start_conversion,
            state=tk.DISABLED,
            width=30
        )
        self.convert_btn.grid(row=6, column=0, columnspan=2)
        
    def create_default_options_ui(self):
        """Create default options UI (when no video selected)"""
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        info_label = ttk.Label(
            self.options_frame,
            text="Select a video file to see conversion options",
            foreground="gray"
        )
        info_label.pack()
    
    def create_options_ui_for_short_video(self):
        """Create options UI for videos under 60 seconds"""
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        info_label = ttk.Label(
            self.options_frame,
            text="✓ Video is under 60 seconds - will convert as-is with optimal settings",
            foreground="green"
        )
        info_label.pack()
    
    def create_options_ui_for_long_video(self):
        """Create options UI for videos over 60 seconds"""
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.options_widgets = {}
        
        # Warning
        warning_label = ttk.Label(
            self.options_frame,
            text=f"⚠️  Video is {self.video_info.duration:.1f}s (over 60s limit)",
            foreground="orange",
            font=("Arial", 10, "bold")
        )
        warning_label.pack(pady=(0, 15))
        
        # Mode selection
        mode_frame = ttk.Frame(self.options_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.mode_var = tk.StringVar(value="speed")
        
        ttk.Radiobutton(
            mode_frame,
            text="Speed Adjustment (Recommended)",
            variable=self.mode_var,
            value="speed",
            command=self.update_options_visibility
        ).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(
            mode_frame,
            text="Select Specific Segment",
            variable=self.mode_var,
            value="segment",
            command=self.update_options_visibility
        ).pack(anchor=tk.W)
        
        # === Speed Options ===
        self.speed_frame = ttk.Frame(self.options_frame)
        self.speed_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(self.speed_frame, text="Speed:").grid(row=0, column=0, sticky=tk.W, padx=(20, 10))
        
        self.speed_var = tk.DoubleVar(value=self.video_info.duration / 59.0)
        speed_scale = ttk.Scale(
            self.speed_frame,
            from_=1.0,
            to=4.0,
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        speed_scale.grid(row=0, column=1, padx=(0, 10))
        
        self.speed_label_var = tk.StringVar()
        self.update_speed_label()
        speed_label = ttk.Label(self.speed_frame, textvariable=self.speed_label_var)
        speed_label.grid(row=0, column=2)
        
        speed_scale.config(command=lambda _: self.update_speed_label())
        
        # Suggested speed button
        suggested_speed = self.video_info.duration / 59.0
        ttk.Button(
            self.speed_frame,
            text=f"Use Suggested ({suggested_speed:.2f}x)",
            command=lambda: self.speed_var.set(suggested_speed)
        ).grid(row=1, column=1, pady=(5, 0))
        
        # === Segment Options ===
        self.segment_frame = ttk.Frame(self.options_frame)
        self.segment_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Start time
        start_frame = ttk.Frame(self.segment_frame)
        start_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(start_frame, text="Start Time (seconds):").pack(side=tk.LEFT, padx=(20, 10))
        self.start_var = tk.DoubleVar(value=0)
        start_spinbox = ttk.Spinbox(
            start_frame,
            from_=0,
            to=self.video_info.duration - 1,
            textvariable=self.start_var,
            width=10
        )
        start_spinbox.pack(side=tk.LEFT)
        
        # Duration
        duration_frame = ttk.Frame(self.segment_frame)
        duration_frame.pack(fill=tk.X)
        
        ttk.Label(duration_frame, text="Duration (seconds):").pack(side=tk.LEFT, padx=(20, 10))
        self.duration_var = tk.DoubleVar(value=min(60, self.video_info.duration))
        duration_spinbox = ttk.Spinbox(
            duration_frame,
            from_=1,
            to=60,
            textvariable=self.duration_var,
            width=10
        )
        duration_spinbox.pack(side=tk.LEFT)
        
        self.options_widgets['speed_frame'] = self.speed_frame
        self.options_widgets['segment_frame'] = self.segment_frame
        
        # Initial visibility
        self.update_options_visibility()
    
    def update_options_visibility(self):
        """Update which options are visible based on mode"""
        if not hasattr(self, 'mode_var'):
            return
        
        mode = self.mode_var.get()
        
        if mode == "speed":
            self.speed_frame.pack(fill=tk.X, pady=(10, 0))
            self.segment_frame.pack_forget()
        else:
            self.speed_frame.pack_forget()
            self.segment_frame.pack(fill=tk.X, pady=(10, 0))
    
    def update_speed_label(self):
        """Update speed label with calculated duration"""
        if not self.video_info:
            return
        
        speed = self.speed_var.get()
        output_duration = self.video_info.duration / speed
        self.speed_label_var.set(f"{speed:.2f}x → {output_duration:.1f}s")
    
    def select_input_file(self):
        """Open file dialog to select input video"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.mkv *.avi *.webm"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.input_file = Path(file_path)
            self.file_path_var.set(str(self.input_file))
            
            # Load video info
            try:
                self.video_info = get_video_info(self.input_file)
                info_text = (
                    f"Duration: {self.video_info.duration:.1f}s | "
                    f"Resolution: {self.video_info.width}x{self.video_info.height}"
                )
                self.video_info_var.set(info_text)
                
                # Update options UI based on duration
                if self.video_info.is_short:
                    self.create_options_ui_for_short_video()
                else:
                    self.create_options_ui_for_long_video()
                
                # Enable convert button
                self.convert_btn.config(state=tk.NORMAL)
                
                # Set default output folder to input file's folder
                if not self.output_folder:
                    self.output_folder = self.input_file.parent
                    self.output_path_var.set(str(self.output_folder))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load video info:\n{str(e)}")
                self.input_file = None
                self.video_info = None
    
    def select_output_folder(self):
        """Open dialog to select output folder"""
        folder_path = filedialog.askdirectory(
            title="Select Output Folder"
        )
        
        if folder_path:
            self.output_folder = Path(folder_path)
            self.output_path_var.set(str(self.output_folder))
    
    def get_conversion_options(self) -> ConversionOptions:
        """Get conversion options from UI"""
        if self.video_info.is_short:
            return ConversionOptions()
        
        mode = self.mode_var.get()
        
        if mode == "speed":
            return ConversionOptions(speed=self.speed_var.get())
        else:
            return ConversionOptions(
                start_time=self.start_var.get(),
                duration=self.duration_var.get()
            )
    
    def progress_callback(self, progress: float):
        """Update progress bar"""
        self.progress_var.set(progress)
        self.root.update_idletasks()
    
    def start_conversion(self):
        """Start video conversion in background thread"""
        if self.is_processing:
            return
        
        if not self.input_file or not self.video_info:
            messagebox.showerror("Error", "Please select a video file first")
            return
        
        # Get options
        try:
            options = self.get_conversion_options()
            
            # Validate
            is_valid, error_msg = options.validate(self.video_info)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid options:\n{str(e)}")
            return
        
        # Determine output path
        output_path = self.output_folder / f"{self.input_file.stem}_shorts.mp4"
        
        # Confirm overwrite if exists
        if output_path.exists():
            if not messagebox.askyesno("File Exists", f"File already exists:\n{output_path.name}\n\nOverwrite?"):
                return
        
        # Disable UI
        self.is_processing = True
        self.convert_btn.config(state=tk.DISABLED)
        self.status_var.set("Converting...")
        self.progress_var.set(0)
        
        # Start conversion in thread
        def conversion_thread():
            try:
                convert_to_shorts(
                    self.input_file,
                    output_path,
                    options,
                    self.progress_callback
                )
                
                # Success
                self.root.after(0, lambda: self.on_conversion_complete(output_path))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_conversion_error(str(e)))
        
        thread = threading.Thread(target=conversion_thread, daemon=True)
        thread.start()
    
    def on_conversion_complete(self, output_path: Path):
        """Called when conversion completes successfully"""
        self.is_processing = False
        self.convert_btn.config(state=tk.NORMAL)
        self.status_var.set("✓ Conversion complete!")
        self.progress_var.set(100)
        
        messagebox.showinfo(
            "Success",
            f"Video converted successfully!\n\nSaved to:\n{output_path}"
        )
    
    def on_conversion_error(self, error_msg: str):
        """Called when conversion fails"""
        self.is_processing = False
        self.convert_btn.config(state=tk.NORMAL)
        self.status_var.set("✗ Conversion failed")
        self.progress_var.set(0)
        
        messagebox.showerror("Conversion Error", f"Failed to convert video:\n\n{error_msg}")
    
    def apply_theme(self):
        """Apply custom theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', font=('Arial', 10, 'bold'))
        
        self.root.configure(bg='#f0f0f0')


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = ShortsConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
