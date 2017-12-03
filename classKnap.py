from inspyred import ec
from inspyred.ec import selectors
from inspyred import swarm


class Benchmark(object):
    def __init__(self, dimensions, objectives=1):
        self.dimensions = dimensions
        self.objectives = objectives
        self.bounder = None
        self.maximize = True

    def __str__(self):
        if self.objectives > 1:
            return '{0} ({1} dimensions, {2} objectives)'.format(self.__class__.__name__, self.dimensions,
                                                                 self.objectives)
        else:
            return '{0} ({1} dimensions)'.format(self.__class__.__name__, self.dimensions)

    def __repr__(self):
        return self.__class__.__name__

    def generator(self, random, args):
        """The generator function for the benchmark problem."""
        raise NotImplementedError

    def evaluator(self, candidates, args):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        candidate = [a for a in args]
        fit = self.evaluator([candidate], kwargs)
        return fit[0]


class Knapsack(Benchmark):
    def __init__(self, capacity, items, duplicates=False):
        Benchmark.__init__(self, len(items))
        self.capacity = capacity
        self.items = items
        self.components = [swarm.TrailComponent((item[0]), value=item[1]) for item in items]
        self.duplicates = duplicates
        self.bias = 0.5
        if self.duplicates:
            max_count = [self.capacity // item[0] for item in self.items]
            self.bounder = ec.DiscreteBounder([i for i in range(max(max_count) + 1)])
        else:
            self.bounder = ec.DiscreteBounder([0, 1])
        self.maximize = True
        self._use_ants = False

    def generator(self, random, args):
        if self.duplicates:
            max_count = [self.capacity // item[0] for item in self.items]
            return [random.randint(0, m) for m in max_count]
        else:
            return [random.choice([0, 1]) for _ in range(len(self.items))]

    def constructor(self, random, args):
        self._use_ants = True
        candidate = []
        remaining_capacity = []
        while len(candidate) < len(self.components):
            feasible_components = []
            if len(candidate) == 0:
                feasible_components = self.components
            else:
                remaining_capacity_weigth = self.capacity[0] - sum([c.element[0] for c in candidate])
                remaining_capacity_value = self.capacity[1] - sum([c.element[1] for c in candidate])
                if self.duplicates:
                    feasible_components = [c for c in self.components if c.element[0] <= remaining_capacity_weigth and
                                           c.element[1] <= remaining_capacity_value]
                else:
                    feasible_components = [c for c in self.components if
                                           c not in candidate and c.element[0] <= remaining_capacity_weigth and
                                           c.element[1] <= remaining_capacity_value]
            if len(feasible_components) == 0:
                break
            else:
                # Choose a feasible component
                if random.random() <= self.bias:
                    next_component = max(feasible_components)
                else:
                    next_component = \
                    selectors.fitness_proportionate_selection(random, feasible_components, {'num_selected': 1})[0]
                candidate.append(next_component)
        return candidate

    def evaluator(self, candidates, args):
        fitness = []
        if self._use_ants:
            for candidate in candidates:
                total = 0
                for c in candidate:
                    total += c.value
                fitness.append(total)
        else:
            for candidate in candidates:
                total_value = 0
                total_weight = 0
                for c, i in zip(candidate, self.items):
                    total_weight += c * i[0]
                    total_value += c * i[1]
                if total_weight > self.capacity:
                    fitness.append(self.capacity - total_weight)
                else:
                    fitness.append(total_value)
        return fitness