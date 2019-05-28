
.DEFAULT_GOAL := init

init:
	test -e ./venv/bin/python || {\
		python3 -m venv venv ;} && \
	  test -r requirements.txt && ./venv/bin/pip install requirements.txt || exit 0;

test:
	./venv/bin/python -m unittest

run:
	./venv/bin/python blackjack-ai-runner.py

play:
	./venv/bin/python blackjack-ai-runner.py --interactive

