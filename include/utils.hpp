//
// Created by konov on 11/23/2025.
//

#ifndef HMW_3_UTILS_HPP
#define HMW_3_UTILS_HPP

#include <vector>
#include <numeric>
#include <algorithm>
#include <cmath>

bool hasEulerCycle(const vector<vector<size_t>>& adj);
bool hasEulerPath(const vector<vector<size_t>>& adj);
vector<size_t> getEulerCycle(vector<vector<size_t>> adj);
vector<size_t> getEulerPath(vector<vector<size_t>> adj);

#endif //HMW_3_UTILS_HPP