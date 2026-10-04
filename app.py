import math
from flask import Flask, render_template, request

app = Flask(__name__)

class Node:
    """Represents a single node in the linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Singly Linked List to store activity/calculation history."""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Adds a new node to the end of the linked list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def to_list(self):
        """Traverses the linked list and returns items as a standard Python list for Jinja2 rendering."""
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

history_list = LinkedList()

# CIPHER HELPER

def run_cipher(text):
    if not text:
        return ""
    return text[::-1]

# PAGES & ROUTES

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        note = request.form.get("message", "").strip()
        if name and email and note:
            message = f"Thanks {name}! I received your message."
        else:
            message = "Please complete all fields."
    return render_template("contact.html", message=message)

@app.route("/works", methods=["GET"])
def works():
    return render_template("works.html")

# ---------- Tool: To Upper Case ----------
@app.route("/tool/touppercase", methods=["GET", "POST"])
def touppercase_tool():
    result = None
    if request.method == "POST":
        input_str = request.form.get("inputString", "")
        result = input_str.upper()
        
        history_list.append(f"To Upper Case: '{input_str}' ➔ '{result}'")

    return render_template("touppercase.html", result=result, history=history_list.to_list())

# ---------- Tool: Area of Circle ----------
@app.route("/works/circle", methods=["GET", "POST"])
def circle_tool():
    result = None
    error = None
    if request.method == "POST":
        try:
            r_raw = request.form.get("radius", "").strip()
            r = float(r_raw)
            if r < 0:
                raise ValueError("Radius must be non-negative.")
            result = round(math.pi * (r ** 2), 4)
 
            history_list.append(f"Area of Circle: r = {r} ➔ Area = {result}")
        except ValueError as e:
            error = str(e)
            
    return render_template("circle.html", result=result, error=error, history=history_list.to_list())

# ---------- Tool: Area of Triangle ----------
@app.route("/works/triangle", methods=["GET", "POST"])
def triangle_tool():
    result = None
    error = None
    if request.method == "POST":
        try:
            b_raw = request.form.get("base", "").strip()
            h_raw = request.form.get("height", "").strip()
            b = float(b_raw)
            h = float(h_raw)
            if b < 0 or h < 0:
                raise ValueError("Base and height must be non-negative.")
            result = round(0.5 * b * h, 4)

            history_list.append(f"Area of Triangle: b = {b}, h = {h} ➔ Area = {result}")
        except ValueError as e:
            error = str(e)
            
    return render_template("triangle.html", result=result, error=error, history=history_list.to_list())

# ---------- Tool: Cipher Project ----------
@app.route("/works/cipher", methods=["GET", "POST"])
def cipher_tool():
    result = None
    expr = None
    if request.method == "POST":
        expr = request.form.get("expression", "")
        result = run_cipher(expr)

        history_list.append(f"Cipher: '{expr}' ➔ '{result}'")
        
    return render_template("cipher.html", result=result, expression=expr, history=history_list.to_list())

if __name__ == "__main__":
    app.run(debug=True)