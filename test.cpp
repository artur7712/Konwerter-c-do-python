#include <iostream>
#include <vector>
#include <map>
using namespace std;



int multiply(int a, int b) {
    return a * b;
}

void printGreeting(string name) {
    cout << "Hello, " << name << "!" << endl;
}

int sumArray(int arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum = sum + arr[i];
    }
    return sum;
}


int main() {
    int a = 5;
    int b = 10;
    int c = multiply(a, b);
    cout << c;

    string names[3];
    names[0] = "Alice";
    names[1] = "Bob";
    names[2] = "Charlie";

    int arr[5];
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 2;
    }

    cout << "Array elements: ";
    for (int i = 0; i < 5; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    cout << "Sum of array: " << sumArray(arr, 5) << endl;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cout << "i: " << i << ", j: " << j << endl;
        }
    }

    for (int i = 0; i < 3; i++) {
        printGreeting(names[i]);
    }

    int x = 0;
    do {
        cout << "Do-while loop, x = " << x << endl;
        x++;
    } while (x < 3);

    if (a > 0 && b < 20) {
        cout << "a is positive and b is less than 20" << endl;
    } else if (c == 50) {
        cout << "c is 50" << endl;
    } else {
        cout << "Default case" << endl;
    }

    return 0;



 }
