if not exist "%cd%\stats" (
    mkdir "./stats"
)
radon cc ./pygerber -s > stats/cc.txt
radon mi ./pygerber -s > stats/mi.txt
radon raw ./pygerber -s > stats/raw.txt
radon hal ./pygerber > stats/hal.txt
coverage run -m unittest discover
coverage report -m --skip-covered --skip-empty --omit="./tests/**/*.*","./tests/*.*" > stats/test_coverage.txt