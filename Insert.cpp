#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::cout << "Old set of Numbers:";
    for (int num : numbers) {
        std::cout << " " << num;
    }
    std::cout << std::endl;

    int new_num = 21;
    numbers.insert(numbers.begin() + 5, new_num);
    
    std::cout << "New set of Numbers:";
    for (int num : numbers) {
        std::cout << " " << num;
    }
    std::cout << std::endl;

    return 0;
}