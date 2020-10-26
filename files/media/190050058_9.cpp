#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

struct Triple {
	int x,y,index;
};

struct compareX {
	bool operator()(Triple const &t1, Triple const &t2) const { return t1.x < t2.x; }
};

struct compareY {
	bool operator()(Triple const &t1, Triple const &t2) const { return t1.y < t2.y; }
};

int main(){
	int n; cin >> n;
	vector<Triple> S1(n), S2(n);
	vector<multiset<Triple,compareY>> A, C, B, D;

	for(int i=0; i<n; i++) cin >> S1[i].x;
	for(int i=0; i<n; i++) cin >> S1[i].y;
	for(int i=0; i<n; i++) S1[i].index = i+1;
	sort(S1.begin(), S1.end(), compareX());

	for(int i=0; i<n; i++) cin >> S2[i].x;
	for(int i=0; i<n; i++) cin >> S2[i].y;
	for(int i=0; i<n; i++) S2[i].index = i+1;
	sort(S2.begin(), S2.end(), compareX());

	int nmultiset1 = 1, nmultiset2 = 1;
	multiset<Triple,compareY> h,k;
	h.insert(S1[0]); A.push_back(h);
	k.insert(S2[0]); C.push_back(k);

	for(int i=1; i<n; i++){
		if(S1[i].x == S1[i-1].x) A[nmultiset1-1].insert(S1[i]);
		else {
			multiset<Triple,compareY> a;
			a.insert(S1[i]);
			A.push_back(a);
			nmultiset1 += 1;
		}

		if(S2[i].x == S2[i-1].x) C[nmultiset2-1].insert(S2[i]);
		else {
			multiset<Triple,compareY> c;
			c.insert(S2[i]);
			C.push_back(c);
			nmultiset2 += 1;
		}
	}

	int i = 0, j = 0;
	vector<int> p, q;
	bool possible = true;
	bool unique = true;
	while(i < nmultiset1 && j < nmultiset2) {
        if(min(A[i].size(),C[j].size()) > 1)
        unique = false;
		if(A[i].size() >= C[j].size()) {
			multiset<Triple,compareY>::iterator it;
			for(it = C[j].begin(); it != C[j].end(); it++){
				multiset<Triple,compareY>::iterator t = A[i].lower_bound(*it);
				if(t == A[i].end()) {
					possible = false;
					break;
				}
				p.push_back(t->index);
				q.push_back(it->index);
				A[i].erase(t);
			}
			j++;
			if(A[i].empty())i++;
			if(!possible) break;
		}

		else {
			multiset<Triple,compareY>::iterator it;
			for(it = A[i].begin(); it != A[i].end(); it++) {
				auto t = C[j].upper_bound(*it);
				if(t == C[j].begin()) {
					possible = false;
					break;
				}
				t--;
				p.push_back(it->index);
				q.push_back(t->index);
				C[j].erase(t);
			}
			i++;
			if(C[j].empty()) j++;
			if(!possible) break;
		}
	}

	if(possible){
        	for(int i = 0; i < n; i++)  cout << p[i] << " ";    cout << endl;
        	for(int i = 0; i < n; i++)  cout << q[i] << " ";    cout << endl;
    	}
    	else {
		cout << "impossible" << endl;
        	return 0;
    	}


	int nSet1 = 1, nSet2 = 1;
	multiset<Triple,compareY> h1,k1;
	h1.insert(S1[0]); B.push_back(h1);
	k1.insert(S2[0]); D.push_back(k1);

	for(int i=1; i<n; i++){
		if(S1[i].x == S1[i-1].x) B[nSet1-1].insert(S1[i]);
		else {
			multiset<Triple,compareY> b;
			b.insert(S1[i]);
			B.push_back(b);
			nSet1 += 1;
		}

		if(S2[i].x == S2[i-1].x) D[nSet2-1].insert(S2[i]);
		else {
			multiset<Triple,compareY> d;
			d.insert(S2[i]);
			D.push_back(d);
			nSet2 += 1;
		}
	}

	i = nSet1-1, j = nSet2-1;
	vector<int> p_rev, q_rev;
	while(p_rev.size() < n) {
        if(!possible)
        break;
        if(B[i].size() >= D[j].size()) {
			for(auto it = D[j].rbegin(); it != D[j].rend(); it++){
				multiset<Triple,compareY>::iterator t = B[i].lower_bound(*it);
				if(t == B[i].end()) {
					possible = false;
					break;
				}
				p_rev.push_back(t->index);
				q_rev.push_back(it->index);
				B[i].erase(t);
			}
			j--;
			if(B[i].empty())i--;
			if(!possible) break;
		}

		else {
			for(auto it = B[i].rbegin(); it != B[i].rend(); it++) {
				auto t = D[j].upper_bound(*it);
				if(t == D[j].begin()) {
					possible = false;
					break;
				}
				t--;
				p_rev.push_back(it->index);
				q_rev.push_back(t->index);
				D[j].erase(t);
			}
			i--;
			if(D[j].empty()) j--;
			if(!possible) break;
		}
	}


	if(!possible) cout << "unique" << endl;
	else {
		for(int x=0; x<n ; x++) {
			//cout << p[x] << ' ';
			if(p[x] != p_rev[n-1-x]) unique = false;
		}
		//cout << endl;
		for(int x=0; x<n ; x++) {
			//cout << q[x] << ' ';
			if(q[x] != q_rev[n-1-x]) unique = false;
		}
		//cout << endl;
		if(unique) cout << "unique" << endl;
		else cout << "not unique" << endl;
	}


	return 0;
}
