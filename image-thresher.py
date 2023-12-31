import time
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os



# Settings

CONFIG_FILE_PATH = "image-thresher.conf"

# Maximum dimensions of each image
maxWidth = 600
maxHeight = 400



# Globals

# Set to false to quit program
keepRunning = True

# Global variable to store a reference to the current window object
currentWindow = None
currentWindowFrame = None

# Labels to store paths to folders
lblInput = None
lblTrash = None
lblKeep = None

# The place to display each image
lblImage = None

# List of input files and the decisions made about them
imagePaths = []
# {
#   'path': path,
#   'dest': path
# }

# Index of current image being looked at
currentImageIndex = 0

# Output folders
trashFolder = ''
keepFolder = ''



# Util functions

def newWindow(title):
    global currentWindow
    global currentWindowFrame
    # Check if there is currently a window with a frame that needs to be closed
    if currentWindow is not None:
        currentWindowFrame.destroy()
    # Create and return a new window if there isn't one
    if currentWindow is None:
        currentWindow = Tk()
    # Set the title of the window
    currentWindow.title(title)
    # Add a frame to the window
    currentWindowFrame = Frame(currentWindow)
    currentWindowFrame.pack()
    return currentWindowFrame

def endProgram():
    # Close the current window if there is one
    try:
        currentWindow.quit()
        currentWindow.destroy()
    except:
        pass
    # Terminate the program
    global keepRunning
    keepRunning = False



# Logic

def browseInput():
    foldername = filedialog.askdirectory()
    lblInput.config(text=foldername)
def browseTrash():
    foldername = filedialog.askdirectory()
    lblTrash.config(text=foldername)
def browseKeep():
    foldername = filedialog.askdirectory()
    lblKeep.config(text=foldername)
    
def startSorting():
    # Save the output folders as globals
    global trashFolder
    global keepFolder
    # Get folder names
    inputFolder = lblInput["text"]
    trashFolder = lblTrash["text"]
    keepFolder = lblKeep["text"]
    # Make sure folders are selected
    # TODO
    # Make sure we have write access to the folders
    # TODO
    # Save folder list to file
    try:
        file = open(CONFIG_FILE_PATH, "w")
        file.write("%s\n%s\n%s\n"%(inputFolder, trashFolder, keepFolder));
        file.close()
    except:
        print("Failed to save folder settings")
    # Read list of images in input folder
    fileList = os.listdir(path=inputFolder)
    global imagePaths
    imagePaths = [
        {
            'path': inputFolder + os.sep + fileName,
            'dest': ''
        }
        for fileName in fileList
    ]
    # Show sorting window
    showSortingWindow()
    # Display the first image
    displayImage()

def displayImage():
    global lblImage
    if currentImageIndex < len(imagePaths):
        try:
            img = Image.open(imagePaths[currentImageIndex]['path'])
            width, height = img.size
            if width / height > maxWidth / maxHeight:
                # Set width
                img = img.resize((maxWidth,round(maxWidth*height/width)))
            else:
                # Set height
                img = img.resize((round(maxHeight*width/height), maxHeight))
            img = ImageTk.PhotoImage(img)
            if lblImage != None:
                lblImage.destroy()
            lblImage = Label(currentWindowFrame, image=img)
            lblImage.image = img
            lblImage.grid(row=0, column=0, columnspan=3)
        except Exception as e:
            print("Error displaying image:")
            print(e)
    else:
        if lblImage != None:
            lblImage.destroy()
        lblImage = Label(currentWindowFrame, text="Press Enter to confirm changes")
        lblImage.grid(row=0, column=0, columnspan=3)

def moveFilesAndExit():
    # Move image files to their destinations
    for image in imagePaths:
        os.rename(image['path'], image['dest'])
    # Exit the program
    endProgram()

def actionUndo(event):
    global currentImageIndex
    # Reverse index back one step
    currentImageIndex -= 1
    if currentImageIndex < 0:
        currentImageIndex = 0
    displayImage()

def actionSaveImage(event):
    global currentImageIndex
    global keepFolder
    global imagePaths
    # Make sure we're not at the end
    if currentImageIndex >= len(imagePaths):
        return
    # Set image dest to keep folder
    imagePaths[currentImageIndex]['dest'] = keepFolder + os.sep + os.path.basename(imagePaths[currentImageIndex]['path'])
    # Advance index
    currentImageIndex += 1
    # Prevent index from going too far
    if currentImageIndex >= len(imagePaths):
        currentImageIndex = len(imagePaths)
    # Display the image if we haven't reached the end
    displayImage()

def actionThrowAwayImage(event):
    global currentImageIndex
    global trashFolder
    global imagePaths
    # Make sure we're not at the end
    if currentImageIndex >= len(imagePaths):
        return
    # Set image dest to trash folder
    imagePaths[currentImageIndex]['dest'] = trashFolder + os.sep + os.path.basename(imagePaths[currentImageIndex]['path'])
    # Advance index
    currentImageIndex += 1
    # Prevent index from going too far
    if currentImageIndex >= len(imagePaths):
        currentImageIndex = len(imagePaths)
    # Display the image if we haven't reached the end
    displayImage()

def actionFinish(event):
    global currentImageIndex
    global imagePaths
    # Make sure we're at the end
    if currentImageIndex == len(imagePaths):
        moveFilesAndExit()



# Windows

def showSetupWindow():
    window = newWindow('Setup');
    # Buttons for selecting the folders
    btnBrowseInput = Button(window, text="Select Input", command=browseInput)
    btnBrowseInput.grid(row=1, column=0)
    btnBrowseTrash = Button(window, text="Select Trash", command=browseTrash)
    btnBrowseTrash.grid(row=2, column=0)
    btnBrowseKeep = Button(window, text="Select Keep", command=browseKeep)
    btnBrowseKeep.grid(row=3, column=0)
    # Labels for displaying folder paths
    global lblInput
    lblInput = Label(window)
    lblInput.grid(row=1, column=1)
    global lblTrash
    lblTrash = Label(window)
    lblTrash.grid(row=2, column=1)
    global lblKeep
    lblKeep = Label(window)
    lblKeep.grid(row=3, column=1)
    # Try to load folder paths from previous execution
    if os.path.isfile(CONFIG_FILE_PATH):
        # Read folder paths from file
        file = open(CONFIG_FILE_PATH)
        lines = file.readlines()
        lines = [s.strip() for s in lines]
        file.close()
        # Put paths in label text
        lblInput['text'] = lines[0]
        lblTrash['text'] = lines[1]
        lblKeep['text'] = lines[2]
    # Start button
    btnStart = Button(window, text="Start", command=startSorting)
    btnStart.grid(row=4, column=0, columnspan=2)

def showSortingWindow():
    window = newWindow('Sort Images')
    # A place to show the image
    global lblImage
    lblImage = Label(window)
    lblImage.grid(row=0, column=0, columnspan=3)
    # Buttons
    # TODO
    # Keyboard shortcuts
    currentWindow.bind("<Left>", actionUndo)
    currentWindow.bind("<Up>", actionSaveImage)
    currentWindow.bind("<Down>", actionThrowAwayImage)
    currentWindow.bind("<Return>", actionFinish)



# Init

# Show setup window
showSetupWindow()
# Main loop
while keepRunning:
    time.sleep(0.01)
    # Update the window
    currentWindow.update_idletasks()
    currentWindow.update()
    # Exit the program if the window was closed by the user
    try:
        currentWindow.winfo_exists() # throws an error if the window has been closed
    except:
        endProgram()
