filename="fedpaper.txt"

sed '1,265d' $filename > tsta
mv tsta $filename

#./to_dataframe.py $filename

