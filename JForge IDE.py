from customtkinter import*
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import platform;
from tkinter import*
import os
import re
import webbrowser
from PIL import Image

global file_path;
global tv;
tv=True;

global font_size;



current_line_count = 1
words_to_highlight = {
    # Control flow keywords
    "if": "#CC7832",        
    "else": "#CC7832",
    "switch": "#CC7832",
    "case": "#CC7832",
    "default": "#CC7832",
    "for": "#CC7832",
    "while": "#CC7832",
    "do": "#CC7832",
    "break": "#CC7832",
    "continue": "#CC7832",
    "return": "#CC7832",

    # Logical operators / literals
    "true": "#6A8759",      
    "false": "#6A8759",
    "null": "#6A8759",

    # Exception handling
    "try": "#CC7832",        
    "catch": "#CC7832",
    "finally": "#CC7832",
    "throw": "#CC7832",
    "throws": "#CC7832",

    # Class / Method / OOP
    "class": "#A9B7C6",      
    "interface": "#A9B7C6",
    "enum": "#A9B7C6",
    "extends": "#CC7832",    
    "implements": "#CC7832",
    "this": "#9876AA",       
    "super": "#9876AA",
    "new": "#CC7832",        
    "package": "#CC7832",
    "import": "#CC7832",

    # Modifiers
    "public": "#CC7832",     
    "private": "#CC7832",
    "protected": "#CC7832",
    "static": "#CC7832",
    "final": "#CC7832",
    "abstract": "#CC7832",
    "synchronized": "#CC7832",
    "volatile": "#CC7832",
    "transient": "#CC7832",
    "native": "#CC7832",
    "strictfp": "#CC7832",

    # Data types
    "int": "#9876AA",        
    "long": "#9876AA",
    "float": "#9876AA",
    "double": "#9876AA",
    "char": "#9876AA",
    "byte": "#9876AA",
    "short": "#9876AA",
    "boolean": "#9876AA",
    "void": "#9876AA",

   
}


    


def highlight_words(event=None, full=False):
    if full:
        content = TextArea.get("1.0", "end-1c")
        for word in words_to_highlight:
            TextArea.tag_remove(word, "1.0", "end")
        for word, color in words_to_highlight.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            for match in re.finditer(pattern, content):
                start_index = f"1.0+{match.start()}c"
                end_index = f"1.0+{match.end()}c"
                TextArea.tag_add(word, start_index, end_index)
    else:
        cursor_line = TextArea.index("insert").split(".")[0]
        line_start = f"{cursor_line}.0"
        line_end = f"{cursor_line}.end"
        line_content = TextArea.get(line_start, line_end)
        for word in words_to_highlight:
            TextArea.tag_remove(word, line_start, line_end)
        for word, color in words_to_highlight.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            for match in re.finditer(pattern, line_content):
                start_index = f"{cursor_line}.{match.start()}"
                end_index = f"{cursor_line}.{match.end()}"
                TextArea.tag_add(word, start_index, end_index)



def adjust_linearea_width():
    # Find max line number (based on number of lines in TextArea)
    total_lines = int(TextArea.index('end-1c').split('.')[0])  # total line lene ke liye
    digits = len(str(total_lines))# kinte digit ka Number hai

    # Get font from LineArea
    font_conf = LineArea.cget("font")         # font kaunsa hai
    f = font_conf[0];
    size = int(font_conf[1])                    #font ka size

    # Measure width of '9' * digits
    font_measure = CTkFont(family=f, size=size);       
    needed_width = font_measure.measure("9" * digits) + 20  # +10 padding

    # Apply new width
    LineArea.configure(width=needed_width)
    


def ZoomIn(event=None):
    font_con=font=TextArea.cget("font");
    size=int(font_con[1]);
    f=font_con[0];
    size+=1;
    LineArea.configure(font=(f,size));
    TextArea.configure(font=(f,size));
    adjust_linearea_width();
    
    
def ZoomOut(event=None):
    font_con=font=TextArea.cget("font");
    size=int(font_con[1]);
    f=font_con[0];
    size-=1;
    LineArea.configure(font=(f,size));
    TextArea.configure(font=(f,size));
    adjust_linearea_width();

def git():
    webbrowser.open("https://www.github.com");
    

def NewFile(event=None):
    TextArea.delete("1.0","end");
         
    
    
def update_line_count(event=None):
    LineArea.configure(state="normal");
    TextArea.edit_modified(False);
    num_lines = int(TextArea.index("end-1c").split(".")[0]);
    LineArea.delete("1.0", "end")
    for i in range(1, num_lines + 1):
        LineArea.insert("end", f"{i}\n")
    LineArea.configure(state="disabled");





def cut(e):
    global select
    if e:
        select=Root.clipboard_get()
    if TextArea.selection_get():
        select=TextArea.selection_get()
        TextArea.delete("sel.first","sel.last")
        Root.clipboard_clear()
        Root.clipboard_append(select)

def copy(e):
    global select
    if e:
        select=Root.clipboard_get()
    else:
        if TextArea.selection_get():
            select=TextArea.selection_get()
            Root.clipboard_clear()
            Root.clipboard_append(select)
def paste(e):
    global select
    select=Root.clipboard_get()
    if select:
        position=TextArea.index(INSERT)
        TextArea.insert(position,select)
def delete(e):
    global select
    if TextArea.selection_get():
        TextArea.delete("sel.first","sel.last")
def select_all(event):
    TextArea.tag_add(SEL, "1.0", END)
    TextArea.mark_set(INSERT, "1.0")
    TextArea.see(INSERT)

    
def set_file_path(path):
    global file_path
    file_path = path

def check_for_changes():
    if TextArea.edit_modified():  # Check if the editor content has been modified
        response = messagebox.askyesno("Save Changes", "Do you want to save changes to your code?")
        if response:  # Yes, save changes
            save_as()
            return True
        elif response is None:  # Cancel the operation
            return False
    return True  # No changes or No, continue without saving


def savefilem(e):
    save_as();

    


def save_as():
    try:
        path = asksaveasfilename(filetypes=[('Java Files', '*.java'),('ALL Files', '*.*')])
        if not path:
            return  # If the user cancels the save dialog, do nothing

        with open(path, 'w') as file:
            code = TextArea.get('1.0', END)
            file.write(code)
            set_file_path(path)
            ConsoleTextArea.configure(state="normal");
            ConsoleTextArea.insert("1.0","Saved_File_path:"+str(path)+"\n");
            ConsoleTextArea.configure(state="disabled");
        highlight_words();
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def openfilem(e):
    open_file();
    

def open_file():
    if check_for_changes():
        try:
            path = askopenfilename(filetypes=[('Java Files', '*.java'),('ALL Files', '*.*')])
            if not path:
                return  # If the user cancels the open dialog, do nothing
            with open(path, 'r') as file:
                Root.title("J_Forge_Studio");
                title=Root.title();
                Root.title(title+" "+path);
                code = file.read();
                TextArea.delete('1.0', END);
                TextArea.insert('1.0', code);
                highlight_words(full=True);
                update_line_count();    
                ConsoleTextArea.configure(state="normal");
                ConsoleTextArea.insert("1.0","Opened_File_path:"+str(path)+"\n");
                ConsoleTextArea.configure(state="disabled");
                set_file_path(path);
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")


def Run():
    if str(TextArea.get(1.0, END)).isspace():
        messagebox.showerror("Error", "Please write some code to run.")
        return
    if file_path == "":
        messagebox.showerror("Error", "Please save the file first.")
        return

    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    class_name = os.path.splitext(file_name)[0]

    # Open new CMD and run java
    if platform.system() == 'Windows':
         command = f'start cmd /k "cd /d {file_dir} && javac {file_name} && java {class_name}"'
         
    elif platform.system() == 'Darwin':  # macOS
        command = f'osascript -e \'tell app "Terminal" to do script "cd {file_dir} && javac {file_name} && java {class_name}"\''
    else:  # Linux
        command = f'gnome-terminal -- bash -c "cd {file_dir} && javac {file_name} && java {class_name}; exec bash"'

    try:
        ConsoleTextArea.configure(state="normal");
        ConsoleTextArea.insert("1.0","File_path:"+str(file_path)+"\n");
        ConsoleTextArea.configure(state="disabled");
        os.system(command)
    except Exception as e:
        ConsoleTextArea.configure(state="normal");
        ConsoleTextArea.insert("1.0","File_path:"+str(file_path)+"\n");
        messagebox.showerror("Error", f"Failed to run: {str(e)}");
        ConsoleTextArea.configure(state="disabled");


    


def hide_terminal():
    global tv;
    if(tv==True):
        ConsoleBar.pack_forget();
        Console_Title.pack_forget();
        Console.pack_forget();
        ConsoleTextArea.pack_forget();
        tv=False;
    else:
         messagebox.showerror("Error","Terminal is already Hidden");
    
def Start():
    Root1.destroy();

def about():
    info="J Forge-ide  is a simple but  powerful Integrated Development Environment (IDE) specifically designed for Java development. Created by RajharpreetSingh Student of Amity University Noida MCA Section - D."
    messagebox.showinfo("Info",info);



def show_terminal():
    global tv;
    if(tv==False):
        Background.pack_forget();
        TextArea.pack_forget();
        Background.pack(fill = BOTH, expand = True);
        TextArea.pack(fill = BOTH, expand = True);
        Console.pack(side=BOTTOM,fill=X);
        ConsoleBar.pack(side=BOTTOM,fill=X);
        Console_Title.pack();
        ConsoleTextArea.pack(fill = BOTH, expand = True);
        tv=True;
    else:
         messagebox.showerror("Error","Terminal is already Visibile");
    

def on_key_release(event=None):
    update_line_count(event);
    highlight_words(event);


#------------------------------front page --------------------------------------#    
Root1 = CTk()
Root1.geometry("1080x700");
Root1.minsize(800,600);
Root1.title("Welcome To J_Forge IDE");
Root1.iconbitmap("Java.ico");
Background=CTkFrame(Root1,fg_color="#383838");
Background.pack(fill=BOTH,expand=True);
logo = CTkImage(light_image=Image.open("lo.png"),dark_image=Image.open("lo.png"),size=(200, 150));
label = CTkLabel(Background, image=logo, text="");
label.pack();
label_1 = CTkLabel(Background,  text="J_FORGE IDE" , font=("Lucida Sans",40));
label_1.pack();
label_1 = CTkLabel(Background,  text="Version:0.9" , font=("Lucida Sans",20));
label_1.pack();
label_2 = CTkLabel(Background,  text="" , font=("Lucida Sans",20));
label_2.pack();
Create=CTkButton(Background,height=50,width=400,text="Start New Project",font=("Lucida Sans",15),command=Start);
Create.pack();
label_2 = CTkLabel(Background,  text="" , font=("Lucida Sans",20));
label_2.pack();
Clone=CTkButton(Background,height=50,width=400,text="Clone Repository",font=("Lucida Sans",15),command=git);
Clone.pack();
label_2 = CTkLabel(Background,  text="" , font=("Lucida Sans",20));
label_2.pack();
About=CTkButton(Background,height=50,width=400,text="About ",font=("Lucida Sans",15),command=about);
About.pack();
Root1.mainloop();
#------------------------------front page --------------------------------------#

Root=CTk();
Root.geometry("1000x700");
Root.title("J_Forge_Studio")
Root.iconbitmap("Java.ico") ;
Topbar=CTkFrame(Root,height=30,bg_color="#282C34",fg_color="#282C34");
Topbar.pack(side=TOP,fill=X);

New_Button=CTkButton(Topbar,text="New File",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=2,command=NewFile);
New_Button.pack(side=LEFT);


Open_Button=CTkButton(Topbar,text="Open File",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=2,command=open_file);
Open_Button.pack(side=LEFT);

Save_Button=CTkButton(Topbar,text="Save FIle",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=2,command=save_as);
Save_Button.pack(side=LEFT);


Run_Button=CTkButton(Topbar,text="Compile Run File",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=5,command=Run);
Run_Button.pack(side=LEFT);



Hide_Button=CTkButton(Topbar,text="Hide Terminal",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=5,command=hide_terminal);
Hide_Button.pack(side=LEFT);

Show_Button=CTkButton(Topbar,text="Show Terminal",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=5,command=show_terminal);
Show_Button.pack(side=LEFT);

ZoomIn_Button=CTkButton(Topbar,text="Zoom In",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=5,command=ZoomIn);
ZoomIn_Button.pack(side=LEFT);

ZoomOut_Button=CTkButton(Topbar,text="Zoom Out",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=5,command=ZoomOut);
ZoomOut_Button.pack(side=LEFT);                            

about_Button=CTkButton(Topbar,text="About",fg_color="#282C34",border_color="#282C34",border_width=1,corner_radius=5,command=about);
about_Button.pack(side=LEFT);

    
Background=CTkFrame(Root,bg_color="#282C34");
Background.pack(fill = BOTH, expand = True);

LineArea=CTkTextbox(Background,fg_color="#282C34",border_color="#4F575F",width=40,border_width=1,font=("verdana", 12),corner_radius=0,activate_scrollbars=False,wrap="char");
LineArea.configure(state="disabled");
LineArea.pack(side=LEFT,fill = Y);



TextArea=CTkTextbox(Background,fg_color="#282C34",border_color="#4F575F",border_width=1,font=("verdana", 12),corner_radius=2,wrap="word",undo=True);
TextArea.bind("<KeyRelease>",update_line_count);
TextArea.pack(fill = BOTH, expand = True);

for word, color in words_to_highlight.items():
    TextArea.tag_config(word, foreground=color);




Console=CTkFrame(Root,height=200,fg_color="#21252B",bg_color="#21252B",border_color="#4F575F",border_width=1);
Console.pack(side=BOTTOM,fill=X);


ConsoleBar=CTkFrame(Root,height=15,fg_color="#21252B",bg_color="#21252B");
ConsoleBar.pack(side=BOTTOM,fill=X);




Console_Title=CTkLabel(ConsoleBar,text="Terminal");
Console_Title.pack();



ConsoleTextArea=CTkTextbox(Console,text_color="orange",font=("monospace",16)); 
ConsoleTextArea.configure(state="disabled");
ConsoleTextArea.pack(fill = BOTH, expand = True);


m = Menu(Root, tearoff = 0,fg="#ffffff",bg="#282C34");
m.add_command(label ="Cut          ",command=lambda: cut(False),font=("verdana",16));
m.add_command(label ="Copy          ",command=lambda: copy(False),font=("verdana",16))
m.add_command(label ="Paste          ",command=lambda: paste(False),font=("verdana",16))
m.add_command(label ="Delete          ",command=lambda: delete(False),font=("verdana",16))
m.add_separator()
m.add_command(label ="Select all           ",command=lambda: select_all(False),font=("verdana",16))
#-------shortcut-------#
Root.bind("<Control-Key-s>",save_as);
Root.bind("<Control-Key-o>",open_file)


def do_popup(event): 
    try: 
        m.tk_popup(event.x_root, event.y_root) 
    finally: 
        m.grab_release()


TextArea.bind("<KeyRelease>", on_key_release);
Root.bind("<Button-3>", do_popup)
Root.bind("<Control-Key-s>",savefilem);
Root.bind("<Control-Key-o>",openfilem);
Root.bind("<Control-Key-N>",NewFile);


Root.bind("<Control-plus>",ZoomIn);
Root.bind("<Control-equal>",ZoomIn);
Root.bind("<Control-KP_Add>",ZoomIn);


Root.bind("<Control-minus>",ZoomOut);
Root.bind("<Control-KP_Subtract>",ZoomOut);


Root.mainloop();

