
.DEFAULT_GOAL := init

init:
	test -e ./venv/bin/python || {\
		python3 -m venv venv ;}
	  #test -r requirements.txt && ./venv/bin/pip install -r requirements.txt || exit 0;

test:
	./venv/bin/python -m unittest

run:
	./venv/bin/python blackjack-ai-runner.py \
		--agents CountingStacker2 CountingStacker3 player1 CountingStacker SmartStacker

play:
	./venv/bin/python blackjack-ai-runner.py \
		--rate 0.2 \
		--decks 6 \
		--shoes 3 \
		--verbose \
		--agents human CountingStacker2 CountingStacker3 CountingStacker SmartStacker

curses:
	./venv/bin/python blackjack-ai-runner.py \
		 -u --rate 0.1 -d 2 -s 1 --agents CountingStacker2 CountingStacker3 CountingStacker SmartStacker

update_deps:
	./venv/bin/pipreqs ./

clean:
	rm -r venv && \
	  find . -type d -name __pycache__ -exec rm -r {} \;

