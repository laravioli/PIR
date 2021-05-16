#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>

#include "unpack2.h"

int main(int argc, char *argv[])
{
  if (argc != 3) {
    printf("Usage: unpack_csv <input> <output>\n");
    exit(0);
  }

  open_archive(argv[1]);

  long int *end =  malloc(sizeof(long int));

  FILE *fpt;
  fpt = fopen(argv[2], "w+");

  // HEADER
  fprintf(fpt,"HEAD_0, ");
  fprintf(fpt,"HEAD_1, ");
  fprintf(fpt,"HEAD_2, ");
  fprintf(fpt,"HEAD_3");
  
  fprintf(fpt,"\n");

  while (*end != 1)
  {
    unpack2_(end);

    // ROW
    fprintf(fpt,"%f, ", rec_.HEAD[0]);
    fprintf(fpt,"%f, ", rec_.HEAD[1]);
    fprintf(fpt,"%f, ", rec_.HEAD[2]);
    fprintf(fpt,"%f", rec_.HEAD[3]);

    fprintf(fpt,"\n");
  }

  fclose(fpt);
  return 0;
}
