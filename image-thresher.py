import time
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image



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

# Maximum dimensions of each image
maxWidth = 300
maxHeight = 300

# List of input files and the decisions made about them
imagePaths = []

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
    # Read list of images in input folder
    # TODO
    # Show sorting window
    showSortingWindow()

    # os.path.isfile(path)
    # os.path.abspath(path)
    # os.listdir(path=path)
    # os.rename(curpath, newpath)
    # os.sep
    # os.path.basename(pathtofile)

def displayImage(path):
    try:
        img = Image.open(path)
        width, height = img.size
        if width / height > maxWidth / maxHeight:
            # Set width
            img = img.resize((maxWidth,round(maxWidth*height/width)))
        else:
            # Set height
            img = img.resize((round(maxHeight*width/height), maxHeight))
        img = ImageTk.PhotoImage(img)
        global lblImage
        lblImage.image = img
    except:
        print("Error displaying image")


# Windows

def showSetupWindow():
    window = newWindow('Setup');
    # Instruction label
    lblInstruction = Label(window, text="Choose folders")
    lblInstruction.grid(row=0, column=0, columnspan=2)
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
    # Start button
    btnStart = Button(window, text="Start", command=startSorting)
    btnStart.grid(row=4, column=0, columnspan=2)

def showSortingWindow():
    window = newWindow('Sort Images')
    # A place to show the image
    lblImage = Label(window)
    lblImage.grid(row=0, column=0, columnspan=3)
    # Buttons
    # TODO
    # Keyboard shortcuts
    # TODO



# Init

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