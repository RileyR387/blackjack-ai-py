
.DEFAULT_GOAL := init

init:
	test -e ./venv/bin/python || {\
		python3 -m venv venv ;} && \
	  test -r requirements.txt && ./venv/bin/pip install -r requirements.txt || exit 0;

update_deps:
	./venv/bin/pipreqs ./

test:
	./venv/bin/python -m unittest

run:
	./venv/bin/python blackjack-ai-runner.py

play:
	./venv/bin/python blackjack-ai-runner.py --interactive

clean:
	rm -r venv && \
	  find . -type d -name __pycache__ -exec rm -r {} \;

