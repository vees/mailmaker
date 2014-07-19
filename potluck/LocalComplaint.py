import CodeEnforcementReport
import NeighborhoodList

def main():
    my_hood = [str(x) for x in NeighborhoodList.GetHood("Harford Park")]
    cer = CodeEnforcementReport.CodeEnforcementReport()
    cer.load()
    cer.process()
    cer.display_list(cer.filter_by_list(my_hood))
 
if __name__ == "__main__":
    main()
