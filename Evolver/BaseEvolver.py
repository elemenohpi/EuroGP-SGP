import copy
import datetime
import pickle
import random
import multiprocessing as mp
import sys

from Evolver.AbstractEvolver import AbstractEvolver
from eletility import Files
from eletility import Log


class BaseEvolver(AbstractEvolver):
    def __init__(self, config, pop_obj, fitness_obj, interpreter_obj) -> None:
        super().__init__()
        self.pop = None
        self.pop_obj = pop_obj
        self.config = config
        self.runs = int(self.config["runs"])
        self.Log = Log()
        self.Files = Files()
        self.fitness_obj = fitness_obj
        self.interpreter_obj = interpreter_obj
        self.tournament_size = int(self.config["tournament_size"])
        self.cue_init_radius = int(self.config["cue_init_radius"])
        self.elitism = int(self.config["elitism"])
        self.best_indv_change_counter = 0

    def initialize_elites_list(self):
        elites = [None for _ in range(self.elitism)]
        return elites

    def update_population_fitness(self):
        sum_fitness = 0
        # start = datetime.datetime.now()
        jobs = int(self.config["jobs"].strip())
        if jobs > 1:
            # process_list = []
            # num_workers = jobs
            # pool = mp.Pool(num_workers)
            # for index, individual in enumerate(self.pop):
            #     process = pool.apply_async(self.fitness_obj.evaluate, (individual, ))
            #     process_list.append(process)
            # pool.close()
            # pool.join()
            # print(process_list)
            # exit()
            with mp.Pool(processes=jobs) as pp:
                results = pp.map(self.fitness_obj.evaluate, self.pop)
            pp.close()
            pp.join()
            # for result in results:
            #     print (result)
            # exit()
            for index, result in enumerate(results):
                fitness, rvalue, rmse = result
                self.pop[index].fitness = fitness
                self.pop[index].rvalue = rvalue
                self.pop[index].rmse = rmse
                sum_fitness += fitness
        else:
            for index, individual in enumerate(self.pop):
                # fitness, rvalue, rmse = self.fitness_obj.evaluate(individual)
                try:
                    fitness, rvalue, rmse = self.fitness_obj.evaluate(individual)


                except OverflowError:
                    print("overflow error")
                    # ToDo:: fix this
                    if self.config["optimization_goal"] == "min":
                        fitness = sys.float_info.max
                        rvalue = 0
                        rmse = 0
                    elif self.config["optimization_goal"] == "max":
                        fitness = sys.float_info.max * -1
                        rvalue = 0
                        rmse = 0
                    else:
                        raise "Unknown optimization goal"
                # misleading naming convention
                # print(fitness, rvalue, rmse)
                self.pop[index].fitness = fitness
                self.pop[index].rvalue = rvalue
                self.pop[index].rmse = rmse
                sum_fitness += fitness

        # print(datetime.datetime.now() - start)
        return sum_fitness

    def sort_population(self):
        if self.config["optimization_goal"] == "min":
            order = False
        elif self.config["optimization_goal"] == "max":
            order = True
        else:
            raise "Unknown optimization goal"
        self.pop.sort(key=lambda x: x.fitness, reverse=order)

    # noinspection PyUnresolvedReferences
    def run(self):
        self.pop = self.pop_obj.pop
        best_individual = None
        elites = self.initialize_elites_list()
        best_fitness = 0
        for gen in range(self.runs):
            log_msg = "\t{}: ".format(gen)
            avg_fitness = self.update_population_fitness()

            self.sort_population()

            elites = copy.deepcopy(self.pop[0:self.elitism])
            if best_individual is None or elites[0].fitness != best_individual.fitness:
                best_individual = copy.deepcopy(elites[0])
                if self.config["make_viz_data"] == "True":
                    self.log_individual_for_visualization(best_individual)
                self.best_indv_change_counter += 1
            avg_fitness /= len(self.pop)

            alen = 0
            for indv in self.pop:
                alen += len(indv.programs)
            alen /= len(self.pop)

            log_msg += "best Fitness: {}, info1: {}, info2: {}, avg: {}, blen: {}, alen: {}".format(elites[0].fitness, elites[0].rvalue,
                                                                                 elites[0].rmse, avg_fitness, len(elites[0].programs), alen)
            save_log_msg = "{}, {}, {}, {}".format(elites[0].fitness, elites[0].rvalue, elites[0].rmse, avg_fitness)
            # ToDo:: Save the best individual
            best_individual_annotation = elites[0].annotate_program()

            self.save_best(best_individual_annotation)
            self.save_log(gen, save_log_msg)
            self.Log.I(log_msg)
            # for elite in elites:
            #     self.Log.Yprint(elite.fitness)
            # print()

            self.tournament(elites)
            # for indv in self.pop:
            #     print(indv.fitness, end=" ")
            #     if indv.fitness == 0:
            #         self.Log.Rprint("wtf?")
            # print()
        # best_individual.annotate_program(True)
        try:
            self.pickle_object(best_individual)
        except TypeError:
            pass

        top_right = 0
        bottom_right = 0
        bottom_left = 0
        top_left = 0
        for model in self.pop:
            for program in model.programs:
                if program.pos[0] >= 0 and program.pos[1] >= 0:
                    top_right += 1
                elif program.pos[0] >= 0 and program.pos[1] < 0:
                    bottom_right += 1
                elif program.pos[0] < 0 and program.pos[1] < 0:
                    bottom_left += 1
                elif program.pos[0] < 0 and program.pos[1] >= 0:
                    top_left += 1
        print("Final Positional Counts -> top_right:", top_right, "bot_right:", bottom_right, "bot_left:", bottom_left, "top_left:", top_left)
        if elites[0] is not None:
            return elites[0].fitness
        return None

    def test_pop_sanity(self, indv):
        output_count = len(indv.output_pool)
        output_counter = 0
        for program in indv.programs:
            if program.program_type == "O":
                output_counter += 1
        if output_count != output_counter:
            print(output_counter, output_count)
            indv.visualize()
            return False
        return True

    def log_individual_for_visualization(self, indv):
        text = ""
        for program in indv.programs:
            text += repr(program.pos[0]) + "," + repr(program.pos[1]) + "\n"
        self.Files.writeTruncate("Output/vis/indv_" + str(self.best_indv_change_counter), text)

    def pickle_object(self, obj):
        destination = self.config["best_object"]
        with open(destination, 'wb') as object_file:
            pickle.dump(obj, object_file)

    def sort_tournament(self, tournament):
        if self.config["optimization_goal"] == "min":
            order = False
        elif self.config["optimization_goal"] == "max":
            order = True
        else:
            raise "Unknown optimization goal"
        tournament.sort(key=lambda x: x.fitness, reverse=order)
        return tournament

    def tournament(self, elites):
        new_pop = copy.deepcopy(elites)
        for i, indv in enumerate(new_pop):
            indv.individual_index = i
        while len(new_pop) < len(self.pop):
            tournament_list = []
            for i in range(self.tournament_size):
                tournament_list.append(random.choice(self.pop))
            sorted_tournament = self.sort_tournament(tournament_list)
            parent_a, parent_b = copy.deepcopy(sorted_tournament[0]), copy.deepcopy(sorted_tournament[1])

            if random.random() < float(self.config["crossover_rate"]):
                offspring_a, offspring_b = parent_a.crossover(parent_b)
            else:
                offspring_a, offspring_b = parent_a, parent_b

            # if self.test_pop_sanity(parent_a) and self.test_pop_sanity(parent_b):
            #     print("parents are ok")
            # else:
            #     print("faulty parents")

            self.mutate_individual(offspring_b)
            self.mutate_individual(offspring_a)

            # if self.test_pop_sanity(offspring_a) and self.test_pop_sanity(offspring_b):
            #     print("offsprings are ok")
            # else:
            #     print("faulty mutation maybe")
            #     exit()
            # fitness = self.fitness_obj.evaluate(new_pop[0])
            # print("b", fitness)
            # rand = random.random()
            # if rand < float(self.config["structural_mutation_rate"]):
            #     # Structural mutation
            #     rand = random.random()
            #     if rand < 0.5:
            #         if len(offspring_a.programs) <= int(self.config["cue_size_max"]):
            #             offspring_a.add_program()
            #     else:
            #         if len(offspring_a.programs) > 0:
            #             random_index = random.randint(0, len(offspring_a.programs)-1)
            #             del offspring_a.programs[random_index]
            # for program in offspring_a.programs:
            #     rand = random.random()
            #     if rand < float(self.config["lgp_mutation_rate"]):
            #         program.lgp_mutation()
            #     if rand < float(self.config["structural_mutation_rate"]):
            #         program.spatial_mutation()
            # if rand < float(self.config["structural_mutation_rate"]):
            #     rand = random.random()
            #     if rand < 0.5:
            #         if len(offspring_b.programs) <= int(self.config["cue_size_max"]):
            #             offspring_b.add_program()
            #     else:
            #         if len(offspring_b.programs) > 0:
            #             random_index = random.randint(0, len(offspring_b.programs)-1)
            #             del offspring_b.programs[random_index]
            # for program in offspring_b.programs:
            #     rand = random.random()
            #     if rand < float(self.config["lgp_mutation_rate"]):
            #         program.lgp_mutation()
            #     if rand < float(self.config["structural_mutation_rate"]):
            #         program.spatial_mutation()
            #
            # fitness = self.fitness_obj.evaluate(new_pop[0])
            # print("a", fitness)
            offspring_a.individual_index = len(new_pop)
            new_pop.append(offspring_a)
            offspring_b.individual_index = len(new_pop)
            new_pop.append(offspring_b)
        self.pop = copy.deepcopy(new_pop)

    def mutate_individual(self, individual):
        rand = random.random()
        if rand < float(self.config["structural_mutation_rate"]):
            # Structural mutation
            rand = random.random()
            if rand < 0.5:
                if len(individual.programs) <= int(self.config["cue_size_max"]):
                    individual.add_program()
            else:
                if len(individual.programs) > 0:
                    random_index = random.randint(0, len(individual.programs) - 1)
                    if individual.programs[random_index].program_type != "O":
                        del individual.programs[random_index]
        for program in individual.programs:
            rand = random.random()
            if rand < float(self.config["lgp_mutation_rate"]):
                program.lgp_mutation()
            if rand < float(self.config["structural_mutation_rate"]):
                program.spatial_mutation()
        pass

    def save_best(self, annotation):
        destination = self.config["best_program"]
        disclaimer = "# This code is a generated/synthesized QGP model/program\n# ============================================ \n\n"
        self.Files.writeTruncate(destination, disclaimer + annotation)

    def save_log(self, gen, log):
        destination = self.config["evo_file"]
        if gen == 0:
            title = "gen, fitness, info1, info2, avg\n"
            self.Files.writeTruncate(destination, title + repr(gen) + ", " + log + "\n")
        else:
            self.Files.writeLine(destination, repr(gen) + ", " + log)
