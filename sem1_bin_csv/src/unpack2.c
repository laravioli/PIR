/* =================================================================   
   Function: unpack2.c                                                   

            unpack2.c performs the reverse function of pack.c 
            routine and returns data to a FORTRAN /REC/ common block.
			unpack2.c also assumes incoming data to be of BIG
			ENDIAN format and converts it to LITTLE ENDIAN.
							
				Little ENDIAN (DEC, PC):  Bytes 1  2  
				Big ENDIAN (Apollo):      Bytes 2  1
				
				Little ENDIAN (DEC, PC):  Bytes 1  2  3  4
				Big ENDIAN (Apollo):      Bytes 4  3  2  1
				            

   Calling Format from FORTRAN:	                                       
                                     CALL unpack2 
                                     (case-insensitive)
                                                                       
   Compilation:  c89 -c unpack2.c                                       
                 Note: Do not use f77 to compile and link unpack2.c     
                 because the preprocessor f77 will use cc instead      
                 c89 and some ANSI standards are not allowed in cc.    
                 
   Linkage:  f77 -o /tiros/dec_readin.exe dec_readin.o unpack.o        
                    correct.o tflux.o c_meped.o pack.o -lcdf.a                                  
             File 'l_dec_readin' contains the above link statement.    
                                                                       
   Programmer: Minh Huynh                                              
                                                                       
   Revision: 1.0 -- Jan 22, 1993
   IMPORTANT NOTES: Do NOT confuse this to unpack.c routine.
                    If there is a choice between code efficiency and
                    clarity, the latter is intentionally used.

   ================================================================= 
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>

#ifdef _WIN32
#include <winsock2.h>
#else
#include <netinet/in.h>
#endif

#include "unpack2.h"

#define DEC 1 /* change to 0 if used on machine with \
                   default 16-bit int. e.g. IBM/PC-AT */
#if DEC == 1
typedef int L_int;
typedef unsigned int u_L_int;
#endif

#if DEC == 0
typedef long int L_int;
typedef unsigned long int u_L_int;
#endif

#define FOREVER (;;)

struct IN_P
{
  long int IHD_Msec;
  long int JHEAD[22];
  long int JTEDFX[4];
  short int JHOUS[15];
  short int IHD[8];
  short int ISTAT_P[2];
  unsigned char Index_MEPI[2];
  unsigned char Index_MEP[4][19];
  unsigned char Index_IHEP[2][11];
  unsigned char Index_TED[4][18];
  unsigned char Prog_Ver;
} in_p_;

/* sizeof_IN_P is 332 */

int sizeof_IN_P = 332;
int i = 0, j = 0, k = 0, num_char;
char filename[] = "N72141.NEW";
struct S
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
  long int ISTAT_P[2];
  long int Index_MEPI[2];
  long int Index_MEP[4][19];
  long int Index_IHEP[2][11];
  long int Index_TED[4][18];
  long int IOPEN;
  long int IEND;
} r_;
archive_rec_t rec_;

FILE *ff_in, *ff_out;

void unpack2_(long int *IEND)

{

  float c2[] = {1057., 1121., 1185., 1249., 1313., 1377., 1441.,
                1505., 1569., 1633., 1697., 1761., 1825., 1889., 1953., 2017.,
                2113., 2241., 2369., 2497., 2625., 2753., 2881., 3009.,
                3137., 3265., 3393., 3521., 3649., 3777., 3905., 4033.,
                4225., 4481., 4737., 4993., 5249., 5505., 5761., 6017.,
                6273., 6529., 6785., 7041., 7297., 7553., 7809., 8065.,
                8449., 8961., 9473., 9985., 10497., 11009., 11521., 12033.,
                12545., 13057., 13569., 14081., 14593., 15105., 15617., 16129.,
                16897., 17921., 18945., 19969., 20993., 22017., 23041., 24065.,
                25089., 26113., 27137., 28161., 29185., 30209., 31233., 32257.,
                33793., 35841., 37889., 39937., 41985., 44033., 46081., 48129.,
                50177., 52225., 54273., 56321., 58369., 60417., 62465., 64513.,
                67584., 71680., 75776., 79872., 83968., 88064., 92160., 96256.,
                4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75,
                135168., 143360., 151552., 159744., 167936., 176128., 184320., 192512.,
                2.125, 2.375, 2.625, 2.875, 3.125, 3.375, 3.625, 3.875,
                0.0625, 0.1875, 0.3125, 0.4375, 0.5625, 0.6875, 0.8125, 0.9375,
                1.0625, 1.1875, 1.3125, 1.4375, 1.5625, 1.6875, 1.8125, 1.9375,
                -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
                8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5,
                17., 18., 19., 20., 21., 22., 23., 24.,
                25., 26., 27., 28., 29., 30., 31., 32.,
                34., 36., 38., 40., 42., 44., 46., 48.,
                50., 52., 54., 56., 58., 60., 62.,
                64., 67., 71., 75., 79., 83., 87.,
                91., 95., 99., 103., 107., 111., 115., 119.,
                123., 127., 133., 141., 149., 157., 165.,
                173., 181., 189., 197., 205., 213.,
                221., 229., 237., 245., 253., 265., 281., 297.,
                313., 329., 345., 361., 377.,
                393., 409., 425., 441., 457., 473., 489., 505.,
                529., 561., 593., 625.,
                657., 689., 721., 753., 785., 817., 849., 881.,
                913., 945., 977., 1009.};

  float ic[] = {1057., 1121., 1185., 1249., 1313., 1377., 1441.,
                1505., 1569., 1633., 1697., 1761., 1825., 1889., 1953., 2017.,
                2113., 2241., 2369., 2497., 2625., 2753., 2881., 3009.,
                3137., 3265., 3393., 3521., 3649., 3777., 3905., 4033.,
                4225., 4481., 4737., 4993., 5249., 5505., 5761., 6017.,
                6273., 6529., 6785., 7041., 7297., 7553., 7809., 8065.,
                8449., 8961., 9473., 9985., 10497., 11009., 11521., 12033.,
                12545., 13057., 13569., 14081., 14593., 15105., 15617., 16129.,
                16897., 17921., 18945., 19969., 20993., 22017., 23041., 24065.,
                25089., 26113., 27137., 28161., 29185., 30209., 31233., 32257.,
                33793., 35841., 37889., 39937., 41985., 44033., 46081., 48129.,
                50177, 52225, 54273, 56321, 58369, 60417, 62465, 64513,
                67585, 71681, 75777, 79873, 83969, 88065, 92161, 96257,
                100353, 104449, 108545, 112641, 116737, 120833, 124929, 129025,
                135169, 143361, 151553, 159745, 167937, 176129, 184321, 192513,
                200705, 208897, 217089, 225281, 233473, 241665, 249857, 258049,
                270337, 286721, 303105, 319489, 333873, 352257, 368641, 385025,
                401409, 417793, 434177, 450561, 466945, 483329, 499713,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 36, 38, 40, 42, 44,
                46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 67, 71, 75, 79, 83, 87, 91, 95,
                99, 103, 107, 111, 115, 119, 123, 127, 133, 141, 149, 157, 165, 173,
                181, 189, 197, 205, 213, 221, 229, 237, 245, 253, 265, 281, 297,
                313, 329, 345, 361, 377, 393, 409, 425, 441, 457, 473, 489, 505,
                529, 561, 593, 625, 657, 689, 721, 753, 785, 817, 849, 881, 913,
                945, 977, 1009};

  long temp;
  short int s_temp;

#if 0 
printf (" Size of struct IN_P = %d ",sizeof(struct IN_P));
printf (" --- r_.IOPEN = %d ",r_.IOPEN);
#endif

  /* --------- Read a record from the PACKED input file --- */
  /*   printf (" Read a buffer ..\n");  */
  num_char = fread(&in_p_, sizeof_IN_P, 1, ff_in);
  if (num_char != 1)
  {
    *IEND = 1;
    r_.IEND = 1;
    printf(" EOF encountered.... \n");
    fclose(ff_in);
    return;
  }

  /* -------- Unpack IHD[] into their engineering values ---- */
  /*   printf(" Start processing a record \n");  */
  for (i = 0; i < 3; i++)
  {
    s_temp = r_.IHD[i] = in_p_.IHD[i];
    r_.IHD[i] = ntohs(s_temp);
  }
  for (i = 3; i < 8; i++)
  {
    s_temp = r_.IHD[i + 1] = in_p_.IHD[i];
    r_.IHD[i + 1] = ntohs(s_temp);
  }
  r_.IHD[3] = ntohl(in_p_.IHD_Msec);

  /* -------- Unpack HEAD[] --------------------------------- */
  for (i = 0; i < 2; i++)
  {
    temp = ntohl(in_p_.JHEAD[i]);
    r_.HEAD[i] = 0.01 * (float)(temp);
  }
  for (i = 2; i < 6; i++)
  {
    temp = ntohl(in_p_.JHEAD[i]);
    r_.HEAD[i] = (float)(temp);
  }
  temp = ntohl(in_p_.JHEAD[6]);
  r_.HEAD[6] = 0.01 * (float)(temp);
  temp = ntohl(in_p_.JHEAD[7]);
  r_.HEAD[7] = 0.01 * (float)(temp);
  for (i = 8; i < 12; i++)
  {
    temp = ntohl(in_p_.JHEAD[i]);
    r_.HEAD[i] = (float)(temp);
  }
  for (i = 12; i < 22; i++)
  {
    temp = ntohl(in_p_.JHEAD[i]);
    r_.HEAD[i] = 0.01 * (float)(temp);
  }
  r_.HEAD[22] = (float)(in_p_.Prog_Ver);
  /* -------- Unpack ISTAT_P[] ------------------------------ */
  for (i = 0; i < 2; i++)
  {
    s_temp = ntohs(in_p_.ISTAT_P[i]);
    r_.ISTAT_P[i] = (long)(s_temp);
  }

  r_.ISTAT[0] = (r_.ISTAT_P[0] & 0x80) >> 7;
  r_.ISTAT[1] = (r_.ISTAT_P[0] & 0x40) >> 6;
  r_.ISTAT[2] = (r_.ISTAT_P[0] & 0x20) >> 5;
  r_.ISTAT[3] = (r_.ISTAT_P[0] & 0x10) >> 4;
  r_.ISTAT[4] = (r_.ISTAT_P[0] & 0x08) >> 3;
  r_.ISTAT[5] = (r_.ISTAT_P[0] & 0x6) >> 1;
  r_.ISTAT[6] = (r_.ISTAT_P[0] & 0x1);
  r_.ISTAT[7] = r_.ISTAT_P[1] & 0xFF;

  /* -------- Unpack HOUS[] --------------------------------- */
  for (i = 0; i < 4; i++)
  {
    s_temp = ntohs(in_p_.JHOUS[i]);
    r_.HOUS[i] = ((float)(s_temp)) / 10.0;
  }
  s_temp = ntohs(in_p_.JHOUS[4]);
  r_.HOUS[4] = (float)(s_temp);
  for (i = 5; i < 7; i++)
  {
    s_temp = ntohs(in_p_.JHOUS[i]);
    r_.HOUS[i] = ((float)(s_temp)) / 10.0;
  }
  s_temp = ntohs(in_p_.JHOUS[7]);
  r_.HOUS[7] = ((float)(s_temp)) / 100.0;
  for (i = 8; i < 12; i++)
  {
    s_temp = ntohs(in_p_.JHOUS[i]);
    r_.HOUS[i] = (float)(s_temp);
  }
  s_temp = ntohs(in_p_.JHOUS[12]);
  r_.HOUS[12] = ((float)(s_temp)) / 100.0;
  for (i = 13; i < 15; i++)
  {
    s_temp = ntohs(in_p_.JHOUS[i]);
    r_.HOUS[i] = ((float)(s_temp)) / 10.0;
  }
  /* -------- Unpack MEPI[] --------------------------------- */
  for (i = 0; i < 2; i++)
    r_.MEPI[i] = (int)(ic[(in_p_.Index_MEPI[i])]);

  /* -------- Unpack MEP[][] -------------------------------- */
  for (i = 0; i < 4; i++)
  {
    for (j = 0; j < 19; j++)
    {
      r_.MEP[i][j] = (int)(ic[(in_p_.Index_MEP[i][j])]);
    }
  }
  /* -------- Unpack IHEP[][] ------------------------------- */
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 11; j++)
    {
      r_.IHEP[i][j] = (int)(ic[(in_p_.Index_IHEP[i][j])]);
    }
  }
  /* -------- Unpack TED[][] --------------------------------- */
  for (i = 0; i < 4; i++)
  {
    for (j = 0; j < 5; j++)
    {
      r_.TED[i][j] = ic[(in_p_.Index_TED[i][j])];
    }
    r_.TED[i][5] = (float)(in_p_.Index_TED[i][5]);
    for (j = 6; j < 18; j = j + 3)
    {
      r_.TED[i][j] = c2[(in_p_.Index_TED[i][j])];
      r_.TED[i][j + 1] = ic[(in_p_.Index_TED[i][j + 1])];
      r_.TED[i][j + 2] = (float)(in_p_.Index_TED[i][j + 2]);
    }
    /* -------- Unpack TEDFX[] --------------------------------- */
    temp = ntohl(in_p_.JTEDFX[i]);
    r_.TEDFX[i] = ((float)(temp)) / 1000.0;
  } /* End of for i=0;i<4 loop */

  /*  copy data to archive record which users are expecting --- */

  for (i = 0; i < 9; i++)
    rec_.IHD[i] = r_.IHD[i];
  for (i = 0; i < 23; i++)
    rec_.HEAD[i] = r_.HEAD[i];
  for (i = 0; i < 8; i++)
    rec_.ISTAT[i] = r_.ISTAT[i];
  for (i = 0; i < 15; i++)
    rec_.HOUS[i] = r_.HOUS[i];
  for (i = 0; i < 2; i++)
    rec_.MEPI[i] = r_.MEPI[i];
  for (i = 0; i < 4; i++)
  {
    for (j = 0; j < 19; j++)
    {
      rec_.MEP[i][j] = r_.MEP[i][j];
    }
  }
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 11; j++)
    {
      rec_.IHEP[i][j] = r_.IHEP[i][j];
    }
  }
  for (i = 0; i < 4; i++)
  {
    for (j = 0; j < 18; j++)
    {
      rec_.TED[i][j] = r_.TED[i][j];
    }
  }
  for (i = 0; i < 4; i++)
    rec_.TEDFX[i] = r_.TEDFX[i];

  /* ---------- END ------------------------------------------ */
}

/*--------------------------------------------------------------
	ROUTINE open_archive : opens 3480 semi-packed archive data file
*/

void open_archive(char* filename)
{
  if ((ff_in = fopen(filename, "rb")) == NULL)
  {
    printf("Error: cannot open %s\n", filename);
    fclose(ff_in);
    exit(1);
  };
}
