import sqlite3
import os

# Universal paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
TODO_DB = os.path.join(DATA_DIR, "todo.db")

# Initialize TO-DO database
def open_database():
	# If path to it does not exist, make it
	if not os.path.exists(DATA_DIR):
		os.makedirs(DATA_DIR)

	# Establish connection and a cursor
	con = sqlite3.connect(TODO_DB)
	cur = con.cursor()

	# Create table if it's the first time
	cur.execute("""
		CREATE TABLE IF NOT EXISTS tasks
		(id INTEGER PRIMARY KEY,
		task TEXT NOT NULL,
		deadline TEXT NOT NULL,
		mark TEXT NOT NULL)
	""")
	
	con.commit()

	# Return current connection and a cursor to main
	return con, cur

# Close connections
def close_database(con):
	con.close()

# Add task
def add_task(con, cur, task, deadline):
	# Make default mark
	mark = "[ ]"
	
	# Insert user's task
	cur.execute("INSERT INTO tasks (task, deadline, mark) VALUES (?, ?, ?)", 				(task, deadline, mark))
	con.commit()
	print(f"Added: {task} (Deadline: {deadline})\n")


# Print out the table
def show_tasks(cur):
	# Get tasks from the DB
	cur.execute("SELECT * FROM tasks ORDER BY deadline")
	tasks = cur.fetchall()
    
	# If list is empty, notify
	if not tasks:
		print("\nNo tasks found!\n")
		return
   
	# Make IDs the user will actually see 
	display_id = 0
	
	# Print tasks
	print("\n--- Your Tasks ---")
	print("-" * 55)
	for task in tasks:
		display_id += 1
		print(f" ID: {display_id} | Task: {task[1]} | Deadline: {task[2]} | Done: {task[3]}")
	print("-" * 55)
	print("\n")
	
	# Return tasks to later be used for removal and marking
	return tasks

# Remove tasks
def remove_task(con, cur, tasks, display_id):
	# Turn what user selected into DB values
	selected_id = tasks[display_id - 1][0]
	selected_task = tasks[display_id - 1][1]
	selected_deadline = tasks[display_id - 1][2]
	
	# Delete task from the table
	cur.execute("DELETE FROM tasks WHERE id = ?", (selected_id,))
	print(f"Removed: {selected_task} | {selected_deadline}\n")
	con.commit()

# Mark task as complete
def mark_task(con, cur, tasks, display_id):
	# Turn what user selected into DB values
	selected_id = tasks[display_id - 1][0]
	selected_task = tasks[display_id - 1][1]

	# Mark task as completed - [X]
	cur.execute("UPDATE tasks SET mark = '[X]' WHERE id = ?", (selected_id,))
	print(f"Completed: {selected_task}\n")
	con.commit()

# TEST CASE
if __name__ == "__main__":
	con, cur = open_database()
    
	# Add sample tasks
	add_task(con, cur, "Test 1", "2025-10-01")
	add_task(con, cur, "Test 2", "2025-10-05")
    
	# Show tasks
	tasks = show_tasks(cur)
    
	# Remove tasks
	for i in range(tasks):
		remove_task(con, cur, tasks, 1)	

	# Finish
	close_database(con)
