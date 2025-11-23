//
// Created by konov on 11/23/2025.
//

#ifndef HMW_3_UTILS_HPP
#define HMW_3_UTILS_HPP

#include <vector>
#include <numeric>
#include <algorithm>
#include <cmath>

bool hasEulerCycle(const std::vector<size_t>& in_deg, const std::vector<size_t>& out_deg);
bool hasEulerPath(const std::vector<size_t>& in_deg, const std::vector<size_t>& out_deg);
std::vector<size_t> getEulerCycle(std::vector<std::vector<size_t>> adj);
std::vector<size_t> getEulerPath(std::vector<std::vector<size_t>> adj);

#endif //HMW_3_UTILS_HPP