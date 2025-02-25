all: ai

ai:
	gcc -fPIC -shared -o ai.dll ai.c

ai-debug:
	gcc -g -fPIC -shared -o ai.dll ai.c

clean:
	rm -f ai.so
	rm -f ai.dll