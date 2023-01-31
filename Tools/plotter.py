import math

import pandas as pd
import argparse
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np


class Plotter:
	# Takes directories, returns a plot of average with q75 and q25. Can plot multiple directories to compare.
	def plot_experiment(self, paths, gens, title, xlabel, ylabel, line_labels, output=None):
		plt.style.use('fast')

		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)

		all_directory_based_data = []
		for index, path in enumerate(paths):
			q25s = []
			q75s = []
			medians = []
			dataframes = []
			files = [f for f in listdir(path) if isfile(join(path, f))]
			for findex, file in enumerate(files):
				# print(findex, file)
				extension = file.split(".")[-1]
				if extension != "csv":
					continue
				file = join(path, file)
				df = pd.read_csv(file, index_col=0)
				if len(df.index) >= gens:
					dataframes.append(df)
				else:
					print("data frame {} has {} rows and thus is disregarded".format(file, len(df.index)))
				# print(len(df.index), file)
			# exit()
			for i in range(gens):
				best_fitness_values_at_gen_i = []
				# print(dataframes)
				# print("================================")
				# print(dataframes[17])
				# exit()
				for dfindex, df in enumerate(dataframes):
					# print(df)
					# exit()
					# try:
						# if i == gens - 1:
						# print("|"+str(df[" fitness"][i])+"|")
						# if str(df[" fitness"][i]) == "nan":
						# 	print("faulty df")
						# 	print(df)
						# 	exit()
						# print(df[" fitness"][i])
					best_fitness_values_at_gen_i.append(float(str(df[" fitness"][i]).strip()))
						# print("--", best_fitness_values_at_gen_i)
					# except:
					# 	print("++", best_fitness_values_at_gen_i)
					# 	exit()

				# exit()
				# print(best_fitness_values_at_gen_i)
				# exit()
				best_fitness_values_at_gen_i_df = pd.DataFrame(best_fitness_values_at_gen_i)
				# print(best_fitness_values_at_gen_i_df)
				# exit()
				try:
					quantiles = best_fitness_values_at_gen_i_df.quantile([0.25, 0.75])
					medians.append(best_fitness_values_at_gen_i_df.median().values[0])
					q25s.append(quantiles[0].iloc[0])
					q75s.append(quantiles[0].iloc[1])
				except:
					print("error")
					print(best_fitness_values_at_gen_i)
					print("----------")
					print(best_fitness_values_at_gen_i_df)
					exit()
			directory_data = [line_labels[index], q25s, q75s, medians]
			all_directory_based_data.append(directory_data)

		x_axis_data = range(0, gens)

		for line_data in all_directory_based_data:
			plt.fill_between(x_axis_data, line_data[1], line_data[2], alpha=.1, linewidth=0)
			plt.plot(x_axis_data, line_data[3], linewidth=2.0, label=line_data[0])
		plt.legend(loc='center right')
		plt.show()
	# plt.savefig(output, dpi=300)




plotter = Plotter()




# ================================================================== Static Loop (solving a^20) ========================
# plotter.plot_experiment(
# 	["Output/29apr-statemprmse/Evo", "Output/29apr-staprogrmse/Evo"],
# 	1000, "x^20 Problem with RMSE", "Generations", "Fitness", ["rmse_p", "rmse_s"])
#
# plotter.plot_experiment(
# 	["Output/29apr-staprog/Evo", "Output/29apr-statemp/Evo"],
# 	50, "x^20 Problem with Correlation", "Generations", "Fitness", ["correl_p", "correl_s"])

# ================================================================== Dyna Loop (solving 2^a) ===========================

# plotter.plot_experiment(
# 	["Output/29apr-dynaprog/Evo", "Output/29apr-dynatemp/Evo"],
# 	50, "2^x Problem with Correlation", "Generations", "Fitness", ["correl_p", "correl_s"])
#
# plotter.plot_experiment(
# 	["Output/29apr-dynaprogrmse/Evo", "Output/29apr-dynatemprmse/Evo"],
# 	1000, "2^x Problem with RMSE", "Generations", "Fitness", ["rmse_p", "rmse_s"])

# ================================================================== Dyna Loop (solving a^b) ===========================
#
# plotter.plot_experiment(
# 	["Output/29apr-powerprog/Evo", "Output/29apr-powertemp/Evo"],
# 	1000, "x^y Problem with Correlation", "Generations", "Fitness", ["correl_p", "correl_s"])

# plotter.plot_experiment(
# 	["Output/29apr-powerprogrmse/Evo", "Output/29apr-powertemprmse/Evo"],
# 	1000, "x^y Problem with RMSE", "Generations", "Fitness", ["rmse_p", "rmse_s"])

# ================================================================== RL + Loop (Ant Problem) ===========================

# plotter.plot_experiment(
# 	["Output/29apr-ant-prog/Evo", "Output/29apr-ant-prog-const/Evo", "Output/29apr-ant-prog-const-reg/Evo"],
# 	999, "Comparing Different SGP Settings for Solving the Ant Problem", "Generations", "Fitness", ["prog", "prog-const", "prog-const-reg"])

# plotter.plot_experiment(
# 	["Output/29apr-ant-spatio/Evo", "Output/29apr-ant-spatio-const/Evo", "Output/29apr-ant-spatio-const-reg/Evo"],
# 	999, "Comparing Different SGP Settings for Solving the Ant Problem", "Generations", "Fitness", ["temporo", "temporo-const", "temporo-const-reg"])

# plotter.plot_experiment(
# 	["Output/29apr-ant-prog/Evo", "Output/29apr-ant-prog-const/Evo", "Output/29apr-ant-prog-const-reg/Evo", "Output/29apr-ant-spatio/Evo", "Output/29apr-ant-spatio-const/Evo", "Output/29apr-ant-spatio-const-reg/Evo"],
# 	999, "Comparing Different Settings for Solving the Ant Problem", "Generations", "Fitness", ["prog", "p_const", "p_const_math", "spatial", "s_const", "s_const_math"])

# ================================================================== State/Decision Making (TicTacToe) ===========================

# plotter.plot_experiment(
# 	["Output/TicTacToe/Evo"],
# 	500, "Evolution of Models for Solving the TicTacToe Problem", "Generations", "Fitness", ["prog"])

# for i in range(21):
# 	title = "../OGP_Results/Regression_E" + str(i+1) + ".ini/Evo"
# 	plotter.plot_experiment(
# 		[title],
# 		500, "N/A", "Generations", "Fitness", ["n/a"])
#

# plotter.plot_experiment(
# 	["../OGP_Results/7-29-2022-Preliminary-OGP-Draft/Regression_E18.ini/Evo"],
# 	999, "E18", "Generations", "Fitness", ["prog"])
#

# plotter.plot_experiment(
# 	["../OGP_Results/DEAP_Results/Processed/TreeGP_Adventure", "../OGP_Results/08-04-2022/ControlProblems_CartPole_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_CartPole_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_CartPole_spatial/Evo"],
# 	100, "Fitness over Generation for solving the Cart Pole Problem", "Generations", "Fitness (Successful Steps)", ["TGP","Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/08-04-2022/ControlProblems_MountainCar_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_MountainCar_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_MountainCar_spatial/Evo"],
# 	500, "Fitness over Generation for solving the Mountain Car Problem", "Generations", "Fitness (Car Altitude)", ["Prog", "Prog RetCon", "Spatial"])
#
# plotter.plot_experiment(
# 	["../OGP_Results/08-04-2022/ControlProblems_Pendulum_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_Pendulum_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_Pendulum_spatial/Evo"],
# 	100, "Fitness over Generation for Solving the Pendulum Problem", "Generations", "Fitness (Free End Altitude)", ["Prog", "Prog RetCon", "Spatial"])



# plotter.plot_experiment(
# 	["../OGP_Results/08-04-2022/ToyProblems_Foraging_noretcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_Foraging_retcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_Foraging_spatio/Evo"],
# 	1000, "Fitness over Generation for Solving the Foraging Problem", "Generations", "Fitness (Count of Food Gathered)", ["Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/08-04-2022/ToyProblems_ObstacleAvoidance_noretcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_ObstacleAvoidance_retcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_ObstacleAvoidance_spatio/Evo"],
# 	100, "Fitness over Generation for Solving the Foraging Problem", "Generations", "Fitness (Time Steps Survived)", ["Prog", "Prog RetCon", "Spatial"])
#

# plotter.plot_experiment(
# 	["../OGP_Results/08-04-2022/revised_loop_ArtificialAntVariation_loop/Evo", "../OGP_Results/08-04-2022/revised_loop_ArtificialAntVariation/Evo",
# 	 "../OGP_Results/08-04-2022/no_spatial_ArtificialAntVariation_loop/Evo", "../OGP_Results/08-04-2022/no_spatial_ArtificialAntVariation/Evo"],
# 	1000, "na", "Generations", "Fitness", ["loop", "noloop", "nosp_loop", "nospnoloop"])

# "../OGP_Results/08-04-2022/reattempt_loop_ArtificialAntVariation_loop/Evo", "../OGP_Results/08-04-2022/reattempt_loop_ArtificialAntVariation/Evo",
# plotter.plot_experiment(
# 	[ "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation/Evo", "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation_loop/Evo",
# 	 "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_Spatial/Evo", "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_loop_Spatial/Evo"],
# 	300, "Fitness over Generation for Solving the Santa-Fe Ant Variation", "Generations", "Fitness (Count of Food Gathered)", ["RetCon", "RetCon Loop", "Spatial", "Spatial Loop"])


# plotter.plot_experiment(
# 	[
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_Acrobat_noretcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_Acrobat_retcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_Acrobat_spatial/Evo",
# 	 "../OGP_Results/08-04-2022/ControlProblems_Acrobat_noretcon/Evo",
# 	 "../OGP_Results/08-04-2022/ControlProblems_Acrobat_retcon/Evo",
# 	 "../OGP_Results/08-04-2022/ControlProblems_Acrobat_spatial/Evo"],
# 	100, "Fitness over Generation for solving the Acrobat Problem", "Generations", "Fitness (Penalty for Low Free End Altitude)", ["nProg", "nProg RetCon", "nSpatial", "Prog", "Prog RetCon", "Spatial"])


# plotter.plot_experiment(
# 	[
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_CartPole_noretcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_CartPole_retcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_CartPole_spatial/Evo",
# 	],
# 	100, "Fitness over Generation for solving the Acrobat Problem", "Generations", "Fitness (Penalty for Low Free End Altitude)", ["nProg", "nProg RetCon", "nSpatial", "Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	[
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_Pendulum_noretcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_Pendulum_retcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_Pendulum_spatial/Evo",
# 	],
# 	100, "Fitness over Generation for solving the Acrobat Problem", "Generations", "Fitness (Penalty for Low Free End Altitude)", ["nProg", "nProg RetCon", "nSpatial", "Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	[
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_MountainCar_noretcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_MountainCar_retcon/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/ControlProblems_MountainCar_spatial/Evo",
# 	],
# 	100, "Fitness over Generation for solving the Acrobat Problem", "Generations", "Fitness (Penalty for Low Free End Altitude)", ["nProg", "nProg RetCon", "nSpatial", "Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	[
# 	 "../OGP_Results/08-18-2022-new_cost/LoopProblems_ArtificialAntVariation/Evo",
# 	 "../OGP_Results/08-18-2022-new_cost/LoopProblems_ArtificialAntVariation_loop/Evo",
# 	 "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation/Evo",
# 		"../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation_loop/Evo",
# 	 "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_Spatial/Evo",
# 		"../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_loop_Spatial/Evo"
# 	],
# 	300, "Fitness over Generation for solving the Acrobat Problem", "Generations", "Fitness (Penalty for Low Free End Altitude)",
# 	["new", "new loop", "old", "old loop", "spatial ", "spatial loop"])

# plotter.plot_experiment(
# 	[ "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation/Evo", "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation_loop/Evo",
# 	 "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_Spatial/Evo", "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_loop_Spatial/Evo"],
# 	300, "Fitness over Generation for Solving the Santa-Fe Ant Variation", "Generations", "Fitness (Count of Food Gathered)", ["RetCon", "RetCon Loop", "Spatial", "Spatial Loop"])

# plotter.plot_experiment(
# 	[ "../OGP_Results/DEAP_Results/Processed/TreeGP_Acrobat"],
# 	300, "Fitness over Generation for Solving the Santa-Fe Ant Variation", "Generations", "Fitness (Count of Food Gathered)", ["RetCon", "RetCon Loop", "Spatial", "Spatial Loop"])

# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_Acrobat_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_Acrobat", "../OGP_Results/08-04-2022/ControlProblems_Acrobat_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_Acrobat_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_Acrobat_spatial/Evo"],
# 	100, "Fitness over Generation for solving the Acrobat Problem", "Generations", "Fitness (Penalty for Low Free End Altitude)", ["LGP", "TGP", "Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_Adventure_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_Adventure", "../OGP_Results/08-04-2022/ToyProblems_Adventure_noretcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_Adventure_retcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_Adventure_spatio/Evo"],
# 	500, "Fitness over Generation for Solving the Adventure Problem", "Generations", "Fitness (Score Achieved)", ["LGP", "TGP", "Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_MountainCar_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_MountainCar", "../OGP_Results/08-04-2022/ControlProblems_MountainCar_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_MountainCar_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_MountainCar_spatial/Evo"],
# 	500, "Fitness over Generation for solving the Mountain Car Problem", "Generations", "Fitness (Car Altitude)", ["LGP", "TGP","Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_Pendulum_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_Pendulum", "../OGP_Results/08-04-2022/ControlProblems_Pendulum_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_Pendulum_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_Pendulum_spatial/Evo"],
# 	100, "Fitness over Generation for Solving the Pendulum Problem", "Generations", "Fitness (Free End Altitude)", ["LGP", "TGP","Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_Foraging_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_Foraging", "../OGP_Results/08-04-2022/ToyProblems_Foraging_noretcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_Foraging_retcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_Foraging_spatio/Evo"],
# 	700, "Fitness over Generation for Solving the Foraging Problem", "Generations", "Fitness (Count of Food Gathered)", ["LGP", "TGP", "Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_ObstacleAvoidance_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_ObstacleAvoidance", "../OGP_Results/08-04-2022/ToyProblems_ObstacleAvoidance_noretcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_ObstacleAvoidance_retcon/Evo", "../OGP_Results/08-04-2022/ToyProblems_ObstacleAvoidance_spatio/Evo"],
# 	100, "Fitness over Generation for Solving the Obstacle Avoidance Problem", "Generations", "Fitness (Time Steps Survived)", ["LGP", "TGP","Prog", "Prog RetCon", "Spatial"])

# plotter.plot_experiment(
# 	["../OGP_Results/LGP_Results/EuroGP_CartPole_lgp/Evo", "../OGP_Results/DEAP_Results/Processed/TreeGP_CartPole", "../OGP_Results/08-04-2022/ControlProblems_CartPole_noretcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_CartPole_retcon/Evo", "../OGP_Results/08-04-2022/ControlProblems_CartPole_spatial/Evo"],
# 	100, "Fitness over Generation for solving the Cart Pole Problem", "Generations", "Fitness (Successful Steps)", ["LGP", "TGP","Prog", "Prog RetCon", "Spatial"])
