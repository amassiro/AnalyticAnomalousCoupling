void draw_mio() {

  int n = 0;
  int n_data = 0;

  TTree* limit = (TTree*) _file0->Get("limit");
  //   n = limit->Draw("2*deltaNLL:r","deltaNLL<10 && deltaNLL>-30","l");
  n = limit->Draw("2*deltaNLL:k_my","deltaNLL<50 && deltaNLL>-30","l");
  TGraph *graphScan = new TGraph(n,limit->GetV2(),limit->GetV1());
  graphScan->RemovePoint(0);


  TGraph *graphScanData = 0;
  TTree* limitData = (TTree*) _file1->Get("limit");
  n_data = limitData->Draw("2*deltaNLL:k_my","deltaNLL<50 && deltaNLL>-30","l");
  graphScanData = new TGraph(n_data,limitData->GetV2(),limitData->GetV1());
  graphScanData->RemovePoint(0);
  graphScanData->SetTitle("");
  graphScanData->SetMarkerStyle(21);
  graphScanData->SetLineWidth(2);
  graphScanData->SetMarkerColor(kRed);
  graphScanData->SetLineColor(kRed);






  TLatex * tex;
  tex = new TLatex(0.94,0.92,"13 TeV");
  tex->SetNDC();
  tex->SetTextAlign(31);
  tex->SetTextFont(42);
  tex->SetTextSize(0.04);
  tex->SetLineWidth(2);

  TLatex * tex2 = new TLatex(0.14,0.92,"CMS");
  tex2->SetNDC();
  tex2->SetTextFont(61);
  tex2->SetTextSize(0.04);
  tex2->SetLineWidth(2);

  TLatex * tex3;
  //changed luminosity to the value used for the simulation
  tex3 = new TLatex(0.236,0.92,"L = 100 fb^{-1}  Preliminary");
  tex3->SetNDC();
  tex3->SetTextFont(52);
  tex3->SetTextSize(0.035);
  tex3->SetLineWidth(2);


  float minX = 999;
  float maxX = -999;


  //---- clean duplicate (it happens during lxbatch scan)
  std::vector <double> x_std;
  std::map <double, double> x_y_map;
  double x_value;
  double y_value;
  for (int ip = 0; ip<graphScan->GetN(); ip++) {

    graphScan->GetPoint (ip, x_value, y_value);
    //     std::cout << " x_value = " << x_value << std::endl;
    if (std::find(x_std.begin(), x_std.end(), x_value) != x_std.end()) {
      graphScan->RemovePoint(ip);
      //       std::cout << "removed " << ip << std::endl;
      ip--;
    }
    else {
      x_std.push_back(x_value);
      x_y_map[x_value] = y_value;
    }
  }

  graphScan->Set(0);


  float mc_min_x = -100;
  //---- fix the 0 of the likelihood scan
  float minimum = 1000;
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    if ( it->second < minimum ) {
      minimum = it->second;
      mc_min_x = it->first;
    }
  }
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    it->second =  it->second - minimum;
  }
  //---- (end) fix the 0 of the likelihood scan


  int ip = 0;
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    graphScan->SetPoint( ip, it->first , it->second);
    ip++;
  }


  //---- just for horizonthal lines
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    if ( it->first < minX ) {
      minX = it->first;
    }
    if ( it->first > maxX ) {
      maxX = it->first;
    }
  }
  //---- (end) just for horizonthal lines






  x_std.clear();
  x_y_map.clear();
  for (int ip = 0; ip<graphScanData->GetN(); ip++) {

    graphScanData->GetPoint (ip, x_value, y_value);
    //     std::cout << " x_value = " << x_value << std::endl;
    if (std::find(x_std.begin(), x_std.end(), x_value) != x_std.end()) {
      graphScanData->RemovePoint(ip);
      ip--;
    }
    else {
      x_std.push_back(x_value);
      x_y_map[x_value] = y_value;
    }
  }

  graphScanData->Set(0);

  float data_min_x = -100;
  //---- fix the 0 of the likelihood scan
  minimum = 1000;
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    if ( it->second < minimum ) {
      minimum = it->second;
      data_min_x = it->first;
    }
  }
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    it->second =  it->second - minimum;
  }
  //---- (end) fix the 0 of the likelihood scan


  ip = 0;
  for (std::map<double, double>::iterator it = x_y_map.begin(); it != x_y_map.end(); it++) {
    graphScanData->SetPoint( ip, it->first , it->second);
    ip++;
  }




  //manual limits for x
  Double_t min_x=-1.;
  Double_t max_x=1.;

  //find intesection of LL with the two lines
  Double_t x_1_p=0;
  Double_t x_1_n=0;
  Double_t x_2_p=0;
  Double_t x_2_n=0;
  Double_t precision=1e-6;
  std::cout << "intesections are(x_2_n, x_1_n,x_1_p,x_2_p)" <<endl;
  while(true){
      if(graphScanData->Eval(x_2_n)<3.84){
          x_2_n-=precision;
      }
      else{
          break;
      }
  }
  std::cout <<x_2_n <<std::endl;

  while(true){
      if(graphScanData->Eval(x_1_n)<1.){
          x_1_n-=precision;
      }
      else{
          break;
      }
  }
  std::cout<<x_1_n <<std::endl;

  while(true){
      if(graphScanData->Eval(x_1_p)<1.){
          x_1_p+=precision;
      }
      else{
          break;
      }
  }
  std::cout<<x_1_p <<std::endl;



  while(true){
      if(graphScanData->Eval(x_2_p)<3.84){
          x_2_p+=precision;
      }
      else{
          break;
      }
  }
  std::cout<<x_2_p <<std::endl;




 auto *c1 = new TCanvas("c1","A Zoomed Graph",200,10,700,500);
 auto *hpx = new TH2F("hpx","Zoomed likelihood scan",10,min_x,max_x,10,0,6.);

 c1->SetGrid();
 c1->SetTicks();
 c1->SetFillColor(0);
 c1->SetBorderMode(0);
 c1->SetBorderSize(2);
 c1->SetTickx(1);
 c1->SetTicky(1);
 c1->SetRightMargin(0.05);
 c1->SetBottomMargin(0.12);
 c1->SetFrameBorderMode(0);
 hpx->SetStats(kFALSE);   // no statistics
 hpx->Draw();
 hpx->GetXaxis()->SetTitle("k");
 hpx->GetYaxis()->SetTitle("-2 #Delta LL");

  if (graphScanData) {
    graphScanData->Draw("l");
  }
  tex->Draw("same");
  tex2->Draw("same");
  tex3->Draw("same");


  //  2deltaLogL = 1.00
  //  2deltaLogL = 3.84

  TLine *line1 = new TLine(min_x,1.0,max_x,1.0);
  line1->SetLineWidth(2);
  line1->SetLineStyle(2);
  line1->SetLineColor(kRed);
  line1->Draw();


  TLine *line2 = new TLine(min_x,3.84,max_x,3.84);
  line2->SetLineWidth(2);
  line2->SetLineStyle(2);
  line2->SetLineColor(kRed);
  line2->Draw();



  std::cout << " data at minimum:   " << data_min_x << std::endl;
  std::cout << " MC   at minimum:   " <<   mc_min_x << std::endl;




  c1->SaveAs("Hbox_ptl1.png");

}
