"""Generate the sample knowledge-base PDF: knowledge_base/python_learning_guide.pdf

Run from the backend folder:
    python scripts/generate_sample_pdf.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    CondPageBreak,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "knowledge_base" / "python_learning_guide.pdf"
DOCUMENT_TITLE = "Python Programming – Student Learning Guide"
BRAND_ORANGE = colors.HexColor("#F07C00")
BRAND_DARK = colors.HexColor("#2B2B2B")

# Each topic is a list of blocks: ("p", text), ("h3", text), ("code", text), ("bullets", [items])
TOPICS = [
    ("1. Introduction to Python", [
        ("p", "Python is a high-level, general-purpose programming language created by Guido van Rossum "
              "and first released in 1991. It is designed to be easy to read and easy to write. Python code "
              "looks close to plain English, which is why it is one of the most popular first languages for "
              "students."),
        ("p", "Python is an interpreted language. This means you do not need to compile your program before "
              "running it. The Python interpreter reads your code line by line and executes it immediately. "
              "This makes it quick to test small ideas and learn by experimenting."),
        ("h3", "Where is Python used?"),
        ("bullets", [
            "Web development (Django, Flask, FastAPI)",
            "Data analysis and visualisation (pandas, Matplotlib)",
            "Artificial Intelligence and Machine Learning (scikit-learn, TensorFlow, PyTorch)",
            "Automation and scripting of everyday tasks",
            "Software testing, desktop applications and games",
        ]),
        ("h3", "Your first Python program"),
        ("code", 'print("Hello, World!")\n# Output: Hello, World!'),
        ("p", "The print() function displays text on the screen. Lines that start with # are comments. "
              "Python ignores comments; they are notes written for humans who read the code."),
    ]),
    ("2. Features of Python", [
        ("p", "Python has several features that make it popular with beginners and professionals alike."),
        ("bullets", [
            "<b>Simple and readable syntax:</b> Python uses indentation (spaces) instead of curly braces to "
            "group code, which keeps programs clean and readable.",
            "<b>Interpreted:</b> Code runs line by line, so errors are reported where they happen.",
            "<b>Dynamically typed:</b> You do not declare variable types. Python works out the type when the "
            "program runs.",
            "<b>Free and open source:</b> Anyone can download, use and share Python at no cost.",
            "<b>Cross-platform:</b> The same Python program runs on Windows, macOS and Linux.",
            "<b>Large standard library:</b> Python comes with ready-made modules for files, dates, maths, "
            "networking and much more – often described as 'batteries included'.",
            "<b>Object-oriented:</b> Python supports classes and objects, but you can also write simple "
            "procedural code.",
            "<b>Huge community:</b> Thousands of third-party packages are available through pip.",
        ]),
        ("h3", "Example: readable syntax"),
        ("code", "marks = 82\nif marks >= 40:\n    print(\"Pass\")\nelse:\n    print(\"Fail\")"),
    ]),
    ("3. Python Installation", [
        ("p", "To start programming, install Python 3 from the official website python.org. Always choose "
              "the latest stable Python 3 version."),
        ("h3", "Installing on Windows"),
        ("bullets", [
            "Download the Windows installer from python.org/downloads.",
            "Run the installer and tick the box <b>'Add Python to PATH'</b> before clicking Install Now.",
            "Open Command Prompt and type <font face='Courier'>python --version</font> to confirm.",
        ]),
        ("h3", "Installing on macOS"),
        ("bullets", [
            "Download the macOS installer from python.org/downloads and run it, or use Homebrew: "
            "<font face='Courier'>brew install python</font>.",
            "Open Terminal and type <font face='Courier'>python3 --version</font> to confirm.",
        ]),
        ("h3", "Running Python code"),
        ("p", "You can run Python in two ways. The <b>interactive shell</b> (type python or python3 in a "
              "terminal) runs one line at a time and is great for quick experiments. A <b>script file</b> "
              "ends with .py and is run with a command such as:"),
        ("code", "python hello.py      # Windows\npython3 hello.py     # macOS / Linux"),
        ("p", "pip is Python's package installer. It downloads extra libraries, for example: "
              "<font face='Courier'>pip install requests</font>."),
    ]),
    ("4. Python Variables", [
        ("p", "A variable is a name that stores a value in memory so you can use it later. In Python you "
              "create a variable simply by assigning a value with the = sign. There is no need to declare "
              "its type first."),
        ("code", 'student_name = "Ravi"\nage = 20\nheight = 5.8\nis_enrolled = True'),
        ("h3", "Rules for variable names"),
        ("bullets", [
            "A name must start with a letter or an underscore (_), not a number.",
            "It can contain only letters, numbers and underscores.",
            "Names are case-sensitive: age, Age and AGE are three different variables.",
            "Python keywords such as if, for, class and def cannot be used as names.",
        ]),
        ("h3", "Multiple assignment and dynamic typing"),
        ("code", "x, y, z = 1, 2, 3\na = b = 0\n\nvalue = 10        # value is an int\nvalue = \"ten\"     # now value is a str"),
        ("p", "Because Python is dynamically typed, the same variable can later hold a value of a different "
              "type. Use the type() function to check the type of any value: "
              "<font face='Courier'>type(age)</font> returns &lt;class 'int'&gt;."),
    ]),
    ("5. Python Data Types", [
        ("p", "A data type tells Python what kind of value a variable holds and what operations are "
              "allowed on it. The main built-in data types are:"),
        ("bullets", [
            "<b>int</b> – whole numbers, for example 10, -3, 2024",
            "<b>float</b> – decimal numbers, for example 3.14, -0.5",
            "<b>complex</b> – complex numbers, for example 2 + 3j",
            "<b>str</b> – text, for example \"Python\"",
            "<b>bool</b> – True or False",
            "<b>list</b> – ordered, changeable collection: [1, 2, 3]",
            "<b>tuple</b> – ordered, unchangeable collection: (1, 2, 3)",
            "<b>dict</b> – key-value pairs: {\"name\": \"Asha\"}",
            "<b>set</b> – unordered collection of unique items: {1, 2, 3}",
            "<b>NoneType</b> – the special value None, meaning 'no value'",
        ]),
        ("h3", "Type conversion"),
        ("p", "You can convert between types using functions such as int(), float(), str() and bool(). "
              "This is called type casting."),
        ("code", 'age_text = "21"\nage = int(age_text)      # 21 (int)\nprice = float("99.5")    # 99.5\nlabel = str(100)         # "100"\nprint(type(price))       # <class \'float\'>'),
        ("p", "Data types can be grouped as <b>mutable</b> (can be changed after creation: list, dict, set) "
              "and <b>immutable</b> (cannot be changed: int, float, str, tuple, bool)."),
    ]),
    ("6. Strings", [
        ("p", "A string is a sequence of characters enclosed in single quotes, double quotes or triple "
              "quotes. Strings are immutable, which means their characters cannot be changed in place."),
        ("code", 'course = "Python"\nmessage = \'Welcome to VPro Skills\'\nparagraph = """This string\nspans multiple lines."""'),
        ("h3", "Indexing and slicing"),
        ("p", "Each character has a position called an index, starting at 0. Negative indexes count from "
              "the end. Slicing extracts part of a string using [start:end]."),
        ("code", 'word = "Python"\nprint(word[0])     # P\nprint(word[-1])    # n\nprint(word[0:3])   # Pyt\nprint(len(word))   # 6'),
        ("h3", "Common string methods"),
        ("code", 'name = "  vpro skills  "\nprint(name.strip())          # "vpro skills"\nprint(name.upper())          # "  VPRO SKILLS  "\nprint("a,b,c".split(","))    # [\'a\', \'b\', \'c\']\nprint("Hi Ravi".replace("Ravi", "Asha"))'),
        ("h3", "f-strings"),
        ("p", "f-strings are the easiest way to put variables inside text."),
        ("code", 'name = "Asha"\nscore = 95\nprint(f"{name} scored {score} marks")'),
    ]),
    ("7. Lists", [
        ("p", "A list is an ordered, mutable collection of items written inside square brackets. A list "
              "can hold values of different types and can grow or shrink while the program runs."),
        ("code", 'fruits = ["apple", "banana", "mango"]\nmixed = [1, "two", 3.0, True]'),
        ("h3", "Accessing and changing items"),
        ("code", 'print(fruits[0])        # apple\nfruits[1] = "grapes"    # lists are mutable\nprint(fruits)           # [\'apple\', \'grapes\', \'mango\']'),
        ("h3", "Useful list methods"),
        ("bullets", [
            "append(x) – add an item to the end",
            "insert(i, x) – add an item at position i",
            "remove(x) – remove the first matching item",
            "pop() – remove and return the last item",
            "sort() – sort the list in place",
            "len(list) – number of items",
        ]),
        ("code", "numbers = [5, 2, 9]\nnumbers.append(1)\nnumbers.sort()\nprint(numbers)          # [1, 2, 5, 9]"),
        ("h3", "List comprehension"),
        ("p", "A list comprehension builds a new list in a single readable line."),
        ("code", "squares = [n * n for n in range(1, 6)]\nprint(squares)          # [1, 4, 9, 16, 25]"),
    ]),
    ("8. Tuples", [
        ("p", "A tuple is an ordered collection like a list, but it is <b>immutable</b>: once created, its "
              "items cannot be added, removed or changed. Tuples are written with round brackets."),
        ("code", 'point = (10, 20)\ncolours = ("red", "green", "blue")\nsingle = ("only",)     # a one-item tuple needs a comma'),
        ("p", "Tuples support indexing and slicing just like lists, and they are slightly faster and use "
              "less memory. Use a tuple for data that should not change, such as coordinates or the days of "
              "the week."),
        ("code", "x, y = point          # tuple unpacking\nprint(x, y)           # 10 20\n# point[0] = 5  ->  TypeError: 'tuple' object does not support item assignment"),
        ("h3", "Difference between List and Tuple"),
        ("bullets", [
            "<b>Syntax:</b> a list uses square brackets [ ]; a tuple uses round brackets ( ).",
            "<b>Mutability:</b> a list is mutable (can be changed); a tuple is immutable (cannot be changed).",
            "<b>Methods:</b> lists have many methods (append, remove, sort); tuples only have count() and index().",
            "<b>Performance:</b> tuples are faster and use less memory than lists.",
            "<b>Use case:</b> use a list for data that changes; use a tuple for fixed data. Tuples can also be "
            "used as dictionary keys, lists cannot.",
        ]),
    ]),
    ("9. Dictionaries", [
        ("p", "A dictionary stores data as <b>key-value pairs</b> inside curly braces. Each key must be "
              "unique and immutable (for example a string or number). Dictionaries are mutable and keep "
              "items in the order they were inserted."),
        ("code", 'student = {\n    "name": "Ravi",\n    "age": 20,\n    "course": "Python"\n}'),
        ("h3", "Reading, adding and removing values"),
        ("code", 'print(student["name"])            # Ravi\nprint(student.get("city", "N/A")) # N/A (safe access)\nstudent["city"] = "Hyderabad"     # add a new key\nstudent["age"] = 21               # update a value\ndel student["course"]             # remove a key'),
        ("h3", "Looping through a dictionary"),
        ("code", "for key, value in student.items():\n    print(key, \"->\", value)"),
        ("p", "Other helpful methods are keys(), values(), items(), update() and pop(). Dictionaries are "
              "ideal when you want to look up information by a meaningful name instead of a position."),
    ]),
    ("10. Sets", [
        ("p", "A set is an unordered collection of <b>unique</b> items written inside curly braces. "
              "Duplicate values are removed automatically. Sets are mutable, but their items must be "
              "immutable, and items cannot be accessed by index."),
        ("code", "numbers = {1, 2, 3, 3, 2}\nprint(numbers)      # {1, 2, 3}\nempty = set()       # {} creates an empty dict, not a set"),
        ("h3", "Set operations"),
        ("code", "a = {1, 2, 3, 4}\nb = {3, 4, 5}\nprint(a | b)   # union        {1, 2, 3, 4, 5}\nprint(a & b)   # intersection {3, 4}\nprint(a - b)   # difference   {1, 2}\nprint(a ^ b)   # symmetric difference {1, 2, 5}"),
        ("p", "Use add() to insert an item and remove() or discard() to delete one. A common practical use "
              "of a set is removing duplicates from a list: <font face='Courier'>unique = list(set(items))</font>."),
    ]),
    ("11. Conditional Statements", [
        ("p", "Conditional statements let a program make decisions. Python uses if, elif (else if) and "
              "else. The code that belongs to each branch must be indented."),
        ("code", 'marks = 72\n\nif marks >= 90:\n    grade = "A"\nelif marks >= 75:\n    grade = "B"\nelif marks >= 50:\n    grade = "C"\nelse:\n    grade = "Fail"\n\nprint("Grade:", grade)   # Grade: C'),
        ("h3", "Comparison and logical operators"),
        ("bullets", [
            "Comparison: == (equal), != (not equal), &gt;, &lt;, &gt;=, &lt;=",
            "Logical: and (both true), or (at least one true), not (reverses the result)",
        ]),
        ("code", 'age = 19\nhas_id = True\nif age >= 18 and has_id:\n    print("Entry allowed")'),
        ("h3", "Conditional expression (ternary)"),
        ("code", 'status = "Adult" if age >= 18 else "Minor"'),
    ]),
    ("12. Loops", [
        ("p", "Loops repeat a block of code. Python has two loops: the <b>for</b> loop and the "
              "<b>while</b> loop."),
        ("h3", "for loop"),
        ("p", "A for loop goes through each item of a sequence such as a list, string or range."),
        ("code", 'for i in range(1, 6):\n    print(i)            # 1 2 3 4 5\n\nfor fruit in ["apple", "mango"]:\n    print(fruit)'),
        ("h3", "while loop"),
        ("p", "A while loop keeps running as long as its condition is True. Make sure the condition "
              "eventually becomes False, or the loop will run forever."),
        ("code", "count = 1\nwhile count <= 3:\n    print(\"Count:\", count)\n    count += 1"),
        ("h3", "break, continue and pass"),
        ("bullets", [
            "<b>break</b> stops the loop immediately.",
            "<b>continue</b> skips the rest of the current iteration and moves to the next one.",
            "<b>pass</b> does nothing; it is a placeholder where code is required.",
        ]),
        ("code", "for n in range(10):\n    if n == 5:\n        break\n    if n % 2 == 0:\n        continue\n    print(n)            # 1 3"),
    ]),
    ("13. Functions", [
        ("p", "A function is a reusable block of code that performs a specific task. Functions help you "
              "avoid repeating code and make programs easier to read and test. Define a function with the "
              "<b>def</b> keyword."),
        ("code", 'def greet(name):\n    """Return a greeting message."""\n    return f"Hello, {name}!"\n\nprint(greet("Asha"))     # Hello, Asha!'),
        ("h3", "Parameters and arguments"),
        ("bullets", [
            "<b>Parameters</b> are the names listed in the function definition.",
            "<b>Arguments</b> are the actual values passed when calling the function.",
            "<b>Default parameters</b> provide a value if none is given.",
            "<b>Keyword arguments</b> are passed by name, so order does not matter.",
        ]),
        ("code", 'def total_price(price, quantity=1, discount=0):\n    return price * quantity - discount\n\nprint(total_price(100))                    # 100\nprint(total_price(100, quantity=3, discount=50))  # 250'),
        ("h3", "*args, **kwargs and lambda"),
        ("code", "def add_all(*numbers):\n    return sum(numbers)\n\nprint(add_all(1, 2, 3))   # 6\n\nsquare = lambda x: x * x  # a small anonymous function\nprint(square(4))          # 16"),
        ("p", "The return statement sends a value back to the caller. A function without return gives "
              "back None."),
    ]),
    ("14. Object-Oriented Programming", [
        ("p", "Object-Oriented Programming (OOP, often called OOPS) is a way of organising code around "
              "<b>objects</b>. A <b>class</b> is a blueprint, and an <b>object</b> is an instance created from "
              "that blueprint. Objects combine data (attributes) and behaviour (methods)."),
        ("code", 'class Student:\n    def __init__(self, name, course):\n        self.name = name          # attribute\n        self.course = course\n\n    def introduce(self):          # method\n        return f"I am {self.name}, learning {self.course}."\n\nravi = Student("Ravi", "Python")\nprint(ravi.introduce())'),
        ("p", "__init__ is the constructor; it runs automatically when an object is created. self refers "
              "to the current object."),
        ("h3", "The four pillars of OOP"),
        ("bullets", [
            "<b>Encapsulation:</b> bundling data and methods together and hiding internal details "
            "(for example using a leading underscore, _balance).",
            "<b>Inheritance:</b> a child class reuses and extends the code of a parent class.",
            "<b>Polymorphism:</b> different classes provide their own version of the same method name.",
            "<b>Abstraction:</b> showing only essential features and hiding complex implementation.",
        ]),
        ("h3", "Inheritance example"),
        ("code", 'class Animal:\n    def speak(self):\n        return "Some sound"\n\nclass Dog(Animal):\n    def speak(self):              # overriding = polymorphism\n        return "Woof!"\n\nprint(Dog().speak())   # Woof!'),
    ]),
    ("15. Exception Handling", [
        ("p", "An exception is an error that happens while a program is running, such as dividing by zero "
              "or opening a missing file. Without handling, the program stops with an error message. "
              "Exception handling lets the program respond gracefully instead of crashing."),
        ("h3", "try, except, else and finally"),
        ("code", 'try:\n    number = int(input("Enter a number: "))\n    result = 100 / number\nexcept ValueError:\n    print("Please enter a valid number.")\nexcept ZeroDivisionError:\n    print("Cannot divide by zero.")\nelse:\n    print("Result:", result)      # runs only if no error\nfinally:\n    print("Done.")                # always runs'),
        ("h3", "Common built-in exceptions"),
        ("bullets", [
            "ValueError – a value has the right type but an invalid content",
            "TypeError – an operation is used on the wrong type",
            "ZeroDivisionError – division by zero",
            "IndexError – a list index is out of range",
            "KeyError – a dictionary key does not exist",
            "FileNotFoundError – a file cannot be found",
        ]),
        ("h3", "Raising your own exceptions"),
        ("code", 'def set_age(age):\n    if age < 0:\n        raise ValueError("Age cannot be negative")\n    return age'),
        ("p", "Good practice: catch specific exceptions rather than using a bare except, and keep the code "
              "inside try blocks as small as possible."),
    ]),
]


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontSize=26, leading=32,
                                textColor=BRAND_DARK, alignment=TA_CENTER, spaceAfter=12),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontSize=13, leading=18,
                                   textColor=BRAND_ORANGE, alignment=TA_CENTER, spaceAfter=30),
        "h2": ParagraphStyle("H2", parent=base["Heading1"], fontSize=18, leading=22,
                             textColor=BRAND_ORANGE, spaceBefore=16, spaceAfter=8, keepWithNext=1),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontSize=12.5, leading=16,
                             textColor=BRAND_DARK, spaceBefore=10, spaceAfter=4, keepWithNext=1),
        "p": ParagraphStyle("Body", parent=base["BodyText"], fontSize=10.5, leading=15, spaceAfter=6),
        "code": ParagraphStyle("Code", parent=base["Code"], fontSize=9, leading=12.5),
    }


def code_box(code_text, style):
    """Grey box around a code example; a one-cell table is never split across pages."""
    box = Table([[Preformatted(code_text, style)]], colWidths=["100%"])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F4F4")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("LINEBEFORE", (0, 0), (0, -1), 3, BRAND_ORANGE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    box.spaceBefore, box.spaceAfter = 4, 10
    return box


def draw_page_frame(canvas, doc):
    """Header line and page-number footer on every page."""
    width, height = A4
    canvas.saveState()
    canvas.setStrokeColor(BRAND_ORANGE)
    canvas.setLineWidth(1.5)
    canvas.line(2 * cm, height - 1.5 * cm, width - 2 * cm, height - 1.5 * cm)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, height - 1.3 * cm, "VPro Skills EduTech")
    canvas.drawRightString(width - 2 * cm, height - 1.3 * cm, DOCUMENT_TITLE)
    canvas.drawCentredString(width / 2, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_story(styles):
    story = [
        Spacer(1, 5 * cm),
        Paragraph(DOCUMENT_TITLE, styles["title"]),
        Paragraph("VPro Skills EduTech · www.vproskills.com", styles["subtitle"]),
        Paragraph("This guide introduces the core concepts of Python programming in simple language, "
                  "with practical code examples for every topic. Read each section, then try the "
                  "examples yourself in the Python shell.", styles["p"]),
        Spacer(1, 0.6 * cm),
        Paragraph("Contents", styles["h3"]),
        ListFlowable([ListItem(Paragraph(title, styles["p"])) for title, _ in TOPICS],
                     bulletType="bullet", start="•", leftIndent=14),
        PageBreak(),
    ]
    for title, blocks in TOPICS:
        story.append(CondPageBreak(6 * cm))  # avoid a heading stranded at the bottom of a page
        story.append(Paragraph(title, styles["h2"]))
        for kind, content in blocks:
            if kind == "code":
                story.append(code_box(content, styles["code"]))
            elif kind == "bullets":
                story.append(ListFlowable(
                    [ListItem(Paragraph(item, styles["p"])) for item in content],
                    bulletType="bullet", start="•", leftIndent=14))
            else:
                story.append(Paragraph(content, styles[kind]))
    return story


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT_PATH), pagesize=A4, title=DOCUMENT_TITLE, author="VPro Skills EduTech",
                            leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2.2 * cm, bottomMargin=2 * cm)
    doc.build(build_story(build_styles()), onFirstPage=draw_page_frame, onLaterPages=draw_page_frame)
    print(f"Created {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
