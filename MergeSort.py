import tkinter as tk
from tkinter import messagebox

class MergeSort:
    @staticmethod
    def merge(arr, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        # Create temp arrays
        L = [0] * n1
        R = [0] * n2

        # Copy data to temp arrays L[] and R[]
        for i in range(n1):
            L[i] = arr[left + i]
        for j in range(n2):
            R[j] = arr[mid + 1 + j]

        i, j, k = 0, 0, left  # Initial indices

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    @staticmethod
    def merge_sort(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            MergeSort.merge_sort(arr, left, mid)
            MergeSort.merge_sort(arr, mid + 1, right)
            MergeSort.merge(arr, left, mid, right)

class GuiDesign:
    def __init__(self, root):
        self.root = root
        self.array = []

        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.entry = tk.Entry(self.controls_frame, width=20)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.controls_frame, text="Add", command=self.add_element)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.sort_button = tk.Button(self.controls_frame, text="Sort", command=self.sort_elements)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.controls_frame, text="Delete", command=self.delete_element)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.controls_frame, text="Search", command=self.search_element)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.controls_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)


    def add_element(self):
        try:
            value = int(self.entry.get())
            if value < 0 or value > 150:
                raise ValueError("Value out of range")
            self.array.append(value)
            self.display_array()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer between 0 and 150")
        finally:
            self.entry.delete(0,tk.END)

    def sort_elements(self):
        if not self.array:
            messagebox.showinfo("Info", "No elements to sort")
            return

        MergeSort.merge_sort(self.array, 0, len(self.array) - 1)
        self.display_array()
        self.entry.delete(0,tk.END)

    def delete_element(self):
        try:
            value = int(self.entry.get())
            if value in self.array:
                self.array.remove(value)
                self.display_array()
            else:
                messagebox.showinfo("Info", f"Value {value} not found in the array")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        finally:
            self.entry.delete(0,tk.END)


    def search_element(self):
        try:
            value = int(self.entry.get())
            if value in self.array:
                index = self.array.index(value)
                messagebox.showinfo("Search Result", f"Value {value} found at index {index} in the array.")
            else:
                messagebox.showinfo("Search Result", f"Value {value} not found in the array.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        finally:
            self.entry.delete(0,tk.END)

    def display_array(self):
        self.clear_canvas()
        x = 50
        for value in self.array:
            self.canvas.create_rectangle(x, 300 - value * 2, x + 30, 300, fill="lightblue")
            self.canvas.create_text(x + 15, 300 - value * 2 - 10, text=str(value), font=("Arial", 10, "bold"))
            x += 40

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Merge Sort Visualizer")
    app = GuiDesign(root)
    root.mainloop()

        

