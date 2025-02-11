#include <stdlib.h> 

#include "gamerep.h"

#define INITIAL_SIZE 8 

/* ------------------------------ *\
|   Dynamic move_t Pointer Array   |
\* ------------------------------ */
typedef struct { 
	size_t size; 
	size_t capacity;
    move_t** array;
}dynamic_array_move_t; 

// function prototypes 
// array container functions 
void arrayInit(dynamic_array_move_t** arr_ptr); 
void freeArray(dynamic_array_move_t* container); 

// Basic Operation functions 
void addItemMove(dynamic_array_move_t* container, move_t* item); 
void insertItemMove(dynamic_array_move_t* container, int i, move_t* item); 
move_t* getItemMove(dynamic_array_move_t* container, int i); 
void deleteItemMove(dynamic_array_move_t* container, move_t* item);

//------Function Definitions------ 
// Array initialization 
void arrayInit(dynamic_array_move_t** arr_ptr) 
{ 
	dynamic_array_move_t *container; 
	container = (dynamic_array_move_t*)malloc(sizeof(dynamic_array_move_t)); 
	if(!container) { 
		printf("Memory Allocation Failed\n"); 
		exit(0); 
	} 

	container->size = 0; 
	container->capacity = INITIAL_SIZE; 
	container->array = (move_t *)malloc(INITIAL_SIZE * sizeof(move_t*)); 
	if (!container->array){ 
		printf("Memory Allocation Failed\n"); 
		exit(0); 
	} 

	*arr_ptr = container; 
} 


void addItemMove(dynamic_array_move_t* container, move_t* item) 
{ 
	if (container->size == container->capacity) { 
		int *temp = container->array; 
		container->capacity <<= 1; 
		container->array = realloc(container->array, container->capacity * sizeof(move_t*)); 
		if(!container->array) { 
			printf("Out of Memory\n"); 
			container->array = temp; 
			return; 
		} 
	} 
	container->array[container->size++] = item; 
} 


move_t* getItemMove(dynamic_array_move_t* container, int index) 
{ 
	if(index >= container->size) { 
		printf("Index Out of Bounds\n"); 
        return NULL;
	} 
	return container->array[index]; 
} 


void insertItemMove(dynamic_array_move_t* container, int index, move_t* item) 
{ 
	if (index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return; 
	} 
	container->array[index] = item; 
} 


void deleteItem(dynamic_array_move_t* container, int index) 
{ 
	if(index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return; 
	} 

	for (int i = index; i < container->size; i++) { 
		container->array[i] = container->array[i + 1]; 
	} 
	container->size--; 
} 


void freeArray(dynamic_array_move_t* container) 
{ 
	free(container->array); 
	free(container); 
}

/* ------------------------------------- *\
|   Dynamic Unsigned Char Pointer Array   |
\* ------------------------------------- */
typedef struct { 
	size_t size; 
	size_t capacity;
    unsigned char** array;
}dynamic_array_ucharp; 


// function prototypes 
// array container functions 
void arrayInit(dynamic_array_ucharp** arr_ptr); 
void freeArray(dynamic_array_ucharp* container); 

// Basic Operation functions 
void addItemUCharP(dynamic_array_ucharp* container, unsigned char* item); 
void insertItemUCharP(dynamic_array_ucharp* container, int i, unsigned char* item); 
unsigned char* getItemUCharP(dynamic_array_ucharp* container, int i); 
void deleteItemUCharP(dynamic_array_ucharp* container, unsigned char* item);

//------Function Definitions------ 
// Array initialization 
void arrayInit(dynamic_array_ucharp** arr_ptr) 
{ 
	dynamic_array_ucharp *container; 
	container = (dynamic_array_ucharp*)malloc(sizeof(dynamic_array_ucharp)); 
	if(!container) { 
		printf("Memory Allocation Failed\n"); 
		exit(0); 
	} 

	container->size = 0; 
	container->capacity = INITIAL_SIZE; 
	container->array = (unsigned char *)malloc(INITIAL_SIZE * sizeof(unsigned char*)); 
	if (!container->array){ 
		printf("Memory Allocation Failed\n"); 
		exit(0); 
	} 

	*arr_ptr = container; 
} 


void addItemUCharP(dynamic_array_ucharp* container, unsigned char* item) 
{ 
	if (container->size == container->capacity) { 
		int *temp = container->array; 
		container->capacity <<= 1; 
		container->array = realloc(container->array, container->capacity * sizeof(unsigned char*)); 
		if(!container->array) { 
			printf("Out of Memory\n"); 
			container->array = temp; 
			return; 
		} 
	} 
	container->array[container->size++] = item; 
} 


unsigned char* getItemUCharP(dynamic_array_ucharp* container, int index) 
{ 
	if(index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return -1; 
	} 
	return container->array[index]; 
} 


void insertItemUCharP(dynamic_array_ucharp* container, int index, unsigned char* item) 
{ 
	if (index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return; 
	} 
	container->array[index] = item; 
} 


void deleteItemUCharP(dynamic_array_ucharp* container, int index) 
{ 
	if(index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return; 
	} 

	for (int i = index; i < container->size; i++) { 
		container->array[i] = container->array[i + 1]; 
	} 
	container->size--; 
} 


void freeArray(dynamic_array_ucharp* container) 
{ 
	free(container->array); 
	free(container); 
}


/* ----------------------- *\
|   Dynamic Integer Array   |
\* ----------------------- */
typedef struct { 
	size_t size; 
	size_t capacity; 
	int* array; 
}dynamic_array_int; 

// function prototypes 
// array container functions 
void arrayInit(dynamic_array_int** arr_ptr); 
void freeArray(dynamic_array_int* container); 

// Basic Operation functions 
void addItemInt(dynamic_array_int* container, int item); 
void insertItemInt(dynamic_array_int* container, int i, int item); 
int getItemInt(dynamic_array_int* container, int i); 
void deleteItemInt(dynamic_array_int* container, int item);

//------Function Definitions------ 
// Array initialization 
void arrayInit(dynamic_array_int** arr_ptr) 
{ 
	dynamic_array_int *container; 
	container = (dynamic_array_int*)malloc(sizeof(dynamic_array_int)); 
	if(!container) { 
		printf("Memory Allocation Failed\n"); 
		exit(0); 
	} 

	container->size = 0; 
	container->capacity = INITIAL_SIZE; 
	container->array = (int *)malloc(INITIAL_SIZE * sizeof(int)); 
	if (!container->array){ 
		printf("Memory Allocation Failed\n"); 
		exit(0); 
	} 

	*arr_ptr = container; 
} 


void addItemInt(dynamic_array_int* container, int item) 
{ 
	if (container->size == container->capacity) { 
		int *temp = container->array; 
		container->capacity <<= 1; 
		container->array = realloc(container->array, container->capacity * sizeof(int)); 
		if(!container->array) { 
			printf("Out of Memory\n"); 
			container->array = temp; 
			return; 
		} 
	} 
	container->array[container->size++] = item; 
} 


int getItemInt(dynamic_array_int* container, int index) 
{ 
	if(index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return -1; 
	} 
	return container->array[index]; 
} 


void insertItemInt(dynamic_array_int* container, int index, int item) 
{ 
	if (index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return; 
	} 
	container->array[index] = item; 
} 


void deleteItemInt(dynamic_array_int* container, int index) 
{ 
	if(index >= container->size) { 
		printf("Index Out of Bounds\n"); 
		return; 
	} 

	for (int i = index; i < container->size; i++) { 
		container->array[i] = container->array[i + 1]; 
	} 
	container->size--; 
} 

 
void freeArray(dynamic_array_int* container) 
{ 
	free(container->array); 
	free(container); 
}
