import tkinter as tk
from tkinter import messagebox
import serial
import time


# ==================================================
# ARDUINO CONNECTION
# ==================================================

try:
    arduino = serial.Serial("COM9", 9600, timeout=0.1)
    time.sleep(2)
    print("Arduino connected on COM9")
except Exception as e:
    arduino = None
    print("Arduino not connected:", e)


# ==================================================
# PARKING MEMORY BLOCKS
# ==================================================

parking = [
    {"id": 1, "size": 30, "occupied": False, "vehicle": ""},
    {"id": 2, "size": 50, "occupied": False, "vehicle": ""},
    {"id": 3, "size": 70, "occupied": False, "vehicle": ""},
    {"id": 4, "size": 100, "occupied": False, "vehicle": ""}
]


selected_algorithm = "First Fit"
vehicle_detected = False


# ==================================================
# MEMORY ALLOCATION ALGORITHMS
# ==================================================

def first_fit(required):

    for i, block in enumerate(parking):

        if not block["occupied"] and block["size"] >= required:
            return i

    return -1


def best_fit(required):

    selected = -1
    smallest_difference = float("inf")

    for i, block in enumerate(parking):

        if not block["occupied"] and block["size"] >= required:

            difference = block["size"] - required

            if difference < smallest_difference:

                smallest_difference = difference
                selected = i

    return selected


def worst_fit(required):

    selected = -1
    largest_size = -1

    for i, block in enumerate(parking):

        if not block["occupied"] and block["size"] >= required:

            if block["size"] > largest_size:

                largest_size = block["size"]
                selected = i

    return selected


# ==================================================
# SEND COMMAND TO ARDUINO
# ==================================================

def send_to_arduino(command):

    if arduino is not None:

        try:
            arduino.write((command + "\n").encode())
            print("Sent to Arduino:", command)

        except Exception as e:
            print("Arduino send error:", e)


# ==================================================
# ALGORITHM SELECTION
# ==================================================

def select_algorithm(name):

    global selected_algorithm

    selected_algorithm = name

    algorithm_label.config(
        text=f"Selected Algorithm: {name}"
    )


# ==================================================
# HANDLE ARDUINO MESSAGE
# ==================================================

def process_arduino_message(message):

    global vehicle_detected
    global selected_algorithm

    print("Arduino:", message)

    # -----------------------------
    # Vehicle detected
    # -----------------------------

    if message == "VEHICLE_DETECTED":

        vehicle_detected = True

        status_label.config(
            text="🚗 VEHICLE DETECTED - Select algorithm",
            fg="#2980b9"
        )


    # -----------------------------
    # Vehicle left
    # -----------------------------

    elif message == "VEHICLE_LEFT":

        vehicle_detected = False

        status_label.config(
            text="No vehicle detected",
            fg="black"
        )


    # -----------------------------
    # Physical First Fit button
    # -----------------------------

    elif message == "FIRST_FIT":

        select_algorithm("First Fit")

        status_label.config(
            text="First Fit selected from hardware",
            fg="#2980b9"
        )


    # -----------------------------
    # Physical Best Fit button
    # -----------------------------

    elif message == "BEST_FIT":

        select_algorithm("Best Fit")

        status_label.config(
            text="Best Fit selected from hardware",
            fg="#2980b9"
        )


    # -----------------------------
    # Physical Worst Fit button
    # -----------------------------

    elif message == "WORST_FIT":

        select_algorithm("Worst Fit")

        status_label.config(
            text="Worst Fit selected from hardware",
            fg="#2980b9"
        )


    # -----------------------------
    # Gate opening
    # -----------------------------

    elif message == "GATE_OPENING":

        status_label.config(
            text="🟢 Allocation successful - Gate opening",
            fg="#27ae60"
        )


    # -----------------------------
    # Gate closed
    # -----------------------------

    elif message == "GATE_CLOSED":

        status_label.config(
            text="Gate closed - Parking allocated",
            fg="#27ae60"
        )


# ==================================================
# CHECK ARDUINO
# ==================================================

def check_arduino():

    if arduino is not None:

        try:

            while arduino.in_waiting:

                message = arduino.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if message:
                    process_arduino_message(message)

        except Exception as e:

            print("Arduino error:", e)

    root.after(100, check_arduino)


# ==================================================
# UPDATE PARKING DISPLAY
# ==================================================

def update_display():

    for i, block in enumerate(parking):

        if block["occupied"]:

            slot_buttons[i].config(
                text=f"SLOT {block['id']}\n"
                     f"{block['size']} units\n"
                     f"OCCUPIED\n"
                     f"{block['vehicle']}",
                bg="#e74c3c",
                fg="white"
            )

        else:

            slot_buttons[i].config(
                text=f"SLOT {block['id']}\n"
                     f"{block['size']} units\n"
                     f"AVAILABLE",
                bg="#2ecc71",
                fg="white"
            )

    available = sum(
        1 for block in parking
        if not block["occupied"]
    )

    occupied = len(parking) - available

    status_label.config(
        text=f"Available: {available}     Occupied: {occupied}"
    )


# ==================================================
# ALLOCATE PARKING
# ==================================================

def allocate():

    global vehicle_detected

    vehicle_id = vehicle_entry.get().strip()

    # ------------------------------------------
    # Vehicle ID validation
    # ------------------------------------------

    if vehicle_id == "":

        messagebox.showerror(
            "Invalid Input",
            "Enter Vehicle ID."
        )

        return


    # ------------------------------------------
    # Required space validation
    # ------------------------------------------

    try:

        required = int(size_entry.get())

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Enter a valid vehicle size."
        )

        return


    if required <= 0:

        messagebox.showerror(
            "Invalid Input",
            "Vehicle size must be greater than zero."
        )

        return


    # ------------------------------------------
    # Check vehicle
    # ------------------------------------------

    if arduino is not None and not vehicle_detected:

        messagebox.showwarning(
            "No Vehicle",
            "No vehicle is currently detected."
        )

        return


    # ------------------------------------------
    # Select algorithm
    # ------------------------------------------

    if selected_algorithm == "First Fit":

        index = first_fit(required)

    elif selected_algorithm == "Best Fit":

        index = best_fit(required)

    else:

        index = worst_fit(required)


    # ------------------------------------------
    # Allocation failed
    # ------------------------------------------

    if index == -1:

        send_to_arduino("ALLOCATION_FAILED")

        messagebox.showwarning(
            "Allocation Failed",
            "No suitable parking block is available."
        )

        status_label.config(
            text="🔴 Allocation failed - No suitable block",
            fg="#e74c3c"
        )

        return


    # ------------------------------------------
    # Allocate memory block
    # ------------------------------------------

    parking[index]["occupied"] = True
    parking[index]["vehicle"] = vehicle_id


    # ------------------------------------------
    # Tell Arduino to open gate
    # ------------------------------------------

    send_to_arduino("OPEN_GATE")


    # ------------------------------------------
    # Show result
    # ------------------------------------------

    messagebox.showinfo(
        "Allocation Successful",

        f"Vehicle: {vehicle_id}\n"
        f"Allocated Slot: {parking[index]['id']}\n"
        f"Block Size: {parking[index]['size']} units\n"
        f"Algorithm: {selected_algorithm}"
    )


    vehicle_entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)

    update_display()


# ==================================================
# DEALLOCATE PARKING
# ==================================================

def deallocate():

    vehicle_id = vehicle_entry.get().strip()

    if vehicle_id == "":

        messagebox.showerror(
            "Input Required",
            "Enter the Vehicle ID to deallocate."
        )

        return


    for block in parking:

        if block["occupied"] and block["vehicle"] == vehicle_id:

            block["occupied"] = False
            block["vehicle"] = ""


            messagebox.showinfo(
                "Deallocation Successful",

                f"Vehicle {vehicle_id} has exited.\n"
                f"Slot {block['id']} is now available."
            )


            vehicle_entry.delete(0, tk.END)

            update_display()

            return


    messagebox.showwarning(
        "Vehicle Not Found",
        "No occupied slot was found for this Vehicle ID."
    )


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()

root.title("Smart Parking Allocation System")
root.geometry("900x700")
root.configure(bg="#f4f6f7")


# ==================================================
# TITLE
# ==================================================

title = tk.Label(
    root,
    text="SMART PARKING ALLOCATION SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#1f2937",
    fg="white",
    pady=15
)

title.pack(fill="x")


subtitle = tk.Label(
    root,
    text="Using Operating System Memory Management",
    font=("Arial", 14),
    bg="#f4f6f7",
    fg="#34495e"
)

subtitle.pack(pady=10)


# ==================================================
# VEHICLE INPUT
# ==================================================

input_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="groove"
)

input_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    input_frame,
    text="Vehicle ID:",
    font=("Arial", 12, "bold"),
    bg="white"
).grid(
    row=0,
    column=0,
    padx=15,
    pady=15
)


vehicle_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=20
)

vehicle_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Label(
    input_frame,
    text="Required Space:",
    font=("Arial", 12, "bold"),
    bg="white"
).grid(
    row=0,
    column=2,
    padx=15
)


size_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=15
)

size_entry.grid(
    row=0,
    column=3,
    padx=10
)


tk.Label(
    input_frame,
    text="units",
    bg="white",
    font=("Arial", 11)
).grid(
    row=0,
    column=4
)


# ==================================================
# ALGORITHM SECTION
# ==================================================

algorithm_frame = tk.Frame(
    root,
    bg="#f4f6f7"
)

algorithm_frame.pack(pady=10)


tk.Label(
    algorithm_frame,
    text="SELECT MEMORY ALLOCATION ALGORITHM",
    font=("Arial", 13, "bold"),
    bg="#f4f6f7"
).pack()


button_frame = tk.Frame(
    algorithm_frame,
    bg="#f4f6f7"
)

button_frame.pack(pady=8)


tk.Button(
    button_frame,
    text="FIRST FIT",
    width=15,
    font=("Arial", 11, "bold"),
    command=lambda: select_algorithm("First Fit")
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    button_frame,
    text="BEST FIT",
    width=15,
    font=("Arial", 11, "bold"),
    command=lambda: select_algorithm("Best Fit")
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    button_frame,
    text="WORST FIT",
    width=15,
    font=("Arial", 11, "bold"),
    command=lambda: select_algorithm("Worst Fit")
).grid(
    row=0,
    column=2,
    padx=5
)


algorithm_label = tk.Label(
    root,
    text="Selected Algorithm: First Fit",
    font=("Arial", 12, "bold"),
    bg="#f4f6f7",
    fg="#2980b9"
)

algorithm_label.pack(pady=5)


# ==================================================
# PARKING BLOCKS
# ==================================================

tk.Label(
    root,
    text="PARKING MEMORY BLOCKS",
    font=("Arial", 16, "bold"),
    bg="#f4f6f7"
).pack(pady=10)


parking_frame = tk.Frame(
    root,
    bg="#f4f6f7"
)

parking_frame.pack()


slot_buttons = []


for i in range(len(parking)):

    button = tk.Button(
        parking_frame,
        text="",
        width=18,
        height=5,
        font=("Arial", 11, "bold"),
        relief="raised"
    )

    button.grid(
        row=0,
        column=i,
        padx=8,
        pady=10
    )

    slot_buttons.append(button)


# ==================================================
# ACTION BUTTONS
# ==================================================

action_frame = tk.Frame(
    root,
    bg="#f4f6f7"
)

action_frame.pack(pady=15)


tk.Button(
    action_frame,
    text="ALLOCATE PARKING",
    width=20,
    height=2,
    font=("Arial", 12, "bold"),
    bg="#3498db",
    fg="white",
    command=allocate
).grid(
    row=0,
    column=0,
    padx=10
)


tk.Button(
    action_frame,
    text="DEALLOCATE PARKING",
    width=20,
    height=2,
    font=("Arial", 12, "bold"),
    bg="#e67e22",
    fg="white",
    command=deallocate
).grid(
    row=0,
    column=1,
    padx=10
)


# ==================================================
# STATUS
# ==================================================

status_label = tk.Label(
    root,
    text="Available: 4     Occupied: 0",
    font=("Arial", 13, "bold"),
    bg="#f4f6f7"
)

status_label.pack(pady=10)


# ==================================================
# START
# ==================================================

update_display()

root.after(100, check_arduino)

root.mainloop()