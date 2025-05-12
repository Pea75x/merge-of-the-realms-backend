from pydantic import BaseModel, root_validator

class CreateGroup(BaseModel):
    name: str
    problem: str
    total_time: int
    submission_time_allocated: int
    build_time_allocated: int
    testing_time_allocated: int

@root_validator(skip_on_failure=True)
def validate_total_time(cls, values):
    submission = values.get("submission_time_allocated", 0)
    build = values.get("build_time_allocated", 0)
    testing = values.get("testing_time_allocated", 0)
    total = values.get("total_time", 0)

    if submission + build + testing != total:
        raise ValueError("Total time must equal the sum of submission, build, and testing times.")
    return values