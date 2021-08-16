if not exist "%cd%\complexity" (
    mkdir "./complexity"
)
radon cc ./pygerber -s > complexity/cc.txt
radon mi ./pygerber -s > complexity/mi.txt
radon raw ./pygerber -s > complexity/raw.txt
radon hal ./pygerber > complexity/hal.txt