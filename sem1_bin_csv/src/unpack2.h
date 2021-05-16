#ifndef UNPACK_2
#define UNPACK_2

typedef struct archive_rec
{
  long int IHD[9];
  float HEAD[23];
  long int ISTAT[8];
  float HOUS[15];
  long int MEPI[2];
  long int MEP[4][19];
  long int IHEP[2][11];
  float TED[4][18];
  float TEDFX[4];
} archive_rec_t;

void unpack2_(long int *IEND);
void open_archive(char* filename);

extern archive_rec_t rec_;

#endif
