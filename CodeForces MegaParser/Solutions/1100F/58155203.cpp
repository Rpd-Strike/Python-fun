#include<bits/stdc++.h>
#define rep(i,a,b) for(int i=a;i<=b;i++)
#define rep2(i,a,b) for(int i=a;i>=b;i--)
using namespace std;
const int maxn=500010;
int p[maxn][21],pos[maxn][21];
int main()
{
    int N,Q,L,R,x;
    scanf("%d",&N);
    rep(i,1,N) {
        rep(j,0,20) p[i][j]=p[i-1][j],pos[i][j]=pos[i-1][j];
        scanf("%d",&x); int ti=i;
        rep2(j,20,0){
            if(x&(1<<j)){
                if(!p[i][j]) { p[i][j]=x; pos[i][j]=ti; break; }
                if(pos[i][j]<ti) swap(p[i][j],x),swap(pos[i][j],ti);
                x^=p[i][j];
            }
        }
    }
    scanf("%d",&Q);
    rep(i,1,Q) {
        scanf("%d%d",&L,&R);
        int res=0;
        rep2(j,20,0) if(pos[R][j]>=L&&(res^p[R][j])>res) res^=p[R][j];
        printf("%d\n",res);
    }
    return 0;
}