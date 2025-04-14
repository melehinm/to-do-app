from todo_db import open_database, add_task, remove_task, show_tasks, close_database, mark_task
from datetime import datetime, date

def main():
	"""This is our main function, no other purpose, other than being there
	like in C"""
	
	# Get values from our database
	con, cur = open_database()

	# List of possible commands
	commands = ["quit", "add", "remove", "mark", "show", "help"] 	
	
	# App is always open, unless user wants to close it
	while True:

		# Get user input
		user_input = input("What would you like to do?\n")

		# Print usage if command is invalid
		if user_input not in commands:
			print()
			print("-" * 40)
			print("Invalid usage!\nUse help to get started!")
			print("-" * 40)
			print()

		else:
			# If user wants to quit let them
			if user_input == "quit":
				break
		
			# Print sort of a manual page
			if user_input == "help":
				print_usage()
		
			# Add item to the list
			if user_input == "add":
				print()
				task = input("Task:\n")
				while True:
					deadline = input("Deadline (YYYY-MM-DD):\n")
					try:
						deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
						if deadline_date < date.today():
							print("\nCan't return to the past. Try again.\n")
						else: 
							break
					except ValueError:
						print("\nInvalid date format!")
				add_task(con, cur, task, deadline)
					
			# Remove item from the list
			if user_input == "remove":
				tasks = show_tasks(cur)
				if len(tasks) == 0:
					print("\nNothing to remove\n")
					continue
	
				while True:
					try:
						display_id = int(input("\nWhich task to remove?\n"))
						if 1 <= display_id <= len(tasks):
							break
						else:
							print("\nInvalid ID. Try again.\n")
					except ValueError:
						print("\nInvalid ID. Try again.\n")
	
				remove_task(con, cur, tasks, display_id)
			
			# Mark task as completed		
			if user_input == "mark":
				tasks = show_tasks(cur)
				if len(tasks) == 0:
					print("\nNo tasks available\n")
					continue
	
				while True:
					try:
						display_id = int(input("\nWhich task is completed?\n"))
						if 1 <= display_id <= len(tasks):
							break
						else:
							print("\nInvalid ID. Try again.\n")
					except ValueError:
						print("\nInvalid ID. Try again.\n")
	
				mark_task(con, cur, tasks, display_id)
		

		
			# Print out the current list
			if user_input == "show":
				show_tasks(cur)

# Manual page
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
	print("\n mark")
	print("Mark task as completed - [X]")
	print("\nshow")
	print("Prints out your current to-do list")
	print("-" * 40)
	
	

if __name__ == "__main__":
	main()
