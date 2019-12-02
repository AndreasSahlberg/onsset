"""
This script produces the summary analysis required to provide input data for the OSeMOSYS soft-link
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from runner import *

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)