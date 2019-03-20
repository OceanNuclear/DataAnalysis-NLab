// History:
// 08-Oct-2016 - PGJ - New LoadBuffit macro.

void LoadBuffit() {
  // Set style attributes
  gStyle->SetTitleBorderSize(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(kTRUE);
  gStyle->SetLineWidth(2);
  //  gStyle->SetTitleAlign(13);
  //  gStyle->SetTitleAlign(23);

  // Help interpreter to find include files
  gROOT->ProcessLine(".include /usr/local/share/physics/labs/y3/np/Buffit/buffit");

  // Load libbuffit.so
  FileStat_t buf;
  if( gSystem->GetPathInfo("buffit/libbuffit.so",buf)==0 ) {
    gSystem->Load("buffit/libbuffit.so");	 
    printf("WARNING: Using local version of buffit library.\n");
  } else if( gSystem->Load("/usr/local/share/physics/labs/y3/np/Buffit/buffit/libbuffit.so")<0 ) {
    printf("ERROR: Can't find buffit library.\n");
    return;
  }

  // Load Buffit.C
  if( gSystem->GetPathInfo("Buffit.C",buf)==0 ) { 
    gROOT->LoadMacro("Buffit.C");
    printf("WARNING: Using local version of Buffit.C.\n");
  } else
    gROOT->LoadMacro("/usr/local/share/physics/labs/y3/np/Buffit/Buffit.C");
}

