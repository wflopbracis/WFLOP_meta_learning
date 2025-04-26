#ifndef GENERATE_NEIGHBORHOOD_H
#define GENERATE_NEIGHBORHOOD_H

#include <vector>
#include <utility>
using namespace std;

vector<vector<int>> build_neighborhood(int number_of_neighbors, vector<pair<double, double>>& lambda_vector, int size_population);

#endif 