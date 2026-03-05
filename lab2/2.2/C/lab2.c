#include <stdio.h>
int main(){
	int noOfy1Modules = 3;
	int year_1grades[3] = {97, 93, 90};
	
	printf("Year 1 grades (%d modules): \n", noOfy1Modules);
	for (int i = 0; i < noOfy1Modules; i++){
		printf("Grade %d = %d\n", i + 1,  year_1grades[i]);
	}
	
	int year_2grades[6];
	for (int i = 0; i < noOfy1Modules; i++){
		year_2grades[i] = year_1grades[i];
		printf("Grade %d added to second array\n", i + 1);
	}
	year_2grades[noOfy1Modules] = 100;
	year_2grades[noOfy1Modules + 1] = 100;
	year_2grades[noOfy1Modules + 2] = 100;
	int noOfy2Modules = noOfy1Modules + 3;
	
	printf("Year 2 grades (%d modules): \n", noOfy2Modules);
	for (int i = 0; i < noOfy2Modules; i++){
		printf("Grade %d = %d\n", i + 1,  year_2grades[i]);
	} 
	int integer;
	printf("Size of year_1grades: %zu bytes\n", sizeof(year_1grades));
	printf("Size of year_2grades: %zu bytes\n", sizeof(year_2grades));
	printf("Number of elements: %zu bytes\n", (sizeof(year_2grades) / sizeof(int)));
	printf("Size of each element: %zu bytes", sizeof(integer));
	
}