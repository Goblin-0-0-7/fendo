all: ai

#TODO: use -OX optimizations
ai-gcc:
	gcc -fPIC -shared -o ./bin/ai.dll ai.c

ai-debug-gcc:
	gcc -g -fPIC -shared -o  ./bin/ai.dll ai.c

ai-debug:
	clang -g -fPIC -shared -fsanitize=address -o  ./bin/ai.dll ai.c

clean:
	rm -f bin\ai.so
	rm -f bin\ai.dll