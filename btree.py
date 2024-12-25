import tkinter as tk
from tkinter import Canvas, ttk

class BTreeNode:
    def __init__(self, t, is_leaf):
        self.t = t  # Minimum degree
        self.is_leaf = is_leaf  # True if leaf node
        self.keys = []  # List of keys
        self.children = []  # List of children

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t  # Minimum degree

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, key)
        else:
            self._insert_non_full(root, key)

    def delete(self, key):
        if self.root:
            self._delete(self.root, key)
            if len(self.root.keys) == 0:  # Shrink the tree
                if not self.root.is_leaf:
                    self.root = self.root.children[0]
                else:
                    self.root = None

    def _delete(self, node, key):
        t = self.t
        if key in node.keys:
            if node.is_leaf:
                node.keys.remove(key)
            else:
                idx = node.keys.index(key)
                if len(node.children[idx].keys) >= t:
                    pred = self._get_predecessor(node, idx)
                    node.keys[idx] = pred
                    self._delete(node.children[idx], pred)
                elif len(node.children[idx + 1].keys) >= t:
                    succ = self._get_successor(node, idx)
                    node.keys[idx] = succ
                    self._delete(node.children[idx + 1], succ)
                else:
                    self._merge(node, idx)
                    self._delete(node.children[idx], key)
        else:
            if node.is_leaf:
                return
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            if len(node.children[idx].keys) < t:
                self._fill(node, idx)
            if idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            self._delete(node.children[idx], key)

    def reset(self):
        self.root = BTreeNode(self.t, True)

    def _get_predecessor(self, node, idx):
        current = node.children[idx]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, idx):
        current = node.children[idx + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def _merge(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        child.keys.append(parent.keys.pop(idx))
        child.keys.extend(sibling.keys)
        if not sibling.is_leaf:
            child.children.extend(sibling.children)
        parent.children.pop(idx + 1)

    def _fill(self, parent, idx):
        t = self.t
        if idx != 0 and len(parent.children[idx - 1].keys) >= t:
            self._borrow_from_prev(parent, idx)
        elif idx != len(parent.children) - 1 and len(parent.children[idx + 1].keys) >= t:
            self._borrow_from_next(parent, idx)
        else:
            if idx != len(parent.children) - 1:
                self._merge(parent, idx)
            else:
                self._merge(parent, idx - 1)

    def _borrow_from_prev(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx - 1]
        child.keys.insert(0, parent.keys[idx - 1])
        parent.keys[idx - 1] = sibling.keys.pop()
        if not sibling.is_leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        child.keys.append(parent.keys[idx])
        parent.keys[idx] = sibling.keys.pop(0)
        if not sibling.is_leaf:
            child.children.append(sibling.children.pop(0))

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.is_leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        t = self.t
        child = parent.children[index]
        new_child = BTreeNode(t, child.is_leaf)

        # Move the middle key of the full child to the parent
        middle_key = child.keys[t - 1]
        parent.keys.insert(index, middle_key)

        # Create the new child node
        parent.children.insert(index + 1, new_child)

        # Assign keys to the new child
        new_child.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]

        # If the child is not a leaf, adjust its children
        if not child.is_leaf:
            new_child.children = child.children[t:]
            child.children = child.children[:t]

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

        self.degree_label = tk.Label(self.control_frame, text="Degree:")
        self.degree_label.pack(side=tk.LEFT)

        self.degree_combobox = ttk.Combobox(self.control_frame, values=[2, 3, 4, 5], state="readonly")
        self.degree_combobox.set(2)
        self.degree_combobox.pack(side=tk.LEFT)
        self.degree_combobox.bind("<<ComboboxSelected>>", self.set_degree)

        self.entry = tk.Entry(self.control_frame)
        self.entry.pack(side=tk.LEFT)

        self.insert_button = tk.Button(self.control_frame, text="Insert", command=self.insert_key)
        self.insert_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.control_frame, text="Delete", command=self.delete_key)
        self.delete_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

    def set_degree(self, event):
        try:
            new_degree = int(self.degree_combobox.get())
            self.tree.t = new_degree
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
        self._draw_circle(x, y, node.keys)
        if not node.is_leaf:
            num_children = len(node.children)
            # Adjust x_offset if necessary to ensure proper spacing
            for i, child in enumerate(node.children):
                child_x = x - (x_offset // 2) + i * (x_offset // num_children)
                child_y = y + 100
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
        finally:
            self.entry.delete(0, tk.END)

    def delete_key(self):
        try:
            key = int(self.entry.get())
            self.tree.delete(key)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            pass
        finally:
            self.entry.delete(0, tk.END)

    def clear_canvas(self):
        self.tree.reset()  
        self.canvas.delete("all")  # Clear the canvas visuals
        self.draw_tree()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    # Create a B-Tree with minimum degree 2
    btree = BTree(2)

    # Visualize the B-Tree
    visualizer = BTreeVisualizer(btree)
    visualizer.draw_tree()
    visualizer.run()
