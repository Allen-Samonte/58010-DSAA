#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers = {5, 4, 3, 2, 1};
    
    std::cout << "Not yet reversed:";
    for (int num : numbers) {
        std::cout << " " << num;
    }
    std::cout << std::endl;

    std::reverse(numbers.begin(), numbers.end());

    std::cout << "Reversed numbers:";
    for (int num : numbers) {
        std::cout << " " << num;
    }
    std::cout << std::endl;

    return 0;
}
