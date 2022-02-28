
import colorama  # text color
from colorama import Fore, Back, Style
import tkinter as tk  # Button and window
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import cv2  # open cv library for image processing
import ntpath  # seprate file names
import numpy as np  # numpy library for image processing
from matplotlib import pyplot as plt  # show the image and result

# greeting text
# print(f'''{Fore.YELLOW}image processing 2022
#             assigment2
#       {Fore.WHITE}     Members:
#           razieh shahsavar      Maryam Bayatzade   Salar Rezaei
#       {Fore.GREEN}objective:
#           The objective of this project is to gain
#           experience with connected components analysis,
#           morphological filters, and the use of features
#           for recognition of objects. A secondary objective
#           is to gain experience with image formats''')

# create the root window
root = tk.Tk()
root.title(' Select the Image file')
root.resizable(False, False)
root.geometry('400x300')


# greeting window
def greeting_window():
    rule_window = tk.Toplevel(root)
    rule_window.title("Introduce & Objective")
    the_rules = tk.Label(rule_window, text=f'''  image processing 2022
            assigment2 
           Members:
          razieh shahsavar      Maryam Bayatzade   Salar Rezaei
      objective:
          The objective of this project is to gain
          experience with connected components analysis,
          morphological filters, and the use of features
          for recognition of objects. A secondary objective
          is to gain experience with image formats''', foreground="red")
    # label.config(font=("Courier", 44))
    the_rules.grid(row=0, column=0, columnspan=5)


# greeting button
greeting_button = ttk.Button(
    root,
    text='Greeting',
    command=greeting_window
)


# OpenDialogBox
def open_image_file():
    # show file type
    filetypes = (
        ('pgm', '*.pgm'),
        ('ppm', '*.ppm'),
        ('pbm', '*.pbm'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfilename(filetypes=filetypes)
    # read the image file and show its content on the image
    f1 = str(f)
    imagefile = cv2.imread(f1)
    # get ImageName of file for title of image
    path, imageName = ntpath.split(f1)
    cv2.imshow(imageName, imagefile)
    # End show
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return f1


# open file button
open_button = ttk.Button(
    root,
    text='Show Image',
    command=open_image_file
)


# thresholdin and cleaning window
def thresh_clean():
    try:
        # open dialog and select image by calling open image function
        f1 = open_image_file()
        # read image
        imagefilename = cv2.imread(f1, 0)
        # get clear image
        # median=cv2.medianBlur(imagefilename,3)
        # get thresholding image
        ret, th = cv2.threshold(imagefilename, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # kernel=np.uint8(np.ones(3,3))
        kernel = np.ones((3, 3))
        erosion = cv2.erode(th, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        # -----------------------
        # apply connected component analysis to the thresholded image
        connectivity = 8
        output = cv2.connectedComponentsWithStats(dilation, connectivity, cv2.CV_32S)
        (numLabels, labels, stats, centroids) = output
        output = dilation.copy()
        # loop over the number of unique connected component labels
        for i in range(0, numLabels):
            # if this is the first component then we examine the *background* (typically we would just ignore this component in our loop)
            if i == 0:
                text = "examining component {}/{} (background)".format(i + 1, numLabels)
                # otherwise, we are examining an actual connected component
            else:
                text = "examining component {}/{}".format(i + 1, numLabels)
                # print a status message update for the current connected component
                print("[INFO] {}".format(text))
                # extract the connected component statistics and centroid for the current label
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                # area = stats[i, cv2.CC_STAT_AREA]
                (cX, cY) = centroids[i]
                # clone our original image (so we can draw on it) and then draw
                # a bounding box surrounding the connected component along with
                # a circle corresponding to the centroid
                cv2.rectangle(output, (x, y), (x + w, y + h), (255, 255, 255), 1)
                cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 0), -1)
                # construct a mask for the current connected component by
                # finding a pixels in the labels array that have the current
                # connected component ID
                componentMask = (labels != i).astype("uint8") * 255
                # show our output image and connected component mask
                cv2.imshow("Output", output)
                cv2.imshow("Connected Component", componentMask)
                cv2.waitKey(0)
            # ----------------------
        cv2.imshow("CLEAR image", dilation)
        cv2.imshow("THRESHOLD image", th)
        cv2.destroyAllWindows()
    except:
        tk.messagebox.showwarning("Alert", "Please select an image")


# thresholdin and cleaning button
thr_cln_filter = ttk.Button(
    root,
    text='Thresholding & Cleaning(Dialation and Erosion)',
    command=thresh_clean
)
# definition buttons and add on the main page
greeting_button.grid(column=1, row=1, sticky='w', padx=100, pady=20)
open_button.grid(column=1, row=2, sticky='w', padx=100, pady=20)
thr_cln_filter.grid(column=1, row=3, sticky='w', padx=100, pady=20)

# run the application
root.mainloop()






