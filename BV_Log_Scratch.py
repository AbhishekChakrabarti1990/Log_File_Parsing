#This Python script is meant to mine BV Log file and print statistics

import string
from datetime import *
from time import *

#defining class for procs

class Procedures:
 Name ="Default_Proc";
 start_time = datetime.now();
 end_time = datetime.now();
 duration = 0;
 
 def generate_duration(self):
  self.duration = timedelta.total_seconds(self.end_time-self.start_time);
  return self.duration;

derivation_procs = [];
validation_procs = [];

parser_total =[];
parser_basic = [];
parser_deriv_proc =[];
parser_val_proc =[];
#parser_val_proc_discard =[];
section_marker =[];
holder = [];


with open("o3089762.txt",'r') as reader:
 for line in reader:
  parser_total.append(line);

print("Parsed BV Log into",len(parser_total),"lines\n");  
print("Converted BV Log into lines. Hopefully!\n");

 
for i in range(0,len(parser_total)):
 if "Derivation Procedure Execution" in parser_total[i]:
  section_marker.append(i); #Derivation proc execution
  
 if "Validation Procedure Execution" in parser_total[i]:
  section_marker.append(i); #Validation proc execution





 
for i in range((section_marker[0]+1),(section_marker[1])):
 parser_deriv_proc.append(parser_total[i]); #Capturing derivation proc lines

for i in parser_deriv_proc:
 if "start time is" in i:
  continue;
 elif "Completed procedure" in i:
  continue;
 else:
  parser_deriv_proc.remove(i);

 
for i in range((section_marker[1]+1),len(parser_total)):
 parser_val_proc.append(parser_total[i]); #Capturing validation proc lines

 #end of Validation proc execution

  
for i in parser_val_proc:
 if "start time is" in i:
  continue;
 elif "Completed procedure" in i:
  continue;
 else:
  parser_val_proc.remove(i);

for i in range(0,len(parser_val_proc)):
 if "Indicator Question Checks for Patients with modified data" in parser_val_proc[i]:
  #print("Line ",i," is",parser_val_proc[i]);
  section_marker.append(i-2);
  
#for i in range(0,3):
 #print(i,section_marker[i]);#Printing section markers

#q = section_marker[2]+1;
#print (q);

 
#for i in range(q,len(parser_val_proc)):
 #parser_val_proc_discard.append(parser_val_proc[i]);
 
 
#for i in parser_val_proc:
 #if i in parser_val_proc_discard:
  #parser_val_proc.remove(i);

#for i in parser_val_proc:
 #print(i);
 
for i in range(0,len(parser_deriv_proc),2):
 proc_holder = Procedures();
 if "start time is" in parser_deriv_proc[i]:
  holder = parser_deriv_proc[i].split();
  parser_basic = holder[1].split("(");
  proc_holder.Name = parser_basic[0];
  derivation_procs.append(proc_holder);
  
for i in derivation_procs:
 for j in range(0,len(parser_deriv_proc)):
  if i.Name in parser_deriv_proc[j]:
   if "start time is" in parser_deriv_proc[j]:
    holder=parser_deriv_proc[j].split();
    i.start_time = datetime.strptime(((holder[(len(holder)-2)]+ " " +holder[(len(holder)-1)])),"%d-%b-%Y %H:%M:%S");
  
   elif "Completed procedure" in parser_deriv_proc[j]:
    holder=parser_deriv_proc[j].split();
    i.end_time = datetime.strptime(((holder[(len(holder)-2)]+ " " +holder[(len(holder)-1)])),"%d-%b-%Y %H:%M:%S");
 
   else:
    continue;
 Procedures.generate_duration(i);

for i in range(0,len(parser_val_proc),2):
 proc_holder = Procedures();
 if "start time is" in parser_val_proc[i]:
  holder = parser_val_proc[i].split();
  parser_basic = holder[1].split("(");
  proc_holder.Name = parser_basic[0];
  validation_procs.append(proc_holder);
  
for i in validation_procs:
 for j in range(0,len(parser_val_proc)):
  if i.Name in parser_val_proc[j]:
   if "start time is" in parser_val_proc[j]:
    holder=parser_val_proc[j].split();
    i.start_time = datetime.strptime(((holder[(len(holder)-2)]+ " " +holder[(len(holder)-1)])),"%d-%b-%Y %H:%M:%S");
  
   elif "Completed procedure" in parser_val_proc[j]:
    holder=parser_val_proc[j].split();
    i.end_time = datetime.strptime(((holder[(len(holder)-2)]+ " " +holder[(len(holder)-1)])),"%d-%b-%Y %H:%M:%S");
 
   else:
    continue;
 Procedures.generate_duration(i);	

#Average time for Derivation Procedures
j = 0;
for i in derivation_procs:
 j = j + i.duration;
deriv_avg = j/(len(derivation_procs));

#Average time for Validation Procedures
j = 0;
for i in validation_procs:
 j = j + i.duration;
val_avg = j/(len(validation_procs));

#Maximum Time for Derivation Procedures
derivation_max = Procedures();
derivation_max.duration = derivation_procs[0].duration;
for i in range(0,len(derivation_procs)):
 if derivation_procs[i].duration > derivation_max.duration:
  derivation_max=derivation_procs[i];

#Maximum Time for Validation Procedures
validation_max = Procedures();
validation_max.duration = validation_procs[0].duration;
for i in range(0,len(validation_procs)):
 if validation_procs[i].duration > validation_max.duration:
  validation_max=validation_procs[i];
 

'''for i in derivation_procs:
 print(i.Name," stared at ",i.start_time," and ended at ",i.end_time," and ran for ",i.duration, " seconds");
 
for i in validation_procs:
 print(i.Name," stared at ",i.start_time," and ended at ",i.end_time," and ran for ",i.duration, " seconds");'''
 
holder = parser_total[1].split();
i = datetime.strptime(((holder[(len(holder)-2)]+ " " +holder[(len(holder)-1)])),"%d-%b-%Y %H:%M:%S");

holder = parser_total[(len(parser_total)-1)].split();
j = datetime.strptime(((holder[(len(holder)-2)]+ " " +holder[(len(holder)-1)])),"%d-%b-%Y %H:%M:%S");


with open("o3089762_stats",'w+') as writer:
#Basic statistics
 writer.write("BASIC STATISTICS\n");
 writer.write("================\n");
 writer.write(parser_total[2]);
 writer.write(parser_total[1]);
 writer.write(parser_total[(len(parser_total)-1)]);
 holder = "BV ran for "+str((timedelta.total_seconds(j-i)))+" seconds";
 writer.write("\n");
 writer.write(holder);
 writer.write("\n\n");
 
 #Derivation Procedure Statistics
 writer.write("DERIVATION PROCEDURE STATISTICS\n");
 writer.write("===============================\n");
 writer.write(parser_total[section_marker[0]]);
 writer.write("Maximum duration taken by a Derivation Procedure is ");
 writer.write(str(derivation_max.duration));
 writer.write(" seconds");
 writer.write(" for ");
 writer.write(derivation_max.Name);
 writer.write("\n");
 writer.write("Average time taken by Derivation Procedures is ");
 writer.write("%.2f" % deriv_avg);
 writer.write(" seconds");
 writer.write("\n");
 for i in derivation_procs:
  writer.write(i.Name);
  writer.write(" started at ");
  writer.write(str(i.start_time));
  writer.write(", ended at ");
  writer.write(str(i.end_time));
  writer.write(" and ran for ");
  writer.write(str(i.duration));
  writer.write(" seconds");
  writer.write("\n");
 writer.write("\n\n");
  
  #Validation Procedure Statistics
 writer.write("VALIDATION PROCEDURE STATISTICS\n");
 writer.write("===============================\n");
 writer.write(parser_total[section_marker[1]]);
 writer.write("Maximum duration taken by a Validation Procedure is ");
 writer.write(str(validation_max.duration));
 writer.write(" seconds");
 writer.write(" for ");
 writer.write(validation_max.Name);
 writer.write("\n");
 writer.write("Average time taken by Validation Procedures is ");
 writer.write("%.2f" % val_avg);
 writer.write(" seconds");
 writer.write("\n");
 for i in validation_procs:
  writer.write(i.Name);
  writer.write(" started at ");
  writer.write(str(i.start_time));
  writer.write(", ended at ");
  writer.write(str(i.end_time));
  writer.write(" and ran for ");
  writer.write(str(i.duration));
  writer.write(" seconds");
  writer.write("\n");
 
