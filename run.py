import argparse
import os
import random
from os import listdir
from os.path import isfile
from os.path import join
from subprocess import call

from SGP import SGP
from eletility import ConfigParser, Files
from eletility import Log
# from playsound2 import playsound

F = Files()
L = Log()


def hpcc(reps, hours, runs, seed, title, config):
	# create a folder
	try:
		os.mkdir("Output/{}".format(title))
		os.mkdir("Output/{}/Error".format(title))
		os.mkdir("Output/{}/Slurm".format(title))
		os.mkdir("Output/{}/Evo".format(title))
		os.mkdir("Output/{}/Object".format(title))
		os.mkdir("Output/{}/Executable".format(title))
		os.mkdir("Output/{}/Subs".format(title))
	except FileExistsError:
		pass
	destination = "Output/{}/{}.ini".format(title, title)
	content = "#Overridden Settings:\n#reps = {}\n#hours = {}\n#runs = {}\n#seed = {}\n\n".format(reps, hours, runs, seed)
	with open(config, "r") as f:
		content += f.read()
	F.writeTruncate(destination, content)

	for i in range(reps):
		filename = "Output/{}/Subs/{}.sb".format(title, i)
		file = open(filename, "w")
		file.write("#!/bin/bash --login\n")
		file.write("\n########## SBATCH Lines for Resource Request ##########\n\n")
		file.write(
			"#SBATCH --time={}:02:00             # limit of wall clock time - how long the job will run (same as -t)\n".format(
				hours))
		file.write(
			"#SBATCH --nodes=1                   # number of different nodes - could be an exact number or a range of nodes (same as -N)\n")
		file.write(
			"#SBATCH --ntasks=1                  # number of tasks - how many tasks (nodes) that you require (same as -n)\n")
		file.write("#SBATCH --cpus-per-task=1           # number of CPUs (or cores) per task (same as -c)\n")
		file.write(
			"#SBATCH --mem-per-cpu=8G            # memory required per allocated CPU (or core) - amount of memory (in bytes)\n")
		file.write(
			"#SBATCH --job-name {}_{}      # you can give your job a name for easier identification (same as -J)\n".format(
				title, i))
		file.write(
			"#SBATCH --error=Output/{}/Error/{}_{}.err      # you can give your job a name for easier identification (same as -J)\n".format(
				title, title, i))
		file.write(
			"#SBATCH --output=Output/{}/Slurm/{}_{}.txt      # you can give your job a name for easier identification (same as -J)\n".format(
				title, title, i))

		# SBATCH --error=%j.err
		file.write("\n########## Command Lines to Run ##########\n\n")
		file.write("module purge")
		file.write("module load Conda/3")
		file.write("conda activate mujoco_env")
		file.write("cd ~/SGP-Collab\n")
		# file.write("module load GCC/6.4.0-2.28 OpenMPI  ### load necessary modules, e.g\n")
		output = "Output/{}/Executable/exec_{}.py".format(title, i)
		pickle = "Output/{}/Object/pickled_{}.sgp".format(title, i)
		evo = "Output/{}/Evo/evo_{}.csv".format(title, i)
		file.write("srun -n 1 python run.py -runs {} -output {} -pickle {} -evo {} -seed {} -config {}\n".format(runs, output, pickle, evo, seed + i, config))
		file.write("scontrol show job Output/{}/Slurm/$SLURM_JOB_ID     ### write job information to output file".format(title))
		file.close()
		call(["sbatch", "Output/{}/Subs/{}.sb".format(title, i)])


def main():
	parser = argparse.ArgumentParser(
		description='Cue Genetic Programming. Command line parameters override the config file entries.')
	parser.add_argument("-hpcc", help="Runs the application as an experiment on HPCC", action='store_true')
	parser.add_argument("-experiment", help="Same as -hpcc but takes config directory instead", action='store_true')
	parser.add_argument("-seed", help="The random seed")
	parser.add_argument("-output", help="Path to the output file")
	parser.add_argument("-pickle", help="Path to the pickled object")
	parser.add_argument("-evo", help="Path to the evolutionary output")
	parser.add_argument("-model", help="Evaluates a pickled object")
	parser.add_argument("-multirun", help="Multiple N runs of the algorithm on a single CPU.")
	parser.add_argument("-runs", help="Number of generations")
	parser.add_argument("-config", help="Config file to operate with")
	parser.add_argument("-compare", help="Compares the evo files and returns some stats about the best run")
	parser.add_argument("-test", help="Tests the validity of all the config files in a directory")
	args = parser.parse_args()

	if args.test:
		report = ""
		path = args.test
		config_directory = [f for f in listdir(path) if isfile(join(path, f))]
		for config_file in config_directory:
			if config_file.split(".")[-1] != "ini":
				continue
			configparser = ConfigParser()
			config_path = join(path, config_file)
			config = configparser.read(config_path)
			config["runs"] = "3"
			try:
				print("\nTesting", config_file)
				sgp = SGP(config)
				best_fitness = sgp.run()
				report += "{} test OK\n".format(config_file)
			except:
				report += "{} test FAIL\n".format(config_file)
		print("\nTest Report:\n")
		print(report)
		exit()

	config_file = "config.ini"
	if args.config:
		config_file = args.config
	configparser = ConfigParser()
	config = configparser.read(config_file)

	if args.seed:
		config["seed"] = args.seed

	random.seed(int(config["seed"]))

	if args.experiment:
		title = input("Experiment title (will be appended by the config name): ")
		hours = int(input("Job time (in hours): "))
		reps = int(input("Number of reps: "))
		runs = int(input("Number of generations: "))
		seed = int(input("Starting seed: "))
		config = input("Config directory: ")
		print("Title: {}, Reps: {}, Hours: {}, Gens: {}, Starting Seed: {}, Config: {}".format(title, reps, hours, runs,
		                                                                                       seed, config))
		confirm = input("Do you confirm these settings? YES to continue ")
		if confirm != "YES":
			print("Exiting...")
			exit()
		config_files = [f for f in listdir(config) if isfile(join(config, f))]
		for config_file in config_files:
			if config_file.split(".")[-1] != "ini":
				continue
			new_title = title + "_" + config_file.split(".")[0]
			config_path = join(config, config_file)
			hpcc(reps, hours, runs, seed, new_title, config_path)
		exit()

	if args.hpcc:
		title = input("Experiment title: ")
		hours = int(input("Job time (in hours): "))
		reps = int(input("Number of reps: "))
		runs = int(input("Number of generations: "))
		seed = int(input("Starting seed: "))
		config = input("Config file: ")

		print("Title: {}, Reps: {}, Hours: {}, Gens: {}, Starting Seed: {}, Config: {}".format(title, reps, hours, runs, seed, config))
		confirm = input("Do you confirm these settings? YES to continue ")
		if confirm != "YES":
			print("Exiting...")
			exit()
		hpcc(reps, hours, runs, seed, title, config)
		exit()

	if args.compare:
		# ToDo:: put in different function
		goal = config["optimization_goal"]
		path = args.compare
		files = [f for f in listdir(path) if isfile(join(path, f))]
		best_info = []
		best_fitness = None
		best_rmse = None
		for file in files:
			if file.split(".")[-1] != "csv":
				continue
			with open(join(path, file), 'r') as f:
				last_line = f.readlines()[-1]
			gen, fitness, rvalue, rmse, avg = last_line.split(",")
			print(file, gen, fitness, rvalue, rmse, avg)
			if goal == "max" and (best_fitness is None or float(best_fitness) < float(fitness)):
				best_info = [file, gen, fitness, rvalue, rmse, avg]
				best_fitness = fitness
			elif goal == "min" and (best_fitness is None or float(best_fitness) >= float(fitness)):
				if best_fitness is not None and float(best_fitness) == float(fitness):
					if rmse > best_rmse:
						continue
				best_info = [file, gen, fitness, rvalue, rmse, avg]
				best_fitness = fitness
				best_rmse = rmse
		print("best: ", best_info)
		exit()

	if args.runs:
		config["runs"] = args.runs

	if args.output:
		config["best_program"] = args.output

	if args.pickle:
		config["best_object"] = args.pickle

	if args.evo:
		config["evo_file"] = args.evo

	if args.model:
		# ToDo:: implement
		raise "This option is not coded yet."

	if args.multirun:
		multirun = True
		count = int(args.multirun)
	else:
		multirun = False
		count = 0

	run_seed = int(config["seed"])
	if multirun:
		for seed in range(run_seed, run_seed + count):
			config["seed"] = seed
			sgp = SGP(config)
			best_fitness = sgp.run()
			msg = "\n==============================================\nRun Finished. Seed: {} Best Fitness: {}\n\n".format(
				seed, best_fitness)
			L.Yprint(msg)
			# if config["optimization_goal"] == "min" and best_fitness == 0:
			# 	file = "wa.mp3"
			# 	playsound(file)
			# 	break
	else:
		sgp = SGP(config)
		best_fitness = sgp.run()
		# if best_fitness == 0:
		# 	file = "wa.mp3"
		# 	playsound(file)


if __name__ == "__main__":
	main()
