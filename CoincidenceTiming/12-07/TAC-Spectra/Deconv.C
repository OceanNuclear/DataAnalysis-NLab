Double_t fitfun(Double_t *x, Double_t *p) {
  Double_t lambda = TMath::Log(2)/p[3];
  Double_t xp = x[0] - p[1];
  Double_t sigma = p[2]/2.35;
  Double_t argexp = -1.*lambda*(xp-sigma*sigma*lambda/2.);
  Double_t argerf = (xp-sigma*sigma*lambda)/(TMath::Sqrt(2)*sigma);
  Double_t fitval = p[0]*0.5*TMath::Exp(argexp)*(1+TMath::Erf(argerf))+p[4];
  return fitval;
}

void Deconv(Char_t *filename) {
  gStyle->SetOptFit(kTRUE);

  float x[8192], y[8192], ex[8192], ey[8192], dy[8192];
  float xlo, xhi, norm, centroid, fwhm, lifetime, bkgnd;
  char line[80];
  string xtitle, ytitle;

  FILE *f = fopen(filename,"r");
  if (f == NULL) {
    printf("File %s not found.\n",filename);
    return;
  }

  // Read data
  int ndat = 0;
  int counts = 0;
  while (fscanf(f,"%f",&(y[ndat])) == 1 ) {
    x[ndat] = ndat;
    ey[ndat] = TMath::Sqrt(y[ndat]);
    counts += y[ndat];
    ndat++;
  }

  TH1F *spectrum = new TH1F("spectrum",filename,ndat,0,ndat);
  for( Int_t i=0; i<ndat; i++ )
    spectrum->SetBinContent(i,y[i]);
  
  printf("Read %d data points.\n",ndat);
  printf("Enter x-axis title\n");
  getline(cin,xtitle,'\n');
  printf("Enter y-axis title\n");
  getline(cin,ytitle,'\n');

  TCanvas* c1 = new TCanvas("c1","Deconv",600,700);
  c1->Divide(1,2);

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
  fit->SetTitle(filename);

  c1->cd(1);
  g->Draw("AP");
  c1->Update();

  printf("Enter lower limit of fit range\n");
  scanf("%f",&xlo);
  printf("Enter upper limit of fit range\n");
  scanf("%f",&xhi);
  func = new TF1("fitfun",fitfun,xlo,xhi,5);
  printf("Enter normalisation\n");
  scanf("%f",&norm);
  func->SetParameter(0,norm);
  printf("Enter gaussian centroid\n");
  scanf("%f",&centroid);
  func->SetParameter(1,centroid);
  printf("Enter gaussian fwhm\n");
  scanf("%f",&fwhm);
  func->SetParameter(2,fwhm);
  printf("Enter exponential lifetime\n");
  scanf("%f",&lifetime);
  func->SetParameter(3,lifetime);
  printf("Enter background\n");
  scanf("%f",&bkgnd);
  func->SetParameter(4,bkgnd);
  func->SetParName(0,"Normalisation");
  func->SetParName(1,"Centroid");
  func->SetParName(2,"FWHM");
  func->SetParName(3,"Halflife");
  func->SetParName(4,"Background");
  g->Fit("fitfun");
  func = g->GetFunction("fitfun");
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

void Deconv() {
	Char_t filename[80];
	printf("Enter filename:\n");
	scanf("%s",filename);
	cin.ignore(); // ignore newline character from filename
	Deconv(filename);
}
