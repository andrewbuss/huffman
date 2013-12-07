#include <stdio.h>
#include <stdlib.h>

struct Node{
  Node* l;
  Node* r;
  Node* p;
  char c;
  unsigned int s;
};

int compare(const void* a, const void* b){
  return (*(Node*)a).s-(*(Node*)b).s;
}

int main(){
  FILE* ifile = fopen("shakespeare.txt","r");
  Node nodes[512];
  int lastnode = 256;
  for(int i=0; i<512; i++){
    nodes[i].c = i;
    nodes[i].s = 0;
  }
  while(true){
    char c = fgetc(ifile);
    if (c==EOF) break;
    nodes[c].s++;
  }
  qsort(nodes, 256, sizeof(Node), compare);
  for(int i=0; i<256; i++){
    printf("%i: %c\n", nodes[i].s, nodes[i].c);
  }
  Node node;
  node.l = nodes;
  node.r = nodes+1;
  node.s = nodes[0].s+nodes[1].s;
  nodes[0].p = nodes+lastnode;
  nodes[1].p = nodes+lastnode;
  node.c = 0;
  nodes[lastnode++] = node;
  
  return 0;
}
