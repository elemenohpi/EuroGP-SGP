import pandas as pd
import argparse
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np

paths = ["../OGP_Results/08-04-2022/analysis_spatial_ArtificialAntVariation/Slurm",
         "../OGP_Results/08-04-2022/analysis_spatial_ArtificialAntVariation_loop/Slurm",
         "../OGP_Results/08-04-2022/analysis_spatial_onspatial_ArtificialAntVariation_loop_Spatial/Slurm",
         "../OGP_Results/08-04-2022/analysis_spatial_onspatial_ArtificialAntVariation_Spatial/Slurm",
         "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_loop_Spatial/Slurm",
         "../OGP_Results/08-04-2022/og_indv_ArtificialAntVariation_Spatial/Slurm",
         "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation/Slurm",
         "../OGP_Results/08-04-2022/og_indv_looporoblems_ArtificialAntVariation_loop/Slurm"
         ]

for index, path in enumerate(paths):
	files = [f for f in listdir(path) if isfile(join(path, f))]
	top_right = 0
	bot_right = 0
	bot_left = 0
	top_left = 0

	for slurm in files:
		complete_file_path = join(path, slurm)
		with open(complete_file_path, "r") as opened_file:
			lines = opened_file.readlines()
			target_line = lines[-2]
			try:
				tokens = target_line.split(" ")
				top_right += int(tokens[5])
				bot_right += int(tokens[7])
				bot_left += int(tokens[9])
				top_left += int(tokens[11])
			except:
				# print("FAIL AT", target_line)
				pass
	total = top_right + bot_right + bot_left + top_left
	print("path:", path)
	print("count distribution:", top_right, bot_right, bot_left, top_left, "total:", total)
	print("percent distribution:", round(top_right/total * 100, 2), round(bot_right/total * 100, 2), round(bot_left/total * 100, 2), round(top_left/total * 100, 2))
