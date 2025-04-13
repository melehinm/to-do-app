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
		deadline TEXT NOT NULL)
	""")
	
	# Get number of tasks
	tasks = cur.fetchall()	
	con.commit()

	# Return current connection and a cursor to main
	return con, cur

# Close connections
def close_database(con):
	con.close()

# Add task
def add_task(con, cur, task, deadline):
	cur.execute("INSERT INTO tasks (task, deadline) VALUES (?, ?)", 
				(task, deadline))
	con.commit()
	print(f"Added: {task} (Deadline: {deadline})\n")


# Print out the table
def show_tasks(cur):
	cur.execute("SELECT * FROM tasks ORDER BY deadline")
	tasks = cur.fetchall()
    
	if not tasks:
		print("\nNo tasks found!\n")
		return
    
	display_id = 0
	print("\n--- Your Tasks ---")
	print("-" * 40)
	for task in tasks:
		display_id += 1
		print(f"ID: {display_id} | Task: {task[1]} | Deadline: {task[2]}")
	print("-" * 40)
	print("\n")

	return tasks

# Remove tasks
def remove_task(con, cur, tasks, display_id):
	selected_id = tasks[display_id - 1][0]
	selected_task = tasks[display_id - 1][1]
	selected_deadline = tasks[display_id - 1][2]
	
	cur.execute("DELETE FROM tasks WHERE id = ?", (selected_id,))
	print(f"Removed: {selected_task} | {selected_deadline}\n")
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
