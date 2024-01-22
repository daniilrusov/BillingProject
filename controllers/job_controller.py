from redis import Redis

from dataobjects.task import Task

from .task_module import task, result_to_db, error_to_db

class JobController:

    def __init__(self, dam) -> None:
        self.dam = dam
        self.redis = Redis(host='myproj_redis', port=6379, decode_responses=True)
    
    def submit(self, task_process, data_provided, username, refund):
        print(f"TASK PROCESS {task_process}")
        status_ok = "Finished"
        status_bad = "Failed"
        id = task.apply_async(data_provided, link=result_to_db.s(status_ok), link_error=error_to_db.s(status=status_bad, username=username, refund=refund)).id
        #id = task.apply_async(data_provided, link=result_to_db.s(status_ok)).id
        print("JOB SENT")
        return id
