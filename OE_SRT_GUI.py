import OE_Subtitle_Collector as SC
import Transcript_to_SRT as T2S
import tkinter as tk
from tkinter import messagebox, font, ttk, filedialog

class mainGUI:

    videoURLErrorFlag = False
    captionDictError = False
    collector = SC.subtitleCollector()

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Office of Online Education SRT Downloader Tool")
        photo = tk.PhotoImage(file = "testlogo.png")
        self.root.iconphoto(False,photo)

        ##### FONTS #####
        textFont1 = font.Font(weight= "normal", family="Arial", size=18)
        
        ##### PAGE FRAMES #####
        self.page1 = tk.Frame(self.root)
        self.page2 = tk.Frame(self.root)

        self.page1.grid(row=0,column=0, sticky=tk.N+tk.W+tk.E+tk.S)
        self.page2.grid(row=0,column=0, sticky=tk.N+tk.W+tk.E+tk.S)
  
        self.check_state = tk.IntVar()

        ##### PAGE 1 #####
        self.label = tk.Label(self.page1, text="Welcome to the OE SRT tool. Please provide Youtube video URL below.", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.urlEntry= tk.Entry(self.page1, font=textFont1, width=40)
        self.urlEntry.pack(padx=10, pady=10)

        self.urlButton = tk.Button(self.page1, text="Enter", font=('Arial', 18), command=self.get_urlEntry)
        self.urlButton.pack(padx=10, pady=10)

        ##### PAGE 2 #####
        self.page2label1 = tk.Label(self.page2, text="Found Youtube Video", font=('Arial', 18))
        self.page2label1.pack(padx=10, pady=10)

        self.page2treebox = ttk.Treeview(self.page2, columns=2)
        self.page2treebox.heading("#0", text="Language Code")
        self.page2treebox.heading("#1", text="Transcript URL")
        self.page2treebox.column("#1", width=800)
        self.page2treebox.xview_scroll(3,'units')

        self.page2savebutton = tk.Button(self.page2, text="Save File", font=textFont1, command=self.save_file)

        ##### CLOSING #####
        
        #Start on page 1
        self.page1.tkraise()

        #Initiate close when requested
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


        

    def on_closing(self):
        answer = messagebox.askyesno("Quit", "Do you want to quit?", parent=self.root)
        if answer is not None:
            self.root.destroy()
            exit(0)

    def get_urlEntry(self):
        self.youtubeURL = self.urlEntry.get()
        if self.youtubeURL == "":
            if self.videoURLErrorFlag == False:
                self.label3 = tk.Label(self.page1, text="Error: Please enter a Youtube URL", font=('Arial', 18))
                self.label3.pack(padx=10, pady=10)
                self.videoURLErrorFlag = True            
            return
        
        self.collector.get_HTMLContent(self.youtubeURL)
        if bool(self.collector.subtitleDict):
            if self.captionDictError == False:
                self.page1label4 = tk.Label(self.page1, text="Error: Captions not found for URL", font=('Arial', 18))
                self.page1label4.pack(padx=10, pady=10)
                self.captionDictError = True
            return
            
        self.collector.get_Subtitles()
        self.create_Page2()
        
    def create_Page2(self):
        for i in self.collector.subtitleDict:
            self.page2treebox.insert(
                "",
                tk.END,
                text=self.collector.subtitleDict[i],
                values=(i)
            )
        self.page2treebox.pack(padx=10, pady=10)
        self.page2savebutton.pack(padx=10, pady=10)
        print(self.collector.subtitleDict)
        self.page2.tkraise()
        
    def save_file(self):
        focus = self.page2treebox.focus()
        if(not focus):
            return

        item = self.page2treebox.item(focus)
        transcriptURL = item.get("values")[0]
        converter = T2S.Transcript_to_SRT(transcriptURL)
        SRT = converter.get_SRT()


        filename = filedialog.asksaveasfilename(initialfile="untitled.srt",
                                                defaultextension="srt",
                                                filetypes=[("SRT", ".srt")])
        if filename != "":
            inFile = open(filename, "w")
            inFile.write(SRT)
            inFile.close()