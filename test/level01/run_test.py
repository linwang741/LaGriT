#! /usr/lanl/bin/python
# for lanl machines /usr/bin/env python
# for sgi /usr/lanl/bin/python
#------------------------------------------------------------------------------
#  Name: check_test.py
#  Last Modified: Jan 2008 by TAM 
#
#  Need to:
#  add debug runs
#  test error captures
#
#------------------------------------------------------------------------------

import fileinput, string, os, sys, datetime, time

##############################################################################
# Routines listed here, main at bottom
#
#------------------------------------------------------------------------------
# Routine: directoryWalker()
# recursively walks through all directories 
#------------------------------------------------------------------------------
def directoryList( unused, dirName, fileList ):
    
    icount = 0
    for entry in fileList:
        icount = icount+1 
        
    print dirName+" has "+repr(icount)+" files."

##############################################################################
# MAIN begin
#
# call lagrit with driver
# starting programs from the command line 
# os.system(cmd) or fo1 = os.popen(cmd) fo1.close()
#
#------------------------------------------------------------------------------

if __name__ == "__main__":

  dirList = []
  errList = []
  errmess = []
  ierr = 0
  itest = 0
  osname="unknown"
  ostag=""
  result_dir = 0

# get platform
  osname= string.lower(sys.platform)
  if osname.find("linux") >= 0 :
     ostag="lin" 
     xlagrit="/home/tam/src/lagrit/bin/lagrit_lin_o"
  elif osname.find("sun")>=0 or osname.find("sol")>=0 :
     ostag="sun" 
     xlagrit="/home/tam/src/lagrit/bin/lagrit_sun_o"
  elif osname.find("darwin")>= 0 :
     ostag="mac" 
     xlagrit="/home/tam/src/lagrit/bin/lagrit_mac_o"
  elif osname.find("IRIX")>= 0 :
     ostag="sgi" 
     xlagrit="/home/tam/src/lagrit/bin/lagrit_sgi_o"
     xlagrit="/home/tam/src/lagrit/bin/lagrit_sgi_g"
  elif osname.find("irix")>= 0 :
     ostag="sgi" 
     xlagrit="/home/tam/src/lagrit/bin/lagrit_sgi_o"
  else :
     raise SystemExit, "Exiting Early, Unrecognized OS: "+osname
 
# for each test directory
# main loop
  dtop = os.curdir
  for name in os.listdir(dtop) :
    dwork = os.path.join(dtop, name)

#---go into each directory and do some work
    if os.path.isdir(dwork) : 
        errmess.append("empty")
  print osname, ostag

# define top directory as current directory
  dtop = os.curdir
  dtop_path = os.getcwd()
  fscreen = dtop_path+"/stdout_"+ostag+".txt"
  date = time.ctime()
  wfile = open(fscreen,'w')
  line= "OS: "+osname+"\n"+"USING: "+xlagrit
  print line
  wfile.write(line+"\n")
  line= "Top directory: "+dtop_path+" at "+date
  print line
  wfile.write(line+"\n")
  wfile.close()

# for each test directory
# main loop
  for name in os.listdir(dtop) :
    dwork = os.path.join(dtop, name)

#---skip results directory until end
    if (dwork == "./result_files") :
        result_dir = 1

#---go into each directory and do some work
    elif os.path.isdir(dwork) : 

        errmess.append("empty")
        os.chdir(dwork)

        itest=itest+1
        line= " "+repr(itest)+"  Test Directory "+dwork+" -----------------------" 
        print line
        wfile = open(fscreen,'a')
        wfile.write(line+"\n")
        wfile.close()

        if (os.path.exists("outx3dgen")) :
          cmd = "cp -p outx3dgen prev_outx3dgen"
          fo1 = os.system(cmd)
          cmd = "rm out*"
          fo1 = os.system(cmd)


        if (os.path.exists("input.lgi")) : 
          cmd = xlagrit+" < input.lgi >> "+fscreen
          print cmd
          fo1 = os.system(cmd)
          print "System exit: "+repr(fo1)
          if (fo1 == 0) :
            dirList.append(repr(itest)+" "+dwork)
          else :
            errList.append(repr(itest)+" "+dwork)
            errmess[ierr]="Exit code: "+repr(fo1)
            ierr = ierr+1

        else :
          print "File missing: input.lgi" 
          errList.append(repr(itest)+" "+dwork)
          errmess[ierr]="Missing LaGriT input file."
          ierr = ierr+1
        
        os.chdir(dtop_path)
#---done with work in lower directory
           
# end main loop
  wfile.close()
  print "Testing Done. "

# search outx3dgen files for key start and end phrases
  progstr="Program header not found. "
  sustr="Program not completed. "
  nfind=0
  rfile=open(fscreen,'r')
  outx3dgen=rfile.readlines()
  for line in outx3dgen :
      
      dirno = line.find("Test Directory")
      progno=line.find("Program")
      suno=line.find("successfully")
   
      if progno >= 0 :
          progstr="   "+line[20:55] 
      if suno >= 0 :
          sustr=line[:29] 
      if dirno >= 0  :
          dirstr="Check outx3dgen "+line[:50]
          if nfind > 0 : 
             print dirprev
             print progstr+" : "+sustr
          nfind=nfind+1
          dirprev=dirstr
  rfile.close()

# attempt to pass error conditions if found
  if (ierr > 0) :
    i = 0
    print
    print  "LAGRIT EXIT ERROR: "+repr(ierr)+" directories failed:"+"/n"
    for d in errList :
      print "    "+errList[i]+" Error: "+errmess[i]
      print "---- tail outx3dgen ------------------"
      cmd="tail "+errList[i]+"/outx3dgen"
      fo1 = os.system(cmd)
      print "--------------------------------------"
      print " "
      i=i+1

  print "\n"+"Found "+repr(nfind)+" completed outx3dgen files out of "+repr(itest)+" test directories."
  if result_dir :
    b = os.system('cp -p '+fscreen+' ./result_files')
    print "Check done."+"\n"+"Screen output written to: "+"\n"
    print fscreen+"\n"
    print "and copied to ./result_files "+"\n"
  
  else :
    print "LaGriT outx3dgen and screen output written to "+fscreen+"\n"
      
# end Main 
#------------------------------------------------------------------------------

