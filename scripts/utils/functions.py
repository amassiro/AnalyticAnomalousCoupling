import ROOT
import numpy as np
from array import array

def _getColor(color):
      if type(color) == int:
        return color
      elif type(color) == long:
        return int(color)
      elif type(color) == tuple:
        # RGB
        return ROOT.TColor.GetColor(*color)
      elif type(color) == str:
        # hex string
        return ROOT.TColor.GetColor(color)

def filter_common_ops_(d, limits="expected"):
    
    #print(d.keys())
    if len(d.keys()) <= 1 :  return 

    ops_ = []
    for an in d.keys():
         ops_.append(d[an]["constraints"][limits].keys())
    
    # select only the operators common to at least 2 analyses
    op_retained = []
    op_discarded = []
    for idx, op_list in enumerate(ops_):
        to_scan = list(ops_)
        del to_scan[idx]
        for op in op_list:
            if op in op_retained: continue
            if any(op in j for j in to_scan): op_retained.append(op)
            else: 
                print("--> Not considring " + op)
                op_discarded.append(op)
    
    # now delete from original dictionary the discarded operators
    for an in d.keys():
        for op in op_discarded:
            if op in d[an]["constraints"][limits].keys(): del d[an]["constraints"][limits][op]


def filter_for_analysis_(d, analysis_key, limits="expected"):
    
    # these are the ops of interest
    ops = d[analysis_key]["constraints"][limits].keys()
    
    # now cycle on all analyses and retain only ops of interest
    for an in d.keys():
        if an == analysis_key: continue
        # check ops not present in baseline list
        op_discarded = [i for i in d[an]["constraints"][limits].keys() if not i in ops]
        # and delete
        for op in op_discarded:
            del d[an]["constraints"][limits][op]
            
            
    # if the analysis has no common operators with baseline, delete
    del_an = []
    for an in d.keys():
        if len(d[an]["constraints"][limits].keys())==0: 
            print("-- Deleting analysis " + an)
            del_an.append(an)
    
    for d_an in del_an: del d[d_an]


def revert_dictionary(d, limits="expected"):
    # invert the logic: analyses: ops -> ops: analyses
    new_d = {}
    for an in d.keys():
        for op in d[an]["constraints"][limits].keys():
            if op not in new_d.keys(): 
                new_d[op] = {"legend_names": [], "reference": [], "best_fit": [], "interval": [], "colors": []}
            
            #print(d[an])
            new_d[op]["legend_names"].append(d[an]["name"])
            new_d[op]["reference"].append(d[an]["reference"])
            new_d[op]["best_fit"].append(d[an]["constraints"][limits][op][0])
            new_d[op]["interval"].append(d[an]["constraints"][limits][op][1:])
            
            color = ROOT.kBlack
            if "color" in d[an].keys(): color = d[an]["color"]
            new_d[op]["colors"].append(d[an]["color"])
            
    return new_d

def scale_operator(plot_dict, op, factor):
    if op not in plot_dict.keys(): return 
    new_name = op + "#times" + str(factor)
    plot_dict[new_name] = plot_dict.pop(op)
    for idx in range(len(plot_dict[new_name]["interval"])):
        # print(plot_dict[new_name]["interval"][idx])
        plot_dict[new_name]["interval"][idx][0] *= factor
        plot_dict[new_name]["interval"][idx][1] *= factor

def remove_analyses(d, keys):
    remove = []
    for k in d.keys():
        if k in keys: remove.append(k)
    for i in remove:
        del d[i]
    
def keep_analyses(d, keys):
    remove = []
    for k in d.keys():
        if k not in keys: remove.append(k)
    for i in remove:
        del d[i]
            

def convert_dict_to_objects(d, h):
    
    limit = [h.GetMinimum(), h.GetMaximum()]
    
    converted_down = 0.92*limit[0]
    converted_up = 0.92*limit[1]
    
    lines = []
    arrows = []
    graphs = []
    legend_graphs = []
    tex_names = []
    tex_references = []
    
    step = 0.3
    
    leg = ROOT.TLegend(0.1, 0.0, 0.9, 0.96)
    
    analyses_in_leg = []
    colors_in_leg = []
    ref_in_leg = []
    
    
    
    # idx here is the bin edge
    for idx, op in enumerate(d.keys()):
        
        center = h.GetBinCenter(idx+1)
        
        N = len(d[op]["legend_names"])
        
        ns = np.arange(step, (N)*step + step-0.01, step)
        ns += (center - ns.mean())
                
        for an_idx in range(N):
            
            inf = d[op]["interval"][an_idx][1]
            sup = d[op]["interval"][an_idx][0]
            
            color = d[op]["colors"][an_idx] 
            if not isinstance(color, int):
                # color = ROOT.TColor.GetColor(*d[op]["colors"][an_idx])
                color = _getColor(d[op]["colors"][an_idx])
            
            if inf < converted_down: 
                inf = converted_down
                arr = ROOT.TArrow(ns[an_idx], 0.94*limit[0] , ns[an_idx], 0.98*limit[0], 0.005, "|>")
                arr.SetLineColor(color)
                arr.SetFillColor(color);
                arrows.append(arr)
                
            if sup > converted_up: 
                sup = converted_up
                arr = ROOT.TArrow(ns[an_idx], 0.95*limit[1] , ns[an_idx], 0.99*limit[1], 0.005, "|>")
                arr.SetLineColor(color)
                arr.SetFillColor(color);
                arrows.append(arr)
            
            #print(ns[an_idx], inf , ns[an_idx], sup)
            
            l = ROOT.TLine(ns[an_idx], inf , ns[an_idx], sup)
            

            l.SetLineStyle(1)
            l.SetLineWidth(5)
            l.SetLineColor(color)
            
            g = ROOT.TGraph(1, array('f', [ns[an_idx]]), array('f', [0]))
            
            g.SetMarkerStyle(8)
            g.SetMarkerSize(1.3)
            g.SetMarkerColor(color)
            g.SetLineWidth(5)
            g.SetLineColor(color)
            
            if d[op]["legend_names"][an_idx] not in analyses_in_leg:
                leg.AddEntry(g, d[op]["legend_names"][an_idx])                
                analyses_in_leg.append(d[op]["legend_names"][an_idx])
                ref_in_leg.append(d[op]["reference"][an_idx])
                colors_in_leg.append(color)
                
            
            

            lines.append(l)
            graphs.append(g)
    

    # now build the tgraphs for the custom legend
    N = len(analyses_in_leg)
    #divide the x axis in equal amount of spaces
    xmin = h.GetXaxis().GetXmin()
    xmax = h.GetXaxis().GetXmax()
    
    xrange_ = abs(xmax) + abs(xmin)
    
    # Padding not symmetric as the last line will have a reference 
    
    xmin = xmin + xrange_ / 40
    xmax = xmax - xrange_ / 20
    
    x_values = np.linspace(xmin, xmax, N)
    
    
    # center of the tgraphs is based on the y axis limits
    graphs_y = limit[0] + (abs(limit[0])+abs(limit[1]))*0.15 
    error = float(abs(limit[0]) + abs(limit[1]))/10
    
    
    #print(analyses_in_leg, colors_in_leg, ref_in_leg, x_values)
    for name, color, ref, xs in zip(analyses_in_leg, colors_in_leg, ref_in_leg, x_values):
        g_ = ROOT.TGraphErrors(1, array("f", [xs]), array("f", [graphs_y]), array("f", [0]), array("f", [abs(error)]))
        g_.SetMarkerStyle(8)
        g_.SetMarkerSize(1.3)
        g_.SetMarkerColor(color)
        g_.SetLineWidth(5)
        g_.SetLineColor(color)
        
        
        legend_graphs.append(g_)
        
        tex1 = ROOT.TLatex(xs + xrange_/160, graphs_y  + 1.5*error,name)
        #tex1.SetTextFont(52)
        tex1.SetTextSize(0.06)
        tex1.SetLineWidth(2)
        tex1.SetTextAngle(90)
        
        tex_names.append(tex1)
        
        tex2 = ROOT.TLatex(xs + xrange_/40, limit[0] + (abs(limit[0]) + abs(limit[1]))*0.02, ref)
        tex2.SetTextFont(52)
        tex2.SetTextSize(0.06)
        tex2.SetLineWidth(2)
        tex2.SetTextAngle(90)
        
        tex_names.append(tex2)
        
        
            
    return lines, graphs, arrows, leg, legend_graphs, tex_names


def printTable(an, columns="ops"):
    ops = []
    analyses = []
    for key in an.keys():
        analyses.append(an[key]["name"])
        for op in an[key]["constraints"]["expected"]: 
            if op not in ops: ops.append(op)
    
    if columns == "ops":
        l = "|| c |"
        for i in ops: l += " c |"
        l += "|"
        print("\\begin{table}[h]")
        print("\\small")
        print("\\begin{center}")
        print("\\renewcommand{\\arraystretch}{1.2}")
        print("\\begin{tabular}{" + l + "}")
        print("\\hline")

        line = "   \\textbf{Analyses / W.C. [TeV$^{-2}$] } & "
        for op in ops:
            line += "\\textbf{" + op + "} & "
        line = line[:-2] + " \\\\"
        print(line)

        for an_ in analyses:

            l = " \\textbf{" + an_.replace("#", "\\") + "} & "
            for key in an.keys():
                if an[key]["name"] != an_: continue
                else:
                    for op in ops:
                        if op in an[key]["constraints"]["expected"]:
                            limits = an[key]["constraints"]["expected"][op]
                            l+= "{:.2f}".format(limits[2]) + "," + "{:.2f}".format(limits[1]) + " & "
                        else:
                            l += " - & "

            l = l[:-2] + " \\\\"
            print(l)



        print("   \\hline")
        print("\\end{tabular}")
        print("\\caption{ \\label{}}")
        print("\\end{center}")
        print("\\end{table}")
        
    elif columns == "an":
        l = "|| c |"
        for i in analyses: l += " c |"
        l += "|"
        print("\\begin{table}[h]")
        print("\\small")
        print("\\begin{center}")
        print("\\renewcommand{\\arraystretch}{1.2}")
        print("\\begin{tabular}{" + l + "}")
        print("\\hline")

        line = "   \\textbf{ W.C. [TeV$^{-2}$] / Analyses } & "
        for an_ in analyses:
            line += "\\textbf{" + an_.replace("#", "\\") + "} & "
        line = line[:-2] + " \\\\"
        print(line)

        for coef in ops:
            l = "\\textbf{" + coef + "}& "
            for ana in analyses:
                for key in an.keys():
                    if an[key]["name"] != ana: continue
                    else:
                        if coef in an[key]["constraints"]["expected"]:
                            limits = an[key]["constraints"]["expected"][coef]
                            l+= "{:.1f}".format(limits[2]) + "," + "{:.1f}".format(limits[1]) + " & "
                        else:
                            l += " - & "

            l = l[:-2] + " \\\\"
            print(l)
            
        print("   \\hline")
        print("\\end{tabular}")
        print("\\caption{ \\label{}}")
        print("\\end{center}")
        print("\\end{table}")