#include <TStyle.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TGraphErrors.h>

void LSF(const Char_t *filename) {
  gStyle->SetOptFit(kTRUE);

  float x[1000], y[1000], ex[1000], ey[1000], dy[1000];
  string xtitle, ytitle, fitfun;
  int ftype;

  FILE *f = fopen(filename,"r");
  if (f == NULL) {
    printf("File %s not found.\n",filename);
    return;
  }

  // Read data
  int ndat = 0;
  while (fscanf(f,"%f %f %f",&(x[ndat]),&(y[ndat]),&(ey[ndat])) == 3 ) {
	ex[ndat] = 0.0;
	ndat++;
  }
/*  for (int i = 0; i < ndat; i++) printf("%d: :%f:\t:%f:\t:%f:\n",
        i,x[i],y[i],ey[i]);*/

  printf("Enter fit type: (1) pol1, (2) pol2, (3) exp, or (4) pow.\n");
  scanf("%d",&ftype);
  cin.ignore();

  printf("Read %d data points.\n",ndat);
  printf("Enter x-axis title\n");
  getline(cin,xtitle,'\n');
  printf("Enter y-axis title\n");
  getline(cin,ytitle,'\n');
 
  TH1F *fit;
  TH1F *residuals;
  TF1 *func;

  TGraphErrors *g = new TGraphErrors(ndat,x,y,ex,ey); 
  g->SetMarkerStyle(21);
  g->SetMarkerColor(kRed);
  g->SetLineColor(kRed);
  g->SetTitle(filename);
  fit = g->GetHistogram();
  fit->SetXTitle(xtitle.c_str());
  fit->SetYTitle(ytitle.c_str());

  TCanvas *c1 = new TCanvas("c1","LSF",600,700);
  c1->Divide(1,2);

  c1->cd(1);
  g->Draw("AP");
  switch(ftype) {
  case 1:
    g->Fit("pol1");
    func = g->GetFunction("pol1");
    break;
  case 2:
    g->Fit("pol2");
    func = g->GetFunction("pol2");
    break;
  case 3:
    g->Fit("expo");
    func = g->GetFunction("expo");
    break;
  case 4:
    func = new TF1("pow","[0]*x**[1]");
    func->SetParameter(0,1);
    func->SetParameter(0,-0.1);
    func->SetParName(0,"Constant");
    func->SetParName(1,"Exponent");
    g->Fit("pow");
    func = g->GetFunction("pow");
    break;
  default:
    printf("Function not found\n");
    return;
  }
  func->SetLineColor(kBlue);

  c1->cd(2);
  for( Int_t i=0; i<ndat; i++ ) {
    dy[i] = y[i]-func->Eval(x[i]);
  }
  TGraphErrors *r = new TGraphErrors(ndat,x,dy,0,ey);
  r->SetTitle("Residuals");
  residuals = r->GetHistogram();
  residuals->SetXTitle(xtitle.c_str());
  residuals->SetYTitle(ytitle.c_str());
  r->SetMarkerStyle(21);
  r->SetMarkerColor(kRed);
  r->Draw("AP");
}

void LSF() {
	Char_t filename[80];
	printf("Enter filename:\n");
	scanf("%s",filename);
	cin.ignore(); // ignore newline character from filename
	LSF(filename);
}
