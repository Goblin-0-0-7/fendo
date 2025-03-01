all: ai

#TODO: use -OX optimizations
ai-gcc:
	gcc -fPIC -shared -o ai.dll ai.c

ai-debug-gcc:
	gcc -g -fPIC -shared -o  ai.dll ai.c

ai-debug:
	clang -g -fPIC -shared -fsanitize=address -o  ai.dll ai.c

clean:
	rm -f ai.so
	rm -f ai.dll