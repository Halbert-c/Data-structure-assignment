import tkinter as tk
from tkinter import Canvas, ttk
from tkinter import messagebox
class BTreeNode:
    def __init__(self, max_keys, is_leaf):
        self.max_keys = max_keys  # Maximum keys a node can hold
        self.is_leaf = is_leaf  # True if leaf node
        self.keys = []  # List of keys
        self.children = []  # List of children

class BTree:
    def __init__(self, max_degree):
        self.root = BTreeNode(max_degree-1 , True)
        self.max_degree = max_degree  # Maximum number of children a node can have

    def insert(self, key):
        root = self.root
        if len(root.keys) == root.max_keys:  # Split when the node is full
            new_root = BTreeNode(self.max_degree-1, False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, key)
        else:
            self._insert_non_full(root, key)

    def _split_child(self, parent, index):
        # Get the full child node
        child = parent.children[index]
        max_keys = child.max_keys
        middle_idx = max_keys // 2
        middle_key = child.keys[middle_idx]

        # Create a new child node
        new_child = BTreeNode(child.max_keys, child.is_leaf)

        # Split the keys and children
        new_child.keys = child.keys[middle_idx + 1:]
        child.keys = child.keys[:middle_idx]

        if not child.is_leaf:
            new_child.children = child.children[middle_idx + 1:]
            child.children = child.children[:middle_idx + 1]

        # Insert the middle key into the parent node
        parent.keys.insert(index, middle_key)
        parent.children.insert(index + 1, new_child)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1

        # If the node is a leaf, find the correct position to insert the key
        if node.is_leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
        else:
            # If not a leaf, find the correct child node to insert into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1  # i will be the index of the child to recurse into

            # Check if the child node is full
            if len(node.children[i].keys) == node.children[i].max_keys:
                self._split_child(node, i)  # Split the child if it's full

                # After splitting, check the key against the parent node to decide which child to recurse into
                if key > node.keys[i]:
                    i += 1

            # Recurse into the appropriate child node
            self._insert_non_full(node.children[i], key)
    def delete(self, key):
        self._delete(self.root, key)
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]  # Update root if it's empty
    def _delete(self, node, key):
        if key in node.keys:  # Key found in the current node
            if node.is_leaf:
                node.keys.remove(key)  # If it's a leaf, simply remove the key
            else:
                idx = node.keys.index(key)

                # Case 1: The left child has enough keys to borrow
                if len(node.children[idx].keys) >= self.max_degree // 2:
                    predecessor = self._get_predecessor(node, idx)
                    node.keys[idx] = predecessor
                    self._delete(node.children[idx], predecessor)

                # Case 2: The right child has enough keys to borrow
                elif len(node.children[idx + 1].keys) >= self.max_degree // 2:
                    successor = self._get_successor(node, idx)
                    node.keys[idx] = successor
                    self._delete(node.children[idx + 1], successor)

                # Case 3: Both children are too small, so merge the children
                else:
                    self._merge(node, idx)
                    self._delete(node.children[idx], key)
        else:
            # Key is not in the current node, continue searching in the children
            idx = self._find_index(node, key)
            if node.is_leaf:
                return  # Key not found, do nothing
            if len(node.children[idx].keys) < self.max_degree // 2:
                self._fill(node, idx)
            self._delete(node.children[idx], key)

    def _get_predecessor(self, node, idx):
        curr = node.children[idx]
        while not curr.is_leaf:
            curr = curr.children[-1]  # Go to the rightmost child
        return curr.keys[-1]

    def _get_successor(self, node, idx):
        curr = node.children[idx + 1]
        while not curr.is_leaf:
            curr = curr.children[0]  # Go to the leftmost child
        return curr.keys[0]

    def _merge(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx + 1]
        child.keys.append(node.keys[idx])  # Move parent key down to the child
        child.keys.extend(sibling.keys)  # Merge sibling keys into the child

        if not sibling.is_leaf:
            child.children.extend(sibling.children)  # Merge sibling children into the child

        node.keys.pop(idx)  # Remove the parent key
        node.children.pop(idx + 1)  # Remove the sibling

    def _fill(self, node, idx):
        if idx > 0 and len(node.children[idx - 1].keys) >= self.max_degree // 2:
            self._borrow_from_prev(node, idx)
        elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) >= self.max_degree // 2:
            self._borrow_from_next(node, idx)
        else:
            if idx < len(node.children) - 1:
                self._merge(node, idx)
            else:
                self._merge(node, idx - 1)

    def _borrow_from_prev(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx - 1]

        child.keys.insert(0, node.keys[idx - 1])  # Borrow a key from the left sibling
        if not sibling.is_leaf:
            child.children.insert(0, sibling.children.pop())  # Borrow a child from the left sibling

        node.keys[idx - 1] = sibling.keys.pop()  # Move the sibling's key up to the parent

    def _borrow_from_next(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys.append(node.keys[idx])  # Borrow a key from the right sibling
        if not sibling.is_leaf:
            child.children.append(sibling.children.pop(0))  # Borrow a child from the right sibling

        node.keys[idx] = sibling.keys.pop(0)  # Move the sibling's key up to the parent

    def _find_index(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        return i
        
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        # Iterate through node keys
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:  # Key found
            return node
        
        if node.is_leaf:  # If leaf, key is not found
            return None
        
        # Otherwise, recurse into the appropriate child node
        return self._search(node.children[i], key)
    
    def reset(self):
        self.root = BTreeNode(self.max_degree - 1, True)

class BTreeVisualizer:
    def __init__(self, tree):
        self.tree = tree
        self.window = tk.Tk()
        self.window.title("B-Tree Visualizer")

        self.canvas = Canvas(self.window, width=800, height=600, bg="white")
        self.canvas.pack()
        self.node_radius = 20

        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack()

        self.degree_label = tk.Label(self.control_frame, text="Max Degree:")
        self.degree_label.pack(side=tk.LEFT)

        self.degree_combobox = ttk.Combobox(self.control_frame, values=[3, 4, 5, 6], state="readonly")
        self.degree_combobox.pack(side=tk.LEFT)
        self.degree_combobox.bind("<<ComboboxSelected>>", self.set_degree)

        self.entry = tk.Entry(self.control_frame)
        self.entry.pack(side=tk.LEFT)

        self.insert_button = tk.Button(self.control_frame, text="Insert", command=self.insert_key)
        self.insert_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.control_frame, text="Search", command=self.search_key)
        self.clear_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.control_frame, text="Delete", command=self.delete_key)
        self.delete_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)
        
        self.node_positions = {}

    def set_degree(self, event):
        try:
            new_degree = int(self.degree_combobox.get())
            self.tree.max_degree = new_degree
            self.tree.reset()
            self.draw_tree()
        except ValueError:
            pass

    def draw_tree(self):
        self.canvas.delete("all")  # Clear the canvas before drawing
        if self.tree.root and len(self.tree.root.keys) > 0:
            self._draw_node(self.tree.root, 400, 50, 200)
        else:
            self.canvas.create_text(400, 300, text="Tree is empty", font=("Arial", 14))

    
    def _draw_node(self, node, x, y, x_offset):
        if len(node.keys) == 0: 
            return

        self._draw_circle(x, y, node.keys)

        if not node.is_leaf:
            num_children = len(node.children)
            
            if num_children == 1:
                child_x_start = x
            else:
                
                total_width = x_offset * (num_children - 1)
                child_x_start = x - total_width // 2  
            for i, child in enumerate(node.children):
                
                child_x = child_x_start + i * x_offset
                child_y = y + 100 

                if len(child.keys) > 0:  
                    self.canvas.create_line(x, y, child_x, child_y, fill="black")
                    
                    self._draw_node(child, child_x, child_y, x_offset // 2)  
    def _draw_circle(self, x, y, keys):
        r = self.node_radius
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue")
        self.canvas.create_text(x, y, text=",".join(map(str, keys)), font=("Arial", 10))


    def insert_key(self):
        try:
            key = int(self.entry.get())
            self.tree.insert(key)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            pass

    def delete_key(self):
        try:
            key = int(self.entry.get())
            self.tree.delete(key)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            pass
    def search_key(self):
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
    def clear_canvas(self):
        self.tree.reset()
        self.canvas.delete("all")  # Clear the canvas visuals
        self.draw_tree()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    tree = BTree(max_degree=3)
    visualizer = BTreeVisualizer(tree)
    visualizer.run()
