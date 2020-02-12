void draw2D_easy() {

  int n = 0;
  int n_data = 0;

  TTree* limit = (TTree*) _file0->Get("limit");
  //   n = limit->Draw("2*deltaNLL:r","deltaNLL<10 && deltaNLL>-30","l");
  auto *c1 = new TCanvas("c1","A Zoomed Graph",200,10,700,500);
  limit->Draw("2*deltaNLL:k_my_1:k_my_2>>h(100,-10,10,100,-10,10)","2*deltaNLL<10","prof colz");

  limit->Draw("k_my_1:k_my_2","2*deltaNLL <1.2 && 2*deltaNLL >0.8 ","P same");
  TGraph *best_fit = (TGraph*)gROOT->FindObject("Graph");
  best_fit->SetMarkerSize(1); best_fit->SetMarkerStyle(34);best_fit->SetMarkerColor(kRed); best_fit->Draw("p same");



  std::cout << "Name:" <<std::endl;
  string name;
  std::cin >> name;
  c1->SaveAs(("W_HW_"+name+".png").c_str());

}
