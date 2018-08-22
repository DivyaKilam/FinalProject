#!/usr/local/bin/python3
#
import jinja2
import re
import mysql.connector
import cgi
import urllib.request
import os, os.path
import subprocess

## This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

## This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('final_display.html')


#d where ontology.name = %s")

form = cgi.FieldStorage();
## asign user input values to variables 
libraryterm = form.getvalue('libraryselector')
referenceterm = form.getvalue('refgenome')
bowtieterm=form.getvalue('bowtieanalysis')
if(bowtieterm=='0'):
    bowtie_analysis_term='default'
if(bowtieterm == '1'):
    bowtie_analysis_term=form.getvalue('end_to_end')
if(bowtieterm=='2'):
    bowtie_analysis_term=form.getvalue('Local')

##function to upload user selected file to server
def fileupload():
    if fileitem.filename:
        fn = os.path.basename(fileitem.filename)
        referenceterm = fn;
        open("/var/www/html/dkilam1/final/files/"+fn,'wb').write(fileitem.file.read())
        message="The file" '+ fn +'"was uploaded successfully"
    else:
        message="no file"
## upload file based on single or paired library selection
if (libraryterm== '0'):
    fileitem=form["file1"]
    fileupload();
if (libraryterm == '1'):
    fileitem=form["file1"]
    fileupload();
    fileitem=form["file2"]
    fileupload();

## ftp the reference genome from NCBI based on user selection and index the files
ref_human_file = "/var/www/html/dkilam1/final/ref_human/file_genomic.fna"
ref_mouse_file = "/var/www/html/dkilam1/final/ref_mouse/file_genomic.fna"
ind_human_file = "/var/www/html/dkilam1/final/ref_human/human.1.bt2"
ind_mouse_file = "/var/www/html/dkilam1/final/ref_mouse/mouse.1.bt2"

if (referenceterm == '0'):
    if not (os.path.exists(ref_human_file)):
        url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.38_GRCh38.p12/GCF_000001405.38_GRCh38.p12_genomic.fna.gz'
        urllib.request.urlretrieve(url, '/var/www/html/dkilam1/final/ref_human/file_genomic.fna.gz')
        os.system("gunzip /var/www/html/dkilam1/final/ref_human/file_genomic.fna.gz")
        ##run bowtie build to index the reference file
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_human/file_genomic.fna human")
    if not (os.path.exists(ind_human_file)):
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_human/file_genomic.fna human")

    #run bowtie based on user selection
#    if (libraryterm == '0'):
#        file_single = os.listdir("/var/www/html/dkilam1/final/files")
#        if (bowtieterm == '0'):
#os.system("(/usr/local/bin/bowtie2 -x /var/www/html/dkilam1/final/ref_human/human -U /var/www/html/dkilam1/final/files/SP1.fq -S /var/www/html/dkilam1/final/files/SP1) 2>bowtie1.log ")    
subprocess.call(["bowtie2", "-x", "./ref_human/human", "-U", ".files/SP1.fq", "-S", "./files/SP1"])

if (referenceterm == '1'):
    if not (os.path.exists(ref_mouse_file)):
        url ='ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/635/GCF_000001635.26_GRCm38.p6/GCF_000001635.26_GRCm38.p6_genomic.fna.gz'
        urllib.request.urlretrieve(url, '/var/www/html/dkilam1/final/ref_mouse/file_genomic.fna.gz')
        os.system("gunzip /var/www/html/dkilam1/final/ref_mouse/file_genomic.fna.gz")
        ##run bowtie build to index the reference file
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_mouse/file_genomic.fna mouse")
#    if not (os.path.exists(ind_mouse_file)):
#        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_mouse/file_genomic.fna mouse")



#connect to database and insert values to table
#conn = mysql.connector.connect(user='dkilam1', password='Trinity@02', host='localhost', database='dkilam1')
#curs = conn.cursor()
#qry = ("insert into assembly (AlnID, AssemblySource) values (1, 'human')")

#ontology=request.form['ontology_term']
#curs.execute(qry)
#curs.execute(qry,(ontology,))
#rows = list()

#rows = curs.fetchall()

#for row in curs:
#    rl = tuple([x.decode('utf-8') if type(x) is bytearray else x for x in row])
#    rows.append(rl)

#curs.close()
print ("Content-Type: text/html\n\n")
print(template.render(libraryterm=libraryterm,referenceterm=referenceterm, bowtieterm=bowtieterm, bowtie_analysis_term=bowtie_analysis_term))

