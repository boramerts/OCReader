import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import pytesseract
from pytesseract import Output

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized, dim

def apply_ocr(file_path):
    custom_config = r'--oem 3 --psm 1'

    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    ocr_output = pytesseract.image_to_data(thresh_img, output_type = Output.DICT, \
                                        config=custom_config, lang='eng')

    n_boxes = len(ocr_output['level'])

    for i in range(n_boxes):
        (x,y,w,h) = (ocr_output['left'][i],ocr_output['top'][i],ocr_output['width'][i],ocr_output['height'][i])
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    
    image, dim = image_resize(image, height=800)

    return image, dim

def select_image():
    # Open a file dialog to select an image file
    # TODO: Fix filetypes!!
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    image, dim = apply_ocr(file_path)
    image = ImageTk.PhotoImage(Image.fromarray(image))
    image_label.configure(image=image)
    image_label.configure(width=dim[0], height=dim[1])
    image_label.image = image
    root.geometry("{}x{}".format(dim[0]+100,dim[1]+100))
    
# Create the main window
root = tk.Tk()
window_height = 100
window_width = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

root.attributes("-topmost",True)
root.title("OCReader")

#TODO: * Improve the GUI!!!
#      * Add comments

label_frame = tk.Frame(root)
label_frame.grid(row=0, column=0, padx=10, pady=5)

app_name_label = tk.Label(label_frame, text="Image Viewer", font=("Arial", 16))
app_name_label.pack(anchor='center')

# Create the buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=1, column=0, padx=10, pady=5)
image_frame = tk.Frame(root)
image_frame.grid(row=1,column=1, padx=10, pady=5)

# Create the Select Image button
select_image_button = tk.Button(buttons_frame, text="Select Image", command=select_image)
select_image_button.pack(side=tk.LEFT, padx=10)

# Create the Exit button
exit_button = tk.Button(buttons_frame, text="Exit", command=lambda: root.quit())
exit_button.pack(side=tk.LEFT,anchor='center')

# Create the image label
image_label = tk.Label(image_frame)
image_label.pack(padx=10,anchor='center')

# Start the main event loop
root.mainloop()

