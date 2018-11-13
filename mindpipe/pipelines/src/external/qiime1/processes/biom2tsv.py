#!/usr/bin/env python3
from utils import OtuClass

otu = OtuClass.load_data("$otu")
otu.write_file("${otu.baseName}", file_type="tsv")
