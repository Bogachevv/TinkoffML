#!/bin/bash
for file in $(ls | grep -i ".txt")
do
	echo $file
	sed -i -E "s/<[^>]{1,}>//g" $file	
done

