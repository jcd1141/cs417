"""Lab 20: Build the Other Side — Server

Your FastAPI grading server. Build each section as you work
through the tasks. The TODOs tell you what to add and where.
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from grading import grade
import uuid

app = FastAPI()

grading_log = []
completed = {}
jobs = {}
job_submission_map = {}


@app.post("/grade")
def grade_endpoint(data: dict):
    student = data["student"]
    lab = data["lab"]
    slow = data.get("slow", False)
    submission_id = data.get("submission_id")

    if submission_id is not None and submission_id in completed:
        return completed[submission_id]

    score = grade(student, lab, slow=slow)

    result = {
        "student": student,
        "lab": lab,
        "score": score
    }

    grading_log.append(result)

    if submission_id is not None:
        completed[submission_id] = result

    return result


@app.get("/log")
def get_log():
    return {"entries": grading_log}


@app.post("/reset-log")
def reset_log():
    grading_log.clear()
    return {"status": "cleared"}


@app.post("/reset-completed")
def reset_completed():
    completed.clear()
    return {"status": "cleared"}


def run_grade_job(job_id: str, student: str, lab: int):
    score = grade(student, lab, slow=True)

    result = {
        "student": student,
        "lab": lab,
        "score": score
    }

    grading_log.append(result)
    jobs[job_id] = {
        "status": "complete",
        "result": result
    }


@app.post("/grade-async")
def grade_async(data: dict, background_tasks: BackgroundTasks):
    student = data["student"]
    lab = data["lab"]
    submission_id = data.get("submission_id")

    if submission_id is not None and submission_id in job_submission_map:
        existing_job_id = job_submission_map[submission_id]
        job = jobs[existing_job_id]

        if job["status"] == "pending":
            return JSONResponse(
                {"job_id": existing_job_id, "status": "accepted"},
                status_code=202
            )

        return JSONResponse(
            {
                "job_id": existing_job_id,
                "status": "complete",
                "result": job["result"]
            },
            status_code=200
        )

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}

    if submission_id is not None:
        job_submission_map[submission_id] = job_id

    background_tasks.add_task(run_grade_job, job_id, student, lab)

    return JSONResponse(
        {"job_id": job_id, "status": "accepted"},
        status_code=202
    )


@app.get("/grade-jobs/{job_id}")
def get_grade_job(job_id: str):
    if job_id not in jobs:
        return JSONResponse({"error": "job not found"}, status_code=404)

    job = jobs[job_id]

    if job["status"] == "pending":
        return {"job_id": job_id, "status": "pending"}

    return {
        "job_id": job_id,
        "status": "complete",
        "result": job["result"]
    }