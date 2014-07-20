import CodeEnforcementReport
import NeighborhoodList

def main():
    my_hood = [str(x) for x in NeighborhoodList.GetHood("Harford Park")]
    cer = CodeEnforcementReport.CodeEnforcementReport()
    cer.load()
    cer.process()
    print cer.output_html(cer.filter_by_list(my_hood, ["Closed"]))
 
if __name__ == "__main__":
    main()
