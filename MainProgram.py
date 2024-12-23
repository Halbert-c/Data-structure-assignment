import tkinter as tk
from tkinter import messagebox
from BST import 

class MainProgramGUI: 
    def __init__(self):
        self.root = root 
        self.root.title("Main Program GUI")
        self.canvas = tk.Canvas(root, width=400, height=400,bg="white")
        self.canvas.pack()

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.top)

        self.BST_Button = tk.Button(control_frame, text="Binary Search Tree Visualizer")
        self.BST_Button.pack(side=tk.top, pady=5)

        self.Binary_Tree_Button = tk.Button(control_frame,text="Binary Tree Visualizer")
        self.Binary_Tree_Button.pack(side=tk.top,pady=5)

        self.Merge_Sort_Button = tk.Button(control_frame, text="Merge Sort Visualizer")
        self.Merge_Sort_Button.pack(side=tk.top,pady=5)










