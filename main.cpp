#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct ParkingBlock {
    int id;
    int size;
    bool occupied;
    string vehicleID;
};

vector<ParkingBlock> parking = {
    {1, 30, false, ""},
    {2, 50, false, ""},
    {3, 70, false, ""},
    {4, 100, false, ""}
};

// Display parking status
void displayParking() {
    cout << "\n============================================\n";
    cout << "          PARKING BLOCK STATUS\n";
    cout << "============================================\n";

    cout << "Slot\tSize\tStatus\t\tVehicle\n";
    cout << "--------------------------------------------\n";

    for (const auto& block : parking) {
        cout << block.id << "\t"
             << block.size << "\t";

        if (block.occupied)
            cout << "OCCUPIED\t" << block.vehicleID;
        else
            cout << "FREE\t\t-";

        cout << endl;
    }

    cout << "============================================\n";
}

// First Fit
int firstFit(int requiredSize) {

    for (int i = 0; i < parking.size(); i++) {

        if (!parking[i].occupied &&
            parking[i].size >= requiredSize) {

            return i;
        }
    }

    return -1;
}

// Best Fit
int bestFit(int requiredSize) {

    int selected = -1;
    int smallestDifference = 999999;

    for (int i = 0; i < parking.size(); i++) {

        if (!parking[i].occupied &&
            parking[i].size >= requiredSize) {

            int difference = parking[i].size - requiredSize;

            if (difference < smallestDifference) {
                smallestDifference = difference;
                selected = i;
            }
        }
    }

    return selected;
}

// Worst Fit
int worstFit(int requiredSize) {

    int selected = -1;
    int largestSize = -1;

    for (int i = 0; i < parking.size(); i++) {

        if (!parking[i].occupied &&
            parking[i].size >= requiredSize) {

            if (parking[i].size > largestSize) {
                largestSize = parking[i].size;
                selected = i;
            }
        }
    }

    return selected;
}

// Allocate parking
void allocateParking() {

    string vehicleID;
    int requiredSize;
    int algorithm;

    cout << "\nEnter Vehicle ID: ";
    cin >> vehicleID;

    cout << "Enter required parking size: ";
    cin >> requiredSize;

    cout << "\nSelect Allocation Algorithm\n";
    cout << "1. First Fit\n";
    cout << "2. Best Fit\n";
    cout << "3. Worst Fit\n";
    cout << "Enter choice: ";
    cin >> algorithm;

    int selectedSlot = -1;

    if (algorithm == 1)
        selectedSlot = firstFit(requiredSize);

    else if (algorithm == 2)
        selectedSlot = bestFit(requiredSize);

    else if (algorithm == 3)
        selectedSlot = worstFit(requiredSize);

    else {
        cout << "\nInvalid algorithm choice.\n";
        return;
    }

    if (selectedSlot == -1) {

        cout << "\n❌ No suitable parking block available.\n";
        return;
    }

    parking[selectedSlot].occupied = true;
    parking[selectedSlot].vehicleID = vehicleID;

    cout << "\n✅ PARKING ALLOCATED SUCCESSFULLY\n";
    cout << "Vehicle ID : " << vehicleID << endl;
    cout << "Slot       : " << parking[selectedSlot].id << endl;
    cout << "Block Size : " << parking[selectedSlot].size << endl;
}

// Deallocate parking
void deallocateParking() {

    int slot;

    cout << "\nEnter slot number to deallocate: ";
    cin >> slot;

    if (slot < 1 || slot > parking.size()) {
        cout << "\n❌ Invalid slot number.\n";
        return;
    }

    if (!parking[slot - 1].occupied) {
        cout << "\n❌ This slot is already free.\n";
        return;
    }

    cout << "\nVehicle " << parking[slot - 1].vehicleID
         << " has exited.\n";

    parking[slot - 1].occupied = false;
    parking[slot - 1].vehicleID = "";

    cout << "✅ Slot " << slot << " deallocated successfully.\n";
}

// Main menu
int main() {

    int choice;

    cout << "============================================\n";
    cout << "     SMART PARKING ALLOCATION SYSTEM\n";
    cout << "       USING MEMORY MANAGEMENT\n";
    cout << "============================================\n";

    while (true) {

        cout << "\nMAIN MENU\n";
        cout << "1. Display Parking Status\n";
        cout << "2. Allocate Parking\n";
        cout << "3. Deallocate Parking\n";
        cout << "4. Exit\n";

        cout << "\nEnter choice: ";
        cin >> choice;

        switch (choice) {

            case 1:
                displayParking();
                break;

            case 2:
                allocateParking();
                break;

            case 3:
                deallocateParking();
                break;

            case 4:
                cout << "\nExiting system...\n";
                return 0;

            default:
                cout << "\n❌ Invalid choice.\n";
        }
    }
}