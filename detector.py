import customtkinter as ctk  # Import customtkinter as ctk for the GUI framework
from tkinter import filedialog  # Import filedialog for file dialog
import cv2  # Import OpenCV for image processing
import pandas as pd  # Import pandas for data manipulation
from PIL import Image, ImageTk  # Import PIL for handling image conversion and ImageTk for displaying images


def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()  # Get the screen width
    screen_height = Screen.winfo_screenheight()  # Get the screen height
    x = int(((screen_width / 2) - (width / 2.3)) * scale_factor)  # Calculate x coordinate for centering
    y = int(((screen_height / 2) - (height / 1.7)) * scale_factor)  # Calculate y coordinate for centering
    return f"{width}x{height}+{x}+{y}"  # Return the geometry string for centering the window


class ColorDetectorApp:
    def __init__(self, root):
        self.root = root  # Store the root window
        self.root.title("Color Detector")  # Set the title of the window
        self.root.iconbitmap("color-wheel.ico")  # Set the icon of the window
        self.root.resizable(False, False)  # Make the window non-resizable
        self.root.geometry(CenterWindowToDisplay(root, 800, 785))  # Center the window on the screen

        ctk.set_appearance_mode("dark")  # Set the appearance mode to dark
        ctk.set_default_color_theme("blue")  # Set the color theme to blue

        # Create the main frame
        self.frame = ctk.CTkFrame(root)  # Create a CTkFrame as the main frame
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)  # Pack the frame with padding

        # Create a canvas to display the image
        self.canvas = ctk.CTkCanvas(self.frame, width=800, height=600, bg='#006699', highlightthickness=0)

        self.canvas.pack()  # Pack the canvas

        # Display initial message on the canvas
        self.initial_message = self.canvas.create_text(400, 300, text="Upload your image", fill="white",
                                                       font=(
                                                           "Helvetica", 24))  # Display an initial message on the canvas

        # Create a frame for color information
        self.info_frame = ctk.CTkFrame(self.frame)  # Create a CTkFrame for color information
        self.info_frame.pack(fill="x")  # Pack the frame to fill the x-axis

        # Create a canvas to display the color rectangle and text
        self.color_info_canvas = ctk.CTkCanvas(self.info_frame, height=50, bg='#2c2c2c',
                                               highlightthickness=0)  # Create a CTkCanvas for color information with a grey background
        self.color_info_canvas.pack(fill="x")  # Pack the canvas to fill the x-axis

        # Create buttons
        self.upload_button = ctk.CTkButton(self.frame, text="Upload Image",
                                           command=self.upload_image)  # Create an upload button
        self.upload_button.pack(pady=(10, 4))  # Pack the upload button with padding

        self.exit_button = ctk.CTkButton(self.frame, text="Exit", command=root.quit)  # Create an exit button
        self.exit_button.pack(pady=(10, 10))  # Pack the exit button with padding

        # Initialize variables
        self.img = None  # Initialize img variable
        self.resized_img = None  # Initialize resized_img variable
        self.clicked = False  # Initialize clicked variable

        # Load the CSV file for colors
        index = ['color', 'color_name', 'hex', 'R', 'G', 'B']  # Define the column names for the CSV file
        self.csv = pd.read_csv('colors.csv', names=index)  # Load the CSV file into a DataFrame

        # Bind the mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.draw_function)  # Bind the draw_function to the canvas click event

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")])  # Open a file dialog to select an image
        if file_path:  # If a file is selected
            self.img = cv2.imread(file_path)  # Read the image using OpenCV
            self.resized_img = self.resize_image(self.img, 800, 600)  # Resize the image to fit the canvas
            self.canvas.config(bg='#2c2c2c')  # Set the canvas background to #2c2c2c
            self.display_image(self.resized_img)  # Display the resized image
            self.canvas.delete(self.initial_message)  # Remove the initial message from the canvas

    def resize_image(self, img, canvas_width, canvas_height):
        height, width = img.shape[:2]  # Get the dimensions of the image
        aspect_ratio = width / height  # Calculate the aspect ratio

        if width > canvas_width or height > canvas_height:  # If the image is larger than the canvas
            if width > height:  # If the width is greater than the height
                new_width = canvas_width  # Set the new width to the canvas width
                new_height = int(new_width / aspect_ratio)  # Calculate the new height
                if new_height > canvas_height:  # If the new height is greater than the canvas height
                    new_height = canvas_height  # Set the new height to the canvas height
                    new_width = int(new_height * aspect_ratio)  # Calculate the new width
            else:  # If the height is greater than the width
                new_height = canvas_height  # Set the new height to the canvas height
                new_width = int(new_height * aspect_ratio)  # Calculate the new width
                if new_width > canvas_width:  # If the new width is greater than the canvas width
                    new_width = canvas_width  # Set the new width to the canvas width
                    new_height = int(new_width / aspect_ratio)  # Calculate the new height
        else:  # If the image is smaller than the canvas
            if width > height:  # If the width is greater than the height
                new_width = canvas_width  # Set the new width to the canvas width
                new_height = int(new_width / aspect_ratio)  # Calculate the new height
            else:  # If the height is greater than the width
                new_height = canvas_height  # Set the new height to the canvas height
                new_width = int(new_height * aspect_ratio)  # Calculate the new width

        resized_img = cv2.resize(img, (new_width, new_height))  # Resize the image
        return resized_img  # Return the resized image

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
        img_pil = Image.fromarray(img_rgb)  # Convert the image to a PIL image

        # Resize the image to fit within the canvas while maintaining aspect ratio
        img_pil.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(img_pil)  # Convert the PIL image to an ImageTk object

        # Calculate the position to center the image on the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = img_pil.size
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2

        self.canvas.create_image(x, y, anchor="nw", image=img_tk)  # Create the image on the canvas centered
        self.canvas.image = img_tk  # Store the image in the canvas to prevent garbage collection

        # Store the image position and size
        self.img_x = x
        self.img_y = y
        self.img_width = img_width
        self.img_height = img_height

    def draw_function(self, event):
        if self.resized_img is not None:  # If an image is loaded
            x, y = event.x, event.y  # Get the coordinates of the mouse click
            if self.img_x <= x < self.img_x + self.img_width and self.img_y <= y < self.img_y + self.img_height:  # If the click is within the image bounds
                # Adjust coordinates relative to the image
                x -= self.img_x  # Adjust x coordinate relative to the top-left corner of the image
                y -= self.img_y  # Adjust y coordinate relative to the top-left corner of the image
                b, g, r = self.resized_img[y, x]  # Get the BGR values of the pixel
                b, g, r = int(b), int(g), int(r)  # Convert the values to integers
                color_name = self.get_color_name(r, g, b)  # Get the color name from the CSV
                text = f"{color_name} ({r}, {g}, {b})"  # Create the text to display
                self.display_color_info(text, r, g, b)  # Display the color information

    def get_color_name(self, r, g, b):
        min_distance = 1000  # Initialize the minimum distance
        cname = ""  # Initialize the color name
        for i in range(len(self.csv)):  # Iterate through the CSV
            d = abs(r - int(self.csv.loc[i, "R"])) + abs(g - int(self.csv.loc[i, "G"])) + abs(
                b - int(self.csv.loc[i, "B"]))  # Calculate the distance to each color
            if d <= min_distance:  # If the distance is less than the minimum distance
                min_distance = d  # Update the minimum distance
                cname = self.csv.loc[i, "color_name"]  # Update the color name
        return cname  # Return the color name

    def display_color_info(self, text, r, g, b):
        self.color_info_canvas.delete("all")  # Clear the color info canvas

        # Get the text size
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                                       2)  # Get the size of the text

        # Calculate rectangle coordinates to fit tightly around the text
        rect_x0 = (self.color_info_canvas.winfo_width() - text_width - 20) // 2  # Calculate the x0 coordinate
        rect_y0 = 10  # Set the y0 coordinate
        rect_x1 = rect_x0 + text_width + 20  # Calculate the x1 coordinate
        rect_y1 = rect_y0 + text_height + 20  # Calculate the y1 coordinate

        # Create the rectangle and text on the canvas
        self.color_info_canvas.create_rectangle(rect_x0, rect_y0, rect_x1, rect_y1, fill=self.rgb_to_hex(r, g, b),
                                                outline="")  # Create the rectangle with no outline
        text_color = "white" if r + g + b < 500 else "black"  # Determine the text color based on the background color
        self.color_info_canvas.create_text((rect_x0 + rect_x1) // 2, (rect_y0 + rect_y1) // 2, text=text,
                                           fill=text_color, font=("Helvetica", 14), anchor="center")  # Create the text

    def rgb_to_hex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'  # Convert the RGB values to a hex color string


# Initialize the main application window
if __name__ == "__main__":
    root = ctk.CTk()  # Create the main window
    app = ColorDetectorApp(root)  # Create an instance of the ColorDetectorApp class
    root.mainloop()  # Start the main event loop
