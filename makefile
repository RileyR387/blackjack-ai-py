
.DEFAULT_GOAL := init

init:
	test -e ./venv/bin/python || {\
		python3 -m venv venv ;}
	  #test -r requirements.txt && ./venv/bin/pip install -r requirements.txt || exit 0;

test:
	./venv/bin/python -m unittest

run:
	./venv/bin/python blackjack-ai-runner.py \
		--decks 6 \
		--shoes 300 \
		--agents CountingStacker3 KayOh SmartStacker UpPull CountingStacker2

play:
	./venv/bin/python blackjack-ai-runner.py \
		--rate 0.6 \
		--decks 6 \
		--shoes 3 \
		--verbose \
		--agents human CountingStacker3 KayOh SmartStacker UpPull

update_deps:
	./venv/bin/pipreqs ./

clean:
	rm -r venv && \
	  find . -type d -name __pycache__ -exec rm -r {} \;

