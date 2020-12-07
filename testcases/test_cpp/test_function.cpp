int func(double a, int b) {
	cout<<"Hi buddy"<<endl;
	cout<<a<<b<<endl;
	return a+b+a;
}

int func(int a, int b) {
	cout<<"hello"<<endl;
	cout<<a<<b<<endl;
a
	return a+b+a;
}

int gcd(int a, int b) {
	if(a%b==0) return b;
	else return gcd(b, a%b);
}

int lcm(int f, int g) {
	int d = f*g;
	return d/gcd(f, g);
}

int calculateC( int b) {
	if(b<=1) return 1;
	else return b*calculateC(b-1);
}

int calculateB (int f) {
	return f*f*calculateC(2*f);
}
int calculateD(int a) {
	int u = a*a;
	int v = calculateB(u)*2;
}
int calculateE(int a) {
	int k = a*a;
	int l = calculateD(k)*2;
}
int calculateA(int a) {
	int c = a*a;
	int d = calculateE(c)*2;
}

void main() {
	int cad = 1;
	int dump = 2;
	int e = func(cad, dump);
	cout<<e<<endl;
	cout<< calculateA(2) <<endl;
	cout<<"bye";
	int w = gcd(2, 4)
}