int func(double a, int b) {
}

int func(int a, int b) {
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
}
int calculateD(int a) {

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