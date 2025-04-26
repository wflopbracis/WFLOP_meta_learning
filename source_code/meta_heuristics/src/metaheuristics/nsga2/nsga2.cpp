#include <iostream>
#include <ctime> 
#include <cstdlib>
#include <utility> 
#include <random>
#include "../../../headers/global_modules/generate_initial_population/population.h"
#include "../../../headers/global_modules/generate_initial_population/generate_rSolution.h"
#include "../../../headers/global_modules/genetic_operators/mutation.h"
#include "../../../headers/global_modules/genetic_operators/crossover.h"
#include "../../../headers/metaheuristics/nsga2/modules/binary_tournament.h"
#include "../../../headers/metaheuristics/nsga2/modules/crowding_distance.h"
#include "../../../headers/metaheuristics/nsga2/modules/non_dominated_sorting.h"
#include "../../../headers/metaheuristics/nsga2/modules/arena_non_dominated_sorting.h"


#include "../../../headers/global_modules/dominates.h"
#include "../../../headers/global_modules/isEqual.h"
#include "../../../headers/metaheuristics/nsga2/nsga2.h"
#include "../../../headers/globals.h"

void add(vector<Solution*>& population, Solution* solution){
  for (auto& existing_solution : population) {
    if (isEqual(*existing_solution, *solution)) {
      delete solution; 
      return;          
    }
  }
  population.push_back(solution);
}

vector<Solution*> nsga2(vector<Solution>& pop){

  vector<Solution*> * population = new vector<Solution*>();

  for(auto sol : pop){
    Solution * s = new Solution(sol);
    add(*population, s);
  }

  default_random_engine re{(unsigned)time(nullptr)};
  uniform_real_distribution<double> dist(0.0, 1.0);

  int size_population = population->size(); 
  double cross_prob = 0.6;
  double mutation_prob = 0.5;
  int stop_criteria = 1000000;

  ofstream infoRunNSGA2(root_folder + "infoRun.txt");

  int generation = 0;

  while(countRevalue < stop_criteria){

    infoRunNSGA2 << "Generation " << generation << " | Revalues: " << countRevalue << " | GridSize: " << pareto->getSize() << endl;

    vector<Solution*> * offspring_population = new vector<Solution*>();

    for(int i = 0; i < size_population; i++){
      Solution** parents = binary_tournament(*population);
  
      Solution * child1 = new Solution;
      Solution * child2 = new Solution;
      *child1 = *parents[0];
      *child2 = *parents[1];
      double k = dist(re);

      if((static_cast<double>(rand()) / RAND_MAX) < cross_prob){
        *child1 = crossover(*parents[0], *parents[1]);
        *child2 = crossover(*parents[1], *parents[0]);
      }

      k = dist(re);

      if((static_cast<double>(rand()) / RAND_MAX) < mutation_prob){
        mutation(*child1);
        mutation(*child2);
      }

      add(*offspring_population, new Solution(*child1));
      add(*offspring_population, new Solution(*child2));

      delete parents[0];
      delete parents[1];
      delete[] parents; 

      delete child1;
      delete child2;
    }

    vector<Solution*> * total_population = new vector<Solution*>();

    for(auto i : *population){
      total_population->push_back(new Solution(*i));
    }

    for (auto i : *offspring_population){
      total_population->push_back(new Solution(*i));
      delete i;
    }

    delete offspring_population;

    vector<vector<Solution*> *> * fronts = new vector<vector<Solution*>*>();
    *fronts = arena_non_dominated_sorting(*total_population);

    for(auto i : *total_population){
      delete i;
    }

    delete total_population;

    for(auto i : *population){
      delete i;
    }

    population->clear();
    
    int k = 0;
    for (auto& front : *fronts) {
      if (population->size() + front->size() <= size_population) {
        for (auto solution : *front) {
          population->push_back(new Solution(*solution));
        }
      }
      else {
        auto * front_sorted = new vector<Solution*>();
        *front_sorted = crowding_distance(*front);
        
        int remaining_spots = size_population - population->size();

        vector<Solution*>::iterator it = front_sorted->begin();
        
        for (int i = 0; i < remaining_spots; i++) {
          population->push_back(new Solution(**it));
          it++;
        }

        delete front_sorted;
        
        break;
      }
      k++;
    }

    for(auto front : *fronts){
      for(auto solution : *front){
        delete solution;
      }
      delete front;
    }

    delete fronts;

    generation++;
  }
  
  infoRunNSGA2.close();
  
  return *population;
}