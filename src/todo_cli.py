def main():
	"""This is our main function, no other purpose, other than being there
	like in C"""
	
	# Make a variable for unique id of a task
	global task_id
	with open("list.txt") as file:
		task_id = len(file.readlines())

	# List of possible commands
	commands = ["quit", "add", "remove", "show", "mark", "help"] 	
	
	# App is always open, unless user wants to close it
	while True:

		# Get user input
		user_input = input("What would you like to do?\n")
		
		# If user wants to quit let them
		if user_input == "quit":
			break
		
		# Print sort of a manual page
		if user_input == "help":
			print_usage()
		
		# Add item to the list
		if user_input == "add":
			add_value()
		
		# Remove item from the list
		if user_input == "remove":
			remove_value()
		
		# Print out the current list
		if user_input == "show":
			print_list()

		# Print usage if command is invalid
		if user_input not in commands:
			print()
			print("-" * 40)
			print("Invalid usage!\nUse help to get started!")
			print("-" * 40)
			print()


def remove_value():
	""" Remove specific item from the list """
	
	# We'll need to lower number of tasks, to have correct ids
	global task_id
		
	# If the list is empty, return	
	if task_id == 0:
		print("\nNOTHING TO REMOVE\n")
		return
	
	# Show user what he even has
	print_list()
	
	# Prompt user until item is a viable ID	
	while True:
		item = int(input("Which item would you like to remove?\n"))
		if item not in range(1, task_id + 1):
			print("ERROR. NO SUCH TASK.\nPlease select an id of a task.\nFormat: id / task / deadline\n")
		else:
			break
	
	# Get current list into as list :)	
	with open("list.txt") as file:
		lines = file.readlines()
	
	# Change IDs of everything past the item to -1	
	for i in range(item, len(lines)):
		lines[i] = str(i) + lines[i][1:]
	
	# Remove the item and lower IDs
	del lines[item - 1]
	task_id -= 1		
	
	# Rewrite the file with new list
	with open("list.txt", "w") as file:
		for line in lines:
			file.write(line)
	
	# Probably just a good practice to return	
	print("\nSuccesfully removed!\n")
	return	
	

def add_value():
	""" Add value to the to-do-list """
	
	# We'll need to increment task_id
	global task_id

	print()
	# Get user input
	task = input("Task: ")
	deadline = input("Deadline: ")
	print()
		
	# Increment ID
	task_id += 1
	print("Task added!\n")
		
	# Add task to the list in format: id / task / deadline
	with open("list.txt", "a") as file:
		file.write(f"{task_id}: {task} - {deadline}\n")

def print_list():
	""" Print out the current list """
	
	# Print every line
	with open("list.txt", "r") as file:
		print("\n\n", "TO-DO LIST\n", "-" * 40, "\n")
		for line in file:
			print("", line)
		print("", "-" * 40, "\n")

def print_usage():
	""" Print out a man page for user """

	print("-" * 40)
	print("\nThis is very basic to-do-app.")
	print("To get started, use one of the following commands:\n")
	print("-" * 40)
	print("quit")
	print("Quits an app once you press Enter")
	print("\nadd")
	print("Add a task on your to-do list")
	print("\nremove")
	print("Remove a task from a list")
	print("\nshow")
	print("Prints out your current to-do list")
	print("-" * 40)
	
	

if __name__ == "__main__":
	main()
