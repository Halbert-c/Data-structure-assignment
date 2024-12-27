import tkinter as tk
from tkinter import messagebox
from BST import BSTVisualizer  
from btree import BTreeVisualizer , BTreeNode, BTree
from MergeSort import GuiDesign
import subprocess


class MainProgramGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Program GUI")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP)

        # Button to open the Binary Search Tree Visualizer
        self.BST_Button = tk.Button(self.control_frame, text="Binary Search Tree Visualizer",command=self.open_BST_visualizer)
        self.BST_Button.pack(side=tk.TOP, pady=5)

        # Button to open the Binary Tree Visualizer
        self.Binary_Tree_Button = tk.Button(self.control_frame, text="B-Tree Visualizer",command=self.open_Binary_Tree_visualizer)
        self.Binary_Tree_Button.pack(side=tk.TOP, pady=5)

        # Button to open the Merge Sort Visualizer
        self.Merge_Sort_Button = tk.Button(self.control_frame,text="Merge Sort Visualizer",command=self.open_Merge_Sort_visualizer)
        self.Merge_Sort_Button.pack(side=tk.TOP, pady=5)


    def open_BST_visualizer(self):
        bst_window = tk.Toplevel(self.root)
        BSTVisualizer(bst_window)  

    def open_Merge_Sort_visualizer(self):
        merge_sort_window = tk.Toplevel(self.root)
        GuiDesign(merge_sort_window)  

    def open_Binary_Tree_visualizer(self):
            subprocess.run(['python', 'btree.py'])


if __name__ == "__main__":
    root = tk.Tk()  
    app = MainProgramGUI(root)
    root.mainloop()









