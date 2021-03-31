#include "UartRemote.h"

#include <stdarg.h>
#include <string.h>
#include <cstdio>



#define RXD1 18
#define TXD1 19


//#define UART Serial1

char cmd[20];

 UartRemote u;



void tst(unpackresult& args) {
   float a,b;
   u.getvariables(args,&a,&b);
   
   float c=a+b;
   Serial.println("sum = "+String(c));

   u.send("tstack","f",c);
   // printf("ready tst function\n");
}

void tstarr(unpackresult& args) {
   //printf("Entering tstarr\n");
   float a,b;
   unsigned char r[64];
   unsigned char q[64];
   u.getvariables(args,r);
//   for (int i=0; i<64; i++) {
//    printf("r[%d]=%d   ",i,r[i]);
//   }
//   printf("\n");
   // Serial.println("sum = "+String(c));
   for (int i=0; i<64; i++) {q[i]=i;}
   //printf("before send\n");
   u.send("tstack","a64B",q);
   //printf("after send\n");
}


void led(unpackresult& args) {
   int a,b,c;  float d,e,f,g;
   u.getvariables(args,&a,&b,&c,&d,&e,&f,&g);

   //printf("%d %d %d %f\n",a,b,c,d);
  u.send("ledack","b",0);
}



//u.cmds=own_cmds;

//void test() {
//    printf("Pack/Unpack test\n");
//    int a[3] = {1,2,5};
//    auto packed = pack("a3if",a,42.42f);
//    auto variables = unpack("a3if",packed.data);
//    printf("Pack/Unpack ready\n");
//    //tstarray(variables);
//}    

   
void setup() {
  Serial1.begin(230400, SERIAL_8N1, RXD1, TXD1);
  Serial.begin(115200);
  // put your setup code here, to run once:

  cmd_map own_cmds[]={
  {"led",&led},
  {"tst",&tst},
  {"tstarr",&tstarr},
};

   u.add_command("led", &led);
   u.add_command("tst", &tst);
   u.add_command("tstarr",&tstarr);
//   for (int j=0; j<1; j++) {
//  printf("Pack/Unpack test\n");
//    int a[64];
//    for (int i=0; i<64; i++) {a[i]=i;}
//
//    auto packed = u.pack("a64if",a,42.42f);
//    auto variables = u.unpack("a64if",packed.data);
//    printf("Pack/Unpack ready  size=%d\n",variables.size);
//   }
}



void loop() {
  // put your main code here, to run repeatedly:
  unpackresult rcvunpack = u.receive(cmd);
  Serial.println("Command received: "+String(cmd));
  u.command(cmd,rcvunpack);
 
}



/*

from uartremote import *
u=UartRemote()

for i in range(10):                                                                       
   q=u.send_receive('cmd','3i4f',i,212121,2,3.1715927,1,2,3)  


 
 */
