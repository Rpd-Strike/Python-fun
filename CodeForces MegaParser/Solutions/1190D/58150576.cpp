/*
EVER HERE..
*/
#include <bits/stdc++.h>
#define sz(v)   ((int)(v).size())
#define  all(v)    ((v).begin()),((v).end())
#define  allr(v)    ((v).rbegin()),((v).rend())
#define   pb         push_back
#define   mp         make_pair
#define    clr(v,d)      memset( v, d ,sizeof(v))
typedef  long long     ll ;
typedef  unsigned long long ull;
const double EPS= (1e-9);
using namespace std;
int getBit(int num, int idx) {return ((num >> idx) & 1) == 1;}
int setBit1(int num, int idx) {return num | (1<<idx);}
ll setBit0(ll num, int idx) {return num & ~(1ll<<idx);}
ll flipBit(int num, int idx) {return num ^ (1<<idx);}
void SP(){ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);}
const int N=200009;
vector<int> v1[N],v2[N];
map<int,int> mx,my;
int x[N],y[N],tree[4*N],v3[N],sizX,sizY;
void Put(int no,int fl)
{
    if(fl==0)
    {
        if(mx.find(no)==mx.end())
            mx[no]=sz(mx)+1;
    }
    else
    {
        if(my.find(no)==my.end())
            my[no]=sz(my)+1;
    }
}
int Get(int no,int fl)
{
    if(fl==0)
        return mx[no];
    return my[no];
}
ll calc(int x,int y,int fl)
{
    int id=lower_bound(all(v2[y]),x)-v2[y].begin();
    if(fl==0)
    return id;

    return sz(v2[y])-1-id;
}
void update(int pos,int val,int s=1,int e=sizX,int p=1)
{
    if(s==e)
    {
        tree[p]+=val;
        return ;
    }
    int m=(s+e)>>1;
    int lf= (p<<1);
    int rg= (lf|1);
    if(pos<=m)
    update(pos,val,s,m,lf);
    else
    update(pos,val,m+1,e,rg);
    tree[p]=tree[lf]+tree[rg];
}
int query(int a,int b,int s=1,int e=sizX,int p=1)
{
    if(a>e||b<s)
        return 0;
    if(s>=a&&e<=b)
        return tree[p];
    int m= (s+e)>>1;
    int lf= (p<<1);
    int rg= (lf|1);
    return query(a,b,s,m,lf)+query(a,b,m+1,e,rg);
}

int main()
{
    SP();
    int n;
    cin>>n;
    for(int i=0;i<n;i++)
    {
        cin>>x[i]>>y[i];
        mx[x[i]]=1;
        my[y[i]]=1;
    }
    sizX=0;sizY=0;
    for(auto it=mx.begin();it!=mx.end();it++)
    {
        (*it).second=++sizX;
    }
    for(auto it=my.begin();it!=my.end();it++)
    {
        (*it).second=++sizY;
    }

    for(int i=0;i<n;i++)
    {
        x[i]=mx[x[i]];
        y[i]=my[y[i]];
        v1[y[i]].pb(x[i]);
        v3[x[i]]=max(v3[x[i]],y[i]);
        v2[y[i]].pb(x[i]);
    }
    for(int i=1;i<=sizY;i++)
        sort(all(v2[i])),sort(all(v1[i]));

    for(int i=1;i<=sizX;i++)
        update(i,1);

    ll ans=0;
    for(int i=1;i<=sizY;i++)
    {
        int pre=0;
        for(int j=0;j<sz(v1[i]);j++)
        {
            int X=v1[i][j];
            ll rg= query(X,sizX);

            ll lf= query(pre+1,X);
            ans+= rg*lf;
            pre=X;
        }


        for(int j=0;j<sz(v1[i]);j++)
        {
            int X=v1[i][j];
            if(v3[X]<=i)
             update(X,-1);
        }
    }
    cout<<ans<<endl;
}


























