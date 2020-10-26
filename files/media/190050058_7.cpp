#include <iostream>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <algorithm>
using namespace std;

int main(){
	ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL); // Fast I/O
	int nc, ns, max_course, operations;
	cin >> nc >> ns >> max_course >> operations;
	
	vector<string> courses(nc);
	map<string , int> C;
	vector<set<string>> course_to_student(nc);
	vector<int> slots(nc);
	vector<int> cap(nc);

	for(int i = 0; i < nc; i++) {
		cin >> courses[i] >> slots[i] >> cap[i];
		C[courses[i]] = i;
	}
	
	vector<string> rollnos(ns);
	map<string , int> M;
	vector<set<string>> student_to_course(ns);
	vector<set<int>> student_to_slot(ns);
	for(int i = 0; i < ns; i++) {
		cin >> rollnos[i];
		M[rollnos[i]] = i;
	}

	while(operations--){
		char op;
		cin >> op;
		if( op == 'R'){ // Register
			string r,c;
			cin >> r >> c;
			if(M.find(r) == M.end() || C.find(c) == C.end()) { cout << "fail" << endl; continue;}
			int stud = M[r];
			int cour = C[c];
			if(student_to_course[stud].size() >= max_course) { cout << "fail" << endl; continue;} // OVERLOAD
			if(student_to_slot[stud].find(slots[cour]) != student_to_slot[stud].end()){ cout << "fail" << endl; continue;} // SLOT CLASH
			if(course_to_student[cour].size() >= cap[cour] && cap[cour] != -1) { cout << "fail" << endl; continue;}
			course_to_student[cour].insert(r);
			student_to_course[stud].insert(c);
			student_to_slot[stud].insert(slots[cour]);
			cout << "success" << endl;
		}
	
		else if( op == 'D'){ // Drop
			string r,c;
			cin >> r >> c;
			if(M.find(r) == M.end() || C.find(c) == C.end()) { cout << "fail" << endl; continue;}
			int stud = M[r];
			int cour = C[c];
			if(student_to_course[stud].find(c) == student_to_course[stud].end()) { cout << "fail" << endl; continue;}
			student_to_course[stud].erase(c);
			course_to_student[cour].erase(r);
			student_to_slot[stud].erase(slots[cour]);	
			cout << "success" << endl;
		}

		else if( op == 'P'){ // Print
			string rest;
			getline(cin,rest);
			if(rest.size() == 7){
				string c = rest.substr(1,6);
				if(C.find(c) == C.end()){cout << endl; continue;}
				int cour = C[c];
				for(auto i = course_to_student[cour].begin(); i != course_to_student[cour].end(); i++) cout << *i << ' '; cout << endl;
			}
			else if(rest.size() == 10){
				string r = rest.substr(1,9);
				if(M.find(r) == M.end()){cout << endl; continue;}
				int stud = M[r];
				for(auto i = student_to_course[stud].begin(); i != student_to_course[stud].end(); i++) cout << *i << ' '; cout << endl;
			}
			else if(rest.size() == 20){
				string r1 = rest.substr(1,9), r2 = rest.substr(11,9);
				if(M.find(r1) == M.end() || M.find(r2) == M.end()){ cout << endl; continue;}
				int stud1 = M[r1], stud2 = M[r2];
				vector<string> intersection;
				set<string> A = student_to_course[stud1], B  = student_to_course[stud2];
				auto j = B.begin();
				for (auto i = A.begin(); i != A.end(); i++){
					if(j == B.end()) break;
					if(*i == *j) {
						intersection.push_back(*i);
						j++;
					}
				}
				for(auto i = intersection.begin(); i != intersection.end(); i++) cout << *i << ' '; cout << endl;
			}
			else if(rest.size() == 14){
				string c1 = rest.substr(1,6), c2 = rest.substr(8,9);
				if(C.find(c1) == C.end() || C.find(c2) == C.end()){ cout << endl; continue;}
				int cour1 = C[c1], cour2 = C[c2];
				vector<string> intersection;
				set<string> A = course_to_student[cour1], B  = course_to_student[cour2];
				auto j = B.begin();
				for (auto i = A.begin(); i != A.end(); i++){
					if(j == B.end()) break;
					if(*i == *j) {
						intersection.push_back(*i);
						j++;
					}
				}
				for(auto i = intersection.begin(); i != intersection.end(); i++) cout << *i << ' '; cout << endl;
			}
			else cout << endl;
		}	
			
	}
	return 0;
}