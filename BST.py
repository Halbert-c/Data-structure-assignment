import tkinter as tk
from tkinter import messagebox

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None 
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

class BSTVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Search Tree Visualizer")

        self.tree = BinarySearchTree()

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.entry = tk.Entry(self.controls_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.insert_button = tk.Button(self.controls_frame, text="Insert", command=self.insert)
        self.insert_button.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.controls_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.controls_frame, text="Delete", command=self.delete)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.controls_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def insert(self):
        try:
            key = int(self.entry.get())
            self.tree.insert(key)
            self.clear_canvas()
            self.draw_tree(self.tree.root, 400, 50, 200)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        finally:
            self.entry.delete(0,tk.END)

    def search(self):
        try:
            key = int(self.entry.get())
            result = self.tree.search(key)
            if result:
                messagebox.showinfo("Search Result", f"Key {key} found in the tree!")
            else:
                messagebox.showinfo("Search Result", f"Key {key} not found in the tree.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        finally:
            self.entry.delete(0,tk.END)

    def delete(self):
        try:
            key = int(self.entry.get())
            self.tree.delete(key)
            self.clear_canvas()
            self.draw_tree(self.tree.root, 400, 50, 200)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        finally:
            self.entry.delete(0,tk.END)

    def draw_tree(self, node, x, y, offset):
        if node:
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue")
            self.canvas.create_text(x, y, text=str(node.key), font=("Arial", 12, "bold")) 
            
            if node.left:
                self.canvas.create_line(x, y, x-offset, y+40)
                self.draw_tree(node.left, x-offset, y+50, offset//2)

            if node.right:
                self.canvas.create_line(x, y, x+offset, y+40)
                self.draw_tree(node.right, x+offset, y+50, offset//2)

    def clear_canvas(self):
        self.canvas.delete("all")

