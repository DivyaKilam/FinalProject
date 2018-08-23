#!/usr/local/bin/python3
#
import jinja2
import re
import mysql.connector
import cgi
import urllib.request
import os
import subprocess
import json


## This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

## This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('final_display.html')

##====================================================================##
## READ THE FORM ELEMENTS
form = cgi.FieldStorage();

## ASSIGN USER INPUT VALUES TO VARIABLES 
## READ THE LIBRARY TYPE
libraryterm   = form.getvalue('libraryselector')
## READ THE REFERENCE GENOME
referenceterm = form.getvalue('refgenome')
## READ THE BOWTIE ANALYSIS MODE
bowtieterm    = form.getvalue('bowtieanalysis')

## HASH OUT BOWTIE ANALYSIS TYPE & ALIGNMENT MODES
## CASE 1: DEFAULT ANALYSIS MODE
if(bowtieterm =='0'):
    bowtie_analysis_term='default'
    bowtie_analysis_type='default'
    alignment_mode='default'

## CASE 2: END TO END ANALYSIS MODE
if(bowtieterm == '1'):
    bowtie_analysis_term=form.getvalue('end_to_end')
    bowtie_analysis_type='end to end' + bowtie_analysis_term
    ## Read the alignment model for End to End Analysis Mode
    if bowtie_analysis_term == "very_fast":
        alignment_mode='end-to-end-veryfast'
    if bowtie_analysis_term == "fast":
        alignment_mode='end-to-end-fast'
    if bowtie_analysis_term == "sensitive":
        alignment_mode='end-to-end-sensitive'
    if bowtie_analysis_term == "very_sensitive":
        alignment_mode='end-to-end-verysensitive'

## CASE 3: LOCAL ANALYSIS MODE
if(bowtieterm =='2'):
bowtie_analysis_term = form.getvalue('Local')
    bowtie_analysis_type = 'local' + bowtie_analysis_term
    ## Read the alignment model for local Analysis Mode
    if bowtie_analysis_term == "very_fast_local":
        alignment_mode='local-veryfast'
    if bowtie_analysis_term == "fast_local":
        alignment_mode='local-fast'
    if bowtie_analysis_term == "sensitive_local":
        alignment_mode='local-sensitive'
    if bowtie_analysis_term == "very_sensitive_local":
        alignment_mode='local-verysensitive'
##====================================================================##

##====================================================================##
## FUNCTION TO UPLOAD USER SELECTED FILE TO SERVER
## DESC: Check if Reference file is not present, then download via FTP
##====================================================================##
def fileupload():
    if fileitem.filename:
        fn = os.path.basename(fileitem.filename)
        referenceterm = fn;
        open("/var/www/html/dkilam1/final/files/"+fn,'wb').write(fileitem.file.read())
        message="The file" '+ fn +'"was uploaded successfully"
    else:
        message="no file"
##====================================================================##

##====================================================================##
## UPLOAD FILE BASED ON SINGLE OR PAIRED LIBRARY SELECTION
if (libraryterm == '0'):
    library = 'single'
    fileitem=form["file1"]
    fileupload();
if (libraryterm == '1'):
    library = 'paired'
    fileitem=form["file1"]
    fileupload();
    fileitem=form["file2"]
    fileupload();

## FTP THE REFERENCE GENOME FROM ncbi BASED ON USER SELECTION AND INDEX THE FILES
## STORE THE FILE NAMES IN VARIABLES
ref_human_file = "/var/www/html/dkilam1/final/ref_human/file_genomic.fna"
ref_mouse_file = "/var/www/html/dkilam1/final/ref_mouse/file_genomic.fna"
ind_human_file = "/var/www/html/dkilam1/final/ref_human/human.1.bt2"
ind_mouse_file = "/var/www/html/dkilam1/final/ref_mouse/mouse.1.bt2"

## REFERENCE GENOME == HUMAN
if (referenceterm == '0'):
    gene_ref_name = 'human'
    if not (os.path.exists(ref_human_file)):
        url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.38_GRCh38.p12/GCF_000001405.38_GRCh38.p12_genomic.fna.gz'
        urllib.request.urlretrieve(url, '/var/www/html/dkilam1/final/ref_human/file_genomic.fna.gz')
        os.system("gunzip /var/www/html/dkilam1/final/ref_human/file_genomic.fna.gz")
        ##run bowtie build to index the reference file
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_human/file_genomic.fna human")
    if not (os.path.exists(ind_human_file)):
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_human/file_genomic.fna human")


## REFERENCE GENOME == MOUSE
if (referenceterm == '1'):
    gene_ref_name = 'mouse'
    if not (os.path.exists(ref_mouse_file)):
        url ='ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/635/GCF_000001635.26_GRCm38.p6/GCF_000001635.26_GRCm38.p6_genomic.fna.gz'
        urllib.request.urlretrieve(url, '/var/www/html/dkilam1/final/ref_mouse/file_genomic.fna.gz')
        os.system("gunzip /var/www/html/dkilam1/final/ref_mouse/file_genomic.fna.gz")
        ##run bowtie build to index the reference file
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_mouse/file_genomic.fna mouse")
    if not (os.path.exists(ind_mouse_file)):
        os.system("bowtie2-build -f /var/www/html/dkilam1/final/ref_mouse/file_genomic.fna mouse")
##====================================================================##


##====================================================================##
## SQL DATABASE OPERATION
##====================================================================##
# CONNECT TO DATABASE AND GET VALUES FROM TABLE
conn = mysql.connector.connect(user='dkilam1', password='Trinity@02', host='localhost', database='dkilam1')
curs = conn.cursor()

qry = ("select AlnRate from AlnSummary where AssemblySource like %s and AlnType like %s and AlnMode like %s")
curs.execute(qry,(gene_ref_name, library,alignment_mode))

rows = list()

for row in curs:
    rl = tuple([x.decode('utf-8') if type(x) is bytearray else x for x in row])
    rows.append(rl)

curs.close()
conn.close()
##====================================================================##


print ("Content-Type: text/html\n\n")
print(template.render(libraryterm=library,referenceterm=gene_ref_name, bowtie_analysis_type=bowtie_analysis_type, results=rows))

