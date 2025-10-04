import asana
from datetime import datetime

# CONFIGURATION
PERSONAL_ACCESS_TOKEN = 'YOUR_PERSONAL_ACCESS_TOKEN_HERE'
PROJECT_GID = '1211435660191126'

# Initialize Asana client
configuration = asana.Configuration()
configuration.access_token = PERSONAL_ACCESS_TOKEN
api_client = asana.ApiClient(configuration)
tasks_api = asana.TasksApi(api_client)

def check_and_complete_parent_tasks():
    """
    Check all tasks in the project.
    If a task has subtasks and all subtasks are completed,
    mark the parent task as complete.
    """
    print(f"\n{'='*60}")
    print(f"Running automation at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        # Get all tasks in the project
        print("Fetching tasks from project...")
        opts = {
            'opt_fields': 'name,completed,gid'
        }
        tasks = tasks_api.get_tasks_for_project(PROJECT_GID, opts)
        
        tasks_checked = 0
        tasks_completed = 0
        
        for task in tasks:
            tasks_checked += 1
            task_gid = task['gid']
            task_name = task['name']
            task_completed = task['completed']
            
            # Get subtasks 
            subtask_opts = {
                'opt_fields': 'name,completed'
            }
            subtasks = list(tasks_api.get_subtasks_for_task(task_gid, subtask_opts))
            
            # If task has subtasks
            if len(subtasks) > 0:
                print(f"\nTask: '{task_name}'")
                print(f"  - Subtasks found: {len(subtasks)}")
                
                # Check if all subtasks are completed
                all_subtasks_completed = all(subtask['completed'] for subtask in subtasks)
                
                completed_count = sum(1 for subtask in subtasks if subtask['completed'])
                print(f"  - Completed subtasks: {completed_count}/{len(subtasks)}")
                
                # If all subtasks are complete but parent is not
                if all_subtasks_completed and not task_completed:
                    print(f"  ✓ All subtasks completed! Marking parent task as complete...")
                    
                    # Mark parent task as complete
                    body = {'data': {'completed': True}}
                    tasks_api.update_task(task_gid, body)
                    
                    print(f"  ✓ SUCCESS: Parent task '{task_name}' marked as complete!")
                    tasks_completed += 1
                    
                elif all_subtasks_completed and task_completed:
                    print(f"  - Parent task already completed.")
                    
                else:
                    print(f"  - Not all subtasks completed yet.")
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  - Tasks checked: {tasks_checked}")
        print(f"  - Parent tasks auto-completed: {tasks_completed}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please check:")
        print("  1. Your Personal Access Token is correct")
        print("  2. Your Project GID is correct")
        print("  3. You have access to the project")

if __name__ == "__main__":
    print("=" * 60)
    print("ASANA PARENT TASK AUTO-COMPLETION SCRIPT")
    print("=" * 60)
    check_and_complete_parent_tasks()
    print("\n✓ Script execution completed!")