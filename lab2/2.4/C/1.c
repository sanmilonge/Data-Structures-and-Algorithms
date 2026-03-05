#include <time.h>
#include <stdio.h>

void code()
{
    for (int i = 0; i < 10000; i++)
    {
        printf(".");
    }
    printf("\n");
}

int main()
{
    clock_t t;

    printf("start1: %d\n", (int)(t = clock()));

    code();

    printf("stop1: %d\n", (int)(t = clock() - t));
    double elapsed_time1 = t / CLOCKS_PER_SEC);
	
	printf("start2: %d\n", (int)(t = clock()));

    code();

    printf("stop2: %d\n", (int)(t = clock() - t));
    double elapsed_time2 = t / CLOCKS_PER_SEC);
	
	printf("start3: %d\n", (int)(t = clock()));

    code();

    printf("stop3: %d\n", (int)(t = clock() - t));
    double elapsed_time3 = t / CLOCKS_PER_SEC);
	
	double avg_time = (elapsed_time1 + elapsed_time2 + elapsed_time3) / 3;
	
	printf("Average time: %d\n", avg_time);

    return 0;
}