#!/usr/bin/env python
# -*- coding: UTF-8 -*-

print("Content-Type: text/html\n")
import mysql.connector

mydb = mysql.connector.connect(
  host="10.128.0.12",
  user="eApp",
  password="Argos4905!"
)

print(mydb)
