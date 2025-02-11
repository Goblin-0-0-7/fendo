all: ai

ai: ai.c
	gcc -fPIC -shared -o ai.so ai.c

clean:
	rm -f ai.so