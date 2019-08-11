#include<bits/stdc++.h>

#ifdef lagrang3_DEBUG
#include "../include/debug.h"
#else
#define debug(...)
#endif

#define __fast_io__ \
	std::ios_base::sync_with_stdio(false);std::cin.tie(0);std::cout.tie(0);

#define get_max(a,b) a=std::max(a,b)
#define get_min(a,b) a=std::min(a,b)

typedef long long ll;
typedef long double ld;

const int oo=0x7fffffff;
const ll  OO=0x7fffffffffffffff;

class equiv {
	int N; //number of equivalence classes
	mutable std::vector<int> id;
	std::vector<int> rank;
	
	public:
	equiv(int _N): N(_N), id(N), rank(N,1){
		for(int i=0;i<N;i++)id[i]=i;
	}
	int operator[] (int n) const /* id of the root of [n] */
	{return   id[n]==n ? n : id[n]=(*this)[id[n]] ;}
	
	void link(int a,int b){ /* updates a~b */
		a=(*this)[a], b=(*this)[b];
		if(a!=b){
			N--;
			if(rank[a]<rank[b])std::swap(a,b);
			id[b]=a;
			rank[a]+=rank[b];
		}
	}
	int size()const{return N;}
	int size(int i)const{return rank[(*this)[i]];}
};

/*
	General purpose weighted and directed edge.
	26/07/2019
*/
template<class T>
class edge
{
	public:
	int first,second,id;
	T weight;
	
	edge()=default;
	edge(int u,int v,int i, T x): first(u),second(v),id(i),weight(x){}

	bool operator < (const edge& that)const
	{
		return weight == that.weight ? id < that.id : weight < that.weight;
	}
	
	edge reverse()const
	{
		return edge(second,first,id,weight);
	}
};

using namespace std;

int main(){
	__fast_io__;
	int n,m;cin>>n>>m;
	int a,b,w;
	cin>>a>>b>>w; m--,a--,b--;
	
	vector< edge<int> > E(m);
	for(int i=0;i<m;++i)
	{
		int u,v,w;
		cin>>u>>v>>w;--u,--v;
		E[i]=edge<int>({u,v,i,w});
	}
	
	sort(E.begin(),E.end());
	
	equiv R(n);
	for(auto e: E)
	{
		int u=R[e.first],v=R[e.second];
		a=R[a],b=R[b];
		
		if(u==v)continue;
		if(u>v)swap(u,v);
		if(a>b)swap(a,b);
		
		if(u==a and v==b)
		{
			cout<<e.weight<<"\n";
			return 0;
		}
		
		R.link(u,v);
	}
	
	cout<<"1000000000\n";
	return 0;
}

