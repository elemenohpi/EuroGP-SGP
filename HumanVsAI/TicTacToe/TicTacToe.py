from Fitness.SimpleDecisionMakingTasks.TicTacToe import TicTacToe
from HumanVsAI.TicTacToe import ai1

game = TicTacToe(multiplayer=True)
while not game.is_finished():
	game.display()
	choice = input("Human Choice: ")
	game.play_multi(eval(choice))

	if game.is_finished():
		break

	states = game.get_state()
	for i in range(9):
		input_assignment = "ai1.c{} = states[{}]".format(i, i)
		exec(input_assignment)

	ai1.run()

	param = ai1.program_output
	output = "ai1.{}".format(param)
	game.play_multi(eval(output))

	game.display()
