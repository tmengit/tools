#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import argparse
import csv
import pdfplumber

def extarct_requirement_id_from_pdf(source_pdf_file):
    keyword = 'Req-'
    req_list = []
    with pdfplumber.open(source_pdf_file) as pdf:
        for page in pdf.pages:
            for line in page.extract_text().splitlines():
                if (line_str := line.strip()).startswith(keyword):
                    req_list.append(line_str.split()[0])
    req_list = list(set(req_list))
    req_list.sort()
    return req_list

def write_requirement_id_to_csv_file(req_list, csv_file):
    header = 'Requirement ID'
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([header])
        for item in req_list:
            writer.writerow([item])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract requirement from pdf file and write into CSV file")
    parser.add_argument("-f", "--pdf_file", type=str, required=True,
                        help="Source pdf file to process")
    parser.add_argument("-o", "--output_file", type=str, default= 'requirement_id.csv',
                        help="CSV file for storing the reult, if not provided, "
                             "write to requirement_id.csv under current directory")
    args = parser.parse_args()

    if not args.output_file:
        current_dir = os.getcwd()
        csv_file = os.sep.join((current_dir, args.output_file.default))
    else:
        csv_file = args.output_file
    req_list = extarct_requirement_id_from_pdf(args.pdf_file)
    write_requirement_id_to_csv_file(req_list, csv_file)
