from tkinter import filedialog
from tkinter import *
import subprocess as sub
import datetime
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# Instantiating a window
window = Tk()

event_log:StringVar = StringVar(window, "example.xes")

dcr_graph:StringVar = StringVar(window, "DCRGraph.xml")
# Add a title to the window
window.title("DCR graphs conformance checker")

result = Text(window, width=80)


# Define Window functions
def run_conformance_checking_callback():
    """
    Runs conformance checking and shows output in Text of window
    :return:
    """
    event_log_arg = '--eventLog \"{0}\"'.format(event_log.get())
    dcr_graph_arg = '--XmlDcr \"{0}\"'.format(dcr_graph.get())
    command = 'python ../conformancechecker/cc_dcr.py {0} {1}'.format(event_log_arg, dcr_graph_arg)
    process = sub.Popen(command, stdout=sub.PIPE, shell=True)
    output, code = process.communicate()
    result.insert(END, output)


def browse_event_log():
    """
    Initiates file browsing for an event log file
    :return:
    """
    global event_log
    event_log.set(filedialog.askopenfilename(initialdir=dir_path, title="Select event log .xes"))


def browse_dcr_graph():
    """
    Initiates file browsing for a DCR graph
    :return:
    """
    global dcr_graph
    dcr_graph.set(filedialog.askopenfilename(initialdir=dir_path, title="Select DCR graph .xml"))


# Instantiate Buttons
run_button = Button(window, text='Run Conformance Checking', command=run_conformance_checking_callback)
exit_button = Button(window, text='Exit', command=window.quit())

# Set parameters for Conformance checking
# 1. Name of analysis
name = StringVar()
name.set(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S_DCR_CC_run'))
name_entry = Entry(window, bd=5, width=40, textvariable=name)
name_entry_label = Label(window, text="Enter name of analysis")

# 2. Choose location of event log
event_log_label = Label(window, text="Choose event-log")
event_log_entry = Entry(window, bd=5, width=40, textvariable=event_log)
event_log_button = Button(window, text="Browse", command=browse_event_log)

# 3. Choose location of DCR Graph XML
dcr_graph_label = Label(window, text="Choose DCR graph")
dcr_graph_entry = Entry(window, bd=5, width=40, textvariable=dcr_graph)
dcr_graph_button = Button(window, text="Browse", command=browse_dcr_graph)

# 4. Result
result_label = Label(window, text="Conformance Checking Results")

# Place everything in the window
event_log_label.grid(row=1, column=0)
event_log_entry.grid(row=1, column=1)
event_log_button.grid(row=1, column=2)
dcr_graph_label.grid(row=2, column=0)
dcr_graph_entry.grid(row=2, column=1)
dcr_graph_button.grid(row=2, column=2)
run_button.grid(row=3, column=1)
exit_button.grid(row=3, column=0)
name_entry_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
result_label.grid(row=4, column=0)
result.grid(row=4, column=1, columnspan=5)

window.mainloop()
