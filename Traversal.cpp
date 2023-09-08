#include <iostream>
#include <vector>

int main() {
    std::vector<int> int_array = {12, 23, 34, 45, 56, 67, 78, 89, 90, 100};
    std::cout << "10 Integers:";
    
    for (int i = 0; i < int_array.size(); ++i) {
        std::cout << " " << int_array[i];
    }
    
    std::cout << std::endl;

    int total = 0;
    for (int i = 0; i < int_array.size(); ++i) {
        std::cout << "Integer " << i + 1 << ": " << int_array[i] << std::endl;
        total += int_array[i];
    }

    std::cout << "Sum of Integers: " << total << std::endl;

    return 0;
}