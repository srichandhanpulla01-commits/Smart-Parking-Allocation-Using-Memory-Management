# Smart Parking Allocation Using Memory Management

## Project Overview

Smart Parking Allocation Using Memory Management is an Operating Systems project that demonstrates memory allocation algorithms through a smart parking prototype.

The Arduino Uno detects a vehicle at the entrance using an ultrasonic sensor. A Python desktop GUI runs the allocation logic and displays the parking blocks. The system demonstrates First Fit, Best Fit, and Worst Fit algorithms, and uses an Arduino-controlled servo motor to simulate an entrance gate.

## Objectives

- Demonstrate First Fit, Best Fit, and Worst Fit memory allocation.
- Model vehicles as processes and parking blocks as memory blocks.
- Demonstrate allocation and deallocation through a graphical interface.
- Integrate an Arduino Uno with a Python application using serial communication.
- Use a servo motor and LEDs to indicate gate and allocation status.

## Technologies Used

- C++
- Python 3
- Tkinter for the desktop GUI
- Arduino Uno and Arduino IDE
- Serial communication using `pyserial`

## Hardware Components

- Arduino Uno
- HC-SR04 ultrasonic distance sensor
- SG90 servo motor
- Green LED and red LED
- Three push buttons
- Breadboard and jumper wires

## Operating System Concepts

| OS concept | Project representation |
|---|---|
| Memory block | Parking block |
| Process | Vehicle |
| Memory request | Required parking capacity |
| Allocation | Assigning a parking block |
| Deallocation | Releasing a parking block when the vehicle leaves |
| First Fit | Select the first suitable free block |
| Best Fit | Select the smallest suitable free block |
| Worst Fit | Select the largest suitable free block |

The demonstration uses parking-block capacities of 30, 50, 70, and 100 units. The required capacity is entered in the GUI; the ultrasonic sensor detects vehicle presence but does not measure the vehicle's full length.

## How It Works

1. The ultrasonic sensor detects a vehicle near the entrance.
2. The Arduino sends a vehicle-detection message to the Python GUI.
3. The user selects First Fit, Best Fit, or Worst Fit using the GUI or the connected buttons.
4. The Python application searches for a suitable free block.
5. If allocation succeeds, the GUI sends a command to the Arduino to open the gate. The green LED indicates success.
6. If allocation fails, the red LED indicates failure.
7. When the vehicle leaves, the user can deallocate its parking block in the GUI.

## Project Files

- `main.cpp` — C++ implementation of the memory-management allocation logic.
- `parking_gui.py` — Python GUI and serial communication with the Arduino.
- `sketch_nov20a/sketch_nov20a.ino` — Arduino sketch, if this is the final sketch used by the project.
- `arduino_test.py` and `gate_test.py` — optional hardware test scripts.
- `project_demo.mp4` — optional project demonstration video.

**Important:** Confirm that `sketch_nov20a/sketch_nov20a.ino` is the final Arduino sketch before submitting. Rename it to `SmartParking.ino` if you prefer, and update this section accordingly.

## Requirements

- Python 3 installed on the computer.
- Arduino IDE.
- Arduino Uno connected to the computer.
- `pyserial` Python package.

Install `pyserial` with:

```bash
python -m pip install pyserial
```

## How to Run

1. Open the Arduino sketch in Arduino IDE.
2. Select the correct board and COM port, then upload the sketch to the Arduino Uno.
3. Close the Arduino IDE Serial Monitor so the Python program can access the serial port.
4. Open `parking_gui.py` and confirm that its configured COM port matches the Arduino's port (for example, `COM9` on the development computer).
5. Run the GUI from a terminal:

   ```bash
   python parking_gui.py
   ```

6. Enter a vehicle ID and required capacity, choose an allocation algorithm, and use Allocate or Deallocate to demonstrate the memory-management process.

## Limitations

- The ultrasonic sensor detects vehicle presence at the entrance; it does not independently measure the vehicle's full length.
- Parking allocation is simulated in the Python GUI rather than performed by an operating system kernel.
- The COM port may differ between computers.

## Project Authors

- G Vishnnu Wardan — CH.SC.U4CYS25009
- P Sri Chandhan — CH.SC.U4CYS25025

## Academic Context

Operating Systems project: **Smart Parking Allocation Using Memory Management**.
